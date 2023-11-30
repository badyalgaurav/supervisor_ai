#!/bin/bash
echo "start\n"
for f in *.jpg
do
  fname=$(basename "$f")
  echo "fname is $fname\n"
  fname="${filename%.*}"
  echo "fname is $fname\n"
  if [ $((fname %  2)) -eq 1 ]
  then
    echo "removing $fname\n"
    rm "$f"
  fi
done