#!/bin/bash

# This script takes a directory of .txt files and creates corresponding .ogg files for each of the text files it finds.

for f in /fileshare/textfiles/*.txt
do
	filename=$(basename "$f")
	extension="${filename##*.}"
	filename="${filename%.*}"
	
	espeak --stdout -f $f > "$filename.wav"
	oggenc -q 6 "$filename.wav" -o "/fileshare/$filename.ogg"
done