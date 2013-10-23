###
#
# Prototype for a LLVM-IR generator for B
#
# Caveat: This is the first Python program of the author, and he is aware
# that an object oriented (or, rather, a class oriented) solution could be
# appropriate.
#
###

import b2llvm.ast as ast
import b2llvm.loadbxml as loadbxml 
import b2llvm.names as names
from b2llvm.strutils import commas, nconc, sp, nl, tb, tb2
from b2llvm.bproject import BProject

#
# Main entry point for this module
#

def translate_bxml(bmodule, outfile, mode='comp', dir='bxml', settings='project.xml'):
    '''
    Main function for applying the code generator to a B module

    Keywords:
      - mode: the code generation mode
      - bmodule: the name of the B machine to have code generated for
      - outfile: the name of the file where code shall be output
      - dir: the name of the directory where files shall be read (default is 'bxml')
      - settings: the name of the file in dir where the project settings
      are stored (default: project.xml)
    Result:
      None
    '''
    project = loadbxml.load_project(dirname=dir, filename=settings)
    ast = loadbxml.load_module(dir, project, bmodule)
    if mode == 'comp':
        filecontents = translate_mode_comp(ast)
    else:
        filecontents = translate_mode_proj(ast)
    llvm = open(outfile, 'w')
    llvm.write(";;; -*- mode: asm -*-"+nl) # emacs syntax highlight on
    llvm.write(";;; file name: "+outfile+nl)
    llvm.write(";;; B module: "+bmodule+nl)
    llvm.write(";;; generation mode: "+mode+nl)
    llvm.write(";;; generated with b2llvm."+nl)
    llvm.write(filecontents)
    llvm.close()

#
# TOP-LEVEL FUNCTION FOR EACH TRANSLATION MODE
#

def translate_mode_comp(m):
    '''
    Translation in component mode.

    Inputs:
      - c: cache
      - n: root AST node for a B machine in proj
    Output:
      LLVM text corresponding to the implementation of n. The produced
      LLVM module is a component to be linked against in the compilation
      of a full project.
    '''
    check_kind(m, {"Machine"})
    if is_base(m):
        return section_typedef(m)
    else:
        assert is_developed(m)
        res = str()
        i = implementation(m)
        acc = set()
        for q in comp_indirect(m):
            if q.mach["id"] not in acc:
                res += state_opaque_typedef(q.mach)
                res += state_ref_typedef(q.mach)
                acc.add(q.mach["id"])
        acc.clear()
        for q in comp_direct(m):
            if q.mach["id"] not in acc:
                res += section_interface(q.mach)
                acc.add(q.mach["id"])
        acc.clear()
        if is_stateful(m):
            res += section_typedef_impl(i, m)
            res += state_ref_typedef(m)
        res += section_implementation(m)
        return res

def translate_mode_proj(m):
    '''
    Translation in project mode.

    Inputs:
      - n: root AST node for a B machine
    Output:
      LLVM text corresponding to the implementation of n. The produced
      LLVM module is the main component to be linked against in the compilation
      of a full project.
    '''
    check_kind(m, "Machine")
    assert is_developed(m)
    res = str()
    # identify all the module instances that need to be created
    root = Comp([], m)
    comps = [root] + comp_indirect(m)
    # emit the type definitions corresponding to the instantiated modules
    # forward references are disallowed: enumerate definitions bottom-up
    comps.reverse()
    acc = set()
    for q in comps:
        if q.mach["id"] not in acc:
            if is_stateful(q.mach):
                res += section_typedef(q.mach)
                res += state_ref_typedef(q.mach)
            acc.add(q.mach["id"])
    acc.clear()
    # the instances are now declared, top down
    comps.reverse()
    for q in comps:
        if is_stateful(q.mach):
            res += (str(q)+" = common global "+state_t_name(q.mach) +
                    " zeroinitializer"+nl)
    # emit the declarations for the operations offered by root module
    # only the initialisation is necessary actually
    res += section_interface(m)
    # generate the code of the routine that initializes the system
    # by calling the initialization function for the root module.
    args = [state_r_name(root.mach) + sp + str(root)]
    args += [state_r_name(q.mach)+sp+str(q) for q in comp_stateful(m)]
    res += "define void @$init$() {"+nl
    res += "entry:"+nl
    res += tb+"call void "+init_name(m)+"("+commas(args)+")"+nl
    res += tb+"ret void"+nl
    res += "}"
    return res

#
# SECTION-LEVEL CODE GENERATION FUNCTIONS
# 

def section_interface(m):
    '''
    Generates the declaration of all externally visible elements of machine n:
    reference type, initialisation function, operation function.

    Input:
      - n: AST root node of a machine
    Output:
    Text of LLVM declarations (see section interface in translation definition).
    '''
    check_kind(m, {"Machine"})
    res = str()
    res += section_interface_init(m)
    res += nconc([ section_interface_op(m, op) for op in operations(m) ])
    return res

def operations(m):
    '''
    Gets list of operations of machine m.

    TODO: currently, the AST of developed machines does not have operations
    and this query is forwarded to the corresponding implementation. I would
    prefer to load properly the full AST of such machines.
    '''
    check_kind(m, {"Machine"})
    if is_developed(m):
        return implementation(m)["operations"]
    else:
        return m["operations"]

def section_interface_init(m):
    '''
    Generates the declaration of the initialization function for n

    Inputs:
      - m: a machine AST root node
    Output:
      Text of a LLVM function declaration.
    '''
    global nl
    check_kind(m, {"Machine"})
    comp = list()
    if is_stateful(m):
        comp.append(m)
    comp.extend([comp.mach for comp in comp_indirect(m)])
    res = str()
    res += "declare void"+sp+init_name(m)
    res += "("+commas(list_machine_refs(comp))+")"+nl
    return res

def section_interface_op(m, op):
    '''
    Declaration of the function implementing operation op in m.

    Inputs:
      - m: a machine AST root node
      - op: an operation AST node
    Output:
      Text of a LLVM function declaration.
    '''
    global nl
    # compute in tl the list of arguments types
    tl = list()
    if is_stateful(m):
        tl.append(state_r_name(m))
    tl.extend([ x_type(i["type"]) for i in op["inp"] ])
    tl.extend([ x_type(o["type"])+"*" for o in op["out"] ])
    return "declare void"+sp+global_name(op)+"("+commas(tl)+")"+nl

def section_typedef(m):
    '''
    Generates the definition of the state type and reference type of machine n.

    Inputs:
      - m: AST root node of a machine
    Output:
      Text of LLVM definitions for the types associated with the state of
      machine m. If the machine is stateful, two types are created: an
      aggregate type encoding the state of n (or its implementation if it is a 
      developed machine), and one reference type, pointer to the previous type.
      Otherwise, nothing is generated.
    '''
    global nl
    check_kind(m, {"Machine"})
    if is_developed(m):
        return section_typedef_impl(implementation(m), m)
    else:
        assert is_base(m)
        res = str()
        if is_stateful(m):
            res += state_t_name(m)+" = type {"
            res += commas([x_type(v["type"]) for v in m["variables"]])
            res += "}"+nl
        return res

def section_typedef_impl(i, m):
    '''
    Generates the section implementation of the translation to LLVM.

    Inputs:
      - c: cache
      - i: AST node for a B implementation
      - m: AST node for the B machine corresponding to i
    Output:
    String with the definitions of the LLVM functions implementing the
    initialisation and operations of the implementation i.
    '''
    check_kind(i, {"Impl"})
    check_kind(m, {"Machine"})
    res = str()
    if is_stateful(i):
        res += state_t_name(m)+" = type {"
        res += commas(imports_type(i["imports"]) +
                           [x_type(v["type"]) for v in i["variables"]])
        res += "}"+nl
    return res

def section_implementation(m):
    '''
    Generates the section implementation of the translation to LLVM.

    Inputs:
      - m: AST node for a B machine
    Output:
    String with the definitions of the LLVM functions implementing the
    initialisation and operations of the implementation of n in the
    project proj.    
    '''
    check_kind(m, {"Machine"})
    res = str()
    if is_developed(m):
        i = implementation(m)
        res += x_init(m, i)
        for op in i["operations"]:
            res += x_operation(op)
    return res

#
# TRANSLATION FUNCTIONS OF INDIVIDUAL ELEMENTS OF THE B AST
#

#
# From now on, use x_ as prefix as a shortcut for the prefix translate_
#

### TYPE TRANSLATION ###

#
# This function is responsible for translation B0 type names to LLVM types
#
def x_type(t):
    assert(t == ast.INTEGER or t == ast.BOOL)
    return "i32" if t == ast.INTEGER else "i1"

### TRANSLATION FOR INITIALISATION

def x_init(m, i):
    '''
    Input:
      - m: root AST node of a B machine
      - i: root AST node of the implementation of m
    Output:
    LLVM implementation of the initialization clause of i (a LLVM function).
    '''
    global tb, nl, sp
    check_kind(m, {"Machine"})
    check_kind(i, {"Impl"})
    tm = state_r_name(m) # LLVM type name: pointer to structure storing m data
    names.reset()
    # 1. generate function signature: one parameter for the implementation
    # instance, one parameter for each transitively imported module instance.
    res = str()
    # 1.1 generate argument names for the imported instances, store in lexicon
    lexicon = dict()
    count = 0 # to generate fresh names
    for q in comp_indirect(m):
        if is_stateful(q.mach):
            lexicon[q] = "%arg"+str(count)+"$"
            count += 1
    # 1.2 generate parameter type, name list
    arg_list = [ tm+sp+"%self$" ]
    for q in comp_indirect(m):
        if is_stateful(q.mach):
            arg_list.append(state_r_name(q.mach)+sp+lexicon[q])
    # 1.3 the signature
    res += "define void"+sp+init_name(i)+"("+commas(arg_list)+")"
    # 2. generate function body
    res += "{"+nl
    res += "entry:"+nl
    # 2.1 reserve stack space for local variables
    res += x_alloc_inst_list(i["initialisation"])
    # 2.2 bind direct imports to elements of state structure
    direct = [ q for q in comp_direct(m) if is_stateful(q.mach) ]
    for j in range(len(direct)):
        lbl = names.new_local()
        q = direct[j]
        tm2 = state_r_name(q.mach)
        res += tb+lbl+" = getelementptr "+tm+" %self$, i32 0, i32 "+str(j)+nl
        res += tb+"store "+tm2+sp+lexicon[q]+", "+tm2+"* "+lbl+nl
    # 2.3 initialize direct imports
    offset = len(direct)+1
    for q in comp_direct(m):
        mq = q.mach     # the imported machine
        arg_list2 = []  # to store parameters needed to initialize mq
        if is_stateful(mq):
            arg_list2.append(state_r_name(mq)+sp+lexicon[q])
        n = len([x for x in comp_indirect(mq) if is_stateful(x.mach)])
        arg_list2.extend(arg_list[offset:offset+n])
        res += tb+"call void "+init_name(mq)+"("+commas(arg_list2)+")"+nl
    # 2.4 translate initialisation instructions
    res += x_inst_list_label(i["initialisation"], "exit")
    res += "exit:"+nl
    res += tb+"ret void"+nl
    res += "}"+nl
    return res

### TRANSLATION OF OPERATIONS

def x_operation(n):
    global tb, nl
    check_kind(n, {"Oper"})
    names.reset()
    res = str()
    res += "define void "+global_name(n)
    res += "("+commas([state_r_name(n["root"])+sp+"%self$"]+
                           [x_type(i["type"])+sp+"%"+i["id"] for i in n["inp"]]+
                           [x_type(o["type"])+"*"+sp+"%"+o["id"] for o in n["out"]])+")"
    res += "{"+nl
    res += "entry:"+nl
    res += x_alloc_inst(n["body"])
    res += x_inst_label(n["body"], "exit")
    res += "exit:"+nl
    res += tb+"ret void"+nl
    res += "}"+nl
    return res

### TRANSLATION OF STACK VARIABLE ALLOCATION

def x_alloc_inst_list(n):
    return nconc([x_alloc_inst(inst) for inst in n])

def x_alloc_inst(n):
    check_kind(n, {"Beq", "Blk", "Call", "Case", "If", "Skip", "VarD", "While"})
    if n["kind"] in {"Beq", "Call"}:
        return ""
    elif n["kind"] in {"Case", "If"}:
        return nconc(x_alloc_inst(br["body"]) for br in n["branches"])
    elif n["kind"] in {"Blk", "While"}: 
        return x_alloc_inst_list(n["body"])
    elif n["kind"] == "VarD":
        return x_alloc_var_decl(n)
    else:
        print("error: unknown instruction kind")
        return ""
    
def x_alloc_var_decl(n):
    global tb, nl, sp
    check_kind(n, {"VarD"})
    res = nconc([ tb+"%"+v["id"]+" = alloca "+x_type(v["type"])+nl
                  for v in n["vars"] ])
    res += x_alloc_inst_list(n["body"])
    return res

### TRANSLATION OF INSTRUCTIONS ###

#
# WARNING:
# WARNING: The LLVM is sensitive to the order local variables and labels names
# WARNING: consequently reordering the translation of the different elements
# WARNING: of an AST node may well generate uncompilable LLVM code.
# WARNING:
# WARNING: Have this is mind before changing the order of the instructions in
# WARNING: the following functions.
# WARNING:
#

def x_inst_list_label(l, lbl):
    global tb, nl
    if len(l) == 0:
        return tb + "br label %" + lbl + nl
    else:
        i = l[0]
        l2 = l[1:]
        if i["kind"] in {"Case", "If", "While"}:
            lbl2 = names.new_label()
            p1 = x_inst_label(i, lbl2) + lbl2 + ":\n"
        elif i["kind"] in {"Blk"}:
            p1 = x_inst_list(i["body"])
        else:
            p1 = x_inst(i)
        p2 = x_inst_list_label(l2, lbl)
        return p1 + p2

def x_inst_list(l):
    if len(l) == 0:
        return ""
    else:
        i = l[0]
        l2 = l[1:]
        if i["kind"] in {"If", "While"}:
            lbl2 = names.new_label()
            p1 = x_inst_label(i, lbl2) + lbl2 + ":\n"
        elif i["kind"] in {"Blk"}:
            p1 = x_inst_list(i["body"])
        else:
            p1 = x_inst(i)
        p2 = x_inst_list(l2)
        return p1 + p2

def x_inst_label(n, lbl):
    check_kind(n, {"Beq", "Blk", "Call", "Case", "If", "VarD", "While"})
    if n["kind"] == "Blk":
        return x_inst_list_label(n["body"], lbl)
    elif n["kind"] == "Case":
        return x_case(n, lbl)
    elif n["kind"] == "If":
        return x_if(n, lbl)
    elif n["kind"] == "While":
        return x_while(n, lbl)
    elif n["kind"] in {"Beq", "Call"}:
        res = str()
        res += x_inst(n)
        res += tb + "br label %" + lbl + nl
        return res
    elif n["kind"] == "VarD":
        return x_inst_list_label(n["body"], lbl)
    else:
        print("error: instruction type unknown")

def x_inst(n):
    check_kind(n, {"Beq", "Call", "VarD"})
    if n["kind"] == "Beq":
        return x_beq(n)
    elif n["kind"] == "Call":
        return x_call(n)
    elif n["kind"] == "VarD":
        return x_inst_list(n["body"])
    else:
        return ""

### TRANSLATION OF CASE INSTRUCTIONS

def x_case(n, lbl):
    global nl, tb, sp
    check_kind(n, {"Case"})
    p,v,t = translate_expression(n["expr"])
    lblo = names.new_label()
    # j is a jump table, b is a list of blocks
    j, b = x_case_branch_list(n["branches"], lblo, lbl)
    res = str()
    res += p
    res += tb + "switch " + t + sp + v + ", label %" + lblo + " [" + nl
    res += j
    res += tb + "]" + nl
    res += b
    return res

def x_case_branch_list(bl, lblo, lble):
    # br: first branch, bl2: list of remaining branches
    br = bl[0]
    bl2 = bl[1:]
    j, b = str(), str()
    # if br is the last branch
    if bl2 == []:
        # if the last branch is a default branch
        if "val" not in br.keys() or br["val"] == [] or br["val"] == None:
            b += tb + lblo + ":" + nl
            b += x_inst_label(br["body"], lble)
        # if the last branch has some associated values
        else:
            lbl = names.new_label()
            j += x_case_val_list(br["val"], lbl)
            b += tb + lbl + ":" + nl
            b += x_inst_label(br["body"], lble)
            b += tb + lblo + ":" + nl
            b += tb + "branch label %" + lble
    # if br is not the last branch
    else:
        lbl = names.new_label()
        j += x_case_val_list(br["val"], lbl)
        b += lbl + ":" + nl
        b += x_inst_label(br["body"], lble)
        j2, b2 = x_case_branch_list(bl2, lblo, lble)
        j += j2
        b += b2
    return j, b

def x_case_val_list(vl, lbl):
    global tb2, sp, nl
    res = str()
    for v in vl:
        _, v, t = translate_expression(v)
        res += tb2 + t + sp + v + ", label %" + lbl + nl
    return res

### TRANSLATION OF IF INSTRUCTIONS

def x_if(n, lbl):
    check_kind(n, {"If"})
    return x_if_br(n["branches"], lbl)

def x_if_br(lbr, lbl):
    assert(len(lbr)>=1)
    # br: first if branch, lbr2: list of remaining branches
    br = lbr[0]
    lbr2 = lbr[1:]
    check_kind(br, {"IfBr"})
    # br is the last branch
    if lbr2 == []:
        # br is an else branch
        if "cond" not in br.keys() or br["cond"] == None:
            res = x_inst_label(br["body"], lbl)
        # br is an elsif branch
        else:
            lbl_1 = names.new_label()
            res = str()
            res += translate_form(br["cond"], lbl_1, lbl)
            res += lbl_1 + ":" + nl
            res += x_inst_label(br["body"], lbl)
    # br is not the last branch
    else:
        lbl_1 = names.new_label()
        lbl_2 = names.new_label()
        res = str()
        res += translate_form(br["cond"], lbl_1, lbl_2)
        res += lbl_1 + ":" + nl
        res += x_inst_label(br["body"], lbl)
        res += lbl_2 + ":" + nl
        res += x_if_br(lbr2, lbl)
    return res

### TRANSLATION OF WHILE INSTRUCTIONS

def x_while(n, lbl):
    global nl, tb, sp
    check_kind(n, {"While"})
    lbl1 = names.new_label()
    c, v = translate_pred(n["cond"])
    lbl2 = names.new_label()
    body = x_inst_list_label(n["body"], lbl1)
    res = str()
    res += tb + "br label %" + lbl1 + nl
    res += lbl1 + ":" + nl
    res += c
    res += tb + "br i1 " + v + ", label %" + lbl2 + ", label %" + lbl + nl
    res += lbl2 + ":" + nl
    res += body
    return res

### TRANSLATION OF BECOMES EQUAL INSTRUCTIONS

def x_beq(n):
    global tb, sp, nl
    check_kind(n, {"Beq"})
    r,v,t = translate_expression(n["rhs"])
    l,p,_ = x_lvalue(n["lhs"])
    return (r + 
            l + 
            tb + "store " + t + sp + v + ", " + t + "* " + p + nl)

def x_lvalue(n):
    '''
    Translate of "lvalues" (elements to the left of an assignment).

    Input:
      - n: AST node for lvalue
    Output:
      A triple composed of a sequence of LLVM instructions computing
      the lvalue, the name of the local storing the lvalue, and the
      type of the lvalue.
    Note:
      Used to translate assignments and operation calls with output(s).
    Caveat:
      Currently limited to simple identifiers.
    '''
    global tb, nl
    check_kind(n, {"Vari"})
    t = x_type(n["type"]) + "*"
    if n["scope"] == "Impl":
        v = names.new_local()
        return (tb + v + " = getelementptr " + state_r_name(n["root"])+ 
                " %self$, i32 0, i32 " + str(state_position(n)) + nl, v, t)
    elif n["scope"] in {"Oper", "Local"}:
        return ("", "%"+n["id"],t)
    else:
        print("error: unknown scope for variable " + v["id"])
        return ("", "UNKNOWN", "UNKNOWN")

### TRANSLATION OF CALL INSTRUCTIONS

def x_call(n):
    global sp
    check_kind(n, {"Call"})
    res = str()
    # pi, po: evaluate arguments - il, ol: get parameters types and names
    pi, il = x_inputs(n["inp"])
    po, ol = x_outputs(n["out"])
    res += pi
    res += po
    operation = n["op"]
    local = (n["inst"] == None) # is a local operation?
    impl = operation["root"]
    args = list()
    if is_stateful(impl):
        # get the LLVM type of the machine offering the operation
        if local:
            mach_t = state_r_name(operation["root"])
        else:
            mach_t = state_r_name(n["inst"]["root"])
        if local:
            t = selftype
            v = "%self$"
        else:
            t = state_r_name(n["inst"]["mach"])
            v1 = names.new_local()
            v2 = names.new_local()
            res += (tb + v1 + " = getelementptr " + mach_t + 
                    " %self$, i32 0, i32 " + str(state_position(n["inst"])) +
                    nl)
            res += tb + v2 + " = load " + t +"*" + sp + v1 + nl
        args.append(t + sp + v2)
    args.extend(il)
    args.extend(ol)
    id = global_name(operation)
    res += tb + "call void" + sp + id + "(" + commas(args) + ")" + nl
    return res

def x_inputs(n):
    global sp
    preamble = str()
    args = list()
    for elem in n:
        p,v,t = translate_expression(elem)
        preamble += p
        args.append(t + sp + v)
    return preamble, args

def x_outputs(n):
    global sp
    preamble = str()
    args = list()
    for elem in n:
        p,v,t = x_lvalue(elem)
        preamble += p
        args.append(t + sp + v)
    return preamble, args

### LLVM IDENTIFIER GENERATION ###

def instance_name(n):
    '''
    - Input:
      n: A node representing a B implementation
    - Output:
      A string for the name of the LLVM variable representing the instance 
      of that implementation.
    '''
    check_kind(n, {"Impl"})
    return "@"+n["id"]+"$self$"

def state_t_name(n):
    '''
    - Input:
      n: A node representing a B machine
    - Output:
      A string for the name of the LLVM type representing the state of
      (the implementation) of n.
    '''
    check_kind(n, {"Machine", "Impl"})
    if n["kind"] == "Machine":
        return "%"+n["id"]+"$state$"
    else:
        return state_r_name(machine(n))

def state_r_name(n):
    '''
    - Input:
      n: A node representing a B machine
    - Output:
      A string for the name of the LLVM type representing a reference to
      the state of (the implementation) of n.
    '''
    check_kind(n, {"Machine", "Impl"})
    if n["kind"] == "Machine":
        return "%"+n["id"]+"$ref$"
    else:
        return state_r_name(machine(n))

def global_name(n):
    '''
    - Input:
      n: A node representing a B construct
    - Output:
      A string for the name of the LLVM construct representing n.
    '''
    return "@" + n["root"]["id"] + "$" + n["id"]

def init_name(n):
    '''
    - Input:
      n : a node representing a B implementation
    - Output:
    String with the name of the LLVM function encoding the initialization
    of that implementation.
    '''
    return "@"+n["id"]+"$init$"

### LLVM names for B operators ###

def llvm_op(str):
    '''
    Input:
        - str: the name of an operator in B0
    Output: The name of the corresponding LLVM operator
    Example:
        >>> llvm_op("=") == "eq"
        True
        >>> llvm_op("+") == "add"
        True
    Note: An error message is printed and the empty string
    is returned if the translation has not been defined.
    '''
    lex = dict({"=":"eq", "!=": "ne", 
                "<":"slt", "<=":"sle", ">":"sgt", ">=":"sge",
                "+":"add", "-": "sub", 
                "*":"mul", "/":"sdiv", "mod":"srem"})
    if str not in lex.keys():
        print("error: operator " + str + " not translated")
        return ""
    else:
        return lex[str]
        
### MISC ###

#
# Function check_kind is used to assert that the arguments of translation
# function arguments are in the correct syntactic category
#
def check_kind(n, s):
    '''
    Input:
       - n: represents a B0 syntactic entity
       - s: a set of syntactic entity class names
    Output: None.
    Description: Checks that the class of n is one in s.
    Example:
       >>> check_kind(n, {"IntegerLit, BooleanLit"})
    '''
    assert(n["kind"] in s)

def state_position(n):
    '''
    Input:
      - n: represents a B state variable or imported machine
    Output:
      - position of n in the list of imported machines and state variables
    An error message is printed and the value 0 is returned if n is
    not found.
    '''
    root = n["root"]
    result = 0
    for n2 in root["imports"] + root["variables"]:
        if n2 == n:
            return result
        result += 1
    print("error: position of imported machine or variable not found in implementation")
    return 0

def state_opaque_typedef(m):
    '''
    Input:
      - m: represents a B machine
    Output:
      String for LLVM definition of type pointer to type representing the
      state of n.
      This only makes sense if n is stateful.
    '''
    global nl
    return state_t_name(m) + " = type opaque" + nl

def state_ref_typedef(m):
    '''
    Input:
      - m: represents a B machine
    Output:
      String for LLVM definition of type pointer to type representing the
      state of n.
      This only makes sense if n is stateful.
    '''
    global nl
    return state_r_name(m) + " = type " + state_t_name(m) + "*" + nl

###

def is_developed(m):
    check_kind(m, {"Machine"})
    return m["implementation"] != None
    
def is_base(m):
    check_kind(m, {"Machine"})
    return m["implementation"] == None
    
def implementation(m):
    check_kind(m, {"Machine"})
    assert(is_developed(m))
    return m["implementation"]
    
def machine(m):
    check_kind(m, {"Impl"})
    return m["machine"]
    
#
# This function is responsible for building the LLVM type expression for
# the type corresponding to the state of B0 implementation n.
#
def state_expression(n):
    check_kind(n, {"Impl", "Machine"})
    result = "{"
    components = []
    for impo in n["imports"]:
        components += [state_t_name(impo["mach"]["impl"])]
    for var in n["variables"]:
        components += [x_type(var["type"])]
    for i in range(len(components)):
        if i > 0:
            result += ", "
        result += components[i]
    result += "}"
    return result

#
# Function responsible for producing LLVM code defining type corresponding to
# the state of B0 implementation n
#
def translate_state(n):
    global nl
    check_kind(n, {"Impl", "Machine"})
    if (len(n["variables"]) == 0):
        return ""
    else:
        return state_t_name(n) + " = type " + state_expression(n) + nl

### TRANSLATION OF EXPRESSIONS ###

def translate_integerlit(n):
    check_kind(n, {"IntegerLit"})
    return ("",n["value"],"i32")

def translate_booleanlit(n):
    check_kind(n, {"BooleanLit"})
    if n["value"] == "TRUE":
        val = "1"
    else:
        val = "0"
    return ("",val,"i1")

def translate_name(n):
    check_kind(n, {"Vari"})
    t = x_type(n["type"])
    if n["scope"] == "Local":
        v1 = "%"+n["id"]
        v2 = names.new_local()
        t = x_type(n["type"])
        text = tb+ v2 + " = load" + sp + t + "*" + sp + v1 + nl
        return (text, v2, t)
    elif n["scope"] == "Oper":
        return ("", "%"+n["id"], t)
    elif n["scope"] == "Impl":
        p = names.new_local()
        v = names.new_local()
        text = ""
        text += (tb + p + " = getelementptr " + state_t_name(n["root"]) + 
                 sp + "%self$, i32 0, i32 " + str(state_position(n)) + nl)
        text += tb + v + " = load " + t + "* " + p + nl
        return (text, v, t)
    else:
        print("error: name translation not supported")
        return ("", "", "")
        
def translate_unary(n):
    check_kind(n, {"Term"})
    assert (n["op"] in {"succ", "pred"})
    if n["op"] == "succ":
        p,v,t = translate_expression(n["args"][0])
        w = names.new_local()
        text = ""
        text += p
        text += tb + w + " = add i32 1," + sp + v + nl
        return (text, w, "i32")
    elif n["op"] == "pred":
        p,v,t = translate_expression(n["args"][0])
        w = names.new_local()
        text = ""
        text += p
        text += tb + w + " = sub i32 " + v + ", 1" + nl
        return (text, w, "i32")
    else:
        print("error: unary operator translation not supported")
        return ("", "", "")

def translate_term(n):
    global tb, sp, nl
    check_kind(n, {"Term"})
    if n["op"] == "succ" or n["op"] == "pred":
        return translate_unary(n)
    else:
        assert(len(n["args"]) == 2)
        p1,v1,t1 = translate_expression(n["args"][0])
        p2,v2,t2 = translate_expression(n["args"][1])
        v = names.new_local()
        return (p1 +
                p2 +
                tb + v + " = " + llvm_op(n["op"]) + sp + t1 + sp + v1 + ", " + v2 + nl), v, t1

def translate_expression(n):
    check_kind(n, {"IntegerLit", "BooleanLit", "Vari", "Term", "Cons"})
    if n["kind"] == "IntegerLit":
        return translate_integerlit(n)
    elif n["kind"] == "BooleanLit":
        return translate_booleanlit(n)
    elif n["kind"] == "Vari":
        return translate_name(n)
    elif n["kind"] == "Term":
        return translate_term(n)
    elif n["kind"] == "Cons":
        return translate_expression(n["value"])
    else:
        return ("","","")

### TRANSLATION OF CONDITIONS ###

def translate_comp(n):
    global tb, sp, nl
    check_kind(n, {"Comp"})
    p1,v1,t1 = translate_expression(n["arg1"])
    p2,v2,t2 = translate_expression(n["arg2"])
    v = names.new_local()
    return (p1 +
            p2 +
            tb + v + " = icmp " + llvm_op(n["op"]) + sp + t1 + sp + v1 + ", " + v2 + nl), v

def translate_pred(n):
    if n["kind"] == "Comp":
        return translate_comp(n)
    else:
        print("error: not implemented translation for such predicate")
        return ("", "")

def translate_and(n, lbl1, lbl2):
    check_kind(n, {"Form"})
    assert(n["op"] == "and")
    assert(len(n["args"]) == 2)
    arg1 = n["args"][0]
    arg2 = n["args"][1]
    lbl = names.new_label()
    p1 = translate_form(arg1, lbl, lbl2)
    p2 = translate_form(arg2, lbl1, lbl2)
    result = ""
    result += p1
    result += lbl + ":" + nl
    result += p2
    return result

def translate_or(n, lbl1, lbl2):
    check_kind(n, {"Form"})
    assert(n["op"] == "or")
    assert(len(n["args"]) == 2)
    arg1 = n["args"][0]
    arg2 = n["args"][1]
    lbl = names.new_label()
    p1 = translate_form(arg1, lbl1, lbl)
    p2 = translate_form(arg2, lbl1, lbl2)
    result = ""
    result += p1
    result += lbl + ":" + nl
    result += p2
    return result

def translate_not(n, lbl1, lbl2):
    check_kind(n, {"Form"})
    assert(n["op"] == "not")
    return translate_form(n["args"][0], lbl2, lbl1)

def translate_form(n, lbl1, lbl2):
    check_kind(n, {"Comp", "Form"})
    if n["kind"] == "Comp":
        text, v = translate_comp(n)
        text += tb + "br i1" + sp + v + sp + ", label %" + lbl1 + ", label %" + lbl2 + nl
        return text
    elif n["kind"] == "Form":
        if n["op"] == "and":
            return translate_and(n, lbl1, lbl2)
        elif n["op"] == "or":
            return translate_or(n, lbl1, lbl2)
        elif n["op"] == "not":
            return translate_not(n, lbl1, lbl2)
        else:
            print("error: unrecognized formula")
            return ""
    else:
        print("error: not implemented translate_form for formulas.")
        return ""

### TRANSLATION OF INSTRUCTIONS ###

def translate_skip(n):
    check_kind(n, {"Skip"})
    return ""

### TRANSLATION OF CONSTANT DEFINITIONS

def translate_constant(n):
    global tb, sp, nl
    check_kind(n, {"Cons"})
    if n["type"] not in {"INTEGER", "BOOL"}:
        print("error: constant " + n["id"] + " cannot be translated")
    return ""

def translate_constants(n):
    check_kind(n, {"Impl"})
    result = ""
    if "concrete_constants" in n.keys():
        for const in n["concrete_constants"]:
            result += translate_constant(const)
    return result

### TRANSLATION OF IMPLEMENTATION

def x_type_expr_impo(n):
    check_kind(n, {"Impo"})
    return state_t_name(n["mach"]["impl"])

def x_type_expr_vari(n):
    check_kind(n, {"Vari"})
    return x_type(n["type"])

def x_type_expr_impl(n):
    check_kind(n, {"Impl"})
    result = ""
    tl = []
    for ni in n["imports"]:
        tl.append(x_type_expr_impo(ni))
    for nv in n["variables"]:
        tl.append(x_type_expr_vari(nv))
    result += "{" + commas(tl) + "}"
    return result

def x_type_def_import(n, acc):
    '''
    - Input:
      n: a node representing an element of the import clause in a B 
      implementation
    - Output:
      String corresponding to the definition of the LLVM data types 
      encoding the state of the imported machine (and of all the 
      transitively imported machines).
    '''
    global nl, sp
    check_kind(n, {"Machine"})
    impl = n["impl"]
    result = x_type_def_import_list(impl, acc)
    result += state_t_name(impl)+ " = type "+ x_type_expr_impl(impl)+ nl
    return result

def x_type_def_import_list(n, acc = None):
    '''
    - Input:
      n: a node representing a B implementation
      acc: a set containing all machines that have already been
      processed (optional, default being the empty set)
    - Output:
      String corresponding to the definition of the LLVM data types 
      encoding the state of all the imported machines (transitively).
    '''
    check_kind(n, {"Impl"})
    if acc == None:
        acc = set()
    result = ""
    imports = n["imports"]
    if imports == None:
        return result
    for imp in imports:
        mach = imp["mach"]
        check_kind(mach, {"Machine"})
        if mach["id"] not in acc:
            acc.add(mach["id"])
            result += x_type_def_import(mach, acc)
    return result

def translate_op_decl(n, state_t):
    '''
    - Input:
      n: a node representing an operation in a B implementation
      state_t: the LLVM type representing the state of the implementation
    - Output:
      String corresponding to the declaration of the LLVM function
      encoding the operation.
    '''
    check_kind(n, {"Oper"})
    # tl: parameter signature of the LLVM function coding n
    tl = [state_t + "*"]
    for i in n["inp"]:
        tl.append(x_type(i["type"]))
    for o in n["out"]:
        tl.append(x_type(o["type"])+"*")
    result = ""
    result += "declare void " + global_name(n) + "(" + commas(tl) + ")" + nl
    return result

def translate_op_decl_import(n):
    '''
    - Input:
      n: a node representing a B machine
    - Output:
      String corresponding to the declaration of the LLVM functions
      encoding the initialization and operations of the imported machine.
    '''
    global nl, sp
    check_kind(n, {"Machine"})
    impl = n["impl"]
    state_t = state_t_name(impl) 
    result = ""
    result += "declare void" + sp + init_name(impl) + "(" + state_t + "*)" + nl
    impl = n["impl"]
    for op in impl["operations"]:
        result += translate_op_decl(op, state_t)
    return result

def translate_op_decl_import_list(n):
    '''
    - Input:
      n: a node representing a B implementation
      acc: a set containing all the machines that have already
      been processed (optional, default being empty set)
    - Output:
      String corresponding to the declaration of the LLVM functions
      encoding the initialization and operations of the imported 
      machines.
    '''
    check_kind(n, {"Impl"})
    result = ""
    imports = n["imports"]
    acc = set()
    if imports == None:
        return result
    for i in imports:
        m = i["mach"]
        check_kind(m, {"Machine"})
        if m["id"] not in acc:
            acc.add(m["id"])
            result += translate_op_decl_import(m)
    return result

def translate_implementation(i, toplevel):
    '''
    - Input:
      i: a node representing a B implementation
      toplevel: a boolean indicating if this implementation is
      a top-level component (and not a library component)
    - Output:
      The text of the LLVM encoding for i.
    '''
    check_kind(i, {"Impl"})
    result = ""
    result += x_type_def_import_list(i)
    result += translate_op_decl_import_list(i)
    result += translate_constants(i)
    result += translate_state(i)
    result += x_init(i)
    for op in i["operations"]:
        result += x_operation(op)
    if toplevel:
        result += (instance_name(i) + " = common global " 
                   + state_t_name(i) + " zeroinitializer" + nl)
    return result


### COMP(ONENTS)

class Comp:
    '''
    This class represents components in a B project. Objects of this
    class have the following attributes:
    - a path, which shall be given as a list of strings
    - a machine, which shall be given as the root AST node of the machine
    - id, which is a unique identifier computed when an instance is created
    Instances are convertible to strings, and are hashable.
    '''
    def __init__(self, p, m):
        check_kind(m, {"Machine"})
        self.path = p
        self.mach = m
        self.id = "@"+"$".join(p)+"$"+m["id"]  
    def __str__(self):
        return self.id
    def __hash__(self):
        return self.id.__hash__()

def comp_direct(m):
    ''' 
    List of direct components.
    
    Inputs:
      - n: root AST node for a B machine
   Output:
     Sequence of components imported by the implementation of machine m.
   '''
    check_kind(m, {"Machine"})
    if m["comp_direct"] == None:
        if is_base(m):
            m["comp_direct"] = []
        else:
            impl = implementation(m)
            m["comp_direct"] = list()
            for impo in impl["imports"]:
                pre = impo["pre"]
                if pre == None:
                    pre = ""
                m["comp_direct"].append(Comp([pre], impo["mach"]))
    return m["comp_direct"]

def comp_indirect(m):
    ''' 
    List of all (direct and indirect) components.
    
    Inputs:
      - m: root AST node for a B machine
   Output:
     Sequence of components ordered by
     increasing level in the import tree: imported components, followed by
     components imported from imported components, etc. 
     The imports of a machine are those of the corresponding implementation in 
     the given project.
   '''
    check_kind(m, {"Machine"})
    if m["comp_indirect"] == None:
        if is_base(m):
            m["comp_indirect"] = []
        else:
            impl = implementation(m)
            v = comp_direct(m)
            # the intention flattens a list of list into a list
            v.extend([ i for sl in [ comp_indirect(mc.mach) for mc in v ]
                         for i in sl ])
            m["comp_indirect"] = v
    return m["comp_indirect"]

def comp_stateful(m):
    ''' 
    List of (direct and indirect) stateful components.
    
    Inputs:
      - m: root AST node for a B machine
   Output:
     Sequence of stateful components ordered by
     increasing level in the import tree: imported components, followed by
     components imported from imported components, etc. 
     The imports of a machine are those of the corresponding implementation in 
     the given project.
   '''
    return [ x  for x in comp_indirect(m) if is_stateful(x.mach) ]

#
# MISC
#

def is_stateful(n):
    '''
    Checks if n is a stateful module

    Inputs:
      - n: a machine or implementation AST root node
    Output:
      boolean
    '''
    check_kind(n, {"Machine", "Impl"})
    if n["stateful"] == None:
        if n["kind"] == "Machine":
            if is_base(n):
                n["stateful"] = n["variables"] != []
            else:
                n["stateful"] = is_stateful(n["implementation"])
        else:
            if n["variables"] != []:
                n["stateful"] = True
            else:
                n["stateful"] = False
                for i in n["imports"]:
                    if is_stateful(i["mach"]):
                        n["stateful"] = True
                        break
    return n["stateful"]

def imports_type(il):
    '''
    Gets list of reference types for stateful imported machines.

    Inputs:
      - il: imports list
    Output:
      - list of LLVM reference type for the stateful imported machines.
    '''
    return list_machine_refs([ i["mach"] for i in il ])

def list_machine_refs(ml):
    '''
    Generates a list of machine reference types
    
    Inputs:
      - ml: a list of machine AST root nodes
    Output
      List of the names of the machine reference types for
      each stateful machine in ml. Order is maintained.
    '''
    return [state_r_name(m) for m in ml if is_stateful(m)]


