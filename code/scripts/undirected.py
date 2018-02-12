import argparse


parser = argparse.ArgumentParser(description='Reindex edge file')
parser.add_argument('-f', default='edges.reindex.txt')

args = parser.parse_args()
fname = args.f

save_dir = '/'.join(fname.split('/')[:-1])
out_node_fname = save_dir + '/edges.reindex.txt.undirected'

existing_edges = set()

with open(out_node_fname, 'w') as f:
    with open(fname) as read_f:
        for l in read_f:
            edge = l.strip().split()
            current_num_edges = len(existing_edges)
            existing_edges.add(tuple(sorted(edge)))
            if current_num_edges != len(existing_edges):
                f.write('{}\n'.format(' '.join(map(str, edge))))
