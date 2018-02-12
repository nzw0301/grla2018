import numpy as np
import pandas as pd

from graph_tool.centrality import betweenness, closeness, pagerank


def save_centrality(g, node_out_fname, edge_out_fname, weight=None):
    """
    :param g: `Graph` instance
    :return: None
    """

    df = pd.DataFrame()
    df['node'] = pd.Series(np.array([int(v) for v in g.vertices()]))

    # degree
    print('Degree')
    num_nodes = len(g.get_vertices())
    denom = num_nodes - 1

    if g.is_directed():
        unnormalized_in_degree = np.array([v.in_degree() for v in g.vertices()])
        unnormalized_out_degree = np.array([v.out_degree() for v in g.vertices()])

        df['unnormalized_in_degree'] = unnormalized_in_degree
        df['unnormalized_out_degree'] = unnormalized_out_degree
        df['in_degree'] = unnormalized_in_degree / denom
        df['out_degree'] = unnormalized_out_degree / denom

    else:
        # check whether weighted graph or not
        if weight:
            unnormalized_degree = np.zeros(num_nodes)
            edge_weights = np.array(weight.get_array())
            for edge, w in zip(g.get_edges(), edge_weights):
                for node in edge[:2]:
                    unnormalized_degree[node] += w
            df['unnormalized_degree'] = unnormalized_degree
            df['degree'] = unnormalized_degree / denom
        else:
            unnormalized_degree = np.array([v.out_degree() for v in g.vertices()])
            df['unnormalized_degree'] = unnormalized_degree
            df['degree'] = unnormalized_degree / denom

    # closeness
    print('Closeness')
    df['unnormalized_closeness'] = np.array(closeness(g, weight=weight, norm=False).get_array())
    df['closeness'] = np.array(closeness(g, weight=weight, norm=True).get_array())

    # pageRank
    print('PageRank')
    df['pagerank'] = np.array(pagerank(g, weight=weight).get_array())

    # betweenness
    print('Betweenness')
    un_node_between, un_edge_between = betweenness(g, weight=weight, norm=False)
    node_between, edge_between = betweenness(g, weight=weight, norm=True)
    df['unnormalized_betweenness'] = np.array(un_node_between.get_array())
    df['betweenness'] = np.array(node_between.get_array())

    df.to_csv(node_out_fname, index=False)

    # edge
    sources = []
    targets = []
    for e in g.edges():
        source, target = list(map(int, [e.source(), e.target()]))
        sources.append(source)
        targets.append(target)

    df = pd.DataFrame()
    df['source'] = pd.Series(np.array(sources))
    df['target'] = np.array(targets)

    # betweenness
    df['unnormalized_betweenness'] = np.array(un_edge_between.get_array())
    df['betweenness'] = np.array(edge_between.get_array())

    df.to_csv(edge_out_fname, index=False)
