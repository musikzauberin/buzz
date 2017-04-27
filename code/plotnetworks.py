
import networkx as nx
import matplotlib.pyplot as pl

G=nx.Graph()#  G is an empty Graph

Nodes=range(9)
G.add_nodes_from(Nodes)
Edges=[(0,1), (0,2), (1,3), (1,4), (1,7), (2,5), (2,8), (3, 4), (3,5),(4,6), (4,7), (4,8), (5,7)]
G.add_edges_from(Edges)
G.add_edge(6,8)

nx.draw(G, node_color='c',edge_color='k', with_labels=True)
pl.show()