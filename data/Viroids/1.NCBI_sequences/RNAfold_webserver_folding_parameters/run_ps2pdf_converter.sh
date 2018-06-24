#!/bin/bash
#$ -cwd
#
#$ -N spades
#$ -m e
#$ -o spades.out
# requesting 12hrs wall clock time
#$ -l h_rt=12:00:00

#dataPath=/brldata/ccgstaff/share/pbcrc2064/1.Pilot_data/3.Condetri/2.BGI/1.Trimmed_data
#dataPath=/brldata/home/rbarrero/projects/12.PBCRC2064_main_manuscript/1.Datasets/set_21-25nt/original

dataPath=${PWD}

for file in $dataPath/*.ps

do
   var=$(basename $file)
   ps2pdf  ${file}  $var.pdf
done
