#
# This is a crude script to generate coverage data from the set of benchmarks
# that we currently have.
# It relies on the installation of the Python script "coverage"
# https://bitbucket.org/ned/coveragepy
#
#!/bin/bash
COV_RUN="coverage run --source=b2llvm.py,b2llvm -p"
echo "Cleaning up existing coverage data."
coverage erase
echo "   Generating Calculator"
$COV_RUN ./b2llvm.py -m comp Calculator Calculator_i.llvm bxml project.xml
$COV_RUN ./b2llvm.py -m proj Calculator init-Calculator.llvm bxml project.xml

# Simple example BETA
#echo "Calendar"

#$COV_RUN ./b2llvm.py --verbose  -m comp Calendar Calendar.llvm bxml project.xml
#$COV_RUN ./b2llvm.py --verbose  -m skeleton Calendar Calendar.llvm bxml project.xml

# Simple example BETA
#echo " Sort"
#$COV_RUN ./b2llvm.py --verbose  -m skeleton Sort Sort.llvm bxml project.xml
#$COV_RUN ./b2llvm.py --verbose  -m comp Sort Sort.llvm bxml project.xml
#$COV_RUN ./b2llvm.py -m proj BubbleSort init-BubbleSort.llvm bxml project.xml
#echo "END BUBBLE NEW"


echo "   Generating DIVISION"
$COV_RUN ./b2llvm.py --trace -m comp Division Division.llvm bxml project.xml
$COV_RUN ./b2llvm.py -m proj Division init-Division.llvm bxml project.xml
echo "   Generating Prime"
$COV_RUN ./b2llvm.py --trace -m comp  Prime Prime.llvm bxml project.xml
$COV_RUN ./b2llvm.py --trace -m proj Prime init-Prime.llvm bxml project.xml
echo "   Generating bubble "
$COV_RUN ./b2llvm.py --trace -m comp  bubble bubble.llvm bxml project.xml
$COV_RUN ./b2llvm.py --trace -m proj bubble init-bubble.llvm bxml project.xml

#echo " Rooms"
#$COV_RUN ./b2llvm.py -m comp Rooms  Rooms.llvm bxml project.xml
#$COV_RUN ./b2llvm.py -m proj Rooms init-Rooms.llvm bxml project.xml

echo "   Generating swap "
$COV_RUN ./b2llvm.py --trace -m comp swap swap.llvm bxml project.xml
$COV_RUN ./b2llvm.py --trace -m proj swap init-swap.llvm bxml project.xml


echo "   Generating counter"
$COV_RUN ./b2llvm.py --trace -m comp counter counter.llvm bxml project.xml > /dev/null
$COV_RUN ./b2llvm.py --trace -m proj counter init-counter.llvm bxml project.xml
echo "   Generating enumeration"
$COV_RUN ./b2llvm.py --trace -m comp enumeration enumeration.llvm bxml project.xml
$COV_RUN ./b2llvm.py --trace -m proj enumeration init-enumeration.llvm bxml project.xml

#echo "\nGenerating array example"
#$COV_RUN ./b2llvm.py -m comp array array.llvm bxml project.xml
##$COV_RUN ./b2llvm.py -p -t -m proj array array.llvm bxml project.xml
#echo "Generated code!"

##$COV_RUN ./b2llvm.py -m comp ioint ioint.llvm bxml project.xml
##$COV_RUN ./b2llvm.py -t -m comp ioint ioint.llvm bxml project.xml

echo "   Generating WD"
$COV_RUN ./b2llvm.py -m comp wd wd.llvm bxml project.xml
$COV_RUN ./b2llvm.py -m proj wd init-wd.llvm bxml project.xml
echo "   Generating timer"
$COV_RUN ./b2llvm.py -m comp timer timer.llvm bxml project.xml
$COV_RUN ./b2llvm.py -m proj timer init-timer.llvm bxml project.xml

echo "   Generating Body"
$COV_RUN ./b2llvm.py -m comp Body Body_i.llvm bxml project.xml
$COV_RUN ./b2llvm.py -m proj Body init-Body_i.llvm bxml project.xml

echo "   Generating Multiplication"
$COV_RUN ./b2llvm.py -m comp Multiplication MultiplicationI.llvm bxml project.xml
$COV_RUN ./b2llvm.py -m proj Multiplication init-MultiplicationI.llvm bxml project.xml


echo "   Generating Team2"
$COV_RUN ./b2llvm.py -m comp Team2 Team2.llvm bxml project.xml
$COV_RUN ./b2llvm.py -m proj Team2 init-Team2.llvm bxml project.xml

echo "   Generating TicTacToe"
$COV_RUN ./b2llvm.py -m comp TicTacToe TicTacToe.llvm bxml project.xml
$COV_RUN ./b2llvm.py -m proj TicTacToe init-TicTacToe.llvm bxml project.xml

echo "   Generating MOD_Varray"
$COV_RUN ./b2llvm.py -m comp MOD_Varray MOD_Varray.llvm bxml project.xml
$COV_RUN ./b2llvm.py -m proj MOD_Varray init-MOD_Varray.llvm bxml project.xml

echo "   Generating MOD_PositionCounter"
$COV_RUN ./b2llvm.py -m comp TicTacToe MOD_PositionCounter.llvm bxml project.xml
$COV_RUN ./b2llvm.py -m proj TicTacToe init-MOD_PositionCounter.llvm bxml project.xml

echo "   Generating MOD_SizeCounter"
$COV_RUN ./b2llvm.py -m comp MOD_SizeCounter MOD_SizeCounter.llvm bxml project.xml
$COV_RUN ./b2llvm.py -m proj MOD_SizeCounter init-MOD_SizeCounter.llvm bxml project.xml



echo "Combining coverage data."
coverage combine
echo "Generating coverage report."
coverage html -d coverage_html
open coverage_html/index.html
echo "Coverage report is now available."


echo "Generating diff report "
for file in *.h *.llvm; do diff "$file" "expected_code/${file##*/}">expected_code/REPORT_"$file".diff; echo "Diff for ${file##*/}:"; cat expected_code/REPORT_"$file".diff;   done
find expected_code -size -1c -name "*.diff" -exec rm -f {} \;
echo "Report generated"



