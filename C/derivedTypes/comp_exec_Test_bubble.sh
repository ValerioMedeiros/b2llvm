# Before you must generate the bubble.llvm by this command:
# ./b2llvm.py -v -m comp counter bubble.llvm bxml project.xml
cp ../../bubble.llvm .
cp ../../bubble.h .
clang -S -emit-llvm -c initc-bublle.c
llc-mp-3.5  bubble.llvm
llc-mp-3.5  initc-bublle.ll
clang -o executable bubble.llvm.s  initc-bublle.s
./executable 
