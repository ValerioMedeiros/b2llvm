#
# This file provides an Python representation for AST of B machines and
# implementations.
#
# 1. Design
#
# - AST nodes are coded as dict() objects. It would be nicer to have proper
# classes, I suppose.
#
# 2. Shortcomings
#
# - The full B language is not yet represented. You need to read the code 
# to know what is supported.
# - The AST nodes are somehow incomplete in some cases. Their design is
# oriented towards the implementation of the translation to LLVM.
#

### TYPES ###

INTEGER = "INTEGER"
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

def make_bin(lhs):
    '''
    Represents a becomes in susbtitution (but only the left hand side).
    '''
    return { "kind": "Bin", "lhs": lhs}

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
    mach: a machine or a library machine
    prefix: a string prefix (optional).
    - Output:
    Creates an element of an import clause, i.e., a module.
    '''
    assert(mach["kind"] in { "Machine" })
    return { "kind": "Module", "mach": mach, "pre": prefix }

def make_implementation(id, imports, consts, vars, init, ops):
    assert type(imports) is list
    assert type(consts) is list
    assert type(vars) is list
    assert type(init) is list
    assert type(ops) is list
    root = { "kind": "Impl", 
             "id": id,
             "machine": None,
             "imports": imports,
             "concrete_constants": consts,
             "variables": vars, 
             "initialisation": init, "operations": ops,
             "stateful": None}
    for node in imports + vars + ops:
        node["root"] = root
    return root

def make_base_machine(id, consts, vars, ops):
    '''
    Constructor for node that represent a machine interface, namely
    the elements of a machine that may be accessed by a module depending
    on that machine.
    '''
    assert type(consts) is list
    assert type(vars) is list
    assert type(ops) is list
    return { "kind": "Machine", 
             "concrete_constants": consts,
             "variables": vars,
             "operations": ops,
             "implementation": None,
             "stateful": None,
             "comp_direct": None,
             "comp_indirect": None}

def make_developed_machine(id, impl):
    '''
    Constructor for node that represents a developed machine.

    For now we are just interested in the implementation of that machine.
    '''
    return { "kind": "Machine", 
             "id": id,
             "variables": [],
             "implementation": impl,
             "stateful": None,
             "comp_direct": None,
             "comp_indirect": None
             }

