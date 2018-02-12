import sys

fname = sys.argv[1]
out_fname = fname + '.directed'

with open(out_fname, 'w') as fout:
    with open(fname) as fin:
        for l in fin:
            fields = l.split()

            # weighted graph
            if len(fields) == 2:
                u, v = fields
                fout.write(' '.join([u, v, '1']) + '\n')
