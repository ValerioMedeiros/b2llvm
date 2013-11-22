# This file is responsible for providing functions to load a BXML file and
# build the corresponding Python abstract syntax tree, using the format and
# the constructors found in file "ast.py".
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
# The elements stored into the symbol table are:
#   - concrete variables
#   - concrete constants/values
#   - imports: name of import is mapped to ast import node
#   - operations: name of operation is mapped to ast operation node
#   - operation parameters
#   - local variables
#
# When entering a new scope (e.g. an operation, or a VAR...IN substitution),
# a copy of the symbol table is created, and the local symbols are added to
# that copy.
#
# 3. Associative operators
#
# Expressions consisting of the application of an associative operator to
# more than two arguments are represented as a nested application of a
# binary application, associated to the left.
# For instance a + b + c would be represented as ((a + b) + c).
#
# 4. Symbol table(s)
#
# symast is a traditional symbol table where the keys are identifier strings
# and the values the AST node of the corresponding B entity. When the loader
# enters a new scope, it creates a new symbol table initialized with a copy
# of the inherited table.
#
# symimp is a special symbol table to handle imports
# - For imports with prefix, the entry in symimp has as key the prefix and
# as value the import clause.
# - For imports without prefix, there is one entry in symimp for each visible
# symbol of the imported machine, and the key is the identifier of the
# symbol and the value is the import clause.
# In both cases, the key is a string and the value an AST node.
#
# 5. References
#
# [LRM] B Language Reference Manual, version 1.8.6. Clearsy.
#
import os
import xml.etree.ElementTree as ET
import b2llvm.ast as ast
import b2llvm.cache as cache
from b2llvm.bproject import BProject

import b2llvm.printer

###
#
# global variables
#
###
loading = set()

#
# MODULE ENTRY POINTS
#

def load_project(dirname='bxml', filename='project.xml'):
    '''
    Keywords:
      - dirname: path to directory where bxml files are stored;
      default value is 'bxml'.
      - filename: the name of a bproject.bxml file. The default
      value is 'bproject.bxml'.
    Loads the contents of the given file, if it exists, into global variable
    project_db. If the file does not exist, then project_db is left empty,
    i.e. a pair formed by an empty dictionary and an empty set.
    '''
    return BProject(dirname+os.sep+filename)

def load_module(d, p, m):
    '''
    Inputs:
      - d: string with path to directory where B modules are stored
      - p: BProject object storing current project settings
      - m: string with machine name
    Output:
      Root AST node for the representation of m.
    '''
    if not p.has(m):
        error("cannot find machine " + m + " in project settings file.")
        raise Exception("resource not found")
    c = cache.Cache()
    if p.is_base(m):
        return load_base_machine(d, p, c, m)
    else:
        assert p.is_developed(m)
        return load_developed_machine(d, p, c, m)

###
#
# modules
#
###

def load_base_machine(dir, project, c, id):
    '''
    Loads B base machine from file to Python AST.

    Parameters:
      - c: cache from identifiers to root AST machine.
      - id: the name of a B machine.
    Result:
    A Python representation of the B machine.
    Output:
    The routine prints to stdout error messages and warnings; at the end
    it reports the number of errors and warnings detected and printed
    during the execution.
    '''
    global loading
    if c.has(id):
        return c.get(id)
    if id in loading:
        error("there seems to be a recursive dependency in imports")
    loading.add(id)
    symast = sym_table_new() # symbol table: symbol to AST node
    path = dir + os.sep + id + '.bxml'
    tree = ET.parse(path)
    root = tree.getroot()
    assert root.tag == 'Machine'
    assert root.get("type") == "abstraction"
    constants = load_values(root, symast)
    variables = load_concrete_variables(root, symast)
    operations = load_operations(root, symast)
    n = ast.make_base_machine(id, constants, variables, operations)
    symast.clear()
    loading.remove(id)
    c.set(id, n)
    return n

def load_developed_machine(dir, p, c, m):
    '''
    Loads BXML a developed machine from file to Python AST. All dependent
    components are loaded, including implementations of developed
    machines.

    Parameters:
      - dir: the directory where the project files are stored
      - p: project settings object
      - c: cache from identifiers to root AST machine.
      - m: the name of a developed B machine
    Result:
    A Python representation of the B machine
    Output:
    The routine prints to stdout error messages and warnings; at the end
    it reports the number of errors and warnings detected and printed
    during the execution.
    '''
    if c.has(m):
        return c.get(m)
    if m in loading:
        error("there seems to be a recursive dependency in imports")
    loading.add(m)
    if not p.has(m):
        error("machine " + m + " not found in project settings")
        return None
    if not p.is_developed(m):
        error("machine " + m + " is not a developed machine.")
        return None
    filename = dir + os.sep + m + '.bxml'
    tree = ET.parse(filename)
    root = tree.getroot()
    assert root.tag == 'Machine'
    assert root.get("type") == "abstraction"
    assert name(root) == m
    impl_id = p.implementation(m)
    implementation = load_implementation(dir, p, c, impl_id)
    n = ast.make_developed_machine(m, implementation)
    implementation["machine"] = n
    loading.remove(m)
    c.set(m, n)
    return n

def load_implementation(dir, project, c, module):
    '''
    Loads B implementation to Python AST.

    Parameters:
      - dir: the directory where BXML files are to be found
      - project: the object representing the B project settings.
      - c: cache from identifiers to root AST machine.
      - module: the identifier of the implementation
    Result:
      A Python representation of the B implementation, or None if some
      error occured.
    Output:
      The routine prints to stdout error messages and warnings; at the end
      it reports the number of errors and warnings detected and printed
      during the execution.
    '''
    if c.has(module):
        return c.get(module)
    if module in loading:
        error("there seems to be a recursive dependency in imports")
    symast = sym_table_new()
    symimp = sym_table_new()
    loading.add(module)
    path = dir + os.sep + module + '.bxml'
    tree = ET.parse(path)
    root = tree.getroot()
    assert root.tag == 'Machine'
    assert root.get("type") == "implementation"
    id = name(root)
    assert id == module
    imports = load_imports(root, symast, symimp, dir, project, c)
    constants = load_values(root, symast)
    variables = load_concrete_variables(root, symast)
    initialisation = load_initialisation(root, symast, symimp)
    operations = load_operations(root, symast, symimp)
    symast.clear()
    symimp.clear()
    n = ast.make_implementation(id, imports, constants, variables,
                                   initialisation, operations)
    loading.remove(module)
    c.set(module, n)
    return n

###
#
# machine clauses
#
###

def load_imports(root, symast, symimp, dir, project, c):
    '''
    Parameters:
      - root: XML ElementTree representing the root of an implementation
      - symast: a symbol table
      - c: cache from identifiers to root AST machine.
    Result:
      List of import AST nodes.
    Side effects:
      All externally visible elements of the imported modules are added
      to the symbol table.
      All the named imports are added to the symbol table.
    '''
    imports = root.find("./Imports")
    if imports == None:
        return []
    imports = [load_import(i, symast, dir, project, c)
               for i in imports.findall("./Referenced_Machine")]
    # Add visible symbols from imported machines ([LRM, Appendix C.10])
    acc = [] # store machines that have already been processed
    for i in imports:
        m = i["mach"]
        if m not in acc:
            for n in visible_symbols(project, m):
                sym_table_add(symast, n["id"], n)
            acc.append(m)
        if i["pre"] != None:
            sym_table_add(symimp, i["pre"], i)
        else:
            for n in visible_symbols(project, m):
                sym_table_add(symimp, n["id"], i)
    return imports

def load_import(n, symast, dir, project, c):
    '''
    Loads one import clause to Python AST and update symbol table.

    Parameters:
      - n: a BXML tree element for an import.
      - symast: symbol table.
      - c: cache from identifiers to root AST machine.
    Result:
      A Python AST node representing the import clause.
    Side effects:
      If the import clause has a prefix, then it is added to the
      symbol table, together with the result node.
    '''
    module = n.find("./Name").text
    if not project.has(module):
        error("machine "+module+" not found in project settings")
        return None
    if project.is_developed(module):
        mach = load_developed_machine(dir, project, c, module)
    else:
        mach = load_base_machine(dir, project, c, module)
    instance = n.find("./Instance")
    if instance != None:
        impo = ast.make_import(mach, instance.text)
        sym_table_add(symast, instance.text, impo)
    else:
        impo = ast.make_import(mach)
    return impo

def load_values(root, symast):
    vals = root.findall("./Values/Valuation")
    result = []
    for v in vals:
        id = ident(v)
        children = v.findall("./*")
        assert len(children) == 1
        xmlexp = children[0]
        exp = load_exp(xmlexp, symast)
        type = get_type(xmlexp)
        pyt = ast.make_const(id, type, exp)
        result.append(pyt)
        sym_table_add(symast, id, pyt)
    return result

def load_concrete_variables(root, symast):
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
        pyt = ast.make_imp_var(id, type)
        sym_table_add(symast, id, pyt)
        result.append(pyt)
    return result

def load_initialisation(root, symast, symimp):
    initialisation = root.find("./Initialisation")
    if initialisation == None:
        return []
    xmlsubst = initialisation.find("./*")
    return [ load_sub(xmlsubst, symast, symimp) ]

def load_operations(root, symast, symimp):
    operations = root.findall(".//Operation")
    return [load_operation(op, symast, symimp) for op in operations]

def load_operation(n, symast, symimp):
    assert n.tag == "Operation"
    id = name(n)
    body = n.find("./Body/*")
    inputs = n.findall("./Input_Parameters/Identifier")
    outputs = n.findall("./Output_Parameters/Identifier")
    symast2 = symast.copy()
    p_inputs = []
    p_outputs = []
    for i in inputs:
        id2 = value(i)
        type = get_identifier_type(i)
        pyt = ast.make_arg_var(id2, type)
        sym_table_add(symast2, id2, pyt)
        p_inputs.append(pyt)
    for o in outputs:
        id2 = value(o)
        type = get_identifier_type(o)
        pyt = ast.make_arg_var(id2, type)
        sym_table_add(symast2, id2, pyt)
        p_outputs.append(pyt)
    p_body = load_sub(body, symast2, symimp)
    symast2.clear()
    res = ast.make_oper(id, p_inputs, p_outputs, p_body)
    return res

###
#
# substitutions
#
###

def load_sub(n, symast, symimp):
    '''
    Inputs:
      - n: a XML node representing a B0 substitution
      - symast: symbol table as Python dictionary mapping strings to
      Python nodes
    Output:
      Python node representing the substitution n
    '''
    if n.tag == "Bloc_Substitution":
        return load_block_substitution(n, symast, symimp)
    elif n.tag == "Skip":
        return load_skip(n)
    elif n.tag == "Assert_Substitution":
        return load_assert_substitution(n, symast)
    elif n.tag == "If_Substitution":
        return load_if_substitution(n, symast, symimp)
    elif n.tag == "Affectation_Substitution":
        return load_becomes_eq(n, symast)
    elif n.tag == "Case_Substitution":
        return load_case_substitution(n, symast, symimp)
    elif n.tag == "VAR_IN":
        return load_var_in(n, symast, symimp)
    elif n.tag == "Binary_Substitution":
        return load_binary_substitution(n, symast, symimp)
    elif n.tag == "Nary_Substitution":
        return load_nary_substitution(n, symast, symimp)
    elif n.tag == "Operation_Call":
        return load_operation_call(n, symast, symimp)
    elif n.tag == "While":
        return load_while(n, symast, symimp)
    elif n.tag == "Becomes_In":
        return load_becomes_in(n, symast)
    elif n.tag in {"Choice_Substitution", "Becomes_Such_That",
                   "Select_Substitution", "ANY_Substitution",
                   "LET_Substitution"}:
        error("unexpected substitution: " + n.tag)
    else:
        error("unrecognized substitution: " + n.tag)

def load_block_substitution(n, symast, symimp):
    assert n.tag == "Bloc_Substitution"
    return ast.make_blk([ load_sub(s, symast, symimp) for s in n.findall("./*") ])

def load_skip(n):
    assert n.tag == "Skip"
    return ast.make_skip()

def load_assert_substitution(n, symast):
    assert n.tag == "Assert_Substitution"
    warn("assertion replaced by skip")
    return ast.make_skip()

def load_if_substitution(n, symast, symimp):
    '''
    TODO: understand how ELSIF branch are XML-coded and implement
    their translation.
    '''
    assert n.tag == "If_Substitution"
    if n.get("elseif") != None:
        error("unrecognized elseif attribute in IF substitution")
        return ast.make_skip()
    xmlcond = n.find("./Condition")
    xmlthen = n.find("./Then")
    xmlelse = n.find("./Else")
    pycond = load_boolean_expression(xmlcond.find("./*"), symast)
    pythen = load_sub(xmlthen.find("./*"), symast, symimp)
    thenbr = ast.make_if_br(pycond, pythen)
    if xmlelse == None:
        return ast.make_if([thenbr])
    else:
        pyelse = load_sub(xmlelse.find("./*"), symast, symimp)
        elsebr = ast.make_if_br(None, pyelse)
        return ast.make_if([thenbr, elsebr])

def load_becomes_eq(n, symast):
    assert n.tag == "Affectation_Substitution"
    lhs = n.findall("./Variables/*")
    rhs = n.findall("./Values/*")
    if len(lhs) != 1 or len(rhs) != 1:
        error("unsupported multiple becomes equal substitution")
        return ast.make_skip()
    dst = load_exp(lhs[0], symast)
    src = load_exp(rhs[0], symast)
    return ast.make_beq(dst, src)

def load_becomes_in(n, symast):
    assert n.tag == "Becomes_In"
    lhs = n.findall("./Variables/*")
    dst = [ load_exp(x, symast) for x in lhs ]
    return ast.make_bin(dst)

def load_case_substitution(n, symast, symimp):
    assert n.tag == "Case_Substitution"
    xmlexpr = n.find("./Value/*")
    xmlbranches = n.findall("./Choices/Choice")
    xmlelse = n.find("./Else")
    pyexpr = load_exp(xmlexpr, symast)
    pybranches = [ ast.make_case_br(load_exp(xbr.find("./Value/*"), symast),
                                     load_sub(xbr.find("./Then/*"), symast, symimp))
                   for xbr in xmlbranches ]
    if xmlelse != None:
        pybranches.append(ast.make_case_br(None, load_sub(xmlelse.find("./Choice/Then/*"), symast, symimp)))
    return ast.make_case(pyexpr, pybranches)

def load_var_in(n, symast, symimp):
    assert n.tag == "VAR_IN"
    xmlvars = n.findall("./Variables/Identifier")
    xmlbody = n.find("./Body")
    symast2 = symast.copy()
    pyvars = []
    for v in xmlvars:
        id = value(v)
        type = get_identifier_type(v)
        pyt = ast.make_loc_var(id, type)
        sym_table_add(symast2, id, pyt)
        pyvars.append(pyt)
    pybody = [ load_sub(xmlbody.find("./*"), symast2, symimp) ]
    symast2.clear()
    return ast.make_var_decl(pyvars, pybody)

def load_binary_substitution(n, symast, symimp):
    assert n.tag == "Binary_Substitution"
    op = operator(n)
    if op == "||":
        error("parallel substitution cannot be translated")
        return ast.make_skip()
    elif op == ";":
        left = n.find("./Left")
        right = n.find("./Right")
        return [load_sub(left, symast, symimp), load_sub(right, symast, symimp)]
    else:
        error("unrecognized binary substitution")
        return ast.make_skip()

def load_nary_substitution(n, symast, symimp):
    assert n.tag == "Nary_Substitution"
    op = operator(n)
    if op == "||":
        error("parallel substitution cannot be translated")
        return ast.make_skip()
    elif op == ";":
        substs = n.findall("./*")
        return ast.make_blk([load_sub(s, symast, symimp) for s in substs])
    else:
        error("unrecognized n-ary substitution")
        return ast.make_skip()

def load_operation_call(n, symast, symimp):
    assert n.tag == "Operation_Call"
    xmlname = n.find("./Name/*")
    # Operation from import w/o prefix:
    #   <Identifier value='get'>
    # Operation from import w prefix:
    #   <Identifier value='hh.get' instance='hh' component='get'>
    xmlout = n.findall("./Output_Parameters/*")
    xmlinp = n.findall("./Input_Parameters/*")
    astout = [ load_identifier(x, symast) for x in xmlout ]
    astinp = [ load_identifier(x, symast) for x in xmlinp ]
    instance = xmlname.get('instance')
    if instance == None:
        name = value(xmlname)
    else:
        name = xmlname.get('component')

    op = sym_table_get(symast, name)
    # operation is from a directly imported module
    if name in symimp.keys():
        impo = sym_table_get(symimp, name)
        return ast.make_call(op, astinp, astout, impo)
    # operation is from a prefixed imported module
    elif instance in symimp.keys():
        impo = sym_table_get(symimp, instance)
        return ast.make_call(op, astinp, astout, impo)
    # operation is local
    else:
        return ast.make_call(op, astinp, astout)

def load_while(n, symast, symimp):
    assert n.tag == "While"
    xmlcond = n.find("./Condition/*")
    xmlbody = n.find("./Body/*")
    pycond = load_boolean_expression(xmlcond, symast)
    pybody = load_sub(xmlbody, symast, symimp)
    return ast.make_while(pycond, [pybody])

###
#
# expressions
#
###

def load_exp(n, symast):
    if n.tag == "Binary_Expression":
        return load_binary_expression(n, symast)
    elif n.tag == "Nary_Expression":
        return load_nary_expression(n, symast)
    elif n.tag == "Unary_Expression":
        return load_unary_expression(n, symast)
    elif n.tag == "Boolean_Litteral":
        return load_boolean_literal(n, symast)
    elif n.tag == "Integer_Litteral":
        return load_integer_literal(n, symast)
    elif n.tag == "Identifier":
        return load_identifier(n, symast)
    elif n.tag == "Boolean_Expression":
        return load_boolean_expression(n, symast)
    elif n.tag in {"EmptySet", "EmptySeq", "Quantified_Expression",
                   "Quantified_Set", "String_Litteral", "Struct", "Record"}:
        error("unexpected expression " + n.tag)
        return None
    else:
        error("unknown expression " + n.tag)
        return None

def load_identifier(n, symast):
    return symast[value(n)]

def load_boolean_literal(n, symast):
    assert n.tag == "Boolean_Litteral"
    if value(n) == "TRUE":
        return ast.TRUE
    elif value(n) == "FALSE":
        return ast.FALSE
    else:
        error("unknown boolean literal")

def load_integer_literal(n, symast):
    assert n.tag == "Integer_Litteral"
    return ast.make_intlit(int(value(n)))

def setup_expression(n, handlers):
    op = operator(n)
    if op not in handlers.keys():
        error("unexpected operator " + op)
        return None
    return handlers[op], discard_attributes(n)

def load_unary(n, symast, tag, table):
    assert n.tag == tag
    f, par = setup_expression(n, table)
    assert len(par) == 1
    arg = load_exp(par[0], symast)
    return f(arg)

def load_binary(n, symast, tag, table):
    assert n.tag == tag
    f, par = setup_expression(n, table)
    assert len(par) == 2
    arg = [ load_exp(p, symast) for p in par ]
    return f(arg[0], arg[1])

def load_nary(n, symast, tag, table):
    assert n.tag == tag
    f, par = setup_expression(n, table)
    assert len(par) >= 2
    args = [ load_exp(p, symast) for p in par ]
    return list_combine_ltr(args, lambda a0, a1: f(a0, a1))

def load_unary_expression(n, symast):
    return load_unary(n, symast, "Unary_Expression",
                      {"pred":ast.make_pred, "succ":ast.make_succ})

def load_binary_expression(n, symast):
    return load_binary(n, symast, "Binary_Expression",
                       {"+":ast.make_sum, "-":ast.make_diff,
                        "*":ast.make_prod})

def load_nary_expression(n, symast):
    return load_nary(n, symast, "Nary_Expression",
                     {"+":ast.make_sum, "*":ast.make_prod})

def load_binary_predicate(n, symast):
    return load_binary(n, symast, "Binary_Predicate",
                       {"&":ast.make_and, "or":ast_make_or})

def load_unary_predicate(n, symast):
    return load_unary(n, symast, "Unary_Predicate", {"not":ast.make_not})

def load_nary_predicate(n, symast):
    assert n.tag == "Nary_Predicate"
    f, par = setup_expression(n, {"&":ast.make_and, "or":ast.make_or})
    assert len(par) >= 2
    args = [ load_boolean_expression(p, symast) for p in par ]
    return list_combine_ltr(args, lambda a0, a1: f(a0, a1))

def load_expression_comparison(n, symast):
    return load_binary(n, symast, "Expression_Comparison",
                       {"=": ast.make_eq, "/=": ast.make_neq,
                        ">": ast.make_gt, ">=": ast.make_ge,
                        "<": ast.make_lt, "<=": ast.make_le})

def load_boolean_expression(n, symast):
    if n.tag == "Binary_Predicate":
        return load_binary_predicate(n, symast)
    elif n.tag == "Expression_Comparison":
        return load_expression_comparison(n, symast)
    elif n.tag == "Unary_Predicate":
        return load_unary_predicate(n, symast)
    elif n.tag == "Nary_Predicate":
        return load_nary_predicate(n, symast)
    elif n.tag in {"Quantified_Predicate", "Set"}:
        error("unexpected boolean expression" + n.tag)
        return None
    else:
        error("unknown boolean expression " + n.tag)
        return None

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

def sym_table_new():
    table = dict()
    sym_table_add(table, "MAXINT", ast.MAXINT)
    return table

def sym_table_add(table, id, pyt):
    if id in table:
        error("name clash ("+id+")")
    table[id] = pyt

def sym_table_del(table, id):
    if id not in table:
        error(id+"not found in table")
    table.pop(id)

def sym_table_get(table, id):
    if id not in table:
        error(id+"not found in table")
    return table[id]

###
#
# bxml shortcuts
#
###

def ident(node):
    return node.get("ident")

def value(node):
    '''
    Returns the value of an XML element value attribute.

    Return type is string, or None if there is no such attribute.
    '''
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
    res = value(id.find("./Attributes/TypeInfo/Identifier"))
    assert res != None
    return res

def get_type(n):
    '''
    Input:
    - n: a XML node representing an identifier
    Output:
    - "INTEGER" or "BOOL": the string representing the name of the type of id
    '''
    res = value(n.find("./Attributes/TypeInfo/Identifier"))
    assert res != None
    return res

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

def visible_symbols(p, m):
    '''
    List of symbols defined in m that are externally visible.

    Parameters:
      - m: Python AST node for a machine.
    Result:
      List of Python AST nodes representing the entities defined in m
      and accessible from other modules. If m is a developed machine,
      the list is taken from its corresponding implementation.
    '''
    assert m["kind"] in { "Machine" }
    n = m["implementation"]
    return n["concrete_constants"]+n["variables"]+n["operations"]
