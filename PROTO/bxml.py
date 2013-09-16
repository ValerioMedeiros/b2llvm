# This file is responsible for providing functions to load a BXML file and
# build the corresponding Python abstract syntax tree, using the format and
# the constructors found in file "bimp.py".
# 
# We use the xml.etree.ElementTree library
# See http://docs.python.org/2/library/xml.etree.elementtree.html

import xml.etree.ElementTree as ET
import bimp

###
# rudimentary error handling
#

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

ward_nb = 0
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


### 
# cautious inclusion in symbol table
#
def sym_table_add(table, id, pyt):
    if id in table:
        error("name clash ("+id+")")
    table[id] = pyt

### 
# bxml shortcuts 
#

def get(node):
    return val.get("ident")

def value(node):
    return val.get("value")

def operator(node):
    return val.get("operator")

def name(node):
    return val.get("name")

###
# general-purpose accumulators
#

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

#############################################

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
# expressions
#

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

def load_unary(n, symbols, tag, dict):
    assert n.tag == tag
    f, par = setup_expression(n, dict)
    assert len(par) == 1
    arg = load_expression(par[0], symbols)
    return f(arg)

def load_binary(n, symbols, tag, dict):
    assert n.tag == tag
    f, par = setup_expression(n, dict)
    assert len(par) == 2
    arg = [ load_expression(p, symbols) for p in par ]
    return f(arg[0], arg[1])

def load_nary(n, symbols, tag, dict):
    assert n.tag == tag
    f, par = setup_expression(n, dict)
    assert len(par) >= 2
    args = [ load_expression(p, symbols) for p in par ]
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
                       {"&amp;":bimp.make_and, "or":bimp_make_or})
    
def load_unary_predicate(n, symbols):
    return load_unary(n, symbols, "Unary_Predicate", {"not":bimp.make_not})

def load_nary_predicate(n, symbols):
    return load_nary(n, symbols, "Nary_Predicate", 
                     {"&amp;":bimp.make_and, "or":bimp.make_or})

def load_boolean_expression(n, symbols):
    assert n.tag == "Boolean_Expression"
    if n.tag == "Binary_Predicate":
        load_binary_predicate(n, symbols)
    elif n.tag == "Expression_Comparison":
        load_expression_comparison(n, symbols)
    elif n.tag == "Unary_Predicate":
        load_unary_predicate(n, symbols)
    elif n.tag == "Nary_Predicate":
        load_nary_predicate(n, symbols)
    elif n.tag in { "Quantified_predicat", "Set" }
        error("unexpected boolean expression" + n.tag)
    else:
        error("unknown boolean expression " + n.tag)

def load_expression(n, symbols):
    if n.tag == "Binary_Expression":
        load_binary_expression(n, symbols)
    elif n.tag == "Nary_Expression":
        load_nary_expression(n, symbols)
    elif n.tag == "Unary_Expression":
        load_unary_expression(n, symbols)
    elif n.tag == "Boolean_Litteral":
        load_boolean_literal(n, symbols)
    elif n.tag == "Integer_Litteral":
        load_integer_literal(n, symbols)
    elif n.tag == "Identifier":
        load_identifier(n, symbols)
    elif n.tag == "Boolean_Expression":
        load_boolean_expression(n, symbols)
    elif n.tag in {"EmptySet", "EmptySeq", "Quantified_Expression",
                   "Quantified_Set", "String_Litteral", "Struct", "Record"}:
        error("unexpected expression " + n.tag)
    else:
        error("unknown expression " + n.tag)

###
# substitutions
#

def load_becomes_eq(n, symbols):
    assert n.tag == "Affectation_Substitution"
    lhs = n.findall("./Variables")
    rhs = n.findall("./Values")
    if len(lhs) != 1 or len(rhs) != 1:
        error("unsupported multiple becomes equal substitution")
        return make_skip()    
    dst = load_expression(lhs[0], symbols)
    src = load_expression(rhs[0], symbols)
    return bimp.make_beq(dst, src)

def load_skip(n, symbols):
    assert n.tag == "Skip"
    return bimp.make_skip()

def load_assert_substitution(n, symbols):
    assert n.tag == "Assert_Substitution"
    warn("assertion replaced by skip")
    return bimp.make_skip()

def load_if_substitution(n, symbols):
    assert n.tag == "If_Substitution"
    error("load_if_substitution not yet implemented")
    return bimp.make_skip()

def load_case_substitution(n, symbols):
    assert n.tag == "Case_Substitution"
    error("load_case_substitution not yet implemented")
    return bimp.make_skip()

def load_var_in(n, symbols):
    assert n.tag == "VAR_IN"
    error("load_var_in substitution not yet implemented")
    return bimp.make_skip()

def load_binary_substitution(n, symbols):
    assert n.tag == "Binary_Substitution"
    error("load_binary_substitution not yet implemented")
    return bimp.make_skip()

def load_nary_substitution(n, symbols):
    assert n.tag == "Nary_Substitution"
    error("load_nary_substitution not yet implemented")
    return bimp.make_skip()

def load_operation_call(n, symbols):
    assert n.tag == "Operation_Call"
    error("load_operation_call not yet implemented")
    return bimp.make_skip()

def load_while(n, symbols):
    assert n.tag == "While"
    error("load_while not yet implemented")
    return bimp.make_skip()

def load_substitution(n, symbols):
    '''
    Inputs:
      - n: a XML node representing a B0 substitution
      - symbols: symbol table as Python dictionary mapping strings to
      Python nodes
    Output:
      Python node representing the substitution n
    '''
    if n.tag == "Block_Substitution":
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

'''
  <xs:element name="Select_Substitution">
    <xs:complexType>
      <xs:sequence>
	<xs:element name="Attributes" minOccurs="0" maxOccurs="1" type="Attributes_type"/>
	<xs:element name="Select" minOccurs="1" maxOccurs="unbounded">
	  <xs:complexType>
	    <xs:sequence>
	      <xs:element name="When" minOccurs="1" maxOccurs="1" type="Predicate_type"/>
	      <xs:element name="Then" minOccurs="1" maxOccurs="1" type="Substitution_type"/>
	    </xs:sequence>
	  </xs:complexType>
	</xs:element>
	<xs:element name="Else" minOccurs="0" maxOccurs="1" type="Substitution_type"/>
      </xs:sequence>
    </xs:complexType>
  </xs:element>

  <xs:element name="Case_Substitution">
    <xs:complexType>
      <xs:sequence>
	<xs:element name="Attributes" minOccurs="0" maxOccurs="1" type="Attributes_type"/>
	<xs:element name="Value" minOccurs="1" maxOccurs="1" type="Expression_type"/>
	<xs:element name="Choices" minOccurs="1" maxOccurs="unbounded">
	  <xs:complexType>
	    <xs:sequence>
	      <xs:element name="Choice" minOccurs="1" maxOccurs="1" type="Expression_type"/>
	      <xs:element name="Then" minOccurs="1" maxOccurs="1" type="Substitution_type"/>
	    </xs:sequence>
	  </xs:complexType>
	</xs:element>
	<xs:element name="Else" minOccurs="1" maxOccurs="1" type="Substitution_type"/>
      </xs:sequence>
    </xs:complexType>
  </xs:element>

  <xs:element name="Becomes_In">
    <xs:complexType>
      <xs:sequence>
	<xs:element name="Attributes" minOccurs="0" maxOccurs="1" type="Attributes_type"/>
	<xs:element name="Variables" minOccurs="1" maxOccurs="1" type="Variables_type"/>
	<xs:element name="Value" minOccurs="1" maxOccurs="1" type="Expression_type"/>
      </xs:sequence>
    </xs:complexType>
  </xs:element>

  <xs:element name="ANY_Substitution">
    <xs:complexType>
      <xs:sequence>
	<xs:element name="Attributes" minOccurs="0" maxOccurs="1" type="Attributes_type"/>
	<xs:element name="Variables" minOccurs="1" maxOccurs="1" type="Variables_type"/>
	<xs:element name="Predicate" minOccurs="1" maxOccurs="1" type="Predicate_type"/>
	<xs:element name="Then" minOccurs="1" maxOccurs="1" type="Substitution_type"/>
      </xs:sequence>
    </xs:complexType>
  </xs:element>

  <xs:element name="LET_Substitution">
    <xs:complexType>
      <xs:sequence>
	<xs:element name="Attributes" minOccurs="0" maxOccurs="1" type="Attributes_type"/>
	<xs:element name="Variables" minOccurs="1" maxOccurs="1" type="Variables_type"/>
	<xs:element name="Values" minOccurs="1" maxOccurs="1">
	  <xs:complexType>
	    <xs:sequence>
	      <xs:element name="Valuation" minOccurs="1" maxOccurs="unbounded">
		<xs:complexType>
		  <xs:sequence>
		    <xs:group ref="Expression" minOccurs="1" maxOccurs="1" />
	      	  </xs:sequence>
		  <xs:attribute name="ident" type="xs:string"/> 
	      	</xs:complexType>
	      </xs:element>
	    </xs:sequence>
	  </xs:complexType>
	</xs:element>
	<xs:element name="Then" minOccurs="1" maxOccurs="1" type="Substitution_type"/>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
  
  <xs:simpleType name="op_var_sub">
    <xs:restriction base="xs:string">
      <xs:enumeration value="ANY"/>
      <xs:enumeration value="LET"/>
    </xs:restriction>
  </xs:simpleType>

  <xs:element name="VAR_IN">
    <xs:complexType>
      <xs:sequence>
	<xs:element name="Attributes" minOccurs="0" maxOccurs="1" type="Attributes_type"/>
	<xs:element name="Variables" minOccurs="1" maxOccurs="1" type="Variables_type"/>
	<xs:element name="Body" minOccurs="1" maxOccurs="1" type="Substitution_type"/>
      </xs:sequence>
      <xs:attribute name="operator" type="op_var_sub"/> 
    </xs:complexType>
  </xs:element>

  <xs:element name="Binary_Substitution">
    <xs:complexType>
      <xs:sequence>
	<xs:element name="Attributes" minOccurs="0" maxOccurs="1" type="Attributes_type"/>
	<xs:element name="Left" minOccurs="1" maxOccurs="1" type="Substitution_type"/>
	<xs:element name="Right" minOccurs="1" maxOccurs="1" type="Substitution_type"/>
      </xs:sequence>
      <xs:attribute name="operator" type="op_binary"/> 
    </xs:complexType>
  </xs:element>

  <xs:complexType name="Nary_Substitution_type">
    <xs:sequence>
      <xs:element name="Attributes" minOccurs="0" maxOccurs="1" type="Attributes_type"/>
      <xs:group ref="Substitution" minOccurs="0" maxOccurs="unbounded"/>
    </xs:sequence>
    <xs:attribute name="operator" type="op_binary"/> 
  </xs:complexType>
'''
        
### machine clauses

def load_imports(imports):
    if imports == None:
        return []
    # todo
    error("loading imports from XML not yet implemented")
    return []

# <xs:element name="Values" minOccurs="0" maxOccurs="1">
#   <xs:complexType>
#     <xs:sequence>
#       <xs:element name="Valuation" minOccurs="1" maxOccurs="unbounded">
# 	<xs:complexType>
# 	  <xs:sequence>
# 	    <xs:group ref="Expression" minOccurs="1" maxOccurs="1" />
#       	  </xs:sequence>
# 	  <xs:attribute name="ident" type="xs:string"/> 
#       	</xs:complexType>
#       </xs:element>
#     </xs:sequence>
#   </xs:complexType>
# </xs:element>
def load_values(root, symbols):
    vals = root.findall("./Values/Valuation")
    result = []
    for v in vals:
        id = ident(v)
        exp = load_expression(v, symbols)
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
        pyt = bimp.make_imp_var(value(id), get_identifier_type(v))
        sym_table_add(symbols, id, pyt)
        result.append(pyt)
    return result

def load_initialisation(root, symbols):
    initialisation = root.find("./Initialisation")
    if initialisation = None:
        return []
    return [ load_substitution(s, symbols) for s in initialisation ]

# <xs:element name="Operation">
#   <xs:complexType>
#     <xs:sequence>				
#       <xs:element name="Attributes" minOccurs="0" maxOccurs="1" type="Attributes_type"/>
#       <xs:element name="Output_Parameters" minOccurs="0" maxOccurs="1">
#         <xs:complexType>
#           <xs:sequence>
#             <xs:element name="Identifier" minOccurs="1" maxOccurs="unbounded" type="Identifier_type"/>
#           </xs:sequence>
#         </xs:complexType>
#       </xs:element>
#       <xs:element name="Input_Parameters" minOccurs="0" maxOccurs="1">
#         <xs:complexType>
#           <xs:sequence>
#             <xs:element name="Identifier" minOccurs="1" maxOccurs="unbounded" type="Identifier_type"/>
#           </xs:sequence>
#         </xs:complexType>
#       </xs:element>
#       <xs:element name="Precondition" minOccurs="0" maxOccurs="1" type="Predicate_type"/>
#       <xs:element name="Body" type="Substitution_type"/>
#     </xs:sequence>	
#     <xs:attribute name="name" type="xs:string"/> 
#   </xs:complexType>
# </xs:element>
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
        pyt = make_arg_var(id, type)
        sym_table_add(op_symbols, id, pyt)
        p_inputs.append(pyt)
    for o in outputs:
        id = value(o)
        type = get_identifier_type(o)
        pyt = make_arg_var(id, type)
        sym_table_add(op_symbols, id, pyt)
        p_outputs.append(pyt)
    assert len(body) == 1
    p_body = load_substitution(body[0], op_symbols)
    return bimp.make_oper(id, p_inputs, p_outputs, p_body)

def load_operations(root, symbols):
    operations = root.find(".//Operation")
    return [load_operation(op, symbols) for op in operations]

###
# modules
#

def load_bxml(filename):
    symbols = dict()
    tree = ET.parse(filename)
    root = tree.getroot()
    assert root.tag == 'Machine'
    assert root.get("type") == "Implementation"
    id = root.get("name")
    imports = load_imports(root.find("Imports"))
    constants = load_values(root, symbols)
    variables = load_concrete_variables(root, symbols)
    initialisation = load_initialisation(root, symbols)
    operations = load_operations(root, symbols)
    return bimp.make_implementation(id, imports, constants, variables,
                                    initialisation, operations)
