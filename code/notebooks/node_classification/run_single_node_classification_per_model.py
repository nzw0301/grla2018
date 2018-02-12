import os
import copy
import pandas as pd
import numpy as np
import h5py
import sys
from sklearn.linear_model import LogisticRegressionCV
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score
from collections import defaultdict
from time import time

sys.path.append('../../utils/')
from node_vector import load_node_vector

def run_single_node_classification(dname, rnd, model_name, dim):
    dim = str(dim)
    is_normalized_list = [False, True]
    cv = 5
    write_f_name = model_name + '_' + dim + '_single_node_classification_result.h5'
    df = pd.read_csv('./../../../data/{}/labels.reindex.txt'.format(dname), sep=' ', index_col=0)
    y = df.label.values
    path = './../../../data/{}/'.format(dname)
    h5py_path = path + write_f_name
    f = h5py.File(h5py_path, 'w')
    vec_dir = path + model_name + '/'
    vec_names = sorted(os.listdir(vec_dir))
    for vec_name in vec_names:
        if 'vec' not in vec_name:
            continue
        elif dim not in vec_name:
            continue

        vec_file_path = vec_dir + vec_name

        X = load_node_vector(vec_file_path, normalized=False)
        for is_normalized in is_normalized_list:
            if is_normalized:
                norm = np.sqrt(np.sum(X ** 2, axis=1))
                X /= norm[:, None]

            micro_val_results = []
            kf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=rnd)
            incorrect_val_list = np.array([], dtype=np.int)
            for train_idx, val_idx in kf.split(X, y):
                X_train, X_val, y_train, y_val = X[train_idx], X[val_idx], y[train_idx], y[val_idx]
                model = LogisticRegressionCV(Cs=[0.25, 0.5, 1, 2, 4],
                                             cv=cv,
                                             n_jobs=-1,
                                             random_state=rnd)
                s = time()
                model.fit(X_train, y_train)
                print('Training time on one fold {}'.format(time() -s))
                y_pred = model.predict(X_val)
                micro_val_results.append(f1_score(y_pred, y_val, average='micro'))
                incorrect_ids = val_idx[np.where(y_pred != y_val)[0]]
                incorrect_val_list = np.hstack([incorrect_val_list, incorrect_ids]).astype(np.int)

            vec_name = vec_name.replace('.vec', '')
            if is_normalized:
                dataset_name = '/{}/{}/normalized/incorrect_ids'.format(model_name, vec_name)
            else:
                dataset_name = '/{}/{}/unnormalized/incorrect_ids'.format(model_name, vec_name)
            f.create_dataset(dataset_name, data=np.array(incorrect_val_list), dtype='i')
            dataset_name = dataset_name.replace('incorrect_ids', 'micro_f1_scores')
            f.create_dataset(dataset_name, data=np.array(micro_val_results), dtype='f')
            print(dname, vec_name.replace('_', ' '), np.mean(micro_val_results))
    f.close()
