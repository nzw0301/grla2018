from run_single_node_classification_per_model import run_single_node_classification
import numpy as np

dname = 'flickr'
rnd = np.random.RandomState(0)
model_names = ['line', 'node2vec']
for model_name in model_names:
    run_single_node_classification(dname, rnd, model_name, 256)
