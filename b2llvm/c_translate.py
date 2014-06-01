"""Module responsible for translate B implementation to C header skeleton.

This file uses components from LLVM translation.

"""
import math

from b2llvm.opcode import *
import b2llvm.codebuf as codebuf
from b2llvm.strutils import commas, nconc, SP, NL, TB, TB2

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
            if transLLVM.is_stateful(q.mach):
                section_typedef(buf_header, q.mach)
                
                #transLLVM.state_ref_typedef(buf_header, q.mach)
                buf_header.trace.out("The type for references to state encodings of \""+ast["id"]+"\" is:")
                buf_header.code(TYPE, transLLVM.state_r_name(ast), transLLVM.state_t_name(ast)+"*")
            else:
                buf_header.trace.outu("Module "+q.mach["id"]+ " is stateless and has no associated encoding type.")
            acc.add(q.mach["id"])
    acc.clear()
    buf_header.trace.untab()
    
    
    buf_header.code(TYPEDEF, "int32 value" )
    
    #section_interface_init(buf_header, ast)
    comp = list()
    buf_header.trace.out("The declaration of the function implementing initialisation is:")
    if transLLVM.is_stateful(ast):
        comp.append(ast)
    comp.extend([x.mach for x in transLLVM.comp_indirect(ast)])
    args = commas([transLLVM.state_r_name(x) for x in comp if transLLVM.is_stateful(x)])
    buf_header.code(EXTFNDEC, transLLVM.init_name(ast)[1:], args)
    
    
    for op in transLLVM.operations(ast):
        #section_interface_op(buf_header, ast, op)
        # compute in tl the list of arguments types
        buf_header.trace.out("The declaration of the function implementing operation \""+op["id"]+"\" is:")
        tl = list()
        if transLLVM.is_stateful(ast):
            tl.append(transLLVM.state_r_name(ast))
        tl.extend([ transLLVM.x_type(i["type"]) for i in op["inp"] ])
        tl.extend([ transLLVM.x_type(o["type"])+"*" for o in op["out"] ])
        buf_header.code(EXTFNDEC, transLLVM.op_name(op)[1:], commas(tl))

    
    #buf_header.trace.out("Declaration of function responsible for printing the state")
    #buf_header.code(EXTFNDEC, print_name(ast), state_r_name(ast))
    buf_header.code(ENDIFNDEF, bmodule)
    
    header = open(bmodule+".h", 'w')
    header.write(buf_header.contents())
    header.close()

def section_typedef(buf, m):
    '''
    Generates the definition of the state type machine m.

    Inputs:
      - buf: a CodeBuffer object where the generated code is stored
      - m: AST root node of a machine
      - trace: a Tracer object

    Text of LLVM definitions for the types associated with the state of machine
    m is appended to text. If the machine is stateful, one type is created: an
    aggregate type encoding the state of n (or its implementation if it is a
    developed machine). Otherwise, nothing is generated.
    '''
    import b2llvm.translate as transLLVM
    global NL
    transLLVM.check_kind(m, {"Machine"})
    if transLLVM.is_developed(m):
        section_typedef_impl(buf, transLLVM.implementation(m), m)
    else:
        assert transLLVM.is_base(m)
        if transLLVM.is_stateful(m):
            variables = m["variables"]
            buf.trace.out(m["id"] + ": definition of type coding the state")
            buf.trace.tab()
            for i in range(len(variables)):
                buf.trace.out("Position \"" + str(i) + "\" represents \"" +
                              v["id"] + "\".")
            args = [transLLVM.x_type(v["type"]) for v in m["variables"]]
            buf.code(TYPE, transLLVM.state_t_name(m), "{" + commas(args) + "}")

def section_typedef_impl(buf, i, m):
    '''
    Generates the section implementation of the translation to LLVM.

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
        imports = [transLLVM.state_r_name(imp["mach"]) for imp in i["imports"] 
                   if transLLVM.is_stateful(imp["mach"])]
        variables = [transLLVM.x_type(var["type"]) for var in i["variables"]]
        buf.code(TYPE, transLLVM.state_t_name(m), "{" + commas(imports + variables) +"}")
