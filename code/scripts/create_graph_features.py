from __future__ import absolute_import
import argparse
from graph_tool import load_graph_from_csv
from distutils.util import strtobool

import sys
sys.path.append('./code')
from features.graph_feature import save_centrality

parser = argparse.ArgumentParser(description='Create graph features from an edges file')
parser.add_argument('-f')
parser.add_argument('-d', default=' ')
parser.add_argument('-directed', default=False, type=strtobool)
parser.add_argument('-w', default=False, type=strtobool)

args = parser.parse_args()
fname = args.f
dirname = '/'.join(fname.split('/')[:-1])
node_f_name = dirname + '/node_feature.csv'
edge_f_name = dirname + '/edge_feature.csv'

sep = args.d
directed = bool(args.directed)

print('Loaded file name: {},\tis_directed: {},\tis_weighted: {}\n'.format(fname, directed, bool(args.w)))

g = load_graph_from_csv(fname, directed=directed, csv_options={'delimiter': sep, 'quotechar': '"'})

weight = None
if bool(args.w):
    edge_weights = []
    with open(fname) as f:
        for l in f:
            edge_weight = float(l.split()[2])
            edge_weights.append(edge_weight)

    # create property for edge weights
    weight = g.new_edge_property('float')
    weight.a = edge_weights

save_centrality(g, node_f_name, edge_f_name, weight=weight)
