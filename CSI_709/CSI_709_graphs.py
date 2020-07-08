# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 15:59:36 2018

@author: Jericho
"""
#%%
# https://networkx.github.io/documentation/stable/tutorial.html#creating-a-graph

import networkx as nx
import matplotlib.pyplot as plt

G= nx.Graph() #create a graph
#DG = nx.DiGraph() #create a directed graph
#MG = nx.MultiDiGraph # create a directed multigraph
# you can create non directed multigraphs - remove D
# you can add nodes with a string for a name, not just a number

for i in range(0,5):
    G.add_node(i) # add a node
G.add_nodes_from([10,12,15])

G.add_edge(1,2)
G.add_edge(1,3)
G.add_edge(1,4)
G.add_edge(1,10)
G.add_edge(1,5)
G.add_edge(1,6)
G.add_edge(1,'Jericho')
G.add_edge(1,0)
G.add_edge(1,12)
#command line views:
#G[1] 
#G.edges()
#G.nodes()

G.add_edge(5,6)
G.add_edge("Jericho",2)
G.remove_node(15)
print(G.nodes())
print(G.edges())
print(list(G.neighbors(2)))
print(G.degree(1))
print(G[1]) # get dictionary values

nx.draw(G,with_labels=True,font_weight='bold')

G.clear() # erase your graph
#%%

import networkx as nx
import matplotlib.pyplot as plt

# you can create an erdos manually by iterating over all the pairs
# and using the probability of a node + a RNG to decide if there is an edge

er = nx.erdos_renyi_graph(10,0.2)
print(er.nodes())
print(len(er.nodes()))
print(er.edges())
print(len(er.edges()))

#red = nx.random_lobster(20,0.9,0.9)
nx.draw(er,with_labels=True,font_weight='bold')
#nx.draw(red,with_labels=True,font_weight='bold')
#%%
import networkx as nx
import matplotlib.pyplot as plt

# iterates creation of networks where n=100 and p = 0.20

h = {}
#f.degree(0) # this is just an example of how to get degrees

for n in range(0,1000):
    f = nx.erdos_renyi_graph(100,0.95)
    for i in f:
    #    print(i)
        k=f.degree(i)
        h[k]=h.get(k,0)+1
    #plt.plot(h.keys(),h.values(),'o')
    #plt.show()
    print(n)
print(h)
plt.bar(h.keys(),h.values())
plt.show()

#%%
import igraph as ig
import random as rn

#igraph renames nodes if one is deleted!


