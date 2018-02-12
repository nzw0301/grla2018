import argparse
from distutils.util import strtobool

parser = argparse.ArgumentParser(description='Reindex edge file')
parser.add_argument('-f', default='edges.txt')
parser.add_argument('-l', default='')
parser.add_argument('-s', default=False, type=strtobool)

args = parser.parse_args()
fname = args.f
label_fname = args.l
skip_first_in_label = bool(args.s)

save_dir = '/'.join(fname.split('/')[:-1])
out_node_fname = save_dir + '/edges.reindex.txt'

nodeid2reindex_nodeid = {}

with open(out_node_fname, 'w') as f:
    with open(fname) as read_f:
        for l in read_f:
            edge = l.strip().split()
            u, v = edge[0], edge[1]

            new_u = nodeid2reindex_nodeid.get(u, len(nodeid2reindex_nodeid))
            if new_u == len(nodeid2reindex_nodeid):
                nodeid2reindex_nodeid[u] = len(nodeid2reindex_nodeid)

            new_v = nodeid2reindex_nodeid.get(v, len(nodeid2reindex_nodeid))
            if new_v == len(nodeid2reindex_nodeid):
                nodeid2reindex_nodeid[v] = len(nodeid2reindex_nodeid)

            edge[0] = new_u
            edge[1] = new_v
            f.write('{}\n'.format(' '.join(map(str, edge))))

if not label_fname:
    exit(0)

header = ''
labels = {}
label2intlabel = {}
with open(label_fname) as read_f:
    if skip_first_in_label:
        header = read_f.readline().strip()
    for l in read_f:
        data = l.split()
        u = data[0]
        int_labels = []
        for label in data[1:]:
            int_label = label2intlabel.get(label, len(label2intlabel))
            if int_label == len(label2intlabel):
                label2intlabel[label] = int_label
            int_labels.append(int_label)

        if u in nodeid2reindex_nodeid:
            labels[nodeid2reindex_nodeid[u]] = int_labels

out_label_fname = save_dir + '/labels.reindex.txt'
with open(out_label_fname, 'w') as f:
    if not header:
        header = 'node label'
    f.write(header + '\n')
    for k in sorted(labels):
        f.write('{}\n'.format(' '.join(map(str, [k] + labels[k]))))
