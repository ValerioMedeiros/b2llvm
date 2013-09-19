#!/usr/bin/python
import argparse
from b2llvm.translate import translate_bxml

progdescription='Generates LLVM code for a B implementation. The code contains a type declaration, corresponding to the implementation state, and function declarations corresponding to the initialization as well as the operations. Optionally, the generator includes a declaration of a global variable holding the machine state (option --top).'
parser = argparse.ArgumentParser(description=progdescription)
parser.add_argument('bxml_file', help='input BXML file name')
parser.add_argument('llvm_file', help='output LLVM file name')
parser.add_argument('-t', '--top', action='store_true', help='LLVM shall construct an instance of the component (do not set to generate code for library machines)')

args = parser.parse_args()
translate_bxml(args.bxml, args.llvm, args.top)
print("b2llvm code generation completed")
print("- input: " + args.bxml_file)
print("- output: " + args.llvm_file)
print("- mode: " + ("top-level" if args.top else "library machine"))
