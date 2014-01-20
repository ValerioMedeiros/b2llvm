"""A Python representation for AST of B machines and implementations.

1. Design

- AST nodes are coded as dict() objects. It would be nicer to have proper
classes, I suppose.

2. Shortcomings

- The full B language is not yet represented. You need to read the code
to know what is supported.
- The AST nodes are somehow incomplete in some cases. Their design is
oriented towards the implementation of the translation to LLVM.
"""

### TYPES ###

INTEGER = "INTEGER"
BOOL = "BOOL"

### TERMINALS ###

def make_const(name, typedef, value):
    """Creates an AST node for a B constant."""
    return { "kind": "Cons", "id": name, "type": typedef, "value" : value }


def make_var(name, typedef, scope):
    """Creates an AST node for a B variable."""
    return { "kind": "Vari", "id": name, "type": typedef, "scope": scope }

def make_imp_var(name, typedef):
    """Creates an AST node for a B concrete variable."""
    return make_var(name, typedef, "Impl")

def make_loc_var(name, typedef):
    """Creates an AST node for a B local variable."""
    return make_var(name, typedef, "Local")

def make_arg_var(name, typedef):
    """Creates an AST node for a B operation argument."""
    return make_var(name, typedef, "Oper")

def make_intlit(value):
    '''
    Creates an AST node for a B integer literal.

    - Input: an integer value

    '''
    return { "kind": "IntegerLit",
             "value": str(value)}

def make_boollit(value):
    '''
    Creates an AST node for a Boolean literal.

    - Input: "FALSE" or "TRUE"

    '''
    return { "kind": "BooleanLit",
             "value": value}

FALSE = make_boollit("FALSE")
TRUE = make_boollit("TRUE")

ZERO = make_intlit(0)
ONE = make_intlit(1)
MAXINT = make_intlit(2147483647)

#VGM - TODO: move this functions ?

def make_sset_bool():
    """Creates an AST node for a B simple bool set."""
    return { "kind" : "set_BOOL" }

def make_sset_nat():
    """Creates an AST node for a B simple natural set."""
    return { "kind" : "set_NAT" }

def make_sset_int():
    """Creates an AST node for a B simple integer set."""
    return { "kind" : "set_INT" }

def make_interval(start,end):
    """Creates an AST node for a B simple interval set."""
    return { "kind" : "set_interval" , "start" : start, "end" : end }

def make_arrayType(dom, ran):
    """Creates an AST node for a B arrayType."""
    return { "dom": dom, "ran" : ran}

def make_arrayItem(base,index):
    """Creates an AST node for a B arrayType."""
    return { "base": base, "index": index, "type":None}

### COMPOSED EXPRESSIONS ###

def make_term(operator, args):
    """Creates an AST node for a B term."""
    return { "kind": "Term", "op": operator, "args" : args }

def make_succ(term):
    """Creates an AST node for a B succ (successor) expression."""
    return make_term("succ", [term])

def make_pred(term):
    """Creates an AST node for a B pred (predecessor) expression."""
    return make_term("pred", [term])

def make_sum(term1, term2):
    """Creates an AST node for a B sum expression."""
    return make_term("+", [term1, term2])

def make_diff(term1, term2):
    """Creates an AST node for a B subtraction expression."""
    return make_term("-", [term1, term2])

def make_prod(term1, term2):
    """Creates an AST node for a B product expression."""
    return make_term("*", [term1, term2])

def make_comp(operator, arg1, arg2):
    """Creates an AST node for a B comparison."""
    return { "kind": "Comp", "op": operator, "arg1": arg1, "arg2": arg2 }

def make_le(term1, term2):
    """Creates an AST node for a B "lower or equal" expression."""
    return make_comp("<=", term1, term2)

def make_lt(term1, term2):
    """Creates an AST node for a B "lower than" expression."""
    return make_comp("<", term1, term2)

def make_ge(term1, term2):
    """Creates an AST node for a B "greater or equal" expression."""
    return make_comp(">=", term1, term2)

def make_gt(term1, term2):
    """Creates an AST node for a B "greater than" expression."""
    return make_comp(">", term1, term2)

def make_eq(term1, term2):
    """Creates an AST node for a B equality."""
    return make_comp("=", term1, term2)

def make_neq(term1, term2):
    """Creates an AST node for a B inequality."""
    return make_comp("!=", term1, term2)

def make_form(operator, args):
    """Creates an AST node for a B formula."""
    return { "kind": "Form", "op": operator, "args" : args }

def make_and(arg1, arg2):
    """Creates an AST node for a B conjunction."""
    return make_form("and", [arg1, arg2])

def make_or(arg1, arg2):
    """Creates an AST node for a B disjunction."""
    return make_form("or", [arg1, arg2])

def make_not(arg):
    """Creates an AST node for a B negation."""
    return make_form("not", [arg])

### INSTRUCTIONS ###

def make_skip():
    """Creates an AST node for a B skip instruction."""
    return { "kind": "Skip" }

def make_beq(lhs, rhs):
    """Creates an AST node for a B becomes equal instruction."""
    return { "kind": "Beq", "lhs": lhs, "rhs": rhs}

def make_bin(lhs):
    """Represents a becomes in susbtitution (but only the left hand side)."""
    return { "kind": "Bin", "lhs": lhs}

def make_blk(body):
    """Creates an AST node for a B block instruction."""
    assert type(body) is list
    return { "kind": "Blk", "body": body }

def make_var_decl(variables, body):
    """Creates an AST node for a B variable declaration instruction."""
    assert type(variables) is list
    assert type(body) is list
    return { "kind": "VarD", "vars": variables, "body": body }

def make_if_br(cond, body):
    """Creates an AST node for a B if branch."""
    assert type(body) is not list
    return { "kind": "IfBr", "cond": cond, "body": body}

def make_if(branches):
    """Creates an AST node for a B if instruction."""
    assert type(branches) is list
    return { "kind": "If", "branches": branches }

def make_case_br(values, body):
    """Creates an AST node for a B case branch."""
    assert type(values) is list
    assert type(body) is not list
    return { "kind": "CaseBr", "val": values, "body": body }

def make_case(expression, branches):
    """Creates an AST node for a B case instruction."""
    assert type(branches) is list
    return { "kind": "Case", "expr": expression, "branches": branches }

def make_while(cond, body):
    """Creates an AST node for a B while instruction."""
    assert type(body) is list
    return { "kind": "While", "cond": cond, "body": body }

def make_call(operator, inp, out, inst=None):
    '''
    Creates an AST node for a B operation call instruction.

    - Input:
    op: an operation
    inp: a sequence of inputs
    out: a sequence of outputs
    inst: an element of an imported clause (optional)

    '''
    return { "kind": "Call", "op": operator, "inp": inp, "out": out,
             "inst": inst }

### COMPONENT ###

def make_oper(name, inp, out, body):
    """Creates an AST node to represent a B operation."""
    assert type(inp) is list
    assert type(out) is list
    assert type(body) is not list
    return { "kind": "Oper", "id": name, "inp": inp, "out": out, "body": body }

def make_import(mach, prefix = None):
    '''
    Creates an AST node for a B import element.

    - Input:
    mach: a machine or a library machine
    prefix: a string prefix (optional).
    - Output:
    Creates an element of an import clause, i.e., a module.
    '''
    assert(mach["kind"] in { "Machine" })
    return { "kind": "Module", "mach": mach, "pre": prefix }

def make_implementation(name, imports, consts, variables, init, ops):
    """Creates an AST node for a B implementation module."""
    assert type(imports) is list
    assert type(consts) is list
    assert type(variables) is list
    assert type(init) is list
    assert type(ops) is list
    root = { "kind": "Impl",
             "id": name,
             "machine": None,
             "imports": imports,
             "concrete_constants": consts,
             "variables": variables,
             "initialisation": init, "operations": ops,
             "stateful": None}
    for node in imports + variables + ops:
        node["root"] = root
    return root

def make_base_machine(name, consts, variables, ops):
    '''
    Constructor for node that represent a machine interface, namely
    the elements of a machine that may be accessed by a module depending
    on that machine.
    '''
    assert type(consts) is list
    assert type(variables) is list
    assert type(ops) is list
    root = { "kind": "Machine",
             "id": name,
             "base": True,
             "concrete_constants": consts,
             "variables": variables,
             "operations": ops,
             "implementation": None,
             "stateful": None,
             "comp_direct": None,
             "comp_indirect": None}
    for node in variables + ops:
        node["root"] = root
    return root

def make_developed_machine(name, impl):
    '''
    Constructor for node that represents a developed machine.

    For now we are just interested in the implementation of that machine.
    '''
    return { "kind": "Machine",
             "id": name,
             "base": False,
             "concrete_constants": [],
             "variables": [],
             "implementation": impl,
             "stateful": None,
             "comp_direct": None,
             "comp_indirect": None
             }
