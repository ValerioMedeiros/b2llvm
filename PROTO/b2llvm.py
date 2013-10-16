#!/usr/bin/python
import argparse
from b2llvm.translate import translate_bxml

progdescription='Generates LLVM code for a B module. In component mode, the generator produces type and function definitions corresponding to the state and operations of a given developed machine. In project mode, the generator instantiates the given module and all the instances of imported modules, and defines a function to link these modules and initialize their execution.'
parser = argparse.ArgumentParser(description=progdescription)
parser.add_argument('b_module', 
                    help='name of the B module (machine)')
parser.add_argument('llvm_file', 
                    help='output LLVM file name')
parser.add_argument('directory', 
                    help='when set, the program will lookup files in that directory')
parser.add_argument('settings', 
                    help='project settings file')
parser.add_argument('-m', '--mode', choices=['comp','proj'], default='comp', 
                    help='Selects code generation mode.')

args = parser.parse_args()
if args.comp and args.proj:
    print("error: choose only one code generation mode.")
elif not args.comp and not args.proj:
    print("error: choose one code generation mode")
else:
    translate_bxml(b_module, args.llvm_file, mode=args.mode, 
                   dirname=args.directory, settings=args.settings)
    print("b2llvm code generation completed")
    print("- input: " + args.bxml_file)
    print("- output: " + args.llvm_file)
    print("- mode: " + ("top-level" if args.top else "library machine"))
