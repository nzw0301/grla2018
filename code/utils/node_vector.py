from gensim.models.keyedvectors import KeyedVectors
import numpy as np


def load_node_vector(node_vector_path, normalized=False):
    vec = KeyedVectors.load_word2vec_format(node_vector_path)
    num_nodes = len(vec.index2word)

    if 'word2vec' in node_vector_path:
        num_nodes -= 1

    if normalized:
        X = np.array([vec.word_vec(str(i)) / np.sqrt(sum(vec.word_vec(str(i)) ** 2)) for i in range(num_nodes)])
    else:
        X = np.array([vec.word_vec(str(i)) for i in range(num_nodes)])
    return X
