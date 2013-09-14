# This file is responsible for providing functions to load a BXML file and
# build the corresponding Python abstract syntax tree, using the format and
# the constructors found in file "bimp.py".
# 
# We use the xml.etree.ElementTree library
# See http://docs.python.org/2/library/xml.etree.elementtree.html

import xml.etree.ElementTree as ET
import bimp

def get_identifier_type(id):
    '''
    Input:
      - id: a XML node representing an identifier
    Output:
      - "INTEGER" or "BOOL": the string representing the name of the type of id 
    '''
    assert id.tag == "Identifier"
    assert id.find("Attributes") != None
    assert id.find("Attributes").find("TypeInfo") != None
    assert id.find("Attributes").find("TypeInfo").find("Identifier") != None
    assert id.find("Attributes").find("TypeInfo").find("Identifier").get("value") != None
    return id.find("Attributes").find("TypeInfo").find("Identifier").get("value")

def load_imports(imports):
    if imports == None:
        return []
    # todo
    print("Error: loading imports from XML not yet implemented")
    return []

def load_values(values):
    if values == None:
        return []
    valuations = values.findall("Valuation")
    return [ bimp.make_const(val.get('ident'), 
                             val.find('Integer_Litteral').get("value"), 
                             val.find('Integer_Litteral').find('Attributes').find('TypeInfo').find('Identifier').get('value')) 
             for val in valuations ]

def load_concrete_variables(variables):
    if variables == None:
        return []
    if not isinstance(variables, list) # this is in case there is a single element in the XML tree
    variables = [ variables ]
    return [ bimp.make_imp_var(id.get("value"), get_identifier_type(v)) for v in variables ]

def load_initialisation(initialisation):
    if initialisation == None:
        return []
    # todo
    print("Error: loading initialisation from XML not yet implemented")
    return []

def load_operations(operations):
    if operations == None:
        return []
    if not isinstance(operations, list) # this is in case there is a single element in the XML tree
    operations = [ operations ]
    # todo
    print("Error: loading operations from XML not yet implemented")
    return []

def load_bxml(filename):
    print("Error: load_bxml is not yet completed")
    assert False
    tree = ET.parse(filename)
    root = tree.getroot()
    assert root.tag == 'Machine'
    assert root.get("type") == "Implementation"
    id = root.get("name")
    imports = load_imports(root.find("Imports"))
    constants = load_values(root.find("Values"))
    variables = load_concrete_variables(root.findall("Concrete_Variables"))
    initialisation = load_initialisation(root.find("Initialisation"))
    operations = load_operations(root.find("Operations"))
