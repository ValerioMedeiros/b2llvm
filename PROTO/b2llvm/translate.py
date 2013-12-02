###
#
# Prototype for a LLVM-IR generator for B
#
# Caveat: This is the first Python program of the author, and he is aware
# that an object oriented (or, rather, a class oriented) solution could be
# appropriate.
#
# Error handling: When an error is detected, the code generator emits a
# message to stdout, inserts an error in the generated LLVM code and
# tries to proceed processing the input.
#
###

import b2llvm.ast as ast
import b2llvm.loadbxml as loadbxml
import b2llvm.names as names
import b2llvm.printer as printer
from b2llvm.strutils import commas, nconc, SP, NL, TB, TB2
from b2llvm.bproject import BProject

#
# Main entry point for this module
#

def translate_bxml(bmodule, outfile, trace, mode='comp', dir='bxml', settings='project.xml', emit_printer=False):
    '''
    Main function for applying the code generator to a B module

    Keywords:
      - bmodule: the name of the B machine to have code generated for
      - outfile: the name of the file where code shall be output
      - mode: the code generation mode
      - dir: the name of the directory where files shall be read (default is 'bxml')
      - settings: the name of the file in dir where the project settings
      are stored (default: project.xml)
    Result:
      None
    '''
    project = loadbxml.load_project(dirname=dir, filename=settings)
    ast = loadbxml.load_module(dir, project, bmodule)
    res = bytearray()
    res.extend(";; -*- mode: asm -*-"+NL) # emacs syntax highlight on
    trace.outu(res, "file generated with b2llvm")
    trace.outu(res, "B project settings: "+settings)
    trace.outu(res, "B module: "+bmodule)
    trace.outu(res, "B project directory: "+dir)
    trace.outu(res, "code generation mode: " + ("component" if mode == "comp" else "project"))
    trace.outu(res, "output file: "+outfile)
    if mode == 'comp':
        translate_mode_comp(res, ast, trace, emit_printer)
    else:
        translate_mode_proj(res, ast, trace, emit_printer)
    llvm = open(outfile, 'w')
    llvm.write(res)
    llvm.close()

#
# TOP-LEVEL FUNCTION FOR EACH TRANSLATION MODE
#

def translate_mode_comp(text, m, trace, emit_printer):
    '''
    Translation in component mode.

    Inputs:
      - res: a bytearray to store LLVM code
      - m: root AST node for a B machine in proj
      - trace: a Tracer object
      - emit_printer: flag indicating if printing functions shall be produced

    LLVM text corresponding to the implementation of n is stored into res
    '''
    check_kind(m, {"Machine"})
    trace.outu(text, "")
    trace.outu(text, "This file contains LLVM code that implements B machine \"" + m["id"]+"\".")
    if is_base(m):
        trace.outu(text, "This machine is registered as a base machine.")
        section_typedef(text, m, trace)
    else:
        assert is_developed(m)
        i = implementation(m)
        trace.outu(text, "It is registered as a developed machine.")
        trace.outu(text, "The produced LLVM code is based on B implementation \""+i["id"]+"\".")
        trace.outu(text, "")
        tmp = comp_indirect(m)
        if tmp != []:
            trace.out(text, "The type declarations for state encodings of all imported modules are:")
            trace.tab()
            acc = set()
            # TODO see if one should not filter out types for stateless modules
            for q in comp_indirect(m):
                if q.mach["id"] not in acc:
                    state_opaque_typedef(text, q.mach, trace)
                    acc.add(q.mach["id"])
            acc.clear()
            trace.untab()
            trace.out(text, "The type definitions for references to these state encodings are:")
            trace.tab()
            # TODO see if one should not filter out types for stateless modules
            for q in comp_indirect(m):
                if q.mach["id"] not in acc:
                    state_ref_typedef(text, q.mach, trace)
                    acc.add(q.mach["id"])
            acc.clear()
            trace.untab()
        tmp = comp_direct(m)
        if tmp != []:
            trace.out(text, "The interfaces of the directly imported modules are:")
            trace.tab()
            for q in tmp:
                if q.mach["id"] not in acc:
                    trace.out(text, "The interface of \""+q.mach["id"]+"\" is composed of:")
                    trace.tab()
                    section_interface(text, q.mach, trace, emit_printer)
                    trace.untab()
                    acc.add(q.mach["id"])
            acc.clear()
            trace.untab()
        if is_stateful(m):
            section_typedef_impl(text, i, m, trace)
            state_ref_typedef(text, m, trace)
        section_implementation(text, m, trace, emit_printer)

def translate_mode_proj(text, m, trace, emit_printer):
    '''
    Translation in project mode.

    Inputs:
      - text: a bytearray where LLVM code is stored
      - m: root AST node for a B machine
      - trace: a Tracer object
      - emit_printer: flag indicating if printing functions shall be produced

    Appends to text the LLVM code corresponding to the LLVM code generation for m
    in project mode.
    '''
    check_kind(m, "Machine")
    assert is_developed(m)
    trace.outu(text, "Preamble")
    trace.outu(text, "")
    trace.outu(text, "This file instantiates B machine \"" + m["id"]+"\", and all its components,")
    trace.outu(text, "and a function to initialise this instantiation.")
    trace.outu(text, "")
    # identify all the module instances that need to be created
    root = Comp([], m)
    comps = [root] + comp_indirect(m)
    # emit the type definitions corresponding to the instantiated modules
    # forward references are disallowed: enumerate definitions bottom-up
    comps.reverse()
    acc = set()
    trace.out(text, "These are the types encoding the state of each module,")
    trace.out(text, "and the corresponding pointer types.")
    trace.tab()
    for q in comps:
        if q.mach["id"] not in acc:
            if is_stateful(q.mach):
                section_typedef(text, q.mach, trace)
                state_ref_typedef(text, q.mach, trace)
            else:
                trace.outu(text, "Module "+q.mach["id"]+ " is stateless and has no associated encoding type.")
            acc.add(q.mach["id"])
    acc.clear()
    trace.untab()
    # the instances are now declared, top down
    trace.out(text, "Variables representing instances of components forming \""+m["id"]+ "\".")
    trace.tab()
    comps.reverse()
    for q in comps:
        if is_stateful(q.mach):
            trace.out(text, "Variable representing to "+q.bstr())
            text.extend(str(q)+" = common global "+state_t_name(q.mach)+" zeroinitializer"+NL)
    trace.untab()
    # emit the declarations for the operations offered by root module
    # only the initialisation is necessary actually
    section_interface(text, m, trace, emit_printer)
    # generate the code of the routine that initializes the system
    # by calling the initialization function for the root module.
    args = [state_r_name(root.mach) + SP + str(root)]
    args += [state_r_name(q.mach)+SP+str(q) for q in comp_stateful(m)]
    trace.out(text, "Definition of the function to initialise instance \""+str(comps[0])+"\" of \""+m["id"]+ "\".")
    trace.tab()
    text.extend("define void @$init$() {"+NL+
                "entry:"+NL)
    trace.out(text, "Call to initialisation function of \""+m["id"]+"\".")
    text.extend(TB+"call void "+init_name(m)+"("+commas(args)+")"+NL+
                TB+"ret void"+NL+
                "}"+NL)
    trace.untab()
    if emit_printer:
        trace.out(text, "Definition of a function to print the state of the system")
        text.extend("define void @$print$() {"+NL)
        text.extend("entry:"+NL)
        trace.out(text, "Call to printing function of \""+m["id"]+"\".")
        text.extend(TB+"call void "+print_name(m)+"("+args[0]+")"+NL)
        text.extend(TB+"ret void"+NL)
        text.extend("}"+NL)

#
# SECTION-LEVEL CODE GENERATION FUNCTIONS
#

def section_interface(text, m, trace, emit_printer):
    '''
    Generates the declaration of all externally visible elements of machine n:
    reference type, initialisation function, operation function.

    Input:
      - text: bytearray where output shall be stored
      - n: AST root node of a machine
      - trace: a Tracer object
      - emit_printer: flag indicating if printing functions shall be produced

    Extends res with text of LLVM declarations (see section interface in translation
    definition).
    '''
    check_kind(m, {"Machine"})
    section_interface_init(text, m, trace)
    for op in operations(m):
        section_interface_op(text, m, op, trace)
    if emit_printer:
        trace.out(text, "Declaration of function responsible for printing the state")
        text.extend("declare void "+print_name(m)+"("+state_r_name(m)+")"+NL)

def operations(m):
    '''
    Gets list of operations of machine m.

    TODO: currently, the AST of developed machines does not have operations
    and this query is forwarded to the corresponding implementation. I would
    prefer to load properly the full AST of such machines.
    '''
    check_kind(m, {"Machine"})
    if is_developed(m):
        return implementation(m)["operations"]
    else:
        return m["operations"]

def section_interface_init(text, m, trace):
    '''
    Generates the declaration of the initialisation function for n

    Inputs:
      - res: bytearray to store output
      - m: a machine AST root node
      - trace: a Tracer object
    Output:
      res is extended with the text of a LLVM function declaration for
      the initalisation
    '''
    global NL
    check_kind(m, {"Machine"})
    comp = list()
    trace.out(text, "The declaration of the function implementing initialisation is:")
    if is_stateful(m):
        comp.append(m)
    comp.extend([x.mach for x in comp_indirect(m)])
    text.extend("declare void"+SP+init_name(m))
    text.extend("("+commas([state_r_name(m) for m in comp if is_stateful(m)])+")"+NL)

def section_interface_op(text, m, op, trace):
    '''
    Declaration of the function implementing operation op in m.

    Inputs:
      - text: bytearray to store output
      - m: a machine AST root node
      - op: an operation AST node

    The declaration of A LLVM function implementing operation op from m is
    appended to text.
    '''
    global NL
    # compute in tl the list of arguments types
    trace.out(text, "The declaration of the function implementing operation \""+op["id"]+"\" is:")
    tl = list()
    if is_stateful(m):
        tl.append(state_r_name(m))
    tl.extend([ x_type(i["type"]) for i in op["inp"] ])
    tl.extend([ x_type(o["type"])+"*" for o in op["out"] ])
    text.extend("declare void"+SP+op_name(op)+"("+commas(tl)+")"+NL)

def section_typedef(text, m, trace):
    '''
    Generates the definition of the state type machine m.

    Inputs:
      - text: bytearray to store output
      - m: AST root node of a machine
      - trace: a Tracer object

    Text of LLVM definitions for the types associated with the state of machine
    m is appended to text. If the machine is stateful, two types are created: an
    aggregate type encoding the state of n (or its implementation if it is a
    developed machine), and one reference type, pointer to the previous type.
    Otherwise, nothing is generated.
    '''
    global NL
    check_kind(m, {"Machine"})
    if is_developed(m):
        section_typedef_impl(text, implementation(m), m, trace)
    else:
        assert is_base(m)
        if is_stateful(m):
            trace.out(text, m["id"] + ": definition of type coding the state")
            text.extend(state_t_name(m)+" = type {"+NL)
            vars = m["variables"]
            for i in range(len(vars)-1):
                v = vars[i]
                text.extend(TB+x_type(v["type"])+",")
                trace.out(text, "represents "+v["id"])
            v = vars[len(vars)-1]
            text.extend(x_type(v["type"])+",")
            trace.out(text, "represents "+v["id"])
            text.extend("}"+NL)

def section_typedef_impl(text, i, m, trace):
    '''
    Generates the section implementation of the translation to LLVM.

    Inputs:
      - text: bytearray to store output
      - i: AST node for a B implementation
      - m: AST node for the B machine corresponding to i
      - trace: a Tracer object

    Definition of the type representing the states of implementation i
    of machine m is appended to text.
    '''
    check_kind(i, {"Impl"})
    check_kind(m, {"Machine"})
    if is_stateful(i):
        trace.out(text, "The type encoding the state of \""+m["id"] + "\" is an aggregate and is defined as")
        trace.outu(text, "(using implementation \""+i["id"]+"\"):")
        text.extend(state_t_name(m)+" = type {"+NL)
        imports = [imp for imp in i["imports"] if is_stateful(imp["mach"])]
        variables = i["variables"]
        left = len(imports)+len(variables)
        pos = 0
        for imp in imports:
            trace.outu(text, "The state of \""+printer.imports(imp)+ "\" is at position "+str(pos)+" and has type:")
            text.extend(TB+state_r_name(imp["mach"])+("" if left == 1 else ",")+NL)
            left = left - 1
            pos = pos + 1
        for var in variables:
            trace.outu(text, "The representation of variable \""+var["id"]+ "\" is at position "+str(pos)+" and has type:")
            text.extend(TB+x_type(var["type"])+("" if left == 1 else ",")+NL)
            left = left - 1
            pos = pos + 1
        assert left == 0
        text.extend("}"+NL)

def section_implementation(text, m, trace, emit_printer):
    '''
    Generates the section implementation of the translation to LLVM.

    Inputs:
      - text: a bytearray where text is appended
      - m: AST node for a B machine
      - trace: a Tracer object
      - emit_printer: flag indicating if printing functions shall be produced

    The definitions of the LLVM functions implementing the initialisation and
    operations of the implementation of m are appended to text.
    '''
    check_kind(m, {"Machine"})
    if is_developed(m):
        i = implementation(m)
        x_init(text, m, i, trace)
        for op in i["operations"]:
            x_operation(text, op, trace)
        if emit_printer:
            x_printer(text, m, i, trace)

#
# TRANSLATION FUNCTIONS OF INDIVIDUAL ELEMENTS OF THE B AST
#

#
# From now on, use x_ as prefix as a shortcut for the prefix translate_
#

### TYPE TRANSLATION ###

#
# This function is responsible for translation B0 type names to LLVM types
#
def x_type(t):
    assert(t == ast.INTEGER or t == ast.BOOL)
    return "i32" if t == ast.INTEGER else "i1"

### TRANSLATION FOR INITIALISATION

def x_init(text, m, i, trace):
    '''
    Input:
      - text: a bytearray to store output
      - m: root AST node of a B machine
      - i: root AST node of the implementation of m

    LLVM implementation of the initialisation clause of i (a LLVM function) is
    appended to text.
    '''
    global TB, NL, SP
    check_kind(m, {"Machine"})
    check_kind(i, {"Impl"})
    tm = state_r_name(m) # LLVM type name: pointer to structure storing m data
    names.reset()
    # 1. generate function signature: one parameter for the implementation
    # instance, one parameter for each transitively imported module instance.
    # 1.1 generate argument names for the imported instances, store in lexicon
    lexicon = dict()
    count = 0 # to generate fresh names
    for q in comp_indirect(m):
        if is_stateful(q.mach):
            lexicon[q] = "%arg"+str(count)+"$"
            count += 1
    # 1.2 generate parameter type, name list
    arg_list = [ tm+SP+"%self$" ]
    for q in comp_indirect(m):
        if is_stateful(q.mach):
            arg_list.append(state_r_name(q.mach)+SP+lexicon[q])
    # 1.3 the signature
    trace.out(text, "The function implementing initialisation for \""+m["id"]+"\" is \""+init_name(i)+"\"")
    trace.outu(text, "and has the following parameters:")
    trace.tab()
    trace.out(text, "\"%self$\": address of LLVM aggregate storing state of \""+m["id"]+"\";")
    for q in comp_indirect(m):
        if is_stateful(q.mach):
            trace.out(text, "\""+lexicon[q]+"\": address of LLVM aggregate storing state of \""+q.bstr()+"\";")
    text.extend("define void"+SP+init_name(i)+"("+commas(arg_list)+") {"+NL)
    # 2. generate function body
    trace.out(text, "The entry point of the initialisation is:")
    text.extend("entry:"+NL)
    # 2.1 reserve stack space for local variables
    x_alloc_inst_list(text, i["initialisation"], trace)
    # 2.2 bind direct imports to elements of state structure
    direct = [ q for q in comp_direct(m) if is_stateful(q.mach) ]
    if direct != []:
        trace.out(text, "The addresses of aggregates representing components of \""+i["id"]+"\"")
        trace.outu(text, "are bound to elements of aggregate representing \""+m["id"]+"\".")
        trace.tab()
        for j in range(len(direct)):
            lbl = names.new_local()
            q = direct[j]
            trace.out(text, "This binds component \"" + q.bstr() + "\" to aggregate element " + str(j)+":")
            tm2 = state_r_name(q.mach)
            text.extend(TB+lbl+" = getelementptr "+tm+" %self$, i32 0, i32 "+str(j)+NL)
            text.extend(TB+"store "+tm2+SP+lexicon[q]+", "+tm2+"* "+lbl+NL)
        trace.untab()
    # 2.3 initialise direct imports
    offset = len(direct)+1
    if comp_direct(m) != []:
        trace.out(text, "Each component is initialised:")
        trace.tab()
        for q in comp_direct(m):
            mq = q.mach     # the imported machine
            arg_list2 = []  # to store parameters needed to initialise mq
            if is_stateful(mq):
                arg_list2.append(state_r_name(mq)+SP+lexicon[q])
                n = len([x for x in comp_indirect(mq) if is_stateful(x.mach)])
                arg_list2.extend(arg_list[offset:offset+n])
                trace.out(text, "Call initialisation function for component \""+q.bstr()+"\".")
                text.extend(TB+"call void "+init_name(mq)+"("+commas(arg_list2)+")"+NL)
        trace.untab()
    # 2.4 translate initialisation instructions
    trace.out(text, "Execute substitutions in initialisation of \""+i["id"]+"\" then exits:")
    trace.tab()
    x_inst_list_label(text, i["initialisation"], "exit", trace)
    trace.untab()
    trace.out(text, "The exit point of the initialisation is:")
    text.extend("exit:"+NL)
    text.extend(TB+"ret void"+NL)
    text.extend("}"+NL)
    trace.untab()

### TRANSLATION FOR PRINTER

def x_printer(text, m, i, trace):
    '''
    Input:
      - text: a bytearray to store output
      - m: root AST node of a B machine
      - i: root AST node of the implementation of m
      - trace: a Tracer object

    Definition of a LLVM function that prints the value of the elements
    composing the state of m m to the standard output stream.
    '''
    global TB, NL, SP
    check_kind(m, {"Machine"})
    check_kind(i, {"Impl"})
    tm = state_r_name(m) # LLVM type name: pointer to structure storing m data
    names.reset()

    trace.out(text, "Definition of function responsible for printing the state,")
    trace.outu(text, "its generation was activated by option --emit-printer.")
    emit_print_i1 = False
    emit_print_i32 = False
    text.extend("define void "+print_name(m)+"("+state_r_name(m)+"%self$) {"+NL)
    j, nb = 0, len(comp_direct(m))+len(i["variables"])
    text.extend("entry:"+NL)
    text.extend(TB+"call void @$b2llvm.print.ldelim()"+NL)
    for q in comp_direct(m):
        m2 = q.mach
        t2 = state_r_name(m2)
        lbl1 = names.new_local()
        lbl2 = names.new_local()
        text.extend(TB+lbl1+" = getelementptr "+tm+" %self$, i32 0, i32 "+str(j)+NL)
        text.extend(TB+lbl2+" = load "+t2+"* "+lbl1+NL)
        text.extend(TB+"call void "+print_name(m2)+"("+state_r_name(m2)+SP+lbl2+")"+NL)
        j += 1
        if j < nb:
            text.extend(TB+"call void @$b2llvm.print.space()"+NL)
    for var in i["variables"]:
        lbl1 = names.new_local()
        lbl2 = names.new_local()
        t2 = x_type(var["type"])
        text.extend(TB+lbl1+" = getelementptr "+tm+" %self$, i32 0, i32 "+str(j)+NL)
        text.extend(TB+lbl2+" = load "+t2+"* "+lbl1+NL)
        if t2 == "i1":
            text.extend(TB+"call void @$b2llvm.print.i1("+t2+SP+lbl2+")"+NL)
            emit_print_i1 = True
        else:
            assert t2 == "i32"
            text.extend(TB+"call void @$b2llvm.print.i32("+t2+SP+lbl2+")"+NL)
            emit_print_i32 = True
        j += 1
        if j < nb:
            text.extend(TB+"call void @$b2llvm.print.space()"+NL)
    text.extend(TB+"call void @$b2llvm.print.rdelim()"+NL)
    text.extend(TB+"ret void"+NL)
    text.extend("}"+NL)
    text.extend("declare void @$b2llvm.print.ldelim()"+NL)
    text.extend("declare void @$b2llvm.print.rdelim()"+NL)
    if nb > 1:
        text.extend("declare void @$b2llvm.print.space()"+NL)
    if emit_print_i1:
        text.extend("declare void @$b2llvm.print.i1(i1)"+NL)
    if emit_print_i32:
        text.extend("declare void @$b2llvm.print.i32(i32)"+NL)


### TRANSLATION OF OPERATIONS

def x_operation(text, n, trace):
    '''
    Code generation for B operations.

    Input:
      - text: a byte array where LLVM code is stored
      - n: an AST node for a B operation
      - trace: a Tracer object
    '''
    global TB, NL
    check_kind(n, {"Oper"})
    names.reset()
    trace.out(text, "The LLVM function implementing B operation \""+n["id"]+"\" in \""+n["root"]["id"]+"\" follows.")
    text.extend("define void "+op_name(n))
    text.extend("("+commas([state_r_name(n["root"])+SP+"%self$"]+
                          [x_type(i["type"])+SP+"%"+i["id"] for i in n["inp"]]+
                          [x_type(o["type"])+"*"+SP+"%"+o["id"] for o in n["out"]])+")")
    text.extend("{"+NL)
    trace.tab()
    text.extend("entry:"+NL)
    x_alloc_inst(text, n["body"], trace)
    x_inst_label(text, n["body"], "exit", trace)
    text.extend("exit:"+NL)
    text.extend(TB+"ret void"+NL)
    text.extend("}"+NL)
    trace.untab()

### TRANSLATION OF STACK VARIABLE ALLOCATION

def x_alloc_inst_list(text, il, trace):
    '''
    Generation of frame stack allocation for instruction lists.

    Input:
      - text: a bytearray where LLVM code is stored
      - il: a list of B instructions AST nodes
      - trace: a Tracer object

    This function is part of a recursive traversal of the syntax tree so that
    all variable declarations are visisted and handled by function
    x_alloc_var_decl.
    '''
    for inst in il:
        x_alloc_inst(text, inst, trace)

def x_alloc_inst(text, n, trace):
    '''
    Generation of frame stack allocation for individual instructions.

    Input:
      - text: a byterray where LLVM code is stored
      - n: AST node for a B instruction
      - trace: a Tracer object

    This function is part of a recursive traversal of the syntax tree so that
    all variable declarations are visisted and handled by function
    x_alloc_var_decl.
    '''
    check_kind(n, {"Beq", "Blk", "Call", "Case", "If", "Skip", "VarD", "While"})
    if n["kind"] in {"Beq", "Call", "Skip"}:
        return
    elif n["kind"] in {"Case", "If"}:
        for br in n["branches"]:
            x_alloc_inst(text, br["body"], trace)
    elif n["kind"] in {"Blk", "While"}:
        x_alloc_inst_list(text, n["body"], trace)
    elif n["kind"] == "VarD":
        x_alloc_var_decl(text, n, trace)
    else:
        print("error: unknown instruction kind")
        text.extend("<error inserted by b2llvm>")

def x_alloc_var_decl(text, n, trace):
    '''
    Generation of frame stack allocation for variable declarations.

    Input:
      - text: a byterray where LLVM code is stored
      - n: AST node for a B variable declaration
      - trace: a Tracer object

    Emits one LLVM alloca instruction for each declared variable and
    processes the variable declaration body of instructions.
    '''
    global TB, NL, SP
    check_kind(n, {"VarD"})
    trace.out(text, "local variable declarations implemented as frame stack allocations")
    trace.tab()
    for v in n["vars"]:
        trace.out(text, "frame stack allocation for variable "+v["id"])
        text.extend(TB+"%"+v["id"]+" = alloca "+x_type(v["type"])+NL)
    x_alloc_inst_list(text, n["body"], trace)
    trace.untab()

### TRANSLATION OF INSTRUCTIONS ###

#
# WARNING:
# WARNING: The LLVM is sensitive to the order local variables and labels names
# WARNING: consequently reordering the translation of the different elements
# WARNING: of an AST node may well generate uncompilable LLVM code.
# WARNING:
# WARNING: Have this is mind before changing the order of the instructions in
# WARNING: the following functions.
# WARNING:
#

def x_inst_list_label(text, l, lbl, trace):
    global TB, NL
    if len(l) == 0:
        text.extend(TB + "br label %" + lbl + NL)
    else:
        i = l[0]
        l2 = l[1:]
        if i["kind"] in {"Case", "If", "While"}:
            lbl2 = names.new_label()
            x_inst_label(text, i, lbl2, trace)
            text.extend(lbl2 + ":\n")
        elif i["kind"] in {"Blk"}:
            x_inst_list(text, i["body"], trace)
        else:
            x_inst(text, i, trace)
        x_inst_list_label(text, l2, lbl, trace)

def x_inst_list(text, il, trace):
    '''
    Input:
      - text: bytearray to store LLVM code
      - il: list of instruction AST nodes
    '''
    for inst in il:
        if inst["kind"] in {"If", "While"}:
            label = names.new_label()
            x_inst_label(text, inst, label, trace)
            text.extend(label + ":\n")
        elif inst["kind"] in {"Blk"}:
            x_inst_list(text, inst["body"], trace)
        else:
            x_inst(text, inst, trace)

def x_inst_label(text, n, lbl, trace):
    check_kind(n, {"Beq", "Blk", "Call", "Case", "If", "VarD", "While"})
    if n["kind"] == "Blk":
        x_inst_list_label(text, n["body"], lbl, trace)
    elif n["kind"] == "Case":
        x_case(text, n, lbl, trace)
    elif n["kind"] == "If":
        x_if(text, n, lbl, trace)
    elif n["kind"] == "While":
        x_while(text, n, lbl, trace)
    elif n["kind"] in {"Beq", "Call"}:
        x_inst(text, n, trace)
        text.extend(TB + "br label %" + lbl + NL)
    elif n["kind"] == "VarD":
        x_inst_list_label(text, n["body"], lbl, trace)
    else:
        print("error: instruction type unknown")
        text.extend("<error inserted by b2llvm>")

def x_inst(text, n, trace):
    check_kind(n, {"Beq", "Call", "VarD"})
    if n["kind"] == "Beq":
        x_beq(text, n, trace)
    elif n["kind"] == "Call":
        x_call(text, n, trace)
    elif n["kind"] == "VarD":
        x_inst_list(text, n["body"], trace)
    elif n["kind"] == "Skip":
        x_skip(text, n, trace)

### TRANSLATION OF SKIP ###

def x_skip(text, n, trace):
    check_kind(n, {"Skip"})

### TRANSLATION OF CASE INSTRUCTIONS

def x_case(text, n, lbl, trace):
    '''
    Generates LLVM code for a B case instruction.

    Input:
      - text: a byterray where LLVM code is stored
      - n: an AST node representing a B instruction
      - lbl: a LLVM label for the block where control flow must go after
      executing n.
    '''
    global NL, TB, SP
    check_kind(n, {"Case"})
    v, t = x_expression(text, n["expr"], trace)
    br = n["branches"]
    # generate one block label for each branch
    labels = x_case_label_list(br)
    # there is a special treatment for in case there is no explicit
    # default branch (the last branch in the AST is not a default branch)
    last = br(len(br)-1)
    default = "val" not in br.keys() or br["val"] == [] or br["val"] == None
    # generate block label for default branch
    if default:
        lblo = labels[len(br)-1]
    else:
        lblo = names.new_label()
    text.extend(TB + "switch " + t + SP + v + ", label %" + lblo + " [" + NL)
    x_case_jump_table(text, br, labels, trace)
    text.extend(TB + "]" + NL)
    text.extend(x_case_block_list(text, br, labels, lbl, default, lblo, trace))

def x_case_label_list(bl):
    '''
    Input:
      - bl: list of case branches
    Output:
      - list of LLVM block labels, one for each non-default branch
    '''
    return [ names.new_label() for branch in bl]

def x_case_jump_table(text, bl, labels, trace):
    '''
    Generates a LLVM jump table for a switch instruction implementing the case
    branches.

    Input:
      - text: a bytearray where LLVM output is stored
      - bl: a list of case branches
      - labels: a list block labels
      - trace: a Tracer object
    '''
    for i in range(len(bl)):
        x_case_val_list(text, bl[i]["val"], labels[i], trace)

def x_case_val_list(text, vl, lbl, trace):
    '''
    Generates entries in the LLVM jump table from values to a block label.

    Input:
      - text: a bytearray where output is stored
      - vl: a list of AST nodes representing B values
      - lbl: a LLVM block label
    '''
    global TB2, SP, NL
    text2 = bytearray()
    for v in vl:
        # the evaluation of the values should not emit LLVM code
        v, t = x_expression(text2, v, trace)
        assert(len(text2) == 0)
        text.extend(TB2 + t + SP + v + ", label %" + lbl + NL)

def x_case_block_list(text, bl, labels, lble, default, lbld, trace):
    '''
    Generates LLVM code blocks of a switch implementing the instructions in the
    branches of a case instruction.

    Input:
      - text: a bytearray where LLVM output is stored
      - bl: a list of case branches
      - labels: a list block labels
      - lble: label of block where control flow must go after executing a branch
      - default: flag indicating if the last branch is a default branch
      - lbld: label of block for default block
      - trace: a Tracer object
    '''
    for i in range(len(bl)):
        branch = bl[i]
        lbl = labels[i]
        text.extend(TB+lbl+":"+NL)
        text.extend(x_inst_label(text, branch["body"], lble, trace))
    if not default:
        text.extend(TB+lbld+":"+NL)
        text.extend(TB+"branch label %"+lble)

### TRANSLATION OF IF INSTRUCTIONS

def x_if(text, n, lbl, trace):
    '''
    Generates LLVM code for a B if instruction.

    Input:
      - text: a byterray where LLVM code is stored
      - n: an AST node representing a B if instruction
      - lbl: a LLVM label for the block where control flow must go after
      executing n.
      - trace: a Tracer object.
    '''
    check_kind(n, {"If"})
    trace.out(text, "Execute \""+ellipse(printer.subst_if(0, n))+"\" and branch to \""+lbl+"\".")
    trace.tab()
    x_if_br(text, n["branches"], lbl, trace)
    trace.untab()

def x_if_br(text, lbr, lbl, trace):
    '''
    Generates LLVM code for a list of B if instruction branches.

    Input:
      - text: a byterray where LLVM code is stored
      - lbr: a list of AST nodes representing B if instruction branches
      - lbl: a LLVM label for the block where control flow must go after
      executing n.
      - trace: a Tracer object
    '''
    nbr = len(lbr)
    assert(nbr>=1)
    for i in range(nbr):
        br = lbr[i]
        check_kind(br, {"IfBr"})
        trace.out(text, "execute if branch \""+ellipse(printer.if_br(0, 0, br))+"\"")
        if i == nbr-1:
            # br is an else branch
            if "cond" not in br.keys() or br["cond"] == None:
                x_inst_label(text, br["body"], lbl, trace)
            # br is an elsif branch
            else:
                lbl_1 = names.new_label()
                x_formula(text, br["cond"], lbl_1, lbl, trace)
                text.extend(lbl_1 + ":" + NL)
                x_inst_label(text, br["body"], lbl, trace)
        else:
            lbl_1 = names.new_label()
            lbl_2 = names.new_label()
            x_formula(text, br["cond"], lbl_1, lbl_2, trace)
            text.extend(lbl_1 + ":" + NL)
            x_inst_label(text, br["body"], lbl, trace)
            text.extend(lbl_2 + ":" + NL)

### TRANSLATION OF WHILE INSTRUCTIONS

def x_while(text, n, lbl, trace):
    '''
    Generates LLVM code for a B while instruction.

    Input:
      - text: a byterray where LLVM code is stored
      - n: an AST node representing a B while instruction
      - lbl: a LLVM label for the block where control flow must go after
      executing n.
    '''
    global NL, TB, SP
    check_kind(n, {"While"})
    trace.out(text, "Execute \""+ellipse(printer.subst_while(0, n))+"\" and branch to \""+lbl+"\".")
    trace.tab()
    trace.out(text, "Evaluate loop guard \""+ellipse(printer.condition(n["cond"]))+"\".")
    lbl1 = names.new_label()
    text.extend(TB+"br label %"+lbl1+NL)
    text.extend(lbl1 + ":" + NL)
    v = x_pred(text, n["cond"], trace)
    lbl2 = names.new_label()
    text.extend(TB + "br i1 " + v + ", label %" + lbl2 + ", label %" + lbl + NL)
    trace.out(text, "Execute loop body \""+ellipse(printer.subst_l(0, n["body"]))+"\".")
    text.extend(lbl2 + ":" +NL)
    x_inst_list_label(text, n["body"], lbl1, trace)
    trace.untab()

### TRANSLATION OF BECOMES EQUAL INSTRUCTIONS

def x_beq(text, n, trace):
    '''
    Generates LLVM code for a B assignment (becomes equal) instruction.

    Input:
      - text: a byterray where LLVM code is stored
      - n: an AST node representing a B assignment instruction
    '''
    global TB, SP, NL
    check_kind(n, {"Beq"})
    trace.out(text, "Execute assignment \""+printer.beq(0, n)+"\":")
    trace.tab()
    v,t = x_expression(text, n["rhs"], trace)
    p,_ = x_lvalue(text, n["lhs"], trace)
    trace.out(text, "Store value at address to achieve assignment.")
    text.extend(TB + "store " + t + SP + v + ", " + t + "* " + p + NL)
    trace.untab()

def x_lvalue(text, n, trace):
    '''
    Translate of "lvalues" (elements to the left of an assignment).

    Input:
      - n: AST node for lvalue
      - trace: a Tracer object
    Output:
      A triple composed of a sequence of LLVM instructions computing
      the lvalue, the name of the local storing the lvalue, and the
      type of the lvalue.
    Note:
      Used to translate assignments and operation calls with output(s).
    Caveat:
      Currently limited to simple identifiers.
    '''
    global TB, NL
    check_kind(n, {"Vari"})
    trace.out(text, "Evaluate address for \""+printer.term(n)+"\".")
    t = x_type(n["type"]) + "*"
    if n["scope"] == "Impl":
        pos=state_position(n)
        v = names.new_local()
        trace.tab()
        trace.out(text, "Variable \""+n["id"]+"\" is stored at position "+str(pos)+" of \"%self$\".")
        trace.outu(text, "Let temporary " + v + " be the corresponding address:")
        trace.untab()
        text.extend(TB + v + " = getelementptr " + state_r_name(n["root"])+
                    " %self$, i32 0, i32 " + str(state_position(n)) + NL)
        return (v, t)
    elif n["scope"] in {"Oper", "Local"}:
        trace.tab()
        trace.out(text, "\""+n["id"]+"\" is stored in the frame stack and represented by \"%"+n["id"]+"\".")
        trace.untab()
        return ("%"+n["id"],t)
    else:
        text.extend("<error inserted by b2llvm>")
        print("error: unknown scope for variable " + v["id"])
        return ("UNKNOWN", "UNKNOWN")

### TRANSLATION OF CALL INSTRUCTIONS

def x_call(text, n, trace):
    '''
    Generates LLVM code for a B call operation instruction.

    Input:
      - text: a byterray where LLVM code is stored
      - n: an AST node representing a B call operation
    '''
    global SP
    check_kind(n, {"Call"})
    trace.out(text, "Execute operation call \""+printer.call(0, n)+"\".")
    operation = n["op"]
    local = (n["inst"] == None) # is a local operation?
    impl = operation["root"]
    # evaluate arguments
    trace.tab()
    trace.out(text, "Evaluate operation arguments.")
    args = list()
    trace.tab()
    if is_stateful(impl):
        trace.out(text, "(implicit) address of structure representing operation component")
        # get the LLVM type of the machine offering the operation
        if local:
            mach = operation["root"]
        else:
            mach = n["inst"]["root"]
        mach_t = state_r_name(mach)
        if local:
            t = mach_t
            v = "%self$"
            trace.out(text, "is %self$")
        else:
            pos = state_position(n["inst"])
            trace.out(text, "is element "+str(pos)+" of %self$")
            t = state_r_name(n["inst"]["mach"])
            v1 = names.new_local()
            v2 = names.new_local()
            text.extend(TB+v1+" = getelementptr "+mach_t+
                        " %self$, i32 0, i32 "+str(pos)+NL)
            text.extend(TB + v2 + " = load " + t +"*" + SP + v1 + NL)
        args.append(t + SP + v2)
    x_inputs(text, args, n["inp"], trace)
    x_outputs(text, args, n["out"], trace)
    trace.untab()
    id = op_name(operation)
    trace.out(text, "Call LLVM function \""+id+"\" implementing B operation \""+n["op"]["id"]+"\".")
    text.extend(TB + "call void" + SP + id + "(" + commas(args) + ")" + NL)
    trace.untab()

def x_inputs(text, args, n, trace):
    global SP
    for elem in n:
        trace.out(text, "Evaluate input parameter \""+printer.term(elem)+"\".")
        v, t = x_expression(text, elem, trace)
        args.append(t + SP + v)

def x_outputs(text, args, n, trace):
    global SP
    for elem in n:
        trace.out(text, "Evaluate output parameter \""+printer.term(elem)+"\".")
        v,t = x_lvalue(text, elem, trace)
        args.append(t + SP + v)

### TRANSLATION OF CONDITIONS ###

def x_formula(text, n, lbl1, lbl2, trace):
    '''
    Generates LLVM code to evaluate a B formula and branch to either labels.

    Input:
      - text: a byterray where LLVM code is stored
      - n: an AST node representing a B formula.
      - lbl1: a LLVM label string
      - lbl2: a LLVM label string
      - trace: a Tracer object
    '''
    check_kind(n, {"Comp", "Form"})
    trace.out(text, "Evaluate formula \""+ellipse(printer.condition(n))+"\", branch to \""+lbl1+"\" if true, to \""+lbl2+"\" otherwise.")
    trace.tab()
    if n["kind"] == "Comp":
        v = x_comp(text, n, trace)
        text.extend(TB+"br i1 "+v+" , label %"+lbl1+", label %"+lbl2+NL)
    elif n["kind"] == "Form":
        if n["op"] == "and":
            x_and(text, n, lbl1, lbl2, trace)
        elif n["op"] == "or":
            x_or(text, n, lbl1, lbl2, trace)
        elif n["op"] == "not":
            x_not(text, n, lbl1, lbl2, trace)
        else:
            text.extend("<error inserted by b2llvm>")
    else:
        text.extend("<error inserted by b2llvm>")
    trace.untab()

def x_comp(text, n, trace):
    '''
    Generates LLVM code to evaluate a B comparison.

    Input:
      - text: a byterray where LLVM code is stored.
      - n: an AST node representing a B comparison.
    Output:
      The identifier of the LLVM temporary variable storing the result of
      the comparison. This variable has type "i1".
    '''
    global TB, SP, NL
    check_kind(n, {"Comp"})
    v1,t1 = x_expression(text, n["arg1"], trace)
    v2,t2 = x_expression(text, n["arg2"], trace)
    v = names.new_local()
    trace.out(text, "Temporary \""+v+"\" gets the value of \""+ellipse(printer.comp(n))+"\".")
    text.extend(TB+v+" = icmp "+llvm_op(n["op"])+SP+t1+SP+v1+", "+v2+NL)
    return v

def x_and(text, n, lbl1, lbl2, trace):
    '''
    Generates LLVM code to evaluate a B conjunction and branch to either label.

    Input:
      - text: a byterray where LLVM code is stored.
      - n: an AST node representing a B conjunction.
      - lbl1: a LLVM label string
      - lbl2: a LLVM label string
    '''
    check_kind(n, {"Form"})
    assert(n["op"] == "and")
    assert(len(n["args"]) == 2)
    lbl = names.new_label()
    arg1 = n["args"][0]
    arg2 = n["args"][1]
    lbl = names.new_label()
    trace.out(text, "Evaluate conjunction \""+ellipse(printer.condition(n))+"\", branch to \""+lbl1+"\" if true, to \""+lbl2+"\" otherwise.")
    trace.tab()
    trace.out(text, "Create a fresh label \""+lbl+"\".")
    x_formula(text, arg1, lbl, lbl2, trace)
    text.extend(lbl + ":" + NL)
    x_formula(text, arg2, lbl1, lbl2, trace)
    trace.untab()

def x_or(text, n, lbl1, lbl2, trace):
    '''
    Generates LLVM code to evaluate a B disjunction and branch to either label.

    Input:
      - text: a byterray where LLVM code is stored.
      - n: an AST node representing a B disjunction.
      - lbl1: a LLVM label string
      - lbl2: a LLVM label string
    '''
    check_kind(n, {"Form"})
    assert(n["op"] == "or")
    assert(len(n["args"]) == 2)
    arg1 = n["args"][0]
    arg2 = n["args"][1]
    lbl = names.new_label()
    trace.out(text, "Evaluate disjunction \""+ellipse(printer.condition(n))+"\", branch to \""+lbl1+"\" if true, to \""+lbl2+"\" otherwise.")
    trace.tab()
    trace.out(text, "Create a fresh label \""+lbl+"\".")
    x_formula(text, arg1, lbl1, lbl, trace)
    text.extend(lbl + ":" + NL)
    x_formula(text, arg2, lbl1, lbl2, trace)
    trace.untab()

def x_not(text, n, lbl1, lbl2, trace):
    '''
    Generates LLVM code to evaluate a B negation and branch to either label.

    Input:
      - text: a byterray where LLVM code is stored.
      - n: an AST node representing a B negation.
      - lbl1: a LLVM label string
      - lbl2: a LLVM label string
    '''
    check_kind(n, {"Form"})
    assert(n["op"] == "not")
    trace.out(text, "Evaluate negation \""+ellipse(printer.condition(n))+"\", branch to \""+lbl1+"\" if true, to \""+lbl2+"\" otherwise.")
    trace.tab()
    x_formula(text, n["args"][0], lbl2, lbl1, trace)
    trace.untab()

def x_pred(text, n, trace):
    if n["kind"] == "Comp":
        return x_comp(text, n, trace)
    else:
        text.extend("<error inserted by b2llvm>")
        return ""

### TRANSLATION OF EXPRESSIONS ###

def x_expression(text, n, trace):
    '''
    Generates LLVM code to evaluate a B expression.

    Input:
      - text: a byterray where LLVM code is stored.
      - n: an AST node representing a B expression.
    Output:
      A pair containing, the identifier of the LLVM temporary variable storing the value
      of the expression, and the LLVM type of this temporary variable.
    '''
    check_kind(n, {"IntegerLit", "BooleanLit", "Vari", "Term", "Cons"})
    trace.out(text, "Evaluate expression \""+ellipse(printer.term(n))+"\".")
    trace.tab()
    if n["kind"] == "IntegerLit":
        res = x_integerlit(text, n, trace), "i32"
    elif n["kind"] == "BooleanLit":
        res = x_booleanlit(text, n, trace), "i1"
    elif n["kind"] == "Vari":
        res = x_name(text, n, trace)
    elif n["kind"] == "Term":
        res = x_term(text, n, trace)
    elif n["kind"] == "Cons":
        res = x_expression(text, n["value"], trace)
    else:
        res = ("","")
    trace.untab()
    trace.outu(text, "The evaluation of \""+ellipse(printer.term(n))+"\" is \""+res[0]+"\".")
    return res

def x_integerlit(text, n, trace):
    '''
    Generates LLVM code to evaluate a B integer literal.

    Input:
      - text: a byterray where LLVM code is stored.
      - n: an AST node representing a B integer literal.
    Output:
      A string of the integer literal value.
    '''
    check_kind(n, {"IntegerLit"})
    trace.out(text, "An integer literal is represented as such in LLVM.")
    return n["value"]

def x_booleanlit(text, n, trace):
    '''
    Generates LLVM code to evaluate a B boolean literal.

    Input:
      - text: a byterray where LLVM code is stored.
      - n: an AST node representing a B integer literal.
    Output:
      A string of the LLVM boolean literal value, i.e. "1" or "0".
    '''
    check_kind(n, {"BooleanLit"})
    trace.out(text, "A Boolean literal is represented as a one-bit integer in LLVM.")
    return "1" if n["value"] == "TRUE" else "0"

def x_name(text, n, trace):
    '''
    Generates LLVM code to evaluate a B identifier in an expression.

    Input:
      - text: a byterray where LLVM code is stored.
      - n: an AST node representing a B expression.
    Output:
      A pair containing, the identifier of the LLVM variable storing the value
      of the B variable of the given identifier, and the LLVM type of this variable.
    '''
    check_kind(n, {"Vari"})
    bvar, btype = n["id"], n["type"]
    ltype = x_type(btype)
    if n["scope"] == "Local":
        lvar = "%"+bvar
        v2 = names.new_local()
        trace.out(text, "B local variable \""+bvar+"\" is on the LLVM stack at address \""+lvar+"\".")
        trace.out(text, "Temporary \""+v2+"\" gets the contents from this position.")
        text.extend(TB + v2 + " = load" + SP + ltype + "*" + SP + lvar + NL)
        lvar = v2
    elif n["scope"] == "Oper":
        trace.out(text, "Operation parameter \""+n["id"]+"\" is LLVM parameter \"%"+n["id"]+"\".")
        lvar = "%"+bvar
    elif n["scope"] == "Impl":
        lptr = names.new_local()
        lvar = names.new_local()
        pos = str(state_position(n))
        trace.out(text, "State variable \""+bvar+"\" is stored at position \""+pos+"\" of \"%self$\".")
        trace.out(text, "Let temporary \""+lptr+"\" be the corresponding address.")
        text.extend(TB+lptr+" = getelementptr "+state_t_name(n["root"])+" %self$, i32 0, i32 "+pos+NL)
        text.extend(TB+lvar+" = load "+ltype+"* "+lptr+NL)
    else:
        text.extend("<error inserted by b2llvm>")
        lvar, type = "", ""
    return (lvar, ltype)

def x_term(text, n, trace):
    '''
    Generates LLVM code to evaluate a B term.

    Input:
      - text: a byterray where LLVM code is stored.
      - n: an AST node representing a B term.
    Output:
      A pair containing, the identifier of the LLVM variable storing the value
      of the B term, and the LLVM type of this value.
    '''
    global TB, SP, NL
    check_kind(n, {"Term"})
    v1, t = x_expression(text, n["args"][0], trace)
    if n["op"] == "succ" or n["op"] == "pred":
        v2 = "1"
    else:
        assert(len(n["args"]) == 2)
        v2, _ = x_expression(text, n["args"][1], trace)
    v = names.new_local()
    trace.out(text, "Let temporary \""+v+"\" get the value of \""+ellipse(printer.term(n))+"\".")
    text.extend(TB + v + " = " + llvm_op(n["op"]) + SP + t + SP + v1 + ", " + v2 + NL)
    return (v, t)

### LLVM IDENTIFIER GENERATION ###

def state_t_name(n):
    '''
    - Input:
      n: A node representing a B machine
    - Output:
      A string for the name of the LLVM type representing the state of
      (the implementation) of n.
    '''
    check_kind(n, {"Machine", "Impl"})
    if n["kind"] == "Machine":
        return "%"+n["id"]+"$state$"
    else:
        return state_r_name(machine(n))

def state_r_name(n):
    '''
    - Input:
      n: A node representing a B machine
    - Output:
      A string for the name of the LLVM type representing a reference to
      the state of (the implementation) of n.
    '''
    check_kind(n, {"Machine", "Impl"})
    if n["kind"] == "Machine":
        return "%"+n["id"]+"$ref$"
    else:
        return state_r_name(machine(n))

def op_name(n):
    '''
    - Input:
      n: A node representing a B operation
    - Output:
      A string for the name of the LLVM construct representing n.
    '''
    check_kind(n, "Operation")
    root = n["root"]
    check_kind(root, "Impl")
    machine = root["machine"]
    return "@" + machine["id"] + "$" + n["id"]

def init_name(n):
    '''
    - Input:
      n : a node representing a B machine or implementation
    - Output:
    String with the name of the LLVM function encoding the initialisation
    of that implementation.
    '''
    check_kind(n, {"Machine", "Impl"})
    mach = n if n["kind"] == "Machine" else n["machine"]
    return "@"+mach["id"]+"$init$"

def print_name(n):
    '''
    - Input:
      n : a node representing a B machine or implementation
    - Output:
    String with the name of the LLVM function responsible for printing
    the state of the component.
    '''
    check_kind(n, {"Machine", "Impl"})
    mach = n if n["kind"] == "Machine" else n["machine"]
    return "@"+mach["id"]+"$printf$"

### LLVM names for B operators ###

def llvm_op(str):
    '''
    Input:
        - str: the name of an operator in B0
    Output: The name of the corresponding LLVM operator
    Example:
        >>> llvm_op("=") == "eq"
        True
        >>> llvm_op("+") == "add"
        True
    Note: An error message is printed and the empty string
    is returned if the translation has not been defined.
    '''
    lex = dict({"=":"eq", "!=": "ne",
                "<":"slt", "<=":"sle", ">":"sgt", ">=":"sge",
                "+":"add", "-": "sub",
                "succ":"add", "pred":"sub",
                "*":"mul", "/":"sdiv", "mod":"srem"})
    if str not in lex.keys():
        print("error: operator " + str + " not translated")
        return ""
    else:
        return lex[str]

### MISC ###

#
# Function check_kind is used to assert that the arguments of translation
# function arguments are in the correct syntactic category
#
def check_kind(n, s):
    '''
    Input:
       - n: represents a B0 syntactic entity
       - s: a set of syntactic entity class names
    Output: None.
    Description: Checks that the class of n is one in s.
    Example:
       >>> check_kind(n, {"IntegerLit, BooleanLit"})
    '''
    assert(n["kind"] in s)

def state_position(n):
    '''
    Input:
      - n: represents a B state variable or imported machine
    Output:
      - position of n in the list of imported machines and state variables
    An error message is printed and the value 0 is returned if n is
    not found.
    '''
    root = n["root"]
    result = 0
    for n2 in root["imports"] + root["variables"]:
        if n2 == n:
            return result
        result += 1
    print("error: position of imported machine or variable not found in implementation")
    return 0

def state_opaque_typedef(res, m, trace):
    '''
    Input:
      - res: bytearray to store output
      - m: represents a B machine
    Desc:
      Appends to res the LLVM definition of type pointer to type representing the
      state of n.
      This only makes sense if n is stateful.
    '''
    global NL
    trace.out(res, "The state encoding type for module \""+m["id"]+"\" is defined elsewhere:")
    res.extend(state_t_name(m) + " = type opaque" + NL)

def state_ref_typedef(res, m, trace):
    '''
    Input:
      - res: bytearray to store output
      - m: represents a B machine
    Desc:
      Adds to res the LLVM definition of type pointer to type representing the
      state of n.
      This only makes sense if n is stateful.
    '''
    global NL
    trace.out(res, "The type for references to state encodings of \""+m["id"]+"\" is:")
    res.extend(state_r_name(m) + " = type " + state_t_name(m) + "*" + NL)

###

def is_developed(m):
    check_kind(m, {"Machine"})
    return m["implementation"] != None

def is_base(m):
    check_kind(m, {"Machine"})
    return m["implementation"] == None

def implementation(m):
    check_kind(m, {"Machine"})
    assert(is_developed(m))
    return m["implementation"]

def machine(m):
    check_kind(m, {"Impl"})
    return m["machine"]

### TRANSLATION OF IMPLEMENTATION

def x_type_expr_impo(n):
    check_kind(n, {"Impo"})
    return state_t_name(n["mach"]["impl"])

def x_type_expr_vari(n):
    check_kind(n, {"Vari"})
    return x_type(n["type"])

def x_type_expr_impl(n):
    check_kind(n, {"Impl"})
    result = ""
    tl = []
    for ni in n["imports"]:
        tl.append(x_type_expr_impo(ni))
    for nv in n["variables"]:
        tl.append(x_type_expr_vari(nv))
    result += "{" + commas(tl) + "}"
    return result

### COMP(ONENTS)

class Comp:
    '''
    This class represents components in a B project. Objects of this
    class have the following attributes:
    - a path, which shall be given as a list of strings
    - a machine, which shall be given as the root AST node of the machine
    - id, which is a unique identifier computed when an instance is created
    Instances are convertible to strings, and are hashable.
    '''
    def __init__(self, p, m):
        check_kind(m, {"Machine"})
        self.path = p
        self.mach = m
        self.id = "@"+"$".join(p)+"$"+m["id"]
        self.b_id = m["id"] if p == [""] else ".".join(p+[m["id"]])
    def __str__(self):
        return self.id
    def __hash__(self):
        return self.id.__hash__()
    def bstr(self):
        return self.b_id

def comp_direct(m):
    '''
    List of direct components.

    Inputs:
      - n: root AST node for a B machine
   Output:
     Sequence of components imported by the implementation of machine m.
   '''
    check_kind(m, {"Machine"})
    if m["comp_direct"] == None:
        if is_base(m):
            m["comp_direct"] = []
        else:
            impl = implementation(m)
            m["comp_direct"] = list()
            for impo in impl["imports"]:
                pre = impo["pre"]
                if pre == None:
                    pre = ""
                m["comp_direct"].append(Comp([pre], impo["mach"]))
    return m["comp_direct"]

def comp_indirect(m):
    '''
    List of all (direct and indirect) components.

    Inputs:
      - m: root AST node for a B machine
   Output:
     Sequence of components ordered by
     increasing level in the import tree: imported components, followed by
     components imported from imported components, etc.
     The imports of a machine are those of the corresponding implementation in
     the given project.
   '''
    check_kind(m, {"Machine"})
    if m["comp_indirect"] == None:
        if is_base(m):
            m["comp_indirect"] = []
        else:
            impl = implementation(m)
            v = comp_direct(m)
            # the intention flattens a list of list into a list
            v.extend([ i for sl in [ comp_indirect(mc.mach) for mc in v ]
                         for i in sl ])
            m["comp_indirect"] = v
    return m["comp_indirect"]

def comp_stateful(m):
    '''
    List of (direct and indirect) stateful components.

    Inputs:
      - m: root AST node for a B machine
   Output:
     Sequence of stateful components ordered by
     increasing level in the import tree: imported components, followed by
     components imported from imported components, etc.
     The imports of a machine are those of the corresponding implementation in
     the given project.
   '''
    return [ x  for x in comp_indirect(m) if is_stateful(x.mach) ]

#
# MISC
#

def is_stateful(n):
    '''
    Checks if n is a stateful module

    Inputs:
      - n: a machine or implementation AST root node
    Output:
      boolean
    '''
    check_kind(n, {"Machine", "Impl"})
    if n["stateful"] == None:
        if n["kind"] == "Machine":
            if is_base(n):
                n["stateful"] = n["variables"] != []
            else:
                n["stateful"] = is_stateful(n["implementation"])
        else:
            if n["variables"] != []:
                n["stateful"] = True
            else:
                n["stateful"] = False
                for i in n["imports"]:
                    if is_stateful(i["mach"]):
                        n["stateful"] = True
                        break
    return n["stateful"]

def ellipse(str):
    '''
    Utility that creates a shortened version of a text. If str is greater than 24 characters,
    the first 21 characters are kept, and elliptic ... replaces the rest of str. Therefore
    the resulting string has at most 24 characters.
    '''
    str2 = str.replace("\n", "")
    if len(str2) > 24:
        return str2[:21]+"..."
    else:
        return str2
