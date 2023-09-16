#!/bin/bash

read -p "Enter your Roll No: " ROLL_NO

rm "$ROLL_NO"
mkdir "$ROLL_NO"
cp Q1/Q1* ./"$ROLL_NO"/
cp Q2/Q2* ./"$ROLL_NO"/
cp Q3/Q3* ./"$ROLL_NO"/

zip -r "$ROLL_NO".zip ./"$ROLL_NO" > trash.txt

rm -r "$ROLL_NO"
rm trash.txt
mv "$ROLL_NO".zip "$ROLL_NO"