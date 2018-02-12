#!/bin/bash
dim_array=(128 256)
datanames=(
    "blogcatalog"
    "cora"
    "pubmed"
    "flickr"
)

samples=(
    86.20832
    22.63888
    164.83412
    673.08868
)

for i in 0 1 2 3;
do
    data="${datanames[i]}"
    sample="${samples[i]}"
    inpath="data/${data}/edges.reindex.txt.directed"

    for dim in "${dim_array[@]}"
    do
        echo $inpath
        outpath="data/${data}/line/line1st_${dim}.vec"
        ./code/LINE/linux/line -train $inpath -output $outpath -size $dim -order 1 -negative 5 -samples $sample -rho 0.025 -threads 16
        outpath="data/${data}/line/line2nd_${dim}.vec"
        ./code/LINE/linux/line -train $inpath -output $outpath -size $dim -order 2 -negative 5 -samples $sample -rho 0.025 -threads 16
    done
done


# directed graph as undirected
for i in 1 2;
do
    data="${datanames[i]}"
    sample="${samples[i]}"
    inpath="data/${data}/edges.reindex.txt.undirected.directed"

    for dim in "${dim_array[@]}"
    do
        echo $inpath
        outpath="data/${data}/line/line1st_${dim}_undirected.vec"
        ./code/LINE/linux/line -train $inpath -output $outpath -size $dim -order 1 -negative 5 -samples $sample -rho 0.025 -threads 16
        outpath="data/${data}/line/line2nd_${dim}_undirected.vec"
        ./code/LINE/linux/line -train $inpath -output $outpath -size $dim -order 2 -negative 5 -samples $sample -rho 0.025 -threads 16
    done
done
