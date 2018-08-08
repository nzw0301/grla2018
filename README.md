This repository provides the source codes used in _Analyzing Centralities of Embedded Nodes_ submitted to GRLA 2018.

## Experimental environment

### Docker

For `bash/zsh` users:

```bash
$ docker pull nocotan/graph-tool-plus
$ docker run -i -p 8888:8888 -v $(pwd):/grla -w="/grla" -t nocotan/graph-tool-plus /bin/bash
$ export JOBLIB_TEMP_FOLDER="/grla"
$ jupyter notebook --ip=0.0.0.0 --allow-root
```

For `fish` users:

```fish
$ docker pull nocotan/graph-tool-plus
$ docker run -i -p 8888:8888 -v (pwd):/grla -w="/grla" -t nocotan/graph-tool-plus /bin/bash
$ export JOBLIB_TEMP_FOLDER="/grla"
$ jupyter notebook --ip=0.0.0.0 --allow-root
```

### Training embeddings

Please run the command that is `$ sh init.sh` to obtain graph data sets and calculate some graph features.

### Node classifications

```bash
$ cd code/notebooks/node_classification/
$ python cora.py
$ python pubmed.py
$ python blogcatalog.py
# we recommend training flickr dataset per dimension to obtain results fastly.
$ python flickr_128.py
$ python flickr_256.py
```

### View results of node classification results and plot power-law distributions based on node centrality measures.

``` bash
$ jupyter notebook --ip=0.0.0.0 --allow-root save_best_result_on_single_node_classification.ipynb
$ jupyter notebook --ip=0.0.0.0 --allow-root powerlaw_on_single_node_classification.ipynb
```
