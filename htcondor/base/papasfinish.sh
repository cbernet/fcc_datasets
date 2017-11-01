#!/bin/bash
#script is run after all the papas runsa re finished
source parameters.sh
touch $maindirectory/$subdirectory/papasfinish.txt
#call to make the summary of what was produced by the run "info.yaml"
echo python papasinfo.py $subdirectory -b $maindirectory
python papasinfo.py $subdirectory -b $maindirectory
echo $maindirectory/$subdirectory
ls -al  $maindirectory/$subdirectory
rm $maindirectory/$subdirectory/papasfinish.txt

