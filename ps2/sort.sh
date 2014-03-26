#!/bin/bash
rm -f *txt *rpt *map vol_*/*txt 
g++ -w index_data.cc split.cc split.h parser.h parser.c -lz
mv a.out index_data
g++ -w merge.cc split.cc split.h
mv a.out merge
read -p "Please input start number: " start
read -p "Please input stop number: " stop
for (( i=${start}; i<${stop}; i=i+100 ))
do
    tar -xvf ../vol_${i}_*.tar
    mv data/4c/tux-4/polybot/gzipped_sorted_nz/* .
    line=`tail -n 1 docID_url.rpt | awk '{print $1}'`
    line=$((${line}+1))
    echo $line
    ./index_data $i $line
    dir=vol_${i}_*
    echo $dir
    #sort -u $dir/*txt > sort_${i}.txt
    sort $dir/*txt > sort_${i}.txt
done
sort -m sort_*.txt > merge.rpt
./merge
