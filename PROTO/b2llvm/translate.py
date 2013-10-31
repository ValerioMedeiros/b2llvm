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
from b2llvm.strutils import commas, nconc, sp, nl, tb, tb2
from b2llvm.bproject import BProject

import b2llvm.trace as trace

#
# Main entry point for this module
#

def translate_bxml(bmodule, outfile, mode='comp', dir='bxml', settings='project.xml'):
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
    res.extend(";; -*- mode: asm -*-"+nl) # emacs syntax highlight on
    trace.OUTU(res, "file generated with b2llvm")
    trace.OUTU(res, "B module: "+bmodule)
    trace.OUTU(res, "B project directory: "+dir)
    trace.OUTU(res, "B project settings: "+settings)
    trace.OUTU(res, "code generation mode: " + ("component" if mode == "comp" else "project"))
    trace.OUTU(res, "output file: "+outfile)
    if mode == 'comp':
        translate_mode_comp(res, ast)
    else:
        translate_mode_proj(res, ast)
    llvm = open(outfile, 'w')
    llvm.write(res)
    llvm.close()

#
# TOP-LEVEL FUNCTION FOR EACH TRANSLATION MODE
#

def translate_mode_comp(text, m):
    '''
    Translation in component mode.

    Inputs:
      - res: a bytearray to store LLVM code
      - m: root AST node for a B machine in proj

    LLVM text corresponding to the implementation of n is stored into res
    '''
    check_kind(m, {"Machine"})
    trace.OUTU(text, "")
    trace.OUTU(text, "This file contains LLVM code that implements B machine \"" + m["id"]+"\".")
    if is_base(m):
        trace.OUTU(text, "This machine is registered as a base machine.")
        section_typedef(text, m)
    else:
        assert is_developed(m)
        i = implementation(m)
        trace.OUTU(text, "It is registered as a developed machine.")
        trace.OUTU(text, "The produced LLVM code is based on B implementation \""+i["id"]+"\".")
        trace.OUTU(text, "")
        tmp = comp_indirect(m)
        if tmp != []:
            trace.OUT(text, "The type declarations for state encodings of all imported modules are:")
            trace.TAB()
            acc = set()
            # TODO see if one should not filter out types for stateless modules
            for q in comp_indirect(m):
                if q.mach["id"] not in acc:
                    state_opaque_typedef(text, q.mach)
                    acc.add(q.mach["id"])
            acc.clear()
            trace.UNTAB()
            trace.OUT(text, "The type definitions for references to these state encodings are:")
            trace.TAB()
            # TODO see if one should not filter out types for stateless modules
            for q in comp_indirect(m):
                if q.mach["id"] not in acc:
                    state_ref_typedef(text, q.mach)
                    acc.add(q.mach["id"])
            acc.clear()
            trace.UNTAB()
        tmp = comp_direct(m)
        if tmp != []:
            trace.OUT(text, "The interfaces of the directly imported modules are:")
            trace.TAB()
            for q in tmp:
                if q.mach["id"] not in acc:
                    trace.OUT(text, "The interface of \""+q.mach["id"]+"\" is composed of:")
                    trace.TAB()
                    section_interface(text, q.mach)
                    trace.UNTAB()
                    acc.add(q.mach["id"])
            acc.clear()
            trace.UNTAB()
        if is_stateful(m):
            section_typedef_impl(text, i, m)
            state_ref_typedef(text, m)
        section_implementation(text, m)

def translate_mode_proj(text, m):
    '''
    Translation in project mode.

    Inputs:
      - text: a bytearray where LLVM code is stored
      - m: root AST node for a B machine

    Appends to text the LLVM code corresponding to the LLVM code generation for m
    in project mode.
    '''
    check_kind(m, "Machine")
    assert is_developed(m)
    trace.OUTU(text, "This file contains LLVM code that instantiates B machine \"" + m["id"]+"\"")
    trace.OUTU(text, "and for a function to initialise this instantiation.")
    # identify all the module instances that need to be created
    root = Comp([], m)
    comps = [root] + comp_indirect(m)
    # emit the type definitions corresponding to the instantiated modules
    # forward references are disallowed: enumerate definitions bottom-up
    comps.reverse()
    trace.TAB()
    acc = set()
    trace.OUT(text, "The type declarations for state encodings of all imported modules are:")
    for q in comps:
        if q.mach["id"] not in acc:
            if is_stateful(q.mach):
                trace.OUTU(text, "Machine "+q.mach["id"]+ " is stateful.")
                section_typedef(text, q.mach)
            else:
                trace.OUTU(text, "Module "+q.mach["id"]+ " is stateless and has no associated encoding type.")
            acc.add(q.mach["id"])
    acc.clear()
    trace.OUT(text, "The type definitions for references to these state encodings are:")
    for q in comps:
        if q.mach["id"] not in acc:
            if is_stateful(q.mach):
                state_ref_typedef(text, q.mach)
            acc.add(q.mach["id"])
    acc.clear()
    trace.UNTAB()
    # the instances are now declared, top down
    trace.OUT(text, m["id"]+ ": declaration of variables representing module instances")
    trace.TAB()
    comps.reverse()
    for q in comps:
        if is_stateful(q.mach):
            trace.OUT(text, "declaration of variable corresponding to "+q.bstr())
            text.extend(str(q)+" = common global "+state_t_name(q.mach)+" zeroinitializer"+nl)
    trace.UNTAB()
    # emit the declarations for the operations offered by root module
    # only the initialisation is necessary actually
    section_interface(text, m)
    # generate the code of the routine that initializes the system
    # by calling the initialization function for the root module.
    args = [state_r_name(root.mach) + sp + str(root)]
    args += [state_r_name(q.mach)+sp+str(q) for q in comp_stateful(m)]
    trace.OUT(text, "definition of the function to initialise an instance of "+m["id"]+ " and its components")
    trace.TAB()
    text.extend("define void @$init$() {"+nl+
                "entry:"+nl)
    trace.OUT(text, "call to initialisation function of "+m["id"])
    text.extend(tb+"call void "+init_name(m)+"("+commas(args)+")"+nl+
                tb+"ret void"+nl+
                "}")
    trace.UNTAB()

#
# SECTION-LEVEL CODE GENERATION FUNCTIONS
# 

def section_interface(text, m):
    '''
    Generates the declaration of all externally visible elements of machine n:
    reference type, initialisation function, operation function.

    Input:
      - text: bytearray where output shall be stored
      - n: AST root node of a machine

    Extends res with text of LLVM declarations (see section interface in translation 
    definition).
    '''
    check_kind(m, {"Machine"})
    section_interface_init(text, m)
    for op in operations(m):
        section_interface_op(text, m, op)

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

def section_interface_init(text, m):
    '''
    Generates the declaration of the initialisation function for n

    Inputs:
      - res: bytearray to store output
      - m: a machine AST root node
    Output:
      res is extended with the text of a LLVM function declaration for
      the initalisation
    '''
    global nl
    check_kind(m, {"Machine"})
    comp = list()
    trace.OUT(text, "The declaration of the function implementing initialisation is:")
    if is_stateful(m):
        comp.append(m)
    comp.extend([x.mach for x in comp_indirect(m)])
    text.extend("declare void"+sp+init_name(m))
    text.extend("("+commas([state_r_name(m) for m in comp if is_stateful(m)])+")"+nl)

def section_interface_op(text, m, op):
    '''
    Declaration of the function implementing operation op in m.

    Inputs:
      - text: bytearray to store output
      - m: a machine AST root node
      - op: an operation AST node

    The declaration of A LLVM function implementing operation op from m is
    appended to text.
    '''
    global nl
    # compute in tl the list of arguments types
    trace.OUT(text, "The declaration of the function implementing operation \""+op["id"]+"\" is:")
    tl = list()
    if is_stateful(m):
        tl.append(state_r_name(m))
    tl.extend([ x_type(i["type"]) for i in op["inp"] ])
    tl.extend([ x_type(o["type"])+"*" for o in op["out"] ])
    text.extend("declare void"+sp+op_name(op)+"("+commas(tl)+")"+nl)

def section_typedef(text, m):
    '''
    Generates the definition of the state type machine m.

    Inputs:
      - text: bytearray to store output
      - m: AST root node of a machine

    Text of LLVM definitions for the types associated with the state of machine
    m is appended to text. If the machine is stateful, two types are created: an
    aggregate type encoding the state of n (or its implementation if it is a
    developed machine), and one reference type, pointer to the previous type.
    Otherwise, nothing is generated.
    '''
    global nl
    check_kind(m, {"Machine"})
    if is_developed(m):
        section_typedef_impl(text, implementation(m), m)
    else:
        assert is_base(m)
        if is_stateful(m):
            trace.OUT(text, m["id"] + ": definition of type coding the state")
            text.extend(state_t_name(m)+" = type {"+nl)
            vars = m["variables"]
            for i in range(len(vars)-1):
                v = vars[i]
                text.extend(tb+x_type(v["type"])+",")
                trace.OUT(text, "represents "+v["id"])
            v = vars[len(vars)-1]
            text.extend(x_type(v["type"])+",")
            trace.OUT(text, "represents "+v["id"])
            text.extend("}"+nl)

def section_typedef_impl(text, i, m):
    '''
    Generates the section implementation of the translation to LLVM.

    Inputs:
      - text: bytearray to store output
      - i: AST node for a B implementation
      - m: AST node for the B machine corresponding to i

    Definition of the type representing the states of implementation i
    of machine m is appended to text.
    '''
    check_kind(i, {"Impl"})
    check_kind(m, {"Machine"})
    if is_stateful(i):
        trace.OUT(text, "The type encoding the state of \""+m["id"] + "\" is an aggregate and is defined as")
        trace.OUTU(text, "(using implementation \""+i["id"]+"\"):")
        text.extend(state_t_name(m)+" = type {"+nl)
        imports = [imp for imp in i["imports"] if is_stateful(imp["mach"])]
        variables = i["variables"]
        left = len(imports)+len(variables)
        pos = 1
        for imp in imports:
            trace.OUTU(text, "The state of \""+printer.imports(imp)+ "\" is at position "+str(pos)+" and has type:")
            text.extend(tb+state_r_name(imp["mach"])+("" if left == 1 else ",")+nl)
            left = left - 1
            pos = pos + 1
        for var in variables:
            trace.OUTU(text, "The representation of variable \""+var["id"]+ "\" is at position "+str(pos)+" and has type:")
            text.extend(tb+x_type(var["type"])+("" if left == 1 else ",")+nl)
            left = left - 1
            pos = pos + 1
        assert left == 0
        text.extend("}"+nl)

def section_implementation(text, m):
    '''
    Generates the section implementation of the translation to LLVM.

    Inputs:
      - text: a bytearray where text is appended
      - m: AST node for a B machine

    The definitions of the LLVM functions implementing the initialisation and
    operations of the implementation of m are appended to text.
    '''
    check_kind(m, {"Machine"})
    if is_developed(m):
        i = implementation(m)
        x_init(text, m, i)
        for op in i["operations"]:
            x_operation(text, op)

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

def x_init(text, m, i):
    '''
    Input:
      - text: a bytearray to store output
      - m: root AST node of a B machine
      - i: root AST node of the implementation of m

    LLVM implementation of the initialisation clause of i (a LLVM function) is
    appended to text.
    '''
    global tb, nl, sp
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
    arg_list = [ tm+sp+"%self$" ]
    for q in comp_indirect(m):
        if is_stateful(q.mach):
            arg_list.append(state_r_name(q.mach)+sp+lexicon[q])
    # 1.3 the signature
    trace.OUT(text, "The function implementing initialisation for \""+m["id"]+"\" is \""+init_name(i)+"\"")
    trace.OUTU(text, "and has the following parameters:")
    trace.TAB()
    trace.OUT(text, "\"%self$\": address of LLVM aggregate storing state of \""+m["id"]+"\";")
    for q in comp_indirect(m):
        if is_stateful(q.mach):
            trace.OUT(text, "\""+lexicon[q]+"\": address of LLVM aggregate storing state of \""+q.bstr()+"\";")
    text.extend("define void"+sp+init_name(i)+"("+commas(arg_list)+") {"+nl)
    # 2. generate function body
    trace.OUT(text, "The entry point of the initialisation is:")
    text.extend("entry:"+nl)
    # 2.1 reserve stack space for local variables
    x_alloc_inst_list(text, i["initialisation"])
    # 2.2 bind direct imports to elements of state structure
    direct = [ q for q in comp_direct(m) if is_stateful(q.mach) ]
    if direct != []:
        trace.OUT(text, "The addresses of aggregates representing components of \""+i["id"]+"\"")
        trace.OUTU(text, "are bound to elements of aggregate representing \""+m["id"]+"\".")
        trace.TAB()
        for j in range(len(direct)):
            lbl = names.new_local()
            q = direct[j]
            trace.OUT(text, "This binds component \"" + q.bstr() + "\" to aggregate element " + str(j)+":")
            tm2 = state_r_name(q.mach)
            text.extend(tb+lbl+" = getelementptr "+tm+" %self$, i32 0, i32 "+str(j)+nl)
            text.extend(tb+"store "+tm2+sp+lexicon[q]+", "+tm2+"* "+lbl+nl)
        trace.UNTAB()
    # 2.3 initialise direct imports
    offset = len(direct)+1
    if comp_direct(m) != []:
        trace.OUT(text, "Each component is initialised:")
        trace.TAB()
        for q in comp_direct(m):
            mq = q.mach     # the imported machine
            arg_list2 = []  # to store parameters needed to initialise mq
            if is_stateful(mq):
                arg_list2.append(state_r_name(mq)+sp+lexicon[q])
                n = len([x for x in comp_indirect(mq) if is_stateful(x.mach)])
                arg_list2.extend(arg_list[offset:offset+n])
                trace.OUT(text, "Call initialisation function for component \""+q.bstr()+"\".")
                text.extend(tb+"call void "+init_name(mq)+"("+commas(arg_list2)+")"+nl)
        trace.UNTAB()
    # 2.4 translate initialisation instructions
    trace.OUT(text, "Execute substitutions in initialisation of \""+i["id"]+"\" then exits:")
    trace.TAB()
    x_inst_list_label(text, i["initialisation"], "exit")
    trace.UNTAB()
    trace.OUT(text, "The exit point of the initialisation is:")
    text.extend("exit:"+nl)
    text.extend(tb+"ret void"+nl)
    text.extend("}"+nl)
    trace.UNTAB()

### TRANSLATION OF OPERATIONS

def x_operation(text, n):
    '''
    Code generation for B operations.

    Input:
      - text: a byte array where LLVM code is stored
      - n: an AST node for a B operation
    '''
    global tb, nl
    check_kind(n, {"Oper"})
    names.reset()
    trace.OUT(text, "The LLVM function implementing B operation \""+n["id"]+"\" in \""+n["root"]["id"]+"\" follows.")
    text.extend("define void "+op_name(n))
    text.extend("("+commas([state_r_name(n["root"])+sp+"%self$"]+
                          [x_type(i["type"])+sp+"%"+i["id"] for i in n["inp"]]+
                          [x_type(o["type"])+"*"+sp+"%"+o["id"] for o in n["out"]])+")")
    text.extend("{"+nl)
    trace.TAB()
    text.extend("entry:"+nl)
    x_alloc_inst(text, n["body"])
    x_inst_label(text, n["body"], "exit")
    text.extend("exit:"+nl)
    text.extend(tb+"ret void"+nl)
    text.extend("}"+nl)
    trace.UNTAB()

### TRANSLATION OF STACK VARIABLE ALLOCATION

def x_alloc_inst_list(text, il):
    '''
    Generation of frame stack allocation for instruction lists.

    Input:
      - text: a bytearray where LLVM code is stored
      - il: a list of B instructions AST nodes

    This function is part of a recursive traversal of the syntax tree so that
    all variable declarations are visisted and handled by function
    x_alloc_var_decl.
    '''
    for inst in il:
        x_alloc_inst(text, inst)

def x_alloc_inst(text, n):
    '''
    Generation of frame stack allocation for individual instructions.
    
    Input:
      - text: a byterray where LLVM code is stored
      - n: AST node for a B instruction

    This function is part of a recursive traversal of the syntax tree so that
    all variable declarations are visisted and handled by function
    x_alloc_var_decl.
    '''
    check_kind(n, {"Beq", "Blk", "Call", "Case", "If", "Skip", "VarD", "While"})
    if n["kind"] in {"Beq", "Call", "Skip"}:
        return
    elif n["kind"] in {"Case", "If"}:
        for br in n["branches"]:
            x_alloc_inst(text, br["body"])
    elif n["kind"] in {"Blk", "While"}: 
        x_alloc_inst_list(text, n["body"])
    elif n["kind"] == "VarD":
        x_alloc_var_decl(text, n)
    else:
        print("error: unknown instruction kind")
        res.extend("<error inserted by b2llvm>")
    
def x_alloc_var_decl(text, n):
    '''
    Generation of frame stack allocation for variable declarations.
    
    Input:
      - text: a byterray where LLVM code is stored
      - n: AST node for a B variable declaration

    Emits one LLVM alloca instruction for each declared variable and 
    processes the variable declaration body of instructions.
    '''
    global tb, nl, sp
    check_kind(n, {"VarD"})
    trace.OUT(text, "local variable declarations implemented as frame stack allocations")
    trace.TAB()
    for v in n["vars"]:
        trace.OUT(text, "frame stack allocation for variable "+v["id"])
        text.extend(tb+"%"+v["id"]+" = alloca "+x_type(v["type"])+nl)
    x_alloc_inst_list(text, n["body"])
    trace.UNTAB()

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

def x_inst_list_label(text, l, lbl):
    global tb, nl
    if len(l) == 0:
        text.extend(tb + "br label %" + lbl + nl)
    else:
        i = l[0]
        l2 = l[1:]
        if i["kind"] in {"Case", "If", "While"}:
            lbl2 = names.new_label()
            x_inst_label(res, i, lbl2)
            text.extend(lbl2 + ":\n")
        elif i["kind"] in {"Blk"}:
            x_inst_list(text, i["body"])
        else:
            x_inst(text, i)
        x_inst_list_label(text, l2, lbl)

def x_inst_list(text, il):
    '''
    Input:
      - text: bytearray to store LLVM code
      - il: list of instruction AST nodes
    '''
    for inst in il:
        if inst["kind"] in {"If", "While"}:
            label = names.new_label()
            x_inst_label(text, inst, label)
            text.extend(label + ":\n")
        elif inst["kind"] in {"Blk"}:
            x_inst_list(text, inst["body"])
        else:
            x_inst(text, inst)

def x_inst_label(text, n, lbl):
    check_kind(n, {"Beq", "Blk", "Call", "Case", "If", "VarD", "While"})
    if n["kind"] == "Blk":
        x_inst_list_label(text, n["body"], lbl)
    elif n["kind"] == "Case":
        x_case(text, n, lbl)
    elif n["kind"] == "If":
        x_if(text, n, lbl)
    elif n["kind"] == "While":
        x_while(text, n, lbl)
    elif n["kind"] in {"Beq", "Call"}:
        x_inst(text, n)
        text.extend(tb + "br label %" + lbl + nl)
    elif n["kind"] == "VarD":
        x_inst_list_label(text, n["body"], lbl)
    else:
        print("error: instruction type unknown")
        text.extend("<error inserted by b2llvm>")

def x_inst(text, n):
    check_kind(n, {"Beq", "Call", "VarD"})
    if n["kind"] == "Beq":
        x_beq(text, n)
    elif n["kind"] == "Call":
        x_call(text, n)
    elif n["kind"] == "VarD":
        x_inst_list(text, n["body"])
    elif n["kind"] == "Skip":
        x_skip(text, n)

### TRANSLATION OF SKIP ###

def x_skip(text, n):
    check_kind(n, {"Skip"})

### TRANSLATION OF CASE INSTRUCTIONS

def x_case(text, n, lbl):
    '''
    Generates LLVM code for a B case instruction.

    Input:
      - text: a byterray where LLVM code is stored
      - n: an AST node representing a B instruction
      - lbl: a LLVM label for the block where control flow must go after
      executing n.
    '''
    global nl, tb, sp
    check_kind(n, {"Case"})
    v,t = x_expression(text, n["expr"])
    branches = n["branches"]
    # generate one block label for each branch
    labels = x_case_label_list(branches)
    # there is a special treatment for in case there is no explicit
    # default branch (the last branch in the AST is not a default branch)
    last = branches(len(branches)-1)
    default = "val" not in br.keys() or br["val"] == [] or br["val"] == None
    # generate block label for default branch
    if default:
        lblo = labels[len(branches)-1]
    else:
        lblo = names.new_label()
    text.extend(tb + "switch " + t + sp + v + ", label %" + lblo + " [" + nl)
    x_case_jump_table(text, branches, labels)
    text.extend(tb + "]" + nl)
    text.extend(x_case_block_list(branches, labels, default, lblo))

def x_case_label_list(bl):
    '''
    Input:
      - bl: list of case branches
    Output:
      - list of LLVM block labels, one for each non-default branch
    '''
    return [ names.new_label() for branch in bl]

def x_case_jump_table(text, bl, labels):
    ''' 
    Generates a LLVM jump table for a switch instruction implementing the case
    branches.

    Input:
      - text: a bytearray where LLVM output is stored
      - bl: a list of case branches
      - labels: a list block labels
    '''
    for i in range(len(bl)):
        x_case_val_list(text, bl[i]["val"], labels[i])

def x_case_val_list(text, vl, lbl):
    '''
    Generates entries in the LLVM jump table from values to a block label.

    Input:
      - text: a bytearray where output is stored
      - vl: a list of AST nodes representing B values
      - lbl: a LLVM block label
    '''
    global tb2, sp, nl
    text2 = bytearray()
    for v in vl:
        # the evaluation of the values should not emit LLVM code
        v, t = x_expression(text2, v)
        assert(len(text2) == 0)
        text.extend(tb2 + t + sp + v + ", label %" + lbl + nl)

def x_case_block_list(text, bl, labels, lble, default, lbld):
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
    '''
    for i in range(len(bl)):
        branch = bl[i]
        lbl = labels[i]
        text.extend(tb+lbl+":"+nl)
        text.extend(x_inst_label(branch["body"], lble))
    if not default:
        text.extend(tb+lbld+":"+nl)
        text.extend(tb+"branch label %"+lble)

### TRANSLATION OF IF INSTRUCTIONS

def x_if(text, n, lbl):
    '''
    Generates LLVM code for a B if instruction.

    Input:
      - text: a byterray where LLVM code is stored
      - n: an AST node representing a B if instruction
      - lbl: a LLVM label for the block where control flow must go after
      executing n.
    '''
    check_kind(n, {"If"})
    trace.OUT(text, "Execute \""+ellipse(printer.subst_if(0, n))+"\" and branch to \""+lbl+"\".")
    trace.TAB()
    x_if_br(text, n["branches"], lbl)
    trace.UNTAB()

def x_if_br(text, lbr, lbl):
    '''
    Generates LLVM code for a list of B if instruction branches.

    Input:
      - text: a byterray where LLVM code is stored
      - lbr: a list of AST nodes representing B if instruction branches
      - lbl: a LLVM label for the block where control flow must go after
      executing n.
    '''
    nbr = len(lbr)
    assert(nbr>=1)
    for i in range(nbr):
        br = lbr[i]
        check_kind(br, {"IfBr"})
        trace.OUT(text, "execute if branch \""+ellipse(printer.if_br(0, 0, br))+"\"")
        if i == nbr-1:
            # br is an else branch
            if "cond" not in br.keys() or br["cond"] == None:
                x_inst_label(text, br["body"], lbl)
            # br is an elsif branch
            else:
                lbl_1 = names.new_label()
                x_formula(text, br["cond"], lbl_1, lbl)
                text.extend(lbl_1 + ":" + nl)
                x_inst_label(text, br["body"], lbl)
        else:
            lbl_1 = names.new_label()
            lbl_2 = names.new_label()
            x_formula(text, br["cond"], lbl_1, lbl_2)
            text.extend(lbl_1 + ":" + nl)
            x_inst_label(text, br["body"], lbl)
            text.extend(lbl_2 + ":" + nl)

### TRANSLATION OF WHILE INSTRUCTIONS

def x_while(text, n, lbl):
    '''
    Generates LLVM code for a B while instruction.

    Input:
      - text: a byterray where LLVM code is stored
      - n: an AST node representing a B while instruction
      - lbl: a LLVM label for the block where control flow must go after
      executing n.
    '''
    global nl, tb, sp
    check_kind(n, {"While"})
    trace.OUT(text, "Execute \""+ellipse(printer.subst_while(0, n))+"\" and branch to \""+lbl+"\".")
    trace.TAB()
    trace.OUT(text, "Evaluate loop guard \""+ellipse(printer.condition(n["cond"]))+"\".")
    lbl1 = names.new_label()
    text.extend(tb+"br label %"+lbl1+nl)
    text.extend(lbl1 + ":" + nl)
    v = x_pred(text, n["cond"])
    lbl2 = names.new_label()
    text.extend(tb + "br i1 " + v + ", label %" + lbl2 + ", label %" + lbl + nl)
    trace.OUT(text, "Execute loop body \""+ellipse(printer.subst_l(0, n["body"]))+"\".")
    text.extend(lbl2 + ":" +nl)
    x_inst_list_label(text, n["body"], lbl1)
    trace.UNTAB()

### TRANSLATION OF BECOMES EQUAL INSTRUCTIONS

def x_beq(text, n):
    '''
    Generates LLVM code for a B assignment (becomes equal) instruction.

    Input:
      - text: a byterray where LLVM code is stored
      - n: an AST node representing a B assignment instruction
    '''
    global tb, sp, nl
    check_kind(n, {"Beq"})
    trace.OUT(text, "Execute assignment \""+printer.beq(0, n)+"\":")
    trace.TAB()
    v,t = x_expression(text, n["rhs"])
    p,_ = x_lvalue(text, n["lhs"])
    trace.OUT(text, "Store value at address to achieve assignment.")
    text.extend(tb + "store " + t + sp + v + ", " + t + "* " + p + nl)
    trace.UNTAB()

def x_lvalue(text, n):
    '''
    Translate of "lvalues" (elements to the left of an assignment).

    Input:
      - n: AST node for lvalue
    Output:
      A triple composed of a sequence of LLVM instructions computing
      the lvalue, the name of the local storing the lvalue, and the
      type of the lvalue.
    Note:
      Used to translate assignments and operation calls with output(s).
    Caveat:
      Currently limited to simple identifiers.
    '''
    global tb, nl
    check_kind(n, {"Vari"})
    trace.OUT(text, "Evaluate address for \""+printer.term(n)+"\".")
    t = x_type(n["type"]) + "*"
    if n["scope"] == "Impl":
        pos=state_position(n)
        v = names.new_local()
        trace.TAB()
        trace.OUT(text, "Variable \""+n["id"]+"\" is stored at position "+str(pos)+" of \"%self$\".")
        trace.OUTU(text, "Let temporary " + v + " be the corresponding address:")
        trace.UNTAB()
        text.extend(tb + v + " = getelementptr " + state_r_name(n["root"])+ 
                    " %self$, i32 0, i32 " + str(state_position(n)) + nl)
        return (v, t)
    elif n["scope"] in {"Oper", "Local"}:
        trace.TAB()
        trace.OUT(text, "\""+n["id"]+"\" is stored in the frame stack and represented by \"%"+n["id"]+"\".")
        trace.UNTAB()
        return ("%"+n["id"],t)
    else:
        text.extend("<error inserted by b2llvm>")
        print("error: unknown scope for variable " + v["id"])
        return ("UNKNOWN", "UNKNOWN")

### TRANSLATION OF CALL INSTRUCTIONS

def x_call(text, n):
    '''
    Generates LLVM code for a B call operation instruction.

    Input:
      - text: a byterray where LLVM code is stored
      - n: an AST node representing a B call operation
    '''
    global sp
    check_kind(n, {"Call"})
    trace.OUT(text, "Execute operation call \""+printer.call(0, n)+"\".")
    operation = n["op"]
    local = (n["inst"] == None) # is a local operation?
    impl = operation["root"]
    # evaluate arguments
    trace.TAB()
    trace.OUT(text, "Evaluate operation arguments.")
    args = list()
    trace.TAB()
    if is_stateful(impl):
        trace.OUT(text, "(implicit) address of structure representing operation component")
        # get the LLVM type of the machine offering the operation
        if local:
            mach = operation["root"]
        else:
            mach = n["inst"]["root"]
        mach_t = state_r_name(mach)
        if local:
            t = selftype
            v = "%self$"
            trace.OUT(text, "is %self$")
        else:
            pos = state_position(n["inst"])
            trace.OUT(text, "is element "+str(pos)+" of %self$")
            t = state_r_name(n["inst"]["mach"])
            v1 = names.new_local()
            v2 = names.new_local()
            text.extend(tb+v1+" = getelementptr "+mach_t+
                        " %self$, i32 0, i32 "+str(pos)+nl)
            text.extend(tb + v2 + " = load " + t +"*" + sp + v1 + nl)
        args.append(t + sp + v2)
    x_inputs(text, args, n["inp"])
    x_outputs(text, args, n["out"])
    trace.UNTAB()
    id = op_name(operation)
    trace.OUT(text, "Call LLVM function \""+id+"\" implementing B operation \""+n["op"]["id"]+"\".")
    text.extend(tb + "call void" + sp + id + "(" + commas(args) + ")" + nl)
    trace.UNTAB()

def x_inputs(text, args, n):
    global sp
    for elem in n:
        trace.OUT(text, "Evaluate input parameter \""+printer.term(elem)+"\".")
        v,t = translate_expression(text, elem)
        args.append(t + sp + v)

def x_outputs(text, args, n):
    global sp
    for elem in n:
        trace.OUT(text, "Evaluate output parameter \""+printer.term(elem)+"\".")
        v,t = x_lvalue(text, elem)
        args.append(t + sp + v)

### TRANSLATION OF CONDITIONS ###

def x_formula(text, n, lbl1, lbl2):
    '''
    Generates LLVM code to evaluate a B formula and branch to either labels.

    Input:
      - text: a byterray where LLVM code is stored
      - n: an AST node representing a B formula.
      - lbl1: a LLVM label string
      - lbl2: a LLVM label string
    '''
    check_kind(n, {"Comp", "Form"})
    trace.OUT(text, "Evaluate formula \""+ellipse(printer.condition(n))+"\", branch to \""+lbl1+"\" if true, to \""+lbl2+"\" otherwise.")
    trace.TAB()
    if n["kind"] == "Comp":
        v = x_comp(text, n)
        text.extend(tb+"br i1 "+v+" , label %"+lbl1+", label %"+lbl2+nl)
    elif n["kind"] == "Form":
        if n["op"] == "and":
            x_and(text, n, lbl1, lbl2)
        elif n["op"] == "or":
            x_or(text, n, lbl1, lbl2)
        elif n["op"] == "not":
            x_not(text, n, lbl1, lbl2)
        else:
            text.extend("<error inserted by b2llvm>")
    else:
        text.extend("<error inserted by b2llvm>")
    trace.UNTAB()

def x_comp(text, n):
    '''
    Generates LLVM code to evaluate a B comparison.

    Input:
      - text: a byterray where LLVM code is stored.
      - n: an AST node representing a B comparison.
    Output:
      The identifier of the LLVM temporary variable storing the result of
      the comparison. This variable has type "i1".
    '''
    global tb, sp, nl
    check_kind(n, {"Comp"})
    v1,t1 = x_expression(text, n["arg1"])
    v2,t2 = x_expression(text, n["arg2"])
    v = names.new_local()
    trace.OUT(text, "Temporary \""+v+"\" gets the value of \""+ellipse(printer.comp(n))+"\".")
    text.extend(tb+v+" = icmp "+llvm_op(n["op"])+sp+t1+sp+v1+", "+v2+nl)
    return v

def x_and(text, n, lbl1, lbl2):
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
    trace.OUT(text, "Evaluate conjunction \""+ellipse(printer.condition(n))+"\", branch to \""+lbl1+"\" if true, to \""+lbl2+"\" otherwise.")
    trace.TAB()
    trace.OUT(text, "Create a fresh label \""+lbl+"\".")
    x_formula(text, arg1, lbl, lbl2)
    text.extend(lbl + ":" + nl)
    x_formula(text, arg2, lbl1, lbl2)
    trace.UNTAB()

def x_or(text, n, lbl1, lbl2):
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
    trace.OUT(text, "Evaluate disjunction \""+ellipse(printer.condition(n))+"\", branch to \""+lbl1+"\" if true, to \""+lbl2+"\" otherwise.")
    trace.TAB()
    trace.OUT(text, "Create a fresh label \""+lbl+"\".")
    x_formula(text, arg1, lbl1, lbl)
    text.extend(lbl + ":" + nl)
    x_formula(text, arg2, lbl1, lbl2)
    trace.UNTAB()

def x_not(text, n, lbl1, lbl2):
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
    trace.OUT(text, "Evaluate negation \""+ellipse(printer.condition(n))+"\", branch to \""+lbl1+"\" if true, to \""+lbl2+"\" otherwise.")
    trace.TAB()
    trace.OUT(text, "Create a fresh label \""+lbl+"\".")
    x_formula(text, n["args"][0], lbl2, lbl1)
    trace.UNTAB()

def x_pred(text, n):
    if n["kind"] == "Comp":
        return x_comp(text, n)
    else:
        text.extend("<error inserted by b2llvm>")
        return ""

### TRANSLATION OF EXPRESSIONS ###

def x_expression(text, n):
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
    trace.OUT(text, "Evaluate expression \""+ellipse(printer.term(n))+"\".")
    trace.TAB()
    if n["kind"] == "IntegerLit":
        res = x_integerlit(text, n), "i32"
    elif n["kind"] == "BooleanLit":
        res = x_booleanlit(text, n), "i1"
    elif n["kind"] == "Vari":
        res = x_name(text, n)
    elif n["kind"] == "Term":
        res = x_term(text, n)
    elif n["kind"] == "Cons":
        res = x_expression(text, n["value"])
    else:
        res = ("","")
    trace.UNTAB()
    trace.OUTU(text, "The evaluation of \""+ellipse(printer.term(n))+"\" is \""+res[0]+"\".")
    return res

def x_integerlit(text, n):
    '''
    Generates LLVM code to evaluate a B integer literal.

    Input:
      - text: a byterray where LLVM code is stored.
      - n: an AST node representing a B integer literal.
    Output:
      A string of the integer literal value.
    '''
    check_kind(n, {"IntegerLit"})
    trace.OUT(text, "An integer literal is represented as such in LLVM.")
    return n["value"]

def x_booleanlit(text, n):
    '''
    Generates LLVM code to evaluate a B boolean literal.

    Input:
      - text: a byterray where LLVM code is stored.
      - n: an AST node representing a B integer literal.
    Output:
      A string of the LLVM boolean literal value, i.e. "1" or "0".
    '''
    check_kind(n, {"BooleanLit"})
    trace.OUT(text, "A Boolean literal is represented as a one-bit integer in LLVM.")
    return "1" if n["value"] == "TRUE" else "0"

def x_name(text, n):
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
        trace.OUT(text, "B local variable \""+bvar+"\" is on the LLVM stack at address \""+lvar+"\".")
        trace.OUT(text, "Temporary \""+v2+"\" gets the contents from this position.")
        text.extend(tb + v2 + " = load" + sp + ltype + "*" + sp + lvar + nl)
        lvar = v2
    elif n["scope"] == "Oper":
        trace.OUT(text, "Operation parameter \""+n["id"]+"\" is LLVM parameter \"%"+n["id"]+"\".")
        lvar = "%"+bvar
    elif n["scope"] == "Impl":
        lptr = names.new_local()
        lvar = names.new_local()
        pos = str(state_position(n))
        trace.OUT(text, "State variable \""+bvar+"\" is stored at position \""+pos+"\" of \"%self$\".")
        trace.OUT(text, "Let temporary \""+lptr+"\" be the corresponding address.")
        text.extend(tb+lptr+" = getelementptr "+state_t_name(n["root"])+" %self$, i32 0, i32 "+pos+nl)
        text.extend(tb+lvar+" = load "+ltype+"* "+lptr+nl)
    else:
        text.extend("<error inserted by b2llvm>")
        lvar, type = "", ""
    return (lvar, ltype)
        
def x_term(text, n):
    '''
    Generates LLVM code to evaluate a B term.

    Input:
      - text: a byterray where LLVM code is stored.
      - n: an AST node representing a B term.
    Output:
      A pair containing, the identifier of the LLVM variable storing the value
      of the B term, and the LLVM type of this value.
    '''
    global tb, sp, nl
    check_kind(n, {"Term"})
    v1,t = x_expression(text, n["args"][0])
    if n["op"] == "succ" or n["op"] == "pred":
        v2 = "1"
    else:
        assert(len(n["args"]) == 2)
        v2,_ = x_expression(text, n["args"][1])
    v = names.new_local()
    trace.OUT(text, "Let temporary \""+v+"\" get the value of \""+ellipse(printer.term(n))+"\".")
    text.extend(tb + v + " = " + llvm_op(n["op"]) + sp + t + sp + v1 + ", " + v2 + nl)
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

def state_opaque_typedef(res, m):
    '''
    Input:
      - res: bytearray to store output
      - m: represents a B machine
    Desc:
      Appends to res the LLVM definition of type pointer to type representing the
      state of n.
      This only makes sense if n is stateful.
    '''
    global nl
    trace.OUT(res, "The state encoding type for module \""+m["id"]+"\" is defined elsewhere:")
    res.extend(state_t_name(m) + " = type opaque" + nl)

def state_ref_typedef(res, m):
    '''
    Input:
      - res: bytearray to store output
      - m: represents a B machine
    Desc:
      Adds to res the LLVM definition of type pointer to type representing the
      state of n.
      This only makes sense if n is stateful.
    '''
    global nl
    trace.OUT(res, "The type for references to state encodings of \""+m["id"]+"\" is:")
    res.extend(state_r_name(m) + " = type " + state_t_name(m) + "*" + nl)

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

