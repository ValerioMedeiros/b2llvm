# This file is responsible for providing functions to load a BXML file and
# build the corresponding Python abstract syntax tree, using the format and
# the constructors found in file "bimp.py".
# 
# We use the xml.etree.ElementTree library
# See http://docs.python.org/2/library/xml.etree.elementtree.html
#
# 1. General design
#
# The translation recurses over the tree. There is one function for
# each kind of node. When different kinds of node are possible (for
# instance, where a substitution is expected) an additional dispatcher 
# function is responsible for identifying the actual type of node,
# by looking at the XML tag.
# 
# 2. Symbol table
#
# Most of the recursive traversal of the tree requires as parameter
# a symbol table. Such symbol table is structured as a Python dictionary,
# where the keys are strings, and the values are the Python representation
# of the corresponding B symbol. I expect that no name conflict occurs in
# the input XML. Nevertheless, the inclusion in the symbol table is done
# through function sym_table_add, which checks there is no such conflict.
#
# When entering a new scope (e.g. an operation, or a VAR...IN substitution),
# a copy of the symbol table is created, and the local symbols are added to
# that copy.
#
# 3. Associate operators
# 
# Expressions consisting of the application of an associative operator to
# more than two arguments are represented as a nested application of a
# binary application, associated to the left.
# For instance a + b + c would be represented as ((a + b) + c).
#

import xml.etree.ElementTree as ET
import bimp

###
#
# rudimentary error handling
#
###

error_nb = 0
def error(message):
    '''
    Input:
      - a string
    Output: none
    Prints the input string to stdoud and increments error_nb
    '''
    global error_nb
    error_nb += 1
    print("error: " + message)

warn_nb = 0
def warn(message):
    '''
    Input:
      - a string
    Output: none
    Prints the input string to stdout and increments warn_nb
    '''
    global warn_nb
    warn_nb += 1
    print("warning: " + message)

def display_report(id, filename):
    global error_nb, warn_nb
    print("B implementation " + id + " from file " + filename + " loaded.")
    print(str(error_nb)+" error(s), "+str(warn_nb)+" warning(s) reported.")

### 
#
# symbol table stuff
#
###
def sym_table_add(table, id, pyt):
    if id in table:
        error("name clash ("+id+")")
    table[id] = pyt

def sym_table_new():
    table = dict()
    sym_table_add(table, "MAXINT", bimp.MAXINT)
    return table

### 
#
# bxml shortcuts 
#
###

def get(node):
    return node.get("ident")

def value(node):
    return node.get("value")

def operator(node):
    return node.get("operator")

def name(node):
    return node.get("name")

###
#
# general-purpose accumulators
#
###

def list_combine_ltr(l, f):
    '''
    Inputs:
      - l: a list
      - f: a binary function defined on the elements of l
    Output:
    Left-to-right application of f to the elements of l. 
    Example:
       l = [ 'a', 'b', 'c' ]
       f = lambda x, y: '(' + x + '+' + y + ')'
       list_combine_ltr(l, f) --> '((a+b)+c)'
    '''
    result = l[0]
    for i in range(1, len(l)):
        result = f(result, l[i])
    return result

###
#
# utilities
#
###

def get_identifier_type(id):
    '''
    Input:
    - id: a XML node representing an identifier
    Output:
    - "INTEGER" or "BOOL": the string representing the name of the type of id 
    '''
    assert id.tag == "Identifier"
    return value(id.find("./Attributes/TypeInfo/Identifier"))

def get_node(id, symbols):
    '''
    Inputs:
      - id: a bxml "Identifier" node
      - symbols: a dictionary mapping strings to Python node
    '''
    assert id.tag == "Identifier"
    return symbols[value(id)]

def discard_attributes(exp):
    '''
    Inputs:
      - exp: a bxml expression node
    Output:
    All the bxml children node that are not tagged as "Attributes"
    Note:
    The nodes discarded by this function usually contain the typing 
    information of the expression.
    '''
    return [n for n in exp.findall("./*") if n.tag != "Attributes"]

### 
#
# expressions
#
###

def load_identifier(n, symbols):
    return symbols[value(n)]

def load_boolean_literal(n, symbols):
    assert n.tag == "Boolean_Litteral"
    if value(n) == "TRUE":
        return bimp.TRUE
    elif value(n) == "FALSE":
        return bimp.FALSE
    else:
        error("unknown boolean literal")

def load_integer_literal(n, symbols):
    assert n.tag == "Integer_Litteral"
    return bimp.make_intlit(int(value(n)))

def setup_expression(n, handlers):
    op = operator(n)
    if op not in handlers.keys():
        error("unexpected operator " + op)
        return None
    return handlers[op], discard_attributes(n)

def load_unary(n, symbols, tag, table):
    assert n.tag == tag
    f, par = setup_expression(n, table)
    assert len(par) == 1
    arg = load_exp(par[0], symbols)
    return f(arg)

def load_binary(n, symbols, tag, table):
    assert n.tag == tag
    f, par = setup_expression(n, table)
    assert len(par) == 2
    arg = [ load_exp(p, symbols) for p in par ]
    return f(arg[0], arg[1])

def load_nary(n, symbols, tag, table):
    assert n.tag == tag
    f, par = setup_expression(n, table)
    assert len(par) >= 2
    args = [ load_exp(p, symbols) for p in par ]
    return list_combine_ltr(args, lambda a0, a1: f(a0, a1))

def load_unary_expression(n, symbols):
    return load_unary(n, symbols, "Unary_Expression",
                      {"pred":bimp.make_pred, "succ":bimp.make_succ})

def load_binary_expression(n, symbols):
    return load_binary(n, symbols, "Binary_Expression", 
                       {"+":bimp.make_sum, "-":bimp.make_diff, 
                        "*":bimp.make_prod})

def load_nary_expression(n, symbols):
    return load_nary(n, symbols, "Nary_Expression",
                     {"+":bimp.make_sum, "*":bimp.make_prod})

def load_binary_predicate(n, symbols):
    return load_binary(n, symbols, "Binary_Predicate",
                       {"&":bimp.make_and, "or":bimp_make_or})
    
def load_unary_predicate(n, symbols):
    return load_unary(n, symbols, "Unary_Predicate", {"not":bimp.make_not})

def load_nary_predicate(n, symbols):
    return load_nary(n, symbols, "Nary_Predicate", 
                     {"&":bimp.make_and, "or":bimp.make_or})

def load_expression_comparison(n, symbols):
    return load_binary(n, symbols, "Expression_Comparison",
                       {"=": bimp.make_eq, "/=": bimp.make_neq,
                        ">": bimp.make_lt, ">=": bimp.make_ge,
                        "<": bimp.make_lt, "<=": bimp.make_le})

def load_boolean_expression(n, symbols):
    if n.tag == "Binary_Predicate":
        return load_binary_predicate(n, symbols)
    elif n.tag == "Expression_Comparison":
        return load_expression_comparison(n, symbols)
    elif n.tag == "Unary_Predicate":
        return load_unary_predicate(n, symbols)
    elif n.tag == "Nary_Predicate":
        return load_nary_predicate(n, symbols)
    elif n.tag in {"Quantified_Predicate", "Set"}:
        error("unexpected boolean expression" + n.tag)
        return None
    else:
        error("unknown boolean expression " + n.tag)
        return None

def load_exp(n, symbols):
    if n.tag == "Binary_Expression":
        return load_binary_expression(n, symbols)
    elif n.tag == "Nary_Expression":
        return load_nary_expression(n, symbols)
    elif n.tag == "Unary_Expression":
        return load_unary_expression(n, symbols)
    elif n.tag == "Boolean_Litteral":
        return load_boolean_literal(n, symbols)
    elif n.tag == "Integer_Litteral":
        return load_integer_literal(n, symbols)
    elif n.tag == "Identifier":
        return load_identifier(n, symbols)
    elif n.tag == "Boolean_Expression":
        return load_boolean_expression(n, symbols)
    elif n.tag in {"EmptySet", "EmptySeq", "Quantified_Expression",
                   "Quantified_Set", "String_Litteral", "Struct", "Record"}:
        error("unexpected expression " + n.tag)
        return None
    else:
        error("unknown expression " + n.tag)
        return None

###
#
# substitutions
#
###

def load_block_substitution(n, symbols):
    assert n.tag == "Bloc_Substitution"
    return [ load_sub(s, symbols) for s in n.findall("./*") ]

def load_skip(n, symbols):
    assert n.tag == "Skip"
    return bimp.make_skip()

def load_becomes_eq(n, symbols):
    assert n.tag == "Affectation_Substitution"
    lhs = n.findall("./Variables/*")
    rhs = n.findall("./Values/*")
    if len(lhs) != 1 or len(rhs) != 1:
        error("unsupported multiple becomes equal substitution")
        return bimp.make_skip()    
    dst = load_exp(lhs[0], symbols)
    src = load_exp(rhs[0], symbols)
    return bimp.make_beq(dst, src)

def load_assert_substitution(n, symbols):
    assert n.tag == "Assert_Substitution"
    warn("assertion replaced by skip")
    return bimp.make_skip()

def load_if_substitution(n, symbols):
    '''
    TODO: understand how ELSIF branch are XML-coded and implement
    their translation.
    '''
    assert n.tag == "If_Substitution"
    if n.get("elseif") != None:
        error("unrecognized elseif attribute in IF substitution")
        return bimp.make_skip()
    xmlcond = n.find("./Condition")
    xmlthen = n.find("./Then")
    xmlelse = n.find("./Else")
    pycond = load_boolean_expression(xmlcond.find("./*"), symbols)
    pythen = load_sub(xmlthen.find("./*"), symbols)
    thenbr = bimp.make_if_br(pycond, pythen)
    if xmlelse == None:
        return bimp.make_if([thenbr])
    else:
        pyelse = load_sub(xmlelse.find("./*"), symbols)
        elsebr = bimp.make_if_br(None, pyelse)
        return bimp.make_if([thenbr, elsebr])

def load_case_substitution(n, symbols):
    assert n.tag == "Case_Substitution"
    xmlexpr = n.find("./Value/*")
    xmlbranches = n.findall("./Choices/Choice")
    xmlelse = n.find("./Else")
    pyexpr = load_exp(xmlexpr, symbols)
    pybranches = [ bimp.make_case_br(load_exp(xbr.find("./Value/*"), symbols),
                                     load_sub(xbr.find("./Then/*"), symbols))
                   for xbr in xmlbranches ]
    if xmlelse != None:
        pybranches.append(bimp.make_case_br(None, load_sub(xmlelse.find("./Choice/Then/*"), symbols)))
    return bimp.make_case(pyexpr, pybranches)

def load_var_in(n, symbols):
    assert n.tag == "VAR_IN"
    xmlvars = n.findall("./Variables/Identifier")
    xmlbody = n.find("./Body")
    symbols2 = symbols.copy()
    pyvars = []
    for v in xmlvars:
        id = value(v)
        type = get_identifier_type(v)
        pyt = bimp.make_loc_var(id, type)
        sym_table_add(symbols2, id, pyt)
        pyvars.append(pyt)
    pybody = [ load_sub(xmlbody.find("./*"), symbols2) ]
    return bimp.make_var_decl(pyvars, pybody)

def load_binary_substitution(n, symbols):
    assert n.tag == "Binary_Substitution"
    op = operator(n)
    if op == "||":
        error("parallel substitution cannot be translated")
        return bimp.make_skip()
    elif op == ";":
        left = n.find("./Left")
        right = n.find("./Left")
        return [load_sub(left, symbols), load_sub(right, symbols)]
    else:
        error("unrecognized n-ary substitution")
        return bimp.make_skip()


    error("load_binary_substitution not yet implemented")
    return bimp.make_skip()

def load_nary_substitution(n, symbols):
    assert n.tag == "Nary_Substitution"
    op = operator(n)
    if op == "||":
        error("parallel substitution cannot be translated")
        return bimp.make_skip()
    elif op == ";":
        substitutions = n.findall("./*")
        return bimp.make_blk([load_sub(s, symbols) for s in substitutions])
    else:
        error("unrecognized n-ary substitution")
        return bimp.make_skip()

def load_operation_call(n, symbols):
    assert n.tag == "Operation_Call"
    error("load_operation_call not yet implemented")
    return bimp.make_skip()

def load_while(n, symbols):
    assert n.tag == "While"
    xmlcond = n.find("./Condition")
    xmlbody = n.find("./Body")
    pycond = load_boolean_expression(xmlcond, symbols)
    pybody = load_sub(xmlbody, symbols)
    return bimp.make_while(pycond, pybody)

def load_sub(n, symbols):
    '''
    Inputs:
      - n: a XML node representing a B0 substitution
      - symbols: symbol table as Python dictionary mapping strings to
      Python nodes
    Output:
      Python node representing the substitution n
    '''
    if n.tag == "Bloc_Substitution":
        return load_block_substitution(n, symbols)
    elif n.tag == "Skip":
        return load_skip(n, symbols)
    elif n.tag == "Assert_Substitution":
        return load_assert_substitution(n, symbols)
    elif n.tag == "If_Substitution":
        return load_if_substitution(n, symbols)
    elif n.tag == "Affectation_Substitution":
        return load_becomes_eq(n, symbols)
    elif n.tag == "Case_Substitution":
        return load_case_substitution(n, symbols)
    elif n.tag == "VAR_IN":
        return load_var_in(n, symbols)
    elif n.tag == "Binary_Substitution":
        return load_binary_substitution(n, symbols)
    elif n.tag == "Nary_Substitution":
        return load_nary_substitution(n, symbols)
    elif n.tag == "Operation_Call":
        return load_operation_call(n, symbols)
    elif n.tag == "While":
        return load_while(n, symbols)
    elif n.tag in {"Choice_Substitution", "Becomes_Such_That", 
                   "Select_Substitution", "ANY_Substitution",
                   "LET_Substitution", "Becomes_In"}:
        error("unexpected substitution: " + n.tag)
    else:
        error("unrecognized substitution: " + n.tag)

###
#
# machine clauses
#
###

def load_imports(imports):
    if imports == None:
        return []
    # todo
    error("loading imports from XML not yet implemented")
    return []

def load_values(root, symbols):
    vals = root.findall("./Values/Valuation")
    result = []
    for v in vals:
        id = ident(v)
        exp = load_exp(v, symbols)
        type = get_identifier_type(v)
        pyt = bimp.make_const(id, exp, type)
        result.append(pyt)
        sym_table_add(symbols, id, pyt)
    return result

def load_concrete_variables(root, symbols):
    '''
    Input:
    - root: the BXML tree root node of a B implementation
    Output:
    A Python dict mapping variable identifier (strings) to the Python 
    representation for the concrete variables in the B implementation.
    '''
    vars = root.findall("./Concrete_Variables/Identifier")
    result = []
    for v in vars:
        id = value(v)
        type = get_identifier_type(v)
        pyt = bimp.make_imp_var(id, type)
        sym_table_add(symbols, id, pyt)
        result.append(pyt)
    return result

def load_initialisation(root, symbols):
    initialisation = root.find("./Initialisation")
    if initialisation == None:
        return []
    toplevel = initialisation.find("./*")
    assert toplevel.tag == "Nary_Substitution"
    return [ load_nary_substitution(toplevel, symbols) ]

def load_operation(n, symbols):
    assert n.tag == "Operation"
    id = name(n)
    body = n.find("./Body/*")
    inputs = n.findall("./Input_Parameters/Identifier")
    outputs = n.findall("./Output_Parameters/Identifier")
    op_symbols = symbols.copy()
    p_inputs = []
    p_outputs = []
    for i in inputs:
        id = value(i)
        type = get_identifier_type(i)
        pyt = bimp.make_arg_var(id, type)
        sym_table_add(op_symbols, id, pyt)
        p_inputs.append(pyt)
    for o in outputs:
        id = value(o)
        type = get_identifier_type(o)
        pyt = bimp.make_arg_var(id, type)
        sym_table_add(op_symbols, id, pyt)
        p_outputs.append(pyt)
    p_body = load_sub(body, op_symbols)
    return bimp.make_oper(id, p_inputs, p_outputs, p_body)

def load_operations(root, symbols):
    operations = root.findall(".//Operation")
    return [load_operation(op, symbols) for op in operations]

###
#
# modules
#
###

def load_implementation(filename):
    '''
    Parameters:
      - filename: the path to a file containing the BXML representation of
      a B0 implementation
    Result:
    A Python representation of the B0 implementation. 
    Output:
    The routine prints to stdout error messages and warnings; at the end
    it reports the number of errors and warnings detected and printed
    during the execution.
    '''
    
    symbols = sym_table_new()
    tree = ET.parse(filename)
    root = tree.getroot()
    assert root.tag == 'Machine'
    assert root.get("type") == "implementation"
    id = name(root)
    imports = load_imports(root.find("Imports"))
    constants = load_values(root, symbols)
    variables = load_concrete_variables(root, symbols)
    initialisation = load_initialisation(root, symbols)
    operations = load_operations(root, symbols)
    impl = bimp.make_implementation(id, imports, constants, variables,
                                    initialisation, operations)
    display_report(id, filename)
    return impl
