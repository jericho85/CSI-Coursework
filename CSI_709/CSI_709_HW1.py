# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 16:06:39 2018

@author: jmcle


For algorithms with Fixed P and Fixed n. 
Generate your own algorithm
Study Pr (k(sub-i)), <k>
From the math that we’ve done, calculate what Pr (k(sub-i)) should be
Count triangles. t(sub-i) on node i. Pr(t(sub-i)
Count the number of links in each iteration
Create a matrix of values for N and P and these quantities and explore it enough to gain some insight into the relationships
Calculate these values mathematically (item 3, primarily, others if possible)

"""

import networkx as nx
import matplotlib.pyplot as plt
#import pandas as pd


h = {}
#f.degree(0) # this is just an example of how to get degrees

def create_graph(N,q,p):
    for n in range(0,N):
        f = nx.erdos_renyi_graph(q,p)
        t=0
        for i in f:
        #    print(i)
            k=f.degree(i)
            h[k]=h.get(k,0)+1
            triangle=nx.triangles(f).values()
            temp_val = 0
            for tri in triangle:
                temp_val+=tri
            t+=temp_val/3
#            print(tri)
        #plt.plot(h.keys(),h.values(),'o')
        #plt.show()
#        print(n)
#    print(h)
    print("Graph showing N:",N,'q:',q,'p:',p)
    print("Trianges:",t)
    plt.bar(h.keys(),h.values())
    plt.show()
    h.clear()

def iterate_graphs():
    N = 10 # number of iterations
    q = 100 # number of nodes
#    p = .05 # Pr of edge
    for i in range(0,20):
        p = ((i+1)*5)/100
        create_graph(N,q,p)

#create_graph(1000,100,0.05)
iterate_graphs()
#df =pd.DataFrame(h)

#%%
import networkx as nx
import pylab as plt
import pydot

#from networkx.drawing.nx_agraph import draw
f = nx.erdos_renyi_graph(10,0.2)
nx.draw(f,with_labels=True,font_weight='bold')
p= nx.triangles(f).values()
for i in range(0,10):
    k=f.degree(i)
    print(k)
print(p)
print(f.edges)
temp_dict={}
for i in f.edges:
    temp_dict[i] = f.edges(i)
print(f.edges(0))

print("temp dict",temp_dict)
