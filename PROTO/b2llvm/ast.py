### TYPES ###

INT = "INTEGER"
BOOL = "BOOL"

### TERMINALS ###

def make_const(id, type, value):
    return { "kind": "Cons", "id": id, "type": type, "value" : value }


def make_var(name, type, scope):
    return { "kind": "Vari", "id": name, "type": type, "scope": scope }

def make_imp_var(name, type):
    return make_var(name, type, "Impl")

def make_loc_var(name, type):
    return make_var(name, type, "Local")

def make_arg_var(name, type):
    return make_var(name, type, "Oper")

def make_intlit(value):
    '''
    - Input: an integer value
    Creates an integer literal.
    '''
    return { "kind": "IntegerLit", 
             "value": str(value)}

def make_boollit(value):
    '''
    - Input: "FALSE" or "TRUE"
    Creates a boolean literal.
    '''
    return { "kind": "BooleanLit",
             "value": value}

FALSE = make_boollit("FALSE")
TRUE = make_boollit("TRUE")

ZERO = make_intlit(0)
ONE = make_intlit(1)
MAXINT = make_intlit(2147483647)

### COMPOSED EXPRESSIONS ###

def make_term(op, args):
    return { "kind": "Term", "op": op, "args" : args }

def make_succ(term):
    return make_term("succ", [term])

def make_pred(term):
    return make_term("pred", [term])

def make_sum(term1, term2):
    return make_term("+", [term1, term2])

def make_diff(term1, term2):
    return make_term("-", [term1, term2])

def make_prod(term1, term2):
    return make_term("*", [term1, term2])

def make_comp(op, arg1, arg2):
    return { "kind": "Comp", "op": op, "arg1": arg1, "arg2": arg2 }

def make_le(term1, term2):
    return make_comp("<=", term1, term2)

def make_lt(term1, term2):
    return make_comp("<", term1, term2)

def make_ge(term1, term2):
    return make_comp("<=", term1, term2)

def make_gt(term1, term2):
    return make_comp(">", term1, term2)

def make_eq(term1, term2):
    return make_comp("=", term1, term2)

def make_neq(term1, term2):
    return make_comp("!=", term1, term2)

def make_form(op, args):
    return { "kind": "Form", "op": op, "args" : args }

def make_and(arg1, arg2):
    return make_form("and", [arg1, arg2])

def make_or(arg1, arg2):
    return make_form("or", [arg1, arg2])

def make_not(arg):
    return make_form("not", [arg])

### INSTRUCTIONS ###

def make_skip():
    return { "kind": "Skip" }

def make_beq(lhs, rhs):
    return { "kind": "Beq", "lhs": lhs, "rhs": rhs}

def make_blk(body):
    assert type(body) is list
    return { "kind": "Blk", "body": body }

def make_var_decl(vars, body):
    assert type(vars) is list
    assert type(body) is list
    return { "kind": "VarD", "vars": vars, "body": body }

def make_if_br(cond, body):
    assert type(body) is not list
    return { "kind": "IfBr", "cond": cond, "body": body}

def make_if(branches):
    assert type(branches) is list
    return { "kind": "If", "branches": branches }

def make_case_br(values, body):
    assert type(values) is list
    assert type(body) is not list
    return { "kind": "CaseBr", "val": values, "body": body }

def make_case(expression, branches):
    assert type(branches) is list
    return { "kind": "Case", "expr": expression, "branches": branches }

def make_while(cond, body):
    assert type(body) is list
    return { "kind": "While", "cond": cond, "body": body }

def make_call(op, inp, out, inst=None):
    '''
    - Input:
    op: an operation
    inp: a sequence of inputs
    out: a sequence of outputs
    inst: an element of an imported clause (optional)
    - Output:
    an operation call
    '''
    return { "kind": "Call", "op": op, "inp": inp, "out": out, 
             "inst": inst }

### COMPONENT ###

def make_oper(id, inp, out, body):
    assert type(inp) is list
    assert type(out) is list
    assert type(body) is not list
    return { "kind": "Oper", "id": id, "inp": inp, "out": out, "body": body }

def make_import(mach, prefix = None):
    '''
    - Input: 
    mach: a machine
    prefix: a string prefix (optional).
    - Output:
    Creates an element of an import clause.
    '''
    assert(mach["kind"] in { "Mach" })
    return { "kind": "Impo", "mach": mach, "pre": prefix }

def make_implementation(id, imports, consts, vars, init, ops):
    assert type(imports) is list
    assert type(consts) is list
    assert type(vars) is list
    assert type(init) is list
    assert type(ops) is list
    root = { "kind": "Impl", "id": id,
             "imports": imports,
             "concrete_constants": consts,
             "concrete_variables": vars, 
             "initialisation": init, "operations": ops }
    for node in imports + vars + ops:
        node["root"] = root
    return root

def make_machine(id, impl):
    root = { "kind": "Mach", "id": id, "impl": impl }
    return root

