

# Update the files generated from AtelierB
cp /media/B_Resources/Timer2/bdp/array*.bxml ../../bxml/
cp /media/B_Resources/Timer2/src/array*.mch  ../../examples/
cp /media/B_Resources/Timer2/src/array*.imp  ../../examples/

# Update the files here
cp ../../array* .
# Run the B2LLVM
cd ../..
./coverage.sh
cd C/derivedTypes

#Compile and Run
clang -S -emit-llvm -c initc-array.c
llc-mp-3.5  array.llvm
llc-mp-3.5  initc-array.ll
clang -o executable array.llvm.s  initc-array.s
#./executable

# TODO: Put everything organized in Makefile!!!