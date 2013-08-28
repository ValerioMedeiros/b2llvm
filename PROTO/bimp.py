### TYPES ###

INT = "INT"
BOOL = "BOOL"

### TERMINALS ###

def make_var(name, type, scope):
    return { "kind": "Vari", "id": name, "type": type, "scope": scope }

def make_imp_var(name, type):
    return make_var(name, type, "Impl")

def make_loc_var(name, type):
    return make_var(name, type, "Local")

def make_intlit(value):
    return { "kind": "IntegerLit", "value": str(value)}

zero = make_intlit(0)
one = make_intlit(1)

def make_boollit(value):
    return { "kind": "BooleanLit",
             "value": value}
false = make_boollit("FALSE")
true = make_boollit("TRUE")

### COMPOSED EXPRESSIONS ###

def make_term(op, args):
    return { "kind": "Term", "op": op, "args" : args }

def make_succ(term):
    return make_term("succ", [term])

def make_pred(term):
    return make_term("pred", [term])

def make_sum(term1, term2):
    return make_term("+", [term1, term2])

def make_comp(op, arg1, arg2):
    return { "kind": "Comp", "op": op, "arg1": arg1, "arg2": arg2 }

def make_lt(term1, term2):
    return make_comp("<", term1, term2)

### INSTRUCTIONS ###

def make_beq(lhs, rhs):
    return { "kind": "Beq", "lhs": lhs, "rhs": rhs}

def make_blk(body):
    return { "kind": "Blk", "body": body }

def make_var_decl(vars, body):
    return { "kind": "VarD", "vars": vars, "body": body }

def make_while(cond, body):
    return { "kind": "While", "cond": cond, "body": body }

### COMPONENT ###

def make_oper(id, inp, out, body):
    return { "kind": "Oper", "id": id, "inp": inp, "out": out, "body": body }

def make_implementation(id, vars, consts, init, ops):
    root = { "kind": "Impl", "id": id,
             "concrete_variables": vars, "concrete_constants": consts,
             "initialisation": init, "operations": ops }
    for node in root["concrete_variables"]+root["operations"]:
        node["root"] = root
    return root

