###
#
# Prototype for a LLVM-IR generator for B
#
# Caveat: This is the first Python program of the author, and he is aware
# that an object oriented (or, rather, a class oriented) solution could be
# appropriate.
#
###

import ast

### LLVM IDENTIFIER GENERATION ###

# the code in this section is responsible for generating LLVM names for
# local variables and labels

llvm_local_var_counter = 0
llvm_label_counter = 0
def new_llvm_local_var():
    '''
    Input: None
    Output: A string representing a LLVM local variable. This string
    is composed by the prefix "%" followed by a number. Function
    reset_llvm_names is responsible for zeroing that number.
    '''
    global llvm_local_var_counter
    result = "%"+str(llvm_local_var_counter)
    llvm_local_var_counter += 1
    return result

def new_llvm_label():
    '''
    Input: None
    Output: A string representing a LLVM instruction label. This string
    is composed by the prefix "label" followed by a number. Function
    reset_llvm_names is responsible for zeroing that number.
    '''
    global llvm_label_counter
    result = "label"+str(llvm_label_counter)
    llvm_label_counter += 1
    return result

def reset_llvm_names():
    '''
    Output: None
    The role of this function is to zero the counters used to build
    label and local variable identifiers.
    '''
    global llvm_local_var_counter, llvm_label_counter
    llvm_local_var_counter = 0
    llvm_label_counter = 0

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
      n: A node representing a B implementation
    - Output:
      A string for the name of the LLVM type representing the state of
      the implementation n.
    '''
    check_kind(n, {"Impl"})
    return "%"+n["id"]+"$state$"

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
        >>> llvm_op("=") == eq
        True
        >>> llvm_op("+") == add
        True
    Note: An error message is printed and the empty string
    is returned if the translation has not been defined.
    '''
    if str == "=":
        return "eq"
    elif str == "!=":
        return "ne"
    elif str == "<":
        return "slt"
    elif str == "<=":
        return "sle"
    elif str == ">":
        return "sgt"
    elif str == ">=":
        return "sge"
    elif str == "+":
        return "add"
    elif str == "-":
        return "sub"
    elif str == "*":
        return "mul"
    elif str == "/":
        return "sdiv"
    elif str == "mod":
        return "srem"
    else:
        print("error: operator " + str + " not translated")
        return ""
        
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

nl = "\n"
sp = " "
tb = "  "
tb2 = tb*2

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
    for n2 in root["imports"] + root["concrete_variables"]:
        if n2 == n:
            return result
        result += 1
    print("error: position of imported machine or variable not found in implementation")
    return 0

### TYPE TRANSLATION ###

#
# This function is responsible for translation B0 type names to LLVM types
#
def translate_type(t):
    assert(t == ast.INT or t == ast.BOOL)
    if t == ast.INT:
        return "i32"
    else:
        return "i1"

#
# This function is responsible for building the LLVM type expression for
# the type corresponding to the state of B0 implementation n.
#
def state_expression(n):
    check_kind(n, {"Impl", "Mach"})
    result = "{"
    components = []
    for impo in n["imports"]:
        components += [state_t_name(impo["mach"]["impl"])]
    for var in n["concrete_variables"]:
        components += [translate_type(var["type"])]
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
    check_kind(n, {"Impl", "Mach"})
    if (len(n["concrete_variables"]) == 0):
        return ""
    else:
        return state_t_name(n) + " = type " + state_expression(n) + nl

def variable_position(v):
    check_kind(v, {"Vari"})
    m = v["root"]
    for idx in range(len(m["concrete_variables"])):
        if v == m["concrete_variables"][idx]:
            return idx
    print("error: variable " + v["id"] + " not found in variable_position")
    assert(false)

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
    t = translate_type(n["type"])
    if n["scope"] == "Local":
        v1 = "%"+n["id"]
        v2 = new_llvm_local_var()
        t = translate_type(n["type"])
        text = tb+ v2 + " = load" + sp + t + "*" + sp + v1 + nl
        return (text, v2, t)
    elif n["scope"] == "Oper":
        return ("", "%"+n["id"], t)
    elif n["scope"] == "Impl":
        p = new_llvm_local_var()
        v = new_llvm_local_var()
        text = ""
        text += tb + p + " = getelementptr " + state_t_name(n["root"]) + "*" + sp + "%self$, i32 0, i32 " + str(variable_position(n)) + nl
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
        w = new_llvm_local_var()
        text = ""
        text += p
        text += tb + w + " = add i32 1," + sp + v + nl
        return (text, w, "i32")
    elif n["op"] == "pred":
        p,v,t = translate_expression(n["args"][0])
        w = new_llvm_local_var()
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
        v = new_llvm_local_var()
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
    v = new_llvm_local_var()
    return (p1 +
            p2 +
            tb + v + " = icmp " + llvm_op(n["op"]) + sp + t1 + sp + v1 + ", " + v2 + nl), v

def translate_pred(n):
    if n["kind"] == "Comp":
        return translate_comp(n)
    else:
        print("not implemented translation for such predicate")
        return ("", "")

def translate_and(n, lbl1, lbl2):
    check_kind(n, {"Form"})
    assert(n["op"] == "and")
    assert(len(n["args"]) == 2)
    arg1 = n["args"][0]
    arg2 = n["args"][1]
    lbl = new_llvm_label()
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
    lbl = new_llvm_label()
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
        print("not implemented translate_form for formulas.")
        return ""

### TRANSLATION OF INSTRUCTIONS ###

def translate_lv(n):
    global tb, nl
    check_kind(n, {"Vari"})
    t = translate_type(n["type"]) + "*"
    if n["scope"] == "Impl":
        v = new_llvm_local_var()
        return (tb + v + " = getelementptr " + state_t_name(n["root"])+ "* %self$, i32 0, i32 " + str(variable_position(n)) + nl, v, t)
    elif n["scope"] in {"Oper", "Local"}:
        return ("", "%"+n["id"],t)
    else:
        print("unknown scope for variable " + v["id"])
        return ("", "UNKNOWN")

def translate_beq(n):
    global tb, sp, nl
    check_kind(n, {"Beq"})
    r,v,t = translate_expression(n["rhs"])
    l,p,_ = translate_lv(n["lhs"])
    return (r + 
            l + 
            tb + "store " + t + sp + v + ", " + t + "* " + p + nl)

def translate_skip(n):
    check_kind(n, {"Skip"})
    return ""

def translate_if_br(lbr, lbl):
    assert(len(lbr)>=1)
    br = lbr[0]
    check_kind(br, {"IfBr"})
    lbr2 = lbr[1:]
    if len(lbr2) > 0:
        lbl_1 = new_llvm_label()
        lbl_2 = new_llvm_label()
        result = ""
        result += translate_form(br["cond"], lbl_1, lbl_2)
        result += lbl_1 + ":\n"
        result += translate_inst_label(br["body"], lbl)
        result += lbl_2 + ":\n"
        result += translate_if_br(lbr2, lbl)
    else:
        if "cond" not in br.keys() or br["cond"] == None:
            result = translate_inst_label(br["body"], lbl)
        else:
            lbl_1 = new_llvm_label()
            result = ""
            result += translate_form(br["cond"], lbl_1, lbl)
            result += lbl_1 + ":\n"
            result += translate_inst_label(br["body"], lbl)
    return result

def translate_if(n, lbl):
    check_kind(n, {"If"})
    return translate_if_br(n["branches"], lbl)

def translate_while(n, lbl):
    global nl, tb, sp
    check_kind(n, {"While"})
    lbl1 = new_llvm_label()
    (c, v) = translate_pred(n["cond"])
    lbl2 = new_llvm_label()
    body = translate_inst_list_label(n["body"], lbl1)
    result = ""
    result += tb + "br label %" + lbl1 + nl
    result += lbl1 + ":" + nl
    result += c
    result += tb + "br i1 " + v + ", label %" + lbl2 + ", label %" + lbl +nl
    result += lbl2 + ":" + nl
    result += body
    return result

def translate_case_val_list(vl, lbl):
    global tb2, sp, nl
    result = ""
    for v in vl:
        p, v, t = translate_expression(v)
        result += tb2 + t + sp + v + ", label %" + lbl + nl
    return result

def translate_case_branch_list(bl, lblo, lble):
    br = bl[0]
    bl2 = bl[1:]
    j, b = "", ""
    if bl2 == []:
        if "val" not in br.keys() or br["val"] == [] or br["val"] == None:
            b += tb + lblo + ":" + nl
            b += translate_inst_label(br["body"], lble)
        else:
            lbl = new_llvm_label()
            j += translate_case_val_list(br["val"], lbl)
            b += tb + lbl + ":" + nl
            b += translate_inst_label(br["body"], lble)
            b += tb + lblo + ":" + nl
            b += tb + "branch label %" + lble
    else:
        lbl = new_llvm_label()
        j += translate_case_val_list(br["val"], lbl)
        b += lbl + ":" + nl
        b += translate_inst_label(br["body"], lble)
        j2, b2 = translate_case_branch_list(bl2, lblo, lble)
        j += j2
        b += b2
    return j, b

def translate_case(n, lbl):
    global nl, tb, sp
    check_kind(n, {"Case"})
    p,v,t = translate_expression(n["expr"])
    lblo = new_llvm_label()
    j, b = translate_case_branch_list(n["branches"], lblo, lbl)
    result = ""
    result += p
    result += tb + "switch " + t + sp + v + ", label %" + lblo + " [" + nl
    result += j
    result += tb + "]" + nl
    result += b
    return result

def translate_inputs(n):
    global sp
    preamble = ""
    args = []
    for elem in n:
        p,v,t = translate_expression(elem)
        preamble += p
        args.append(t + sp + v)
    return preamble, args

def translate_outputs(n):
    global sp
    preamble = ""
    args = []
    for elem in n:
        p,v,t = translate_lv(elem)
        preamble += p
        args.append(t + sp + v)
    return preamble, args

def translate_call(n):
    global sp
    check_kind(n, {"Call"})
    operation = n["op"]
    pi, il = translate_inputs(n["inp"])
    po, ol = translate_outputs(n["out"])
    result = ""
    result += pi
    result += po
    id = global_name(operation)
    ty = state_t_name(operation["root"])
    if n["inst"] == None:
        val = "%self$"
    else:
        val = new_llvm_local_var()
        result += (tb + val + " = getelementptr " + 
                   state_t_name(n["inst"]["root"]) + "* " +
                   "%self$, i32 0, i32 " + 
                   str(state_position(n["inst"])) + nl)
    args = [ty + sp + val] + il + ol
    result += tb + "call void" + sp + id + "(" + ", ".join(args) + ")" + nl
    return result

def translate_inst(n):
    check_kind(n, {"Beq", "Call", "VarD"})
    if n["kind"] == "Beq":
        return translate_beq(n)
    elif n["kind"] == "Call":
        return translate_call(n)
    elif n["kind"] == "VarD":
        return translate_inst_list(n["body"])
    else:
        return ""

def translate_inst_label(n, lbl):
    check_kind(n, {"Beq", "Blk", "Call", "Case", "If", "VarD", "While"})
    if n["kind"] == "Blk":
        return translate_inst_list_label(n["body"], lbl)
    elif n["kind"] == "Case":
        return translate_case(n, lbl)
    elif n["kind"] == "If":
        return translate_if(n, lbl)
    elif n["kind"] == "While":
        return translate_while(n, lbl)
    elif n["kind"] in {"Beq", "Call"}:
        result = ""
        result += translate_inst(n)
        result += tb + "br label %" + lbl + nl
        return result
    elif n["kind"] == "VarD":
        return translate_inst_list_label(n["body"], lbl)
    else:
        print("error: instruction type unknown")

def translate_inst_list(l):
    if len(l) == 0:
        return ""
    else:
        i = l[0]
        l2 = l[1:]
        if i["kind"] in {"If", "While"}:
            lbl2 = new_llvm_label()
            p1 = translate_inst_label(i, lbl2) + lbl2 + ":\n"
        elif i["kind"] in {"Blk"}:
            p1 = translate_inst_list(i["body"])
        else:
            p1 = translate_inst(i)
        p2 = translate_inst_list(l2)
        return p1 + p2

def translate_inst_list_label(l, lbl):
    global tb, nl
    if len(l) == 0:
        return tb + "br label %" + lbl + nl
    else:
        i = l[0]
        l2 = l[1:]
        if i["kind"] in {"Case", "If", "While"}:
            lbl2 = new_llvm_label()
            p1 = translate_inst_label(i, lbl2) + lbl2 + ":\n"
        elif i["kind"] in {"Blk"}:
            p1 = translate_inst_list(i["body"])
        else:
            p1 = translate_inst(i)
        p2 = translate_inst_list_label(l2, lbl)
        return p1 + p2

### TRANSLATION OF STACK VARIABLE ALLOCATION

def translate_alloc_var_decl(n):
    global tb, nl, sp
    check_kind(n, {"VarD"})
    result = ""
    for v in n["vars"]:
        result += tb+"%"+v["id"]+" = alloca "+translate_type(v["type"])+nl
    result += translate_alloc_inst_list(n["body"])
    return result

def translate_alloc_inst(n):
    check_kind(n, {"Beq", "Blk", "Call", "Case", "If", "Skip", "VarD", "While"})
    if n["kind"] in {"Beq", "Call"}:
        return ""
    elif n["kind"] in {"Case", "If"}:
        result = ""
        for br in n["branches"]:
            result += translate_alloc_inst(br["body"])
        return result
    elif n["kind"] in {"Blk", "While"}: 
        return translate_alloc_inst_list(n["body"])
    elif n["kind"] == "VarD":
        return translate_alloc_var_decl(n)
    else:
        print("error: unknown instruction kind")
        return ""
    
def translate_alloc_inst_list(n):
    result = ""
    for inst in n:
        result += translate_alloc_inst(inst)
    return result

### TRANSLATION OF OPERATIONS AND INITIALISATION

def translate_signature(n):
    check_kind(n, {"Oper"})
    result = ""
    result += "@"+n["root"]["id"]+"$"+n["id"]
    result += "("
    result += state_t_name(n["root"])
    result += "* %self$"
    for inp in n["inp"]:
        t = translate_type(inp["type"])
        id = inp["id"]
        result += "," + sp + t + sp + "%" + id
    for out in n["out"]:
        t = translate_type(out["type"])
        id = out["id"]
        result += "," + sp + t + "*" + sp + "%" + id
    result += ")"
    return result

def translate_import_init_list(n):
    '''
    Input:
      - n: root node of a B implementation AST
    Output:
      LLVM source code consisting of the calls to the initialization functions
      of the instances of machines imported by n.
    '''
    global nl, tb
    check_kind(n, {"Impl"})
    imports = n["imports"]
    idx = 0
    result = ""
    for impo in imports:
        mach = impo["mach"]
        lbl = new_llvm_local_var()
        m = impo["mach"]
        result += (tb + lbl + " = getelementptr " + 
                   state_t_name(n) + "%self$, i32 0, i32 " + str(idx) + nl)
        result += (tb + "call void " + init_name(m) + 
                   "(" + state_t_name(m["impl"]) + "* " + lbl + ")" + nl)
        idx += 1
    return result
    
def translate_init(i):
    '''
    Input:
      - i: root node of a B implementation AST
    Output:
    LLVM implementation of the initialization clause of i (a LLVM function).
    '''
    global tb, nl, sp
    check_kind(i, {"Impl"})
    reset_llvm_names()
    result = "define void" + sp + init_name(i) 
    result += "("+state_t_name(i)+"* %self$) {" + nl
    result += "entry:" + nl
    result += translate_alloc_inst_list(i["initialisation"])
    result += translate_import_init_list(i)
    result += translate_inst_list_label(i["initialisation"], "exit")
    result += "exit:" + nl
    result += tb + "ret void" + nl
    result += "}" + nl
    return result;

def translate_operation(i):
    global tb
    check_kind(i, {"Oper"})
    reset_llvm_names()
    result = ""
    result += "define void" + translate_signature(i) + "{" + nl
    result += "entry:" + nl
    result += translate_alloc_inst(i["body"])
    result += translate_inst_label(i["body"], "exit")
    result += "exit:" + nl
    result += tb + "ret void" + nl
    result += "}" + nl
    return result

### TRANSLATION OF CONSTANT DEFINITIONS

def translate_constant(n):
    global tb, sp, nl
    check_kind(n, {"Cons"})
    if n["type"] not in {"INT", "BOOL"}:
        print("error: constant " + n["id"] + " cannot be translated")
    return ""

def translate_constants(n):
    check_kind(n, {"Impl"})
    result = ""
    if "concrete_constants" in n.keys():
        for const in n["concrete_constants"]:
            result += translate_constant(const)
    return result

### TRANSLATION OF INTERFACE

def translate_interface(n):
    global nl
    check_kind(n, {"Mach"})
    result = ""
    result += translate_state(n)
    result += "declare void @" + n["id"] + "$("+state_t_name(n)+"*)" + nl
    for op in n["operations"]:
        result += "declare void" + translate_signature(op) + nl
    return result

### TRANSLATION OF IMPLEMENTATION

def translate_type_expr_impo(n):
    check_kind(n, {"Impo"})
    return state_t_name(n["mach"]["impl"])

def translate_type_expr_vari(n):
    check_kind(n, {"Vari"})
    return translate_type(n["type"])

def translate_type_expr_impl(n):
    check_kind(n, {"Impl"})
    result = ""
    tl = []
    for ni in n["imports"]:
        tl.append(translate_type_expr_impo(ni))
    for nv in n["concrete_variables"]:
        tl.append(translate_type_expr_vari(nv))
    result += "{" + ", ".join(tl) + "}"
    return result

def translate_type_def_import(n, acc):
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
    check_kind(n, {"Mach"})
    impl = n["impl"]
    result = translate_type_def_import_list(impl, acc)
    result += state_t_name(impl)+ " = type "+ translate_type_expr_impl(impl)+ nl
    return result

def translate_type_def_import_list(n, acc = None):
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
        check_kind(mach, {"Mach"})
        if mach["id"] not in acc:
            acc.add(mach["id"])
            result += translate_type_def_import(mach, acc)
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
        tl.append(translate_type(i["type"]))
    for o in n["out"]:
        tl.append(translate_type(o["type"])+"*")
    result = ""
    result += "declare void " + global_name(n) + "(" + ", ".join(tl) + ")" + nl
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
    check_kind(n, {"Mach"})
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
        check_kind(m, {"Mach"})
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
    result += translate_type_def_import_list(i)
    result += translate_op_decl_import_list(i)
    result += translate_constants(i)
    result += translate_state(i)
    result += translate_init(i)
    for op in i["operations"]:
        result += translate_operation(op)
    if toplevel:
        result += (instance_name(i) + " = common global " 
                   + state_t_name(i) + " zeroinitializer" + nl)
    return result

# def translate(imp, file, toplevel=True):
#     openfile = open(file, 'w')
#     filecontents = translate_implementation(imp, toplevel)
#     openfile.write(";;; -*- mode: asm -*-"+nl) # emacs syntax highlight on
#     openfile.write(";;; File generated with b2llvm.\n")
#     openfile.write(filecontents)
#     openfile.close()

import loadbxml
def translate_bxml(inpfile, outfile, toplevel=True):
    '''
    Parameters:
      - inpfile: the name of the input file, must contain BXML format
      - outfile: the name of the output file, will contain LLVM source code
      - toplevel: optional argument stating if the component is top-level
      (default: True)
    Result:
      None
    '''
    impl = loadbxml.load_implementation(inpfile)
    filecontents = translate_implementation(impl, toplevel)
    llvm = open(outfile, 'w')
    llvm.write(";;; -*- mode: asm -*-"+nl) # emacs syntax highlight on
    llvm.write(";;; file name: "+outfile+nl)
    llvm.write(";;; source: "+inpfile+nl)
    llvm.write(";;; generated with b2llvm."+nl)
    llvm.write(filecontents)
    llvm.close()
