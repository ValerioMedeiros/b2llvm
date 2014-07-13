"""Module responsible for translate B implementation to C header skeleton.
   It allows to integrate C source code to llvm code.

"""
import math

from b2llvm.opcode import *
import b2llvm.codebuf as codebuf
from b2llvm.strutils import semicolon, commas, nconc, SP, NL, TB, TB2

def generate_header_skeleton(ast,bmodule):
    '''
    Generate the header skeleton to allow integration to C programs.
    Inputs:
        - ast: root AST node for a B machine in proj
    '''
    import b2llvm.translate as transLLVM
    
    transLLVM.check_kind(ast, { "Machine" })
    assert transLLVM.is_developed(ast)
    
    buf_header = codebuf.CodeBuffer(False)
    buf_header.code(IFNDEF, bmodule)
    buf_header.code(INCLUDE, "<stdint.h>")
    buf_header.code(INCLUDE, "<stdbool.h>"+NL)

    # The state reference is declared below:
    root = transLLVM.Comp([], ast)
    comps = [root] + transLLVM.comp_indirect(ast)
    # emit the type definitions corresponding to the instantiated modules
    # forward references are disallowed: enumerate definitions bottom-up
    comps.reverse()
    acc = set()
    buf_header.trace.out("These are the types encoding the state of each module,")
    buf_header.trace.out("and the corresponding pointer types.")
    buf_header.trace.tab()
    for q in comps:
        if q.mach["id"] not in acc:
            #if transLLVM.is_stateful(q.mach):
            if True:
                transLLVM.check_kind(q.mach, {"Machine"})
                section_typedef_impl(buf_header, transLLVM.implementation(q.mach), q.mach)
                buf_header.trace.out("The type for references to state encodings of \""+ast["id"]+"\" is:")
            else:
                buf_header.trace.outu("Module "+q.mach["id"]+ " is stateless and has no associated encoding type.")
            acc.add(q.mach["id"])
    acc.clear()
    buf_header.trace.untab()
    
    #section_interface_init(buf_header, ast)
    comp = list()
    buf_header.trace.out("The declaration of the function implementing initialisation is:")
    #if transLLVM.is_stateful(ast):
    comp.append(ast)
    comp.extend([x.mach for x in transLLVM.comp_indirect(ast)])
    args = commas([c_state_r_name(x)+" self" for x in comp if transLLVM.is_stateful(x)])
    #args = commas([c_state_r_name(x)+" self" for x in comp ])
    buf_header.code(EXTFNDEC, transLLVM.init_name(ast)[1:], args)
    
    
    for op in transLLVM.operations(ast):
        #section_interface_op(buf_header, ast, op)
        # compute in tl the list of arguments types
        buf_header.trace.out("The declaration of the function implementing operation \""+op["id"]+"\" is:")
        tl = list()
        #TODO: 
        if transLLVM.is_stateful(ast):
            tl.append(c_state_r_name(ast)+" self")
        tl.extend([ cx_type_name_dec(False, i["type"], i["id"]) for i in op["inp"] ])
        tl.extend([ cx_type_name_dec(True, o["type"], o["id"]) for o in op["out"] ])
        buf_header.code(EXTFNDEC, transLLVM.op_name(op)[1:], commas(tl))

    buf_header.code(ENDIFNDEF, bmodule)
    
    header = open(bmodule+".h", 'w')
    header.write(buf_header.contents())
    header.close()

def section_typedef_impl(buf, i, m):
    '''
    Generates the section implementation of the translation to C.

    Inputs:
      - buf: a CodeBuffer object where the generated code is stored
      - i: AST node for a B implementation
      - m: AST node for the B machine corresponding to i

    Definition of the type representing the states of implementation i
    of machine m is appended to text.
    '''
    import b2llvm.translate as transLLVM
    transLLVM.check_kind(i, {"Impl"})
    transLLVM.check_kind(m, {"Machine"})
    if transLLVM.is_stateful(i):
    #if True:
        buf.trace.out("The type encoding the state of \""+m["id"] + "\" is an aggregate and is defined as")
        buf.trace.outu("(using implementation \""+i["id"]+"\"):")
        buf.trace.tab()
        imports = [imp for imp in i["imports"] if transLLVM.is_stateful(imp["mach"])]
        variables = i["variables"]
        pos = 0
        for imp in imports:
            buf.trace.out("Position \"" + str(pos) + "\" represents \"" +
                          transLLVM.printer.imports(imp) + "\".")
            pos = pos + 1
        for var in variables:
            buf.trace.out("Position \"" + str(pos) + "\" represents \"" +
                          var["id"] + "\".")
            pos = pos + 1
        buf.trace.untab()
        imports = [c_state_r_name(imp["mach"]) for imp in i["imports"] 
                   if transLLVM.is_stateful(imp["mach"])]
        variables = [ cx_type_name_dec(False,var["type"], var["id"]) for var in i["variables"]]
        buf.code(TYPEDEFR,  "struct {" + semicolon(imports + variables) +" }  ", c_state_t_name(m))
        buf.code(TYPEDEFR,   c_state_t_name(m)+" *", c_state_r_name(m))

### C IDENTIFIER GENERATION ###

def c_state_t_name(n):
    '''
    - Input:
      n: A node representing a B machine
    - Output:
      A string for the name of the C type representing the state of
      (the implementation) of n.
    '''
    import b2llvm.translate as transLLVM
    transLLVM.check_kind(n, {"Machine", "Impl"})
    if n["kind"] == "Machine":
        return n["id"]+"$state$"
    else:
        return c_state_r_name(transLLVM.machine(n))
    
def c_state_r_name(n):
    '''
    - Input:
      n: A node representing a B machine
    - Output:
      A string for the name of the C type representing a reference to
      the state of (the implementation) of n.
    '''
    import b2llvm.translate as transLLVM
    transLLVM.check_kind(n, { "Machine", "Impl" })
    if n["kind"] == "Machine":
        return n["id"]+"$ref$"
    else:
        return c_state_r_name(transLLVM.machine(n))


def cx_type_name_dec(is_pointer, t, name):
    '''
    This function is responsible for translation B0 type names to C types
    Input:
     - is_pointer : a boolean that indicates when it is a pointer 
     - t : a node object that represent the type
     -name : a node object that represent the id 
    
    '''
    import b2llvm.translate as transLLVM
    transLLVM.check_kind(t, {"Integer", "Bool", "Enumeration", "arrayType"})
    p=" "
    if (is_pointer):
        p = "* "
    if (t == transLLVM.ast.INTEGER):
        return "int32_t" +p+ name
    if (t == transLLVM.ast.BOOL):
        return "bool" +p+ name
    if (t["kind"] == "Enumeration"):
        return "i"+str(transLLVM.bit_width(len(t["elements"])))+ " "+name
    if (t.get("kind")== "arrayType"):
        if (True) :
            ranType = "int32_t" #TODO: needs support new types of ran
        tl =""
        domain = t.get("dom")
        for elem in domain:
            size =int(elem.get("end")) - int(elem.get("start"))+1
            tl += "["+str(size)+"]"
        return  ranType +p+ name + tl  

    