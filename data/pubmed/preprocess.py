node_file = 'Pubmed-Diabetes.NODE.paper.tab'
edge_file = 'Pubmed-Diabetes.DIRECTED.cites.tab'

valid_nodes = set()
valid_edges = []
with open('labels.txt', 'w') as fout:
    with open(node_file) as f:
        for _ in range(2):
            f.readline()

        for l in f:
            data = l.strip().split()
            node = data[0]
            label = data[1].split('=')[1]
            valid_nodes.add(node)
            fout.write('{} {}\n'.format(node, label))


with open(edge_file) as f:
    for _ in range(2):
        f.readline()
    for l in f:
        data = l.split()
        from_paper, to_paper = list(map(lambda x: x.split(':'), [data[1], data[3]]))
        nodes = set((from_paper[1], to_paper[1]))
        if len(nodes & valid_nodes) == 2:
            valid_edges.append(' '.join(list(nodes)))

with open('./edges.txt', 'w') as f:
    for edge in valid_edges:
        f.write(edge + '\n')
