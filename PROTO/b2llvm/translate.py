###
#
# Prototype for a LLVM-IR generator for B
#
# Caveat: This is the first Python program of the author, and he is aware
# that an object oriented (or, rather, a class oriented) solution could be
# appropriate.
#
# Error handling: When an error is detected, the code generator emits a
# message to stdout, inserts an error in the generated LLVM code and 
# tries to proceed processing the input.
#
###

import b2llvm.ast as ast
import b2llvm.loadbxml as loadbxml 
import b2llvm.names as names
import b2llvm.printer as printer
from b2llvm.strutils import commas, nconc, sp, nl, tb, tb2
from b2llvm.bproject import BProject

import b2llvm.trace as trace

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
    res = bytearray()
    res.extend(";; -*- mode: asm -*-"+nl) # emacs syntax highlight on
    trace.OUT(res, "file generated with b2llvm")
    trace.OUT(res, "B module: "+bmodule)
    trace.OUT(res, "B project directory: "+dir)
    trace.OUT(res, "B project settings: "+settings)
    trace.OUT(res, "code generation mode: " + ("component" if mode == "comp" else "project"))
    trace.OUT(res, "output file: "+outfile)
    if mode == 'comp':
        translate_mode_comp(res, ast)
    else:
        translate_mode_proj(res, ast)
    llvm = open(outfile, 'w')
    llvm.write(res)
    llvm.close()

#
# TOP-LEVEL FUNCTION FOR EACH TRANSLATION MODE
#

def translate_mode_comp(res, m):
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
    trace.OUT(res, "B machine: " + m["id"])
    if is_base(m):
        trace.OUT(res, "machine category: base")
        section_typedef(res, m)
    else:
        assert is_developed(m)
        trace.OUT(res, "machine category: developed")
        i = implementation(m)
        tmp = comp_indirect(m)
        if tmp != []:
            trace.OUT(res, m["id"] + ": types for transitively imported modules")
            trace.TAB()
            acc = set()
            for q in comp_indirect(m):
                if q.mach["id"] not in acc:
                    state_opaque_typedef(res, q.mach)
                    state_ref_typedef(res, q.mach)
                    acc.add(q.mach["id"])
            acc.clear()
            trace.UNTAB()
        tmp = comp_direct(m)
        if tmp != []:
            trace.OUT(res, m["id"] + ": interfaces of directly imported modules")
            trace.TAB()
            for q in tmp:
                if q.mach["id"] not in acc:
                    trace.OUT(res, "module "+q.mach["id"]+": interface")
                    section_interface(res, q.mach)
                    acc.add(q.mach["id"])
            acc.clear()
            trace.UNTAB()
        if is_stateful(m):
            trace.OUT(res, "module "+m["id"]+ ": stateful")
            section_typedef_impl(res, i, m)
            state_ref_typedef(res, m)
        section_implementation(res, m)

def translate_mode_proj(res, m):
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
    trace.OUT(res, "B machine: " + m["id"])
    trace.OUT(res, "machine category: developed")
    # identify all the module instances that need to be created
    root = Comp([], m)
    comps = [root] + comp_indirect(m)
    # emit the type definitions corresponding to the instantiated modules
    # forward references are disallowed: enumerate definitions bottom-up
    comps.reverse()
    trace.OUT(res, m["id"]+ ": definition of module types")
    trace.TAB()
    acc = set()
    for q in comps:
        if q.mach["id"] not in acc:
            if is_stateful(q.mach):
                trace.OUT(res, "module "+q.mach["id"]+ ": stateful")
                section_typedef(res, q.mach)
                state_ref_typedef(res, q.mach)
            else:
                trace.OUT(res, "module "+q.mach["id"]+ ": stateless")
            acc.add(q.mach["id"])
    acc.clear()
    trace.UNTAB()
    # the instances are now declared, top down
    trace.OUT(res, m["id"]+ ": declaration of variables representing module instances")
    trace.TAB()
    comps.reverse()
    for q in comps:
        if is_stateful(q.mach):
            trace.OUT(res, "declaration of variable corresponding to "+q.bstr())
            res += (str(q)+" = common global "+state_t_name(q.mach) +
                    " zeroinitializer"+nl)
    trace.UNTAB()
    # emit the declarations for the operations offered by root module
    # only the initialisation is necessary actually
    section_interface(res, m)
    # generate the code of the routine that initializes the system
    # by calling the initialization function for the root module.
    args = [state_r_name(root.mach) + sp + str(root)]
    args += [state_r_name(q.mach)+sp+str(q) for q in comp_stateful(m)]
    trace.OUT(res, "definition of function to initialize an instance of "+m["id"]+ " and its components")
    trace.TAB()
    res.extend("define void @$init$() {"+nl+
               "entry:"+nl)
    trace.OUT(res, "call to initialization function of "+m["id"])
    res.extend(tb+"call void "+init_name(m)+"("+commas(args)+")"+nl
               +tb+"ret void"+nl
               + "}")
    trace.UNTAB()

#
# SECTION-LEVEL CODE GENERATION FUNCTIONS
# 

def section_interface(res, m):
    '''
    Generates the declaration of all externally visible elements of machine n:
    reference type, initialisation function, operation function.

    Input:
      - res: bytearray where output shall be stored
      - n: AST root node of a machine
    Output:
    Extends res with text of LLVM declarations (see section interface in translation 
    definition).
    '''
    check_kind(m, {"Machine"})
    section_interface_init(res, m)
    for op in operations(m):
        section_interface_op(res, m, op)

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

def section_interface_init(res, m):
    '''
    Generates the declaration of the initialization function for n

    Inputs:
      - res: bytearray to store output
      - m: a machine AST root node
    Output:
      res is extended with the text of a LLVM function declaration for
      the initalisation
    '''
    global nl
    check_kind(m, {"Machine"})
    comp = list()
    trace.OUT(res, m["id"]+": declaration of function implementing initialization")
    if is_stateful(m):
        comp.append(m)
    comp.extend([x.mach for x in comp_indirect(m)])
    res.extend("declare void"+sp+init_name(m))
    res.extend("("+commas(list_machine_refs(comp))+")"+nl)

def section_interface_op(res, m, op):
    '''
    Declaration of the function implementing operation op in m.

    Inputs:
      - res: bytearray to store output
      - m: a machine AST root node
      - op: an operation AST node
    Output:
      Text of a LLVM function declaration.
    '''
    global nl
    # compute in tl the list of arguments types
    trace.OUT(res, m["id"]+": declaration of function implementing operation " + op["id"])
    tl = list()
    if is_stateful(m):
        tl.append(state_r_name(m))
    tl.extend([ x_type(i["type"]) for i in op["inp"] ])
    tl.extend([ x_type(o["type"])+"*" for o in op["out"] ])
    res.extend("declare void"+sp+op_name(op)+"("+commas(tl)+")"+nl)

def section_typedef(res, m):
    '''
    Generates the definition of the state type machine m.

    Inputs:
      - res: bytearray to store output
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
        section_typedef_impl(res, implementation(m), m)
    else:
        assert is_base(m)
        if is_stateful(m):
            trace.OUT(res, m["id"] + ": definition of type coding the state")
            res.extend(state_t_name(m)+" = type {")
            res.extend(commas([x_type(v["type"]) for v in m["variables"]]))
            res.extend("}"+nl)

def section_typedef_impl(res, i, m):
    '''
    Generates the section implementation of the translation to LLVM.

    Inputs:
      - res: bytearray to store output
      - i: AST node for a B implementation
      - m: AST node for the B machine corresponding to i
    Output:
    String with the definitions of the LLVM functions implementing the
    initialisation and operations of the implementation i.
    '''
    check_kind(i, {"Impl"})
    check_kind(m, {"Machine"})
    if is_stateful(i):
        trace.OUT(res, "module "+m["id"] + ": definition of type coding the state (impl.: "+i["id"] + ")")
        res.extend(state_t_name(m)+" = type {")
        res.extend(commas(imports_type(i["imports"]) +
                          [x_type(v["type"]) for v in i["variables"]]))
        res.extend("}"+nl)

def section_implementation(res, m):
    '''
    Generates the section implementation of the translation to LLVM.

    Inputs:
      - res: a bytearray where text is appended
      - m: AST node for a B machine
    Output:
    String with the definitions of the LLVM functions implementing the
    initialisation and operations of the implementation of n in the
    project proj.    
    '''
    check_kind(m, {"Machine"})
    if is_developed(m):
        i = implementation(m)
        x_init(res, m, i)
        for op in i["operations"]:
            x_operation(res, op)

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

def x_init(res, m, i):
    '''
    Input:
      - res: a bytearray to store output
      - m: root AST node of a B machine
      - i: root AST node of the implementation of m
    Output:
    LLVM implementation of the initialization clause of i (a LLVM function).
    '''
    global tb, nl, sp
    check_kind(m, {"Machine"})
    check_kind(i, {"Impl"})
    trace.OUT(res, "definition of function implementing initialization for "+i["id"])
    tm = state_r_name(m) # LLVM type name: pointer to structure storing m data
    names.reset()
    # 1. generate function signature: one parameter for the implementation
    # instance, one parameter for each transitively imported module instance.
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
    res.extend("define void"+sp+init_name(i)+"("+commas(arg_list)+") {"+nl)
    trace.TAB()
    trace.OUT(res, "%self$: address of structure storing main component")
    for q in comp_indirect(m):
        if is_stateful(q.mach):
            trace.OUT(res, lexicon[q]+": address of structure storing component "+q.bstr())
    trace.UNTAB()
    # 2. generate function body
    res.extend("entry:"+nl)
    # 2.1 reserve stack space for local variables
    x_alloc_inst_list(res, i["initialisation"])
    # 2.2 bind direct imports to elements of state structure
    direct = [ q for q in comp_direct(m) if is_stateful(q.mach) ]
    if direct != []:
        trace.OUT(res, "bind addresses of structures representing components of "+i["id"])
        trace.OUT(res, "to fields of main structure.")
        trace.TAB()
        for j in range(len(direct)):
            lbl = names.new_local()
            q = direct[j]
            trace.OUT(res, "bind component " + q.bstr() + " to structure element " + str(j))
            tm2 = state_r_name(q.mach)
            res.extend(tb+lbl+" = getelementptr "+tm+" %self$, i32 0, i32 "+str(j)+nl)
            res.extend(tb+"store "+tm2+sp+lexicon[q]+", "+tm2+"* "+lbl+nl)
        trace.UNTAB()
    # 2.3 initialize direct imports
    offset = len(direct)+1
    if comp_direct(m) != []:
        trace.OUT(res, "initialize components")
        trace.TAB()
        for q in comp_direct(m):
            mq = q.mach     # the imported machine
            arg_list2 = []  # to store parameters needed to initialize mq
            if is_stateful(mq):
                arg_list2.append(state_r_name(mq)+sp+lexicon[q])
                n = len([x for x in comp_indirect(mq) if is_stateful(x.mach)])
                arg_list2.extend(arg_list[offset:offset+n])
                trace.OUT(res, "call to initialization function for component " + q.bstr())
                res.extend(tb+"call void "+init_name(mq)+"("+commas(arg_list2)+")"+nl)
        trace.UNTAB()
    # 2.4 translate initialisation instructions
    trace.OUT(res, "execute substitutions in initialisation of "+i["id"]+", then branch to exit")
    x_inst_list_label(res, i["initialisation"], "exit")
    trace.OUT(res, "exit point of the initialisation")
    res.extend("exit:"+nl)
    res.extend(tb+"ret void"+nl)
    res.extend("}"+nl)

### TRANSLATION OF OPERATIONS

def x_operation(text, n):
    '''
    Code generation for B operations.

    Input:
      - text: a byte array where LLVM code is stored
      - n: an AST node for a B operation
    '''
    global tb, nl
    check_kind(n, {"Oper"})
    names.reset()
    trace.OUT(text, "definition of function implementing operation "+n["id"]+" in "+n["root"]["id"])
    text.extend("define void "+op_name(n))
    text.extend("("+commas([state_r_name(n["root"])+sp+"%self$"]+
                          [x_type(i["type"])+sp+"%"+i["id"] for i in n["inp"]]+
                          [x_type(o["type"])+"*"+sp+"%"+o["id"] for o in n["out"]])+")")
    text.extend("{"+nl)
    trace.TAB()
    text.extend("entry:"+nl)
    x_alloc_inst(text, n["body"])
    x_inst_label(text, n["body"], "exit")
    text.extend("exit:"+nl)
    text.extend(tb+"ret void"+nl)
    text.extend("}"+nl)
    trace.UNTAB()

### TRANSLATION OF STACK VARIABLE ALLOCATION

def x_alloc_inst_list(text, il):
    '''
    Generation of frame stack allocation for instruction lists.

    Input:
      - text: a bytearray where LLVM code is stored
      - il: a list of B instructions AST nodes

    This function is part of a recursive traversal of the syntax tree so that
    all variable declarations are visisted and handled by function
    x_alloc_var_decl.
    '''
    for inst in il:
        x_alloc_inst(text, inst)

def x_alloc_inst(text, n):
    '''
    Generation of frame stack allocation for individual instructions.
    
    Input:
      - text: a byterray where LLVM code is stored
      - n: AST node for a B instruction

    This function is part of a recursive traversal of the syntax tree so that
    all variable declarations are visisted and handled by function
    x_alloc_var_decl.
    '''
    check_kind(n, {"Beq", "Blk", "Call", "Case", "If", "Skip", "VarD", "While"})
    if n["kind"] in {"Beq", "Call"}:
        return
    elif n["kind"] in {"Case", "If"}:
        for br in n["branches"]:
            x_alloc_inst(text, br["body"])
    elif n["kind"] in {"Blk", "While"}: 
        x_alloc_inst_list(text, n["body"])
    elif n["kind"] == "VarD":
        x_alloc_var_decl(text, n)
    else:
        print("error: unknown instruction kind")
        res.extend("<error inserted by b2llvm>")
    
def x_alloc_var_decl(text, n):
    '''
    Generation of frame stack allocation for variable declarations.
    
    Input:
      - text: a byterray where LLVM code is stored
      - n: AST node for a B variable declaration

    Emits one LLVM alloca instruction for each declared variable and 
    processes the variable declaration body of instructions.
    '''
    global tb, nl, sp
    check_kind(n, {"VarD"})
    trace.OUT(text, "local variable declarations implemented as frame stack allocations")
    trace.TAB()
    for v in n["vars"]:
        trace.OUT(text, "frame stack allocation for variable "+v["id"])
        text.extend(tb+"%"+v["id"]+" = alloca "+x_type(v["type"])+nl)
    x_alloc_inst_list(text, n["body"])
    trace.UNTAB()

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

def x_inst_list_label(text, l, lbl):
    global tb, nl
    if len(l) == 0:
        text.extend(tb + "br label %" + lbl + nl)
    else:
        i = l[0]
        l2 = l[1:]
        if i["kind"] in {"Case", "If", "While"}:
            lbl2 = names.new_label()
            x_inst_label(res, i, lbl2)
            text.extend(lbl2 + ":\n")
        elif i["kind"] in {"Blk"}:
            x_inst_list(text, i["body"])
        else:
            x_inst(text, i)
        x_inst_list_label(text, l2, lbl)

def x_inst_list(text, il):
    '''
    Input:
      - text: bytearray to store LLVM code
      - il: list of instruction AST nodes
    '''
    for inst in il:
        if inst["kind"] in {"If", "While"}:
            label = names.new_label()
            x_inst_label(text, inst, label)
            text.extend(label + ":\n")
        elif inst["kind"] in {"Blk"}:
            x_inst_list(text, inst["body"])
        else:
            x_inst(text, inst)

def x_inst_label(text, n, lbl):
    check_kind(n, {"Beq", "Blk", "Call", "Case", "If", "VarD", "While"})
    if n["kind"] == "Blk":
        x_inst_list_label(text, n["body"], lbl)
    elif n["kind"] == "Case":
        x_case(text, n, lbl)
    elif n["kind"] == "If":
        x_if(text, n, lbl)
    elif n["kind"] == "While":
        x_while(text, n, lbl)
    elif n["kind"] in {"Beq", "Call"}:
        x_inst(text, n)
        text.extend(tb + "br label %" + lbl + nl)
    elif n["kind"] == "VarD":
        x_inst_list_label(text, n["body"], lbl)
    else:
        print("error: instruction type unknown")
        text.extend("<error inserted by b2llvm>")

def x_inst(text, n):
    check_kind(n, {"Beq", "Call", "VarD"})
    if n["kind"] == "Beq":
        x_beq(text, n)
    elif n["kind"] == "Call":
        x_call(text, n)
    elif n["kind"] == "VarD":
        x_inst_list(text, n["body"])

### TRANSLATION OF SKIP ###

def translate_skip(text, n):
    check_kind(n, {"Skip"})

### TRANSLATION OF CASE INSTRUCTIONS

def x_case(text, n, lbl):
    '''
    Generates LLVM code for a B case instruction.

    Input:
      - text: a byterray where LLVM code is stored
      - n: an AST node representing a B instruction
      - lbl: a LLVM label for the block where control flow must go after
      executing n.
    '''
    global nl, tb, sp
    check_kind(n, {"Case"})
    v,t = x_expression(text, n["expr"])
    branches = n["branches"]
    # generate one block label for each branch
    labels = x_case_label_list(branches)
    # there is a special treatment for in case there is no explicit
    # default branch (the last branch in the AST is not a default branch)
    last = branches(len(branches)-1)
    default = "val" not in br.keys() or br["val"] == [] or br["val"] == None
    # generate block label for default branch
    if default:
        lblo = labels[len(branches)-1]
    else:
        lblo = names.new_label()
    text.extend(tb + "switch " + t + sp + v + ", label %" + lblo + " [" + nl)
    x_case_jump_table(text, branches, labels)
    text.extend(tb + "]" + nl)
    text.extend(x_case_block_list(branches, labels, default, lblo))

def x_case_label_list(bl):
    '''
    Input:
      - bl: list of case branches
    Output:
      - list of LLVM block labels, one for each non-default branch
    '''
    return [ names.new_label() for branch in bl]

def x_case_jump_table(text, bl, labels):
    ''' 
    Generates a LLVM jump table for a switch instruction implementing the case
    branches.

    Input:
      - text: a bytearray where LLVM output is stored
      - bl: a list of case branches
      - labels: a list block labels
    '''
    for i in range(len(bl)):
        x_case_val_list(text, bl[i]["val"], labels[i])

def x_case_val_list(text, vl, lbl):
    '''
    Generates entries in the LLVM jump table from values to a block label.

    Input:
      - text: a bytearray where output is stored
      - vl: a list of AST nodes representing B values
      - lbl: a LLVM block label
    '''
    global tb2, sp, nl
    text2 = bytearray()
    for v in vl:
        # the evaluation of the values should not emit LLVM code
        v, t = x_expression(text2, v)
        assert(len(text2) == 0)
        text.extend(tb2 + t + sp + v + ", label %" + lbl + nl)

def x_case_block_list(text, bl, labels, lble, default, lbld):
    ''' 
    Generates LLVM code blocks of a switch implementing the instructions in the
    branches of a case instruction.

    Input:
      - text: a bytearray where LLVM output is stored
      - bl: a list of case branches
      - labels: a list block labels
      - lble: label of block where control flow must go after executing a branch
      - default: flag indicating if the last branch is a default branch
      - lbld: label of block for default block 
    '''
    for i in range(len(bl)):
        branch = bl[i]
        lbl = labels[i]
        text.extend(tb+lbl+":"+nl)
        text.extend(x_inst_label(branch["body"], lble))
    if not default:
        text.extend(tb+lbld+":"+nl)
        text.extend(tb+"branch label %"+lble)

### TRANSLATION OF IF INSTRUCTIONS

def x_if(text, n, lbl):
    '''
    Generates LLVM code for a B if instruction.

    Input:
      - text: a byterray where LLVM code is stored
      - n: an AST node representing a B if instruction
      - lbl: a LLVM label for the block where control flow must go after
      executing n.
    '''
    check_kind(n, {"If"})
    x_if_br(text, n["branches"], lbl)

def x_if_br(text, lbr, lbl):
    '''
    Generates LLVM code for a list of B if instruction branches.

    Input:
      - text: a byterray where LLVM code is stored
      - lbr: a list of AST nodes representing B if instruction branches
      - lbl: a LLVM label for the block where control flow must go after
      executing n.
    '''
    assert(len(lbr)>=1)
    # br: first if branch, lbr2: list of remaining branches
    br = lbr[0]
    lbr2 = lbr[1:]
    check_kind(br, {"IfBr"})
    # br is the last branch
    if lbr2 == []:
        # br is an else branch
        if "cond" not in br.keys() or br["cond"] == None:
            x_inst_label(text, br["body"], lbl)
        # br is an elsif branch
        else:
            lbl_1 = names.new_label()
            x_formula(text, br["cond"], lbl_1, lbl)
            text.extend(lbl_1 + ":" + nl)
            x_inst_label(text, br["body"], lbl)
    # br is not the last branch
    else:
        lbl_1 = names.new_label()
        lbl_2 = names.new_label()
        x_formula(text, br["cond"], lbl_1, lbl_2)
        text.extend(lbl_1 + ":" + nl)
        x_inst_label(text, br["body"], lbl)
        text.extend(lbl_2 + ":" + nl)
        x_if_br(text, lbr2, lbl)

### TRANSLATION OF WHILE INSTRUCTIONS

def x_while(text, n, lbl):
    '''
    Generates LLVM code for a B while instruction.

    Input:
      - text: a byterray where LLVM code is stored
      - n: an AST node representing a B while instruction
      - lbl: a LLVM label for the block where control flow must go after
      executing n.
    '''
    global nl, tb, sp
    check_kind(n, {"While"})
    lbl1 = names.new_label()
    text.extend(lbl1 + ":" + nl)
    v = x_pred(text, n["cond"])
    lbl2 = names.new_label()
    text.extend(tb + "br i1 " + v + ", label %" + lbl2 + ", label %" + lbl + nl)
    text.extend(lbl2 + ":")
    x_inst_list_label(text, n["body"], lbl1)

### TRANSLATION OF BECOMES EQUAL INSTRUCTIONS

def x_beq(text, n):
    '''
    Generates LLVM code for a B assignment (becomes equal) instruction.

    Input:
      - text: a byterray where LLVM code is stored
      - n: an AST node representing a B assignment instruction
    '''
    global tb, sp, nl
    check_kind(n, {"Beq"})
    v,t = x_expression(text, n["rhs"])
    p,_ = x_lvalue(text, n["lhs"])
    text.extend(tb + "store " + t + sp + v + ", " + t + "* " + p + nl)

def x_lvalue(text, n):
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
        text.extend(tb + v + " = getelementptr " + state_r_name(n["root"])+ 
                    " %self$, i32 0, i32 " + str(state_position(n)) + nl)
        return (v, t)
    elif n["scope"] in {"Oper", "Local"}:
        return ("%"+n["id"],t)
    else:
        text.extend("<error inserted by b2llvm>")
        print("error: unknown scope for variable " + v["id"])
        return ("UNKNOWN", "UNKNOWN")

### TRANSLATION OF CALL INSTRUCTIONS

def x_call(text, n):
    global sp
    check_kind(n, {"Call"})
    operation = n["op"]
    local = (n["inst"] == None) # is a local operation?
    impl = operation["root"]
    # evaluate arguments
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
            text.extend(tb+v1+" = getelementptr "+mach_t+
                        " %self$, i32 0, i32 "+str(state_position(n["inst"]))+
                    nl)
            text.extend(tb + v2 + " = load " + t +"*" + sp + v1 + nl)
        args.append(t + sp + v2)
    x_inputs(text, args, n["inp"])
    x_outputs(text, args, n["out"])
    id = op_name(operation)
    text.extend(tb + "call void" + sp + id + "(" + commas(args) + ")" + nl)

def x_inputs(text, args, n):
    global sp
    for elem in n:
        v,t = translate_expression(text, elem)
        args.append(t + sp + v)

def x_outputs(text, args, n):
    global sp
    for elem in n:
        v,t = x_lvalue(text, elem)
        args.append(t + sp + v)

### TRANSLATION OF CONDITIONS ###

def x_formula(text, n, lbl1, lbl2):
    check_kind(n, {"Comp", "Form"})
    if n["kind"] == "Comp":
        v = x_comp(text, n)
        text.extend(tb+"br i1 "+v+" , label %"+lbl1+", label %"+lbl2+nl)
    elif n["kind"] == "Form":
        if n["op"] == "and":
            x_and(text, n, lbl1, lbl2)
        elif n["op"] == "or":
            x_or(text, n, lbl1, lbl2)
        elif n["op"] == "not":
            x_not(text, n, lbl1, lbl2)
        else:
            text.extend("<error inserted by b2llvm>")
    else:
        text.extend("<error inserted by b2llvm>")

def x_comp(text, n):
    global tb, sp, nl
    check_kind(n, {"Comp"})
    v1,t1 = x_expression(text, n["arg1"])
    v2,t2 = x_expression(text, n["arg2"])
    v = names.new_local()
    text.extend(tb+v+" = icmp "+llvm_op(n["op"])+sp+t1+sp+v1+", "+v2+nl)
    return v

def x_and(text, n, lbl1, lbl2):
    check_kind(n, {"Form"})
    assert(n["op"] == "and")
    assert(len(n["args"]) == 2)
    arg1 = n["args"][0]
    arg2 = n["args"][1]
    lbl = names.new_label()
    x_formula(text, arg1, lbl, lbl2)
    text.extend(lbl + ":" + nl)
    x_formula(text, arg2, lbl1, lbl2)

def x_or(text, n, lbl1, lbl2):
    check_kind(n, {"Form"})
    assert(n["op"] == "or")
    assert(len(n["args"]) == 2)
    arg1 = n["args"][0]
    arg2 = n["args"][1]
    lbl = names.new_label()
    x_formula(text, arg1, lbl1, lbl)
    text.extend(lbl + ":" + nl)
    x_formula(text, arg2, lbl1, lbl2)

def x_not(text, n, lbl1, lbl2):
    check_kind(n, {"Form"})
    assert(n["op"] == "not")
    x_formula(text, n["args"][0], lbl2, lbl1)

def x_pred(text, n):
    if n["kind"] == "Comp":
        return x_comp(text, n)
    else:
        text.extend("<error inserted by b2llvm>")
        return ""

### TRANSLATION OF EXPRESSIONS ###

def x_expression(text, n):
    check_kind(n, {"IntegerLit", "BooleanLit", "Vari", "Term", "Cons"})
    if n["kind"] == "IntegerLit":
        return x_integerlit(text, n)
    elif n["kind"] == "BooleanLit":
        return x_booleanlit(text, n)
    elif n["kind"] == "Vari":
        return x_name(text, n)
    elif n["kind"] == "Term":
        return x_term(text, n)
    elif n["kind"] == "Cons":
        return x_expression(text, n["value"])
    else:
        return ("","")

def x_integerlit(text, n):
    check_kind(n, {"IntegerLit"})
    return (n["value"],"i32")

def x_booleanlit(text, n):
    check_kind(n, {"BooleanLit"})
    if n["value"] == "TRUE":
        val = "1"
    else:
        val = "0"
    return (val,"i1")

def x_name(text, n):
    check_kind(n, {"Vari"})
    t = x_type(n["type"])
    if n["scope"] == "Local":
        v1 = "%"+n["id"]
        v2 = names.new_local()
        text.extend(tb + v2 + " = load" + sp + t + "*" + sp + v1 + nl)
        return (v2, t)
    elif n["scope"] == "Oper":
        return ("%"+n["id"], t)
    elif n["scope"] == "Impl":
        p = names.new_local()
        v = names.new_local()
        text.extend(tb+p+" = getelementptr "+state_t_name(n["root"])+" %self$, i32 0, i32 "+str(state_position(n))+nl)
        text.extend(tb + v + " = load " + t + "* " + p + nl)
        return (v, t)
    else:
        text.extend("<error inserted by b2llvm>")
        return ("", "")
        
def x_term(text, n):
    global tb, sp, nl
    check_kind(n, {"Term"})
    if n["op"] == "succ" or n["op"] == "pred":
        return x_unary(text, n)
    else:
        assert(len(n["args"]) == 2)
        v1,t1 = x_expression(text, n["args"][0])
        v2,t2 = x_expression(text, n["args"][1])
        v = names.new_local()
        text.extend(tb + v + " = " + llvm_op(n["op"]) + sp + t1 + sp + v1 + ", " + v2 + nl)
        return (v, t1)

def x_unary(text, n):
    check_kind(n, {"Term"})
    assert (n["op"] in {"succ", "pred"})
    if n["op"] == "succ":
        v,t = x_expression(text, n["args"][0])
        w = names.new_local()
        text.extend(tb + w + " = add i32 1," + sp + v + nl)
        return (w, "i32")
    elif n["op"] == "pred":
        v,t = x_expression(text, n["args"][0])
        w = names.new_local()
        text.extend(tb + w + " = sub i32 " + v + ", 1" + nl)
        return (w, "i32")
    else:
        text.extend("<error inserted by b2llvm>")
        return ("", "")

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

def op_name(n):
    '''
    - Input:
      n: A node representing a B operation
    - Output:
      A string for the name of the LLVM construct representing n.
    '''
    check_kind(n, "Operation")
    root = n["root"]
    check_kind(root, "Impl")
    machine = root["machine"]
    return "@" + machine["id"] + "$" + n["id"]

def init_name(n):
    '''
    - Input:
      n : a node representing a B machine or implementation
    - Output:
    String with the name of the LLVM function encoding the initialization
    of that implementation.
    '''
    check_kind(n, {"Machine", "Impl"})
    mach = n if n["kind"] == "Machine" else n["machine"]
    return "@"+mach["id"]+"$init$"

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

def state_opaque_typedef(res, m):
    '''
    Input:
      - res: bytearray to store output
      - m: represents a B machine
    Desc:
      Appends to res the LLVM definition of type pointer to type representing the
      state of n.
      This only makes sense if n is stateful.
    '''
    global nl
    trace.OUT(res, "module "+m["id"]+": declaration of type for state")
    res.extend(state_t_name(m) + " = type opaque" + nl)

def state_ref_typedef(res, m):
    '''
    Input:
      - res: bytearray to store output
      - m: represents a B machine
    Desc:
      Adds to res the LLVM definition of type pointer to type representing the
      state of n.
      This only makes sense if n is stateful.
    '''
    global nl
    trace.OUT(res, "module "+m["id"]+": definition of type pointer to state")
    res.extend(state_r_name(m) + " = type " + state_t_name(m) + "*" + nl)

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
        self.b_id = m["id"] if p == [""] else ".".join(p+[m["id"]])
    def __str__(self):
        return self.id
    def __hash__(self):
        return self.id.__hash__()
    def bstr(self):
        return self.b_id

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


