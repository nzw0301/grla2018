#!/bin/bash

# hyper-parameters
dim_array=(128 256)
ps=(0.25 0.5 1 2 4)
qs=(0.25 0.5 1 2 4)

# datasets and attributes
datanames=(
    "blogcatalog"
    "cora"
    "pubmed"
    "flickr"
)
gtypes=(
    ""
    "-dr"
    "-dr"
    ""
)

# `i` is index of data set
for i in 0 1 2 3;
do
    data="${datanames[i]}"
    gtype="${gtypes[i]}"
    inpath="data/${data}/edges.reindex.txt"

    for dim in "${dim_array[@]}"
    do
        for p in "${ps[@]}"
        do
            for q in "${qs[@]}"
            do
              outpath="data/${data}/node2vec/node2vec_${dim}_p=${p}_q=${q}.vec"
              ./code/snap-ref/examples/node2vec/node2vec -i:$inpath -o:$outpath -d:$dim -p:$p -q:$q $gtype -v
            done
        done
    done
done

# directed graph as undirected graph
for i in 1 2;
do
    data="${datanames[i]}"
    inpath="data/${data}/edges.reindex.txt.undirected"

    for dim in "${dim_array[@]}"
    do
        for p in "${ps[@]}"
        do
            for q in "${qs[@]}"
            do
                outpath="data/${data}/node2vec/node2vec_${dim}_p=${p}_q=${q}_undirected.vec"
                ./code/snap-ref/examples/node2vec/node2vec -i:$inpath -o:$outpath -d:$dim -p:$p -q:$q -v
            done
        done
    done
done
