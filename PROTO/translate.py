
### LLVM IDENTIFIER GENERATION ###

# the code in this section is responsible for generating LLVM names for
# local variables and labels

llvm_local_var_counter = 0
llvm_label_counter = 0
def new_llvm_local_var():
    global llvm_local_var_counter
    result = "%"+str(llvm_local_var_counter)
    llvm_local_var_counter += 1
    return result

def new_llvm_label():
    global llvm_label_counter
    result = "label"+str(llvm_label_counter)
    llvm_label_counter += 1
    return result

def reset_llvm_names():
    global llvm_local_var_counter, llvm_label_counter
    llvm_local_var_counter = 0
    llvm_label_counter = 0

def llvm_op(str):
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
    else:
        print("error: operator " + str + " not translated")
        return ""
        
### MISC ###

#
# Function check_kind is used to assert that the arguments of translation
# function arguments are in the correct syntactic category
#
def check_kind(n, s):
    assert(n["kind"] in s)

nl = "\n"
sp = " "
tb = "  "

### TYPE TRANSLATION ###

#
# This function is responsible for translation B0 type names to LLVM types
#
def translate_type(t):
    assert(t == "INT" or t == "BOOL")
    if t == "INT":
        return "i32"
    else:
        return "i1"

#
# Function responsible for producing the name of the type corresponding
# to the state of B0 implementation n
#
def state_name(n):
    check_kind(n, {"Impl"})
    return "%"+n["id"]+"$state$"

#
# This function is responsible for building the LLVM type expression for
# the type corresponding to the state of B0 implementation n.
#
def state_expression(n):
    check_kind(n, {"Impl"})
    result = "{"
    for idx in range(len(n["concrete_variables"])):
        if idx != 0:
            result = result + ","
        result = result + translate_type(n["concrete_variables"][idx]["type"])
    result = result + "}"
    return result

#
# Function responsible for producing LLVM code defining type corresponding to
# the state of B0 implementation n
#
def translate_state(n):
    global nl
    check_kind(n, {"Impl"})
    if (len(n["concrete_variables"]) == 0):
        return ""
    else:
        return state_name(n) + " = type " + state_expression(n) + nl

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
    if n["scope"] == "Impl":
        p = new_llvm_local_var()
        v = new_llvm_local_var()
        text = ""
        text += tb + p + " = getelementptr %self$, i32 0, i32 " + str() + nl
        text += tb + v + " = load " + t + "* " + p + nl
        return (text, v, t)
    else:
        print("error: name translation not supported")
        return ("", "", "")
        
def translate_term(n):
    global tb, sp, nl
    check_kind(n, {"Term"})
    assert(len(n["args"]) == 2)
    p1,v1,t1 = translate_expression(n["args"][0])
    p2,v2,t2 = translate_expression(n["args"][1])
    v = new_llvm_local_var()
    return (p1 +
            p2 +
            tb + v + " = " + llvm_op(n["op"]) + t1 + sp + v1 + sp + v2 + nl), v, t1

def translate_expression(n):
    check_kind(n, {"IntegerLit", "BooleanLit", "Vari", "Term"})
    if n["kind"] == "IntegerLit":
        return translate_integerlit(n)
    elif n["kind"] == "BooleanLit":
        return translate_booleanlit(n)
    elif n["kind"] == "Vari":
        return translate_name(n)
    elif n["kind"] == "Term":
        return translate_term(n)
    else:
        return ("","","")

### TRANSLATION OF CONDITIONS ###

def translate_comp(n, lbl1, lbl2):
    global tb, sp, nl
    check_kind(n, {"Comp"})
    p1,v1,t1 = translate_expression(n["arg1"])
    p2,v2,t2 = translate_expression(n["arg2"])
    v = new_llvm_local_var()
    return (p1 +
            p2 +
            tb + v + " = icmp " + llvm_op(n["op"]) + sp+ t1 + sp + v1 + sp + v2 + nl), v

def translate_pred(n, lbl1, lbl2):
    if n["kind"] == "Comp":
        text, v = translate_comp(n, lbl1, lbl2)
        text += tb + "br i1" + sp + v + sp + ", label %" + lbl1 + ", label %" + lbl2
        return text
    else:
        print("not implemented translate_pred for formulas.")
        return ""

### TRANSLATION OF INSTRUCTIONS ###

def translate_lv(n):
    global tb, nl
    check_kind(n, {"Vari"})
    t = n["type"]
    v = new_llvm_local_var()
    return (tb + v + " = getelementptr " + state_name(n["root"])+ "* %self$, i32 0, i32 " + str(variable_position(n)) + nl, v)

def translate_beq(n):
    global tb, sp, nl
    check_kind(n, {"Beq"})
    l,p = translate_lv(n["lhs"])
    r,v,t = translate_expression(n["rhs"])
    return (l + 
            r + 
            tb + "store " + t + sp + v + ", " + t + "* " + p + nl)

def translate_if_br(lbr, lbl):
    assert(len(lbr)>=1)
    br = lbr[0]
    check_kind(br, {"IfBr"})
    lbr2 = lbr[1:]
    if len(lbr2) > 0:
        lbl_1 = new_llvm_label()
        lbl_2 = new_llvm_label()
        result = ""
        result += translate_pred(br["cond"], lbl_1, lbl_2)
        result += lbl_1 + ":\n"
        result += translate_inst_label(br["body"], lbl)
        result += lbl_2 + ":\n"
        result += translate_if_br(lbr2, lbl)
    else:
        if "cond" not in br.keys():
            result = translate_inst_label(br["body"], lbl)
        else:
            lbl_1 = new_llvm_label()
            result = ""
            result += translate_pred(br["cond"], lbl_1, lbl)
            result += lbl1 + ":\n"
            result += translate_inst_label(br["body"].lbl)
    return result

def translate_if(n, lbl):
    check_kind(n, {"If"})
    return translate_if_br(n["branches"], lbl)

def translate_inst(n):
    check_kind(n, {"Beq"})
    if n["kind"] == "Beq":
        return translate_beq(n)
    else:
        return ""

def translate_inst_label(n, lbl):
    check_kind(n, {"Blk", "If", "While", "Beq"})
    if n["kind"] == "Blk":
        return translate_inst_list_label(n["body"], lbl)
    elif n["kind"] == "If":
        return translate_if(n, lbl)
    elif n["kind"] == "Beq":
        result = ""
        result += translate_beq(n)
        result += tb + "br label %" + lbl + nl
        return result

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
        if i["kind"] in {"If", "While"}:
            lbl2 = new_llvm_label()
            p1 = translate_inst_label(i, lbl2) + lbl2 + ":\n"
        elif i["kind"] in {"Blk"}:
            p1 = translate_inst_list(i["body"])
        else:
            p1 = translate_inst(i)
        p2 = translate_inst_list_label(l2, lbl)
        return p1 + p2

def translate_init(i):
    global tb, nl
    check_kind(i, {"Impl"})
    reset_llvm_names()
    result = "define void @"+i["id"]+"$init$() {" + nl
    result = result + translate_inst_list_label(i["initialisation"], "exit")
    result = result + "exit:" + nl
    result = result + tb + "ret void" + nl
    result = result + "}" + nl
    return result;


def translate_signature(n):
    check_kind(n, {"Oper"})
    result = ""
    result += "@"+n["root"]["id"]+"$"+n["id"]+"$"
    result += "("
    result += state_name(n["root"])
    result += "* %self$"
    for inp in n["inp"]:
        result += ""
    for out in n["out"]:
        result += ""
    result += ")"
    return result

def translate_alloc(n):
    check_kind(n, {"Blk","Beq", "If"})
    return ""

def translate_operation(i):
    global tb
    check_kind(i, {"Oper"})
    reset_llvm_names()
    h = translate_signature(i)
    a = translate_alloc(i["body"])
    i = translate_inst_label(i["body"], "exit")
    return ("define void " + h + "{\n" + 
            "entry:\n" +
            a +
            i +
            "exit:\n" +
            tb + "ret void\n" +
            "}\n")

def translate_implementation(i):
    check_kind(i, {"Impl"})
    result = ""
    result += translate_state(i)
    result += "@"+i["id"]+"$self$ = common global " + state_name(i) + " zeroinitializer\n"
    result += translate_init(i)
    for op in i["operations"]:
        result += translate_operation(op)
    return result
