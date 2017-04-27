import csv
import operator
import decimal
import numpy as np
import matplotlib.pyplot as pl
import calendar
import sys
import os.path
import networkx as nx


with open('../data/rearranged/testtrial.csv') as csvfile:
   reader = csv.DictReader(csvfile, delimiter=',')
   rows = list(reader)
   data = []
   for row in rows:
      i = []
      i.append(row['Plant']) # Your data columns
      i.append(row['Bee'])
      data.append(map(float, i)) # convert to float
      
print data[0]
print data[0][1]
print data

G=nx.Graph()#  G is an empty Graph

Nodes=range(len(data))
G.add_nodes_from(Nodes)
Edges=data
G.add_edges_from(Edges)


nx.draw(G, node_color='c',edge_color='k', with_labels=True)
pl.show()