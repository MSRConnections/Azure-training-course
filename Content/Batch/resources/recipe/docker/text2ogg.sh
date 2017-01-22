#!/bin/bash

# This script takes a directory of .txt files and creates corresponding .ogg files for each of the text files it finds.

while [ -n "$(ls -A /fileshare/textfiles/*.txt)" ]
do
	files=(/fileshare/textfiles/*.txt)
	f="${files[0]}"
	filename=$(basename "$f")
	extension="${filename##*.}"
	filename="${filename%.*}"
	
	echo "Processing: $f"
	
	mv $f "/$filename.txt"
	
	espeak --stdout -f "/$filename.txt" > "$filename.wav"
	oggenc -q 6 "$filename.wav" -o "/fileshare/$filename.ogg"
	
done