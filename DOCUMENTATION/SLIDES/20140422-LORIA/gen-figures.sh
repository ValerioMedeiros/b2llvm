# This script crops the generated PDFs
# It uses cpdf from http://community.coherentpdf.com
#!/bin/bash

alias CPDF=cpdf-binaries-master/OSX-Intel/cpdf  

dx="4mm"
dy="6mm"
width="60mm"

file="inc_llvm.pdf"
make -s $file
CPDF -crop "$dx $dy $width 32mm" $file -o tmp.pdf 2> /dev/null
CPDF -frombox /CropBox -tobox /MediaBox tmp.pdf -o x_$file 2> /dev/null
echo "x_$file generated"

width="40mm"
file="inc_c.pdf"
make -s $file
CPDF -crop "$dx $dy $width 20mm" $file -o tmp.pdf 2> /dev/null
CPDF -frombox /CropBox -tobox /MediaBox tmp.pdf -o x_$file 2> /dev/null
echo "x_$file generated"

dx="0mm"
width="120mm"

file="count_i.pdf"
make -s $file
CPDF -crop "$dx $dy $width 33mm" $file -o tmp.pdf 2> /dev/null
CPDF -frombox /CropBox -tobox /MediaBox tmp.pdf -o x_$file 2> /dev/null
echo "x_$file generated"

file="count_i_llvm_typedef.pdf"
make -s $file
CPDF -crop "$dx $dy $width 7mm" $file -o tmp.pdf 2> /dev/null
CPDF -frombox /CropBox -tobox /MediaBox tmp.pdf -o x_$file 2> /dev/null
echo "x_$file.pdf generated"

file="count_i_llvm_interface.pdf"
make -s $file
CPDF -crop "$dx $dy $width 16mm" $file -o tmp.pdf 2> /dev/null
CPDF -frombox /CropBox -tobox /MediaBox tmp.pdf -o x_$file 2> /dev/null
echo "x_$file generated"

file="count_i_llvm_implementation.pdf"
make -s $file
CPDF -crop "$dx $dy $width 114mm" $file -o tmp.pdf 2> /dev/null
CPDF -frombox /CropBox -tobox /MediaBox tmp.pdf -o x_$file 2> /dev/null
echo "x_$file generated"

file="wd_i.pdf"
make -s $file
CPDF -crop "$dx $dy $width 60mm" $file -o tmp.pdf 2> /dev/null
CPDF -frombox /CropBox -tobox /MediaBox tmp.pdf -o x_$file 2> /dev/null
echo "x_$file generated"

file="wd_i_llvm_typedef.pdf"
make -s $file
CPDF -crop "$dx $dy $width 7mm" $file -o tmp.pdf 2> /dev/null
CPDF -frombox /CropBox -tobox /MediaBox tmp.pdf -o x_$file 2> /dev/null
echo "x_$file generated"

file="wd_i_llvm_implementation.pdf"
make -s $file
CPDF -crop "$dx $dy $width 139mm" $file -o tmp.pdf 2> /dev/null
CPDF -frombox /CropBox -tobox /MediaBox tmp.pdf -o x_$file 2> /dev/null
echo "x_$file generated"

file="wd_llvm_main.pdf"
make -s $file
CPDF -crop "$dx $dy $width 40mm" $file -o tmp.pdf 2> /dev/null
CPDF -frombox /CropBox -tobox /MediaBox tmp.pdf -o x_$file 2> /dev/null
echo "x_$file generated"

file="with_trace.pdf"
make -s $file
CPDF -crop "$dx $dy $width 40mm" $file -o tmp.pdf 2> /dev/null
CPDF -frombox /CropBox -tobox /MediaBox tmp.pdf -o x_$file 2> /dev/null
echo "x_$file generated"

