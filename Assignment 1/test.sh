#!/bin/bash

read -p "Enter your roll no: " ROLL_NO


mkdir test
mkdir test3
unzip "$ROLL_NO".zip -d test/ > trash.txt
cp -r Q* test/
cp -r test/"$ROLL_NO"/Q1* test/Q1/ 
cp -r test/"$ROLL_NO"/Q2* test/Q2/ 
cp -r test/"$ROLL_NO"/Q3* test/Q3/ 

echo "####### Question 1 #######"
cd test/Q1
# pwd
python3 tester1.py
cat marks.csv

echo "####### Question 2 #######"
cd ../Q2
# pwd
python3 tester2.py
cat marks.csv

echo "####### Question 3 #######"
cd ../Q3
python3 tester3.py

cp -r "$ROLL_NO" ../../test3/

cd ../..
rm -r test
rm trash.txt

