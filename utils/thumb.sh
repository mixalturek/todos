#!/bin/bash
#
# Copyright (C) 2009 Michal Turek
# License: GNU GPL v2
#
# Generates web gallery from images in the current directory

echo '<div class="screenshots">'

mkdir -p out

for file in *.jpg
do
	name=`echo ${file} | cut -f1 -d.`
	convert ${file} -resize 200x200 -quality 95 out/${name}_sm.jpg
	# echo "<div><a href=\"images/screenshots/$file\"><img src=\"images/screenshots/${name}_sm.jpg\" alt=\"\" /></a></div>"
done

for file in *.png
do
	name=`echo ${file} | cut -f1 -d.`
	convert ${file} -resize 200x200 -quality 95 out/${name}_sm.png
	# echo "<div><a href=\"images/screenshots/$file\"><img src=\"images/screenshots/${name}_sm.png\" alt=\"\" /></a></div>"
done

echo '</div>'
