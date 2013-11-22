# This file provides an ASCII printer for Python representations of B0 implementations.
#
# 1. Design
#
# Printing is performed by recursive traversal of the tree representation. There is one
# function for each syntactic category. If the category is the union of several categories
# then the function dispatches control to the corresponding handler.
#
# 2. Shortcomings
#
# - Although the output is decently indented, no provision is taken to limit text width.
# - Some elements of the B representation are not present in the Python representation and
# are therefore not output.
#
from b2llvm.strutils import commas, sp, tb, nl

def term(n):
    '''
    term
    '''
    global sp
    kind = n["kind"]
    if kind == "BooleanLit":
        return n["value"]
    elif kind == "IntegerLit":
        return n["value"]
    elif kind == "Cons":
        return n["id"]
    elif kind == "Vari":
        return n["id"]
    elif n["op"] in { "succ", "pred" }:
        return n["op"] + "(" + term(n["args"][0]) + ")"
    elif n["op"] in { "+", "*", "-" }:
        return (sp + n["op"] + sp).join(term(e) for e in n["args"])
    else:
        return "<< UNRECOGNIZED >>"

def comp(n):
    '''
    comparison
    '''
    return term(n["arg1"])+sp+n["op"]+sp+term(n["arg2"])

def form(n):
    '''
    formula
    '''
    global sp
    op, args = n["op"], n["args"]
    if op == "not":
        return "(" + op + sp + condition(args[0]) + ")"
    else:
        return (sp + op + sp).join([condition(e) for e in args])

def condition(n):
    '''
    condition
    '''
    kind = n["kind"]
    if kind == "Comp":
        return comp(n)
    elif kind == "Form":
        return form(n)
    else:
        return "<<UNRECOGNIZED >>"

def type(n):
    return n

def imports(n):
    result = ""
    if n["pre"] != None:
        result += n["pre"] + "."
    result += n["mach"]["id"]
    return result

def value(n):
    return n["id"] + " = " + term(n["value"])

def invar(n):
    '''
    (typing) invariant
    '''
    return n["id"] + " : " + type(n["type"])

def skip(indent, n):
    global tb
    return (indent*tb) + "SKIP"

def beq(indent, n):
    '''
    Becomes equal
    '''
    global tb
    return (indent*tb) + term(n["lhs"]) + " := " + term(n["rhs"])

def bin(indent, n):
    '''
    Becomes equal
    '''
    global tb
    return ((indent*tb) +
            commas([ term(x) for x in n["lhs"]]) + " :: " +
            commas([ type(x["type"]) for x in n["lhs"]]))

def blk(indent, n):
    '''
    Block
    '''
    global tb, nl
    result = ""
    result += (indent*tb) + "BEGIN" + nl
    result += subst_l(indent+1, n["body"]) + nl
    result += (indent*tb) + "END"
    return result

def var_decl(indent, n):
    '''
    Variable declaration
    '''
    global nl, tb
    result = ""
    result += (indent*tb) + "VAR" + nl
    result += ((indent+1)*tb) + (","+sp).join([term(e) for e in n["vars"]]) + nl
    result += (indent*tb) + "IN" + nl
    result += subst_l(indent+1, n["body"]) + nl
    result += (indent*tb) + "END"
    return result

def if_br(indent, position, branch):
    '''
    If branch
    '''
    global nl
    cond = branch["cond"]
    body = branch["body"]
    if cond == None:
        kw = "ELSE"
    elif position == 0:
        kw = "IF"
    else:
        kw = "ELSIF"
    result = (indent*tb)+kw
    if cond != None:
        result += sp + condition(cond) + sp + "THEN"
    result += nl
    result += subst(indent+1, body)
    if cond == None:
        result += sp+nl+(indent*tb)+"END"
    return result

def subst_if(indent, n):
    '''
    If substitution (if is a Python keyword)
    '''
    global nl
    bits = []
    branches = n["branches"]
    for i in range(len(branches)):
        branch = branches[i]
        bits.append(if_br(indent, i, branch))
    return nl.join(bits)

def case_br(indent, position, values, body):
    '''
    case branch
    '''
    global sp, nl
    default = values == [] or values == None
    if default:
        kw = "ELSE"
    elif position == 0:
        kw = "EITHER"
    else:
        kw = "OR"
    result = (indent*tb)+kw
    if not default:
        result += sp + ", ".join([term(e) for e in values])
        result += " THEN"
    result += nl
    result += subst(indent+1, body)
    if default:
        result += nl+ (indent*tb)+"END"
    return result

def case(indent, n):
    global tb, sp, nl
    result = ""
    result += (indent*tb)+ "CASE" + sp + term(n["expr"]) + sp + "THEN" + nl
    bits = []
    branches = n["branches"]
    for i in range(len(branches)):
        branch = branches[i]
        bits.append(case_br(indent+1, i, branch["val"], branch["body"]))
    result += nl.join(bits) + nl
    result += (indent*tb)+"END"
    return result

def subst_while(indent, n):
    global tb, sp, nl
    result = ""
    result += (indent*tb)+ "WHILE" + sp + condition(n["cond"]) + sp + "DO" + nl
    result += subst_l(indent+1, n["body"]) + nl
    result += (indent*tb)+"END"
    return result

def call(indent, n):
    '''
    operation call
    '''
    global tb
    op, inp, out, inst = n["op"], n["inp"], n["out"], n["inst"]
    result = ""
    result += indent*tb
    if out != []:
        result += ", ".join([term(e) for e in out])
        result += sp + "<-" + sp
    if inst != None:
        if inst["pre"] != None:
            result += inst["pre"] + "."
    result += op["id"]
    if inp != []:
        result += "(" + ", ".join([term(e) for e in inp]) + ")"
    return result

def subst_l(indent, l):
    '''
    Substitution list
    '''
    global nl
    return (";"+nl).join([subst(indent, e) for e in l])

def subst(indent, n):
    '''
    substitution
    '''
    kind = n["kind"]
    table = dict({"Skip":skip, "Beq":beq, "Blk":blk, "VarD":var_decl,
                  "If":subst_if, "Case":case, "While":subst_while, "Call":call})
    if kind in table.keys():
        return table[kind](indent, n)
    else:
        return (indent * tb) + "<< UNRECOGNIZED >>"

def oper(n):
    result = ""
    inp = n["inp"]
    out = n["out"]
    if out != []:
        result += ",".join([term(e) for e in out]) + " <-- "
    result += n["id"]
    if inp != []:
        result += "(" + ",".join([term(e) for e in inp]) + ")"
    result += sp+"="+nl
    result += subst(1, n["body"])
    return result

def implementation(n):
    global sp, tb, nl
    imp, consts, vars = n["imports"], n["concrete_constants"], n["variables"]
    init, ops = n["initialisation"], n["operations"]
    result = ""
    result += "IMPLEMENTATION" + sp + n["id"] + nl
    if imp != []:
        result += "IMPORTS" + nl
        result += tb + commas([imports(e) for e in imp]) + nl
    if consts != []:
        result += "VALUES" + nl
        result += tb + commas([value(e) for e in consts]) + nl
    if vars != []:
        result += "VARIABLES" + nl
        result += tb + commas([e["id"] for e in vars]) + nl
        result += "INVARIANT" + nl
        result += tb + (sp+"&"+nl+tb).join([invar(e) for e in vars]) + nl
    if init != []:
        result += "INITIALISATION" + nl
        result += subst_l(1, init) + nl
    if ops != []:
        result += "OPERATIONS" + nl
        result += (tb+";"+nl).join([oper(e) for e in ops]) + nl
    result += "END" + nl
    return result
