import sys

fname = sys.argv[1]
out_fname = fname + '.directed'

with open(out_fname, 'w') as fout:
    with open(fname) as fin:
        for l in fin:
            fields = l.split()

            # unweighted graph
            if len(fields) == 2:
                u, v = fields
                fout.write(' '.join([u, v, '1']) + '\n')
                fout.write(' '.join([v, u, '1']) + '\n')

            # weighted graph
            if len(fields) == 3:
                u, v, w = fields
                fout.write(' '.join([u, v, w]) + '\n')
                fout.write(' '.join([v, u, w]) + '\n')
