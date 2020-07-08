#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 17:07:08 2019

@author: jmcleod
"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import pylab
#from sklearn.metrics.pairwise import cosine_similarity
#from scipy.spatial.distance import cosine
def done_message():
    print()
    print('DDDD      OOOO    NN  NN   EEEEEE')
    print('DD  DD   OO  OO   NNN NN   EE')
    print('DD  DD   OO  OO   NNNNNN   EEEE')
    print('DD  DD   OO  OO   NN NNN   EE')
    print('DDDDD     OOOO    NN  NN   EEEEEE')
#%%

data = pd.read_csv('cards_by_deck.csv')
data2 = pd.read_csv('long_form.csv')
data3 = pd.read_csv('card_data.csv')

print(list(data2))
print()
print(list(data))
print()
print(list(data3))
data.fillna(0, inplace=True)

deck_names= list(data)
deck_names.pop(0)
card_names = []
for i in data["Card Name"]:
    card_names.append(i)

data = data.drop(columns=["Card Name"])

#%%
print(data3.iloc[3]["Legendary"])

#%%

def calc_same_diff(a,b):
    if a == b:
        same = (a + b)/2
        diff = 0
    else: 
        #card_index.append(i)
        c = max(a,b)
        d = min(a,b)
        same = d
        diff = c-d
    union = a+b
    return(same,diff,union)



def measurement(deck_a,deck_b,card_type):
    diff = 0
    same = 0
    union = 0
#    card_index = []
    for i in range(0,len(data["Affinity"])):
        a = data[deck_a][i]
        b = data[deck_b][i]
#        card = card_names[i]
#        print(card)
        value_ind = data3.iloc[i]["Over $100"] # also change line 120
        #value_ind=1
        if card_type == "All":
            same_update,diff_update,union_update = calc_same_diff(a,b)
            same += (same_update*value_ind)
            diff += (diff_update*value_ind)
            union += (union_update*value_ind)
        else:
            in_type = data3.iloc[i][card_type] # Binary value for card of type
            if in_type ==1:
                same_update,diff_update,union_update = calc_same_diff(a,b)
                same += (same_update*value_ind)
                diff += (diff_update*value_ind)
                union+=(union_update*value_ind)
    return(diff,same,union)

diff,same,union = measurement("UR Delver","Grixis Delver","All")
print(diff,same,union)
        
#%%
def generate_long_form(type_card):
    counter=0
    long_form_adj = [["Deck A","Deck B","Different","Same","Jaccard"]]
    for i in range(0,len(deck_names)):
        for j in range(0,len(deck_names)):
            if j > i:
                counter+=1
                a=deck_names[i]
                b=deck_names[j]
                #print(type_card,counter,a,"vs",b)
                diff,same,union = measurement(a,b,type_card)
                if same >= 1:
                    jaccard = same/(union-same)
                    temp_string1 = str('{"source": "'+a+'", "target": "'+b+'", "value":'+str(jaccard)+'},')
                    temp_string2 = str('{"source": "'+a+'", "target": "'+b+'", "value":'+str(jaccard**2)+'},')
                    temp_list = [a,b,diff,same,jaccard,temp_string1,temp_string2]
                    long_form_adj.append(temp_list)
    return(long_form_adj)

#%%
types = ["All","Land","Creature","Artifact","Enchantment","Planeswalker","Instant","Sorcery"]



for i in types:
    print('starting',i)
    long_form_adj = generate_long_form(i)
    output_name = "Output_adjacency_over100_"+i +".csv" # also change line73
#    output_name = "Output_adjacency_"+i +".csv"
    out_df = pd.DataFrame(long_form_adj)
    out_df.head()
    out_df.to_csv(output_name,sep=",",index=False)
    print("completed",i)

done_message()

#%%

# Network
G.clear()
G = nx.Graph()
for i in deck_names:
    G.add_node(i)

type_card = "Planeswalker"
for i in range(0,len(deck_names)):
    for j in range(0,len(deck_names)):
        if j > i:
            a=deck_names[i]
            b=deck_names[j]
            #print(type_card,counter,a,"vs",b)
            diff,same,union = measurement(a,b,type_card)
            if same > 0:
                jaccard = same/(union-same)
                G.add_edge(a, b, weight= jaccard)
            
            
#%%
G2 = nx.Graph()
G2.clear()
G2 = nx.Graph()
for a, b, data in sorted(G.edges(data=True), key=lambda x: x[2]['weight']):
    print('{a}, {b}, {w}'.format(a=a, b=b, w=data['weight']))
    G2.add_edge(a, b, weight=data['weight'])

for edge in G2.edges.data():
    print(edge)
for node in G2.nodes.data():
    print(node)
    
#%%

pos=nx.circular_layout(G2)
pylab.figure(1)
nx.draw(G2,pos)
pylab.figure(2)
nx.draw(G2,pos,node_size=60,font_size=8)
pylab.figure(3,figsize=(12,12))
nx.draw(G2,pos)
pylab.show()

#%%


print(nx.topological_sort(G2))
