import numpy as np
from sklearn.manifold import spectral_embedding
from scipy.sparse import dok_matrix

# undirected graphs
dir_names = ['blogcatalog', 'cora', 'pubmed'] # flickr is skipped due to OutOfMemory
dataset_paths = []
for dir_name in dir_names:
    directed_datasets = ['cora', 'pubmed']
    if dir_name in directed_datasets:
        dir_path = 'data/{}/edges.reindex.txt.as_undirected'.format(dir_name)
    else:
        dir_path = 'data/{}/edges.reindex.txt.directed'.format(dir_name)
    dataset_paths.append(dir_path)

num_nodes = [10312, 2708, 19717]
n_components_list = [128, 256]

for (dataset_path, num_node) in zip(dataset_paths, num_nodes):
    print('Loading {}'.format(dataset_path.split('/')[-2]))
    adj = dok_matrix((num_node, num_node), dtype=np.float32)

    with open(dataset_path) as f:
        for l in f:
            source, target, weight = l.split()
            u = int(source)
            v = int(target)
            weight = float(weight)
            adj[u, v] = weight

    split_path = dataset_path.split('/')
    save_dir = '/'.join(split_path[:-1]) + '/spectral_embeddings'

    for n_components in n_components_list:
        print('Create spectral embeddings, dim={}'.format(n_components))
        spectral_emb = spectral_embedding(adjacency=adj,
                                          n_components=n_components,
                                          random_state=np.random.RandomState(7),
                                          drop_first=False,
                                          norm_laplacian=True)

        with open('{}/spectral_{}.vec'.format(save_dir, n_components), 'w') as f:
            f.write('{} {}\n'.format(num_node, n_components))
            for node, vec in enumerate(spectral_emb):
                str_vec = ' '.join(map(str, vec))
                f.write('{} {}\n'.format(node, str_vec))
