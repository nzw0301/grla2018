from run_single_node_classification_per_model import run_single_node_classification
import numpy as np

dname = 'pubmed'
rnd = np.random.RandomState(0)
model_names = ['spectral_embeddings', 'line', 'node2vec']
for model_name in model_names:
    for dim in [128, 256]:
        run_single_node_classification(dname, rnd, model_name, dim)
