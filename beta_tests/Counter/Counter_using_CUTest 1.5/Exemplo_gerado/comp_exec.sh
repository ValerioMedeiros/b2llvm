# Before you must generate the counter.llvm by this command:
# ./b2llvm.py -v -m comp counter counter.llvm bxml project.xml
clang -S -emit-llvm -c CuTest.c AllTests.c
llc-mp-3.5  counter.llvm
llc-mp-3.5  CuTest.ll 
llc-mp-3.5  AllTests.ll
clang -o executable counter.llvm.s  CuTest.s AllTests.s
./executable 
