import argparse
from queue import Queue

parser = argparse.ArgumentParser(description='Extract the largest connected component from edgelist file')
parser.add_argument('-f', default='')

args = parser.parse_args()
fname = args.f

save_dir = '/'.join(fname.split('/')[:-1])
out_fname = save_dir + '/edges.txt'


def find_connected_component_from_node(v, g):
    targets_nodes = Queue()
    targets_nodes.put(v)
    components = set()
    components.add(v)
    while not targets_nodes.empty():
        node = targets_nodes.get()
        for adj_node in g.get(node):
            if adj_node not in components:
                targets_nodes.put(adj_node)
                components.add(adj_node)
    return components

edges = {}
with open(fname) as f:
    for l in f:
        nodes = list(map(int, l.split()))
        for node in nodes:
            if node not in edges:
                edges[node] = set()

        for index, from_node in enumerate(nodes):
            to_node = nodes[(index+1) % 2]
            edges[from_node].add(to_node)

# BFS to obtain the largest connected component
candidate_nodes = set(edges.keys())
largest_components = set()
while len(largest_components) < len(candidate_nodes):
    v = candidate_nodes.pop()
    components = find_connected_component_from_node(v, edges)
    if len(components) > len(largest_components):
        largest_components = components
    candidate_nodes -= components

# output
with open(out_fname, 'w') as fout:
    with open(fname) as fin:
        for l in fin:
            nodes = set(map(int, l.split()))
            if nodes & largest_components:
                fout.write(l)
