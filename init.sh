#!/usr/bin/env bash

#### begin BlogCatalog v3
#### http://socialcomputing.asu.edu/datasets/BlogCatalog3
mkdir -p data/blogcatalog/spectral_embeddings data/blogcatalog/line data/blogcatalog/node2vec
cd data/blogcatalog
wget http://socialcomputing.asu.edu/uploads/1283153973/BlogCatalog-dataset.zip
unzip BlogCatalog-dataset.zip
mv BlogCatalog-dataset/readme.txt .
mv BlogCatalog-dataset/data/* .
tr ',' ' ' < edges.csv > edges.txt
tr ',' ' ' < group-edges.csv > labels.txt
cd ../../
python code/scripts/reindex.py -f data/blogcatalog/edges.txt -l data/blogcatalog/labels.txt
python code/scripts/create_graph_features.py -f data/blogcatalog/edges.reindex.txt
python code/scripts/undirected2lineformat.py data/blogcatalog/edges.reindex.txt
cd data/blogcatalog
rm -rf BlogCatalog-dataset BlogCatalog-dataset.zip edges.csv group-edges.csv nodes.csv groups.csv labels.txt edges.txt
cd ../../
#### end BlogCatalog v3


#### begin Flickr
#### http://socialcomputing.asu.edu/datasets/Flickr
mkdir -p data/flickr
cd data/flickr
mkdir line node2vec spectral_embeddings
wget http://socialcomputing.asu.edu/uploads/1283157931/Flickr-dataset.zip
unzip Flickr-dataset.zip
rm Flickr-dataset.zip
mv Flickr-dataset/readme.txt .
mv Flickr-dataset/data/*.csv .
tr ',' ' ' < edges.csv > edges.txt
tr ',' ' ' < group-edges.csv > labels.txt
cd ../../
python code/scripts/reindex.py -f data/flickr/edges.txt -l data/flickr/labels.txt
python code/scripts/create_graph_features.py -f data/flickr/edges.reindex.txt
python code/scripts/undirected2lineformat.py data/flickr/edges.reindex.txt
cd data/flickr
rm -rf edges.txt labels.txt Flickr-dataset/
cd ../../
#### end flickr

#########################
## Directed & unweighted graphs
#########################

#### begin cora citation network
#### https://linqs.soe.ucsc.edu/node/236
mkdir -p data/cora/line data/cora/node2vec data/cora/line data/cora/spectral_embeddings
cd data/cora
wget https://linqs-data.soe.ucsc.edu/public/lbc/cora.tgz
tar -xzvf cora.tgz
mv cora/* .
cat cora.cites | tr '\t' ' ' > edges.txt
rm -rf cora cora.tgz cora.cites
cut -f1,1435  cora.content | sort -n > labels.txt
cd ../../
python code/scripts/reindex.py -f data/cora/edges.txt -l data/cora/labels.txt
python code/scripts/undirected.py -f data/cora/edges.reindex.txt

python code/scripts/create_graph_features.py -f data/cora/edges.reindex.txt -directed True
mv data/cora/node_feature.csv data/cora/node_feature.csv.as_directed
mv data/cora/edge_feature.csv data/cora/edge_feature.csv.as_directed
python code/scripts/create_graph_features.py -f data/cora/edges.reindex.txt.undirected -directed False
mv data/cora/node_feature.csv data/cora/node_feature.csv.as_undirected
mv data/cora/edge_feature.csv data/cora/edge_feature.csv.as_undirected

python code/scripts/undirected2lineformat.py data/cora/edges.reindex.txt.undirected
mv data/cora/edges.reindex.txt.directed data/cora/edges.reindex.txt.as_undirected
python code/scripts/directed2lineformat.py data/cora/edges.reindex.txt

cd data/cora
rm cora.content edges.txt labels.txt
cd ../../
#### end cora


#### begin pubmed
#### https://linqs.soe.ucsc.edu/data
mkdir -p data/pubmed data/pubmed/node2vec data/pubmed/line data/pubmed/spectral_embeddings
cd data/pubmed
wget https://linqs-data.soe.ucsc.edu/public/Pubmed-Diabetes.tgz
tar -xzvf Pubmed-Diabetes.tgz
mv Pubmed-Diabetes/README .
mv Pubmed-Diabetes/data/* .
python preprocess.py
cd ../../
python code/scripts/reindex.py -f data/pubmed/edges.txt -l data/pubmed/labels.txt
python code/scripts/undirected.py -f data/pubmed/edges.reindex.txt

python code/scripts/create_graph_features.py -f data/pubmed/edges.reindex.txt -directed True
mv data/pubmed/node_feature.csv data/pubmed/node_feature.csv.as_directed
mv data/pubmed/edge_feature.csv data/pubmed/edge_feature.csv.as_directed
python code/scripts/create_graph_features.py -f data/pubmed/edges.reindex.txt.undirected -directed False
mv data/pubmed/node_feature.csv data/pubmed/node_feature.csv.as_undirected
mv data/pubmed/edge_feature.csv data/pubmed/edge_feature.csv.as_undirected

python code/scripts/undirected2lineformat.py data/pubmed/edges.reindex.txt.undirected
mv data/pubmed/edges.reindex.txt.directed data/pubmed/edges.reindex.txt.as_undirected
python code/scripts/directed2lineformat.py data/pubmed/edges.reindex.txt

cd data/pubmed
rm -rf *.tab Pubmed-Diabetes Pubmed-Diabetes.tgz edges.txt labels.txt
cd ../../
#### end pubmed

#########################
### create spectral embeddings (eigenmaps) for undirected graphs
#########################
python code/spectral/spectral.py

#########################
#### clone LINE and node2vec and make them, then train!
#########################
cd code
sh init.sh

sh line.sh
sh node2vec.sh
