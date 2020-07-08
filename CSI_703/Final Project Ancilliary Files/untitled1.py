#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 12:49:51 2019

@author: jmcleod
"""

import csv
import json
#%%

file_list=[]

with open("cards_by_deck.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    line_count=0
    for row in csv_reader:
        file_list.append(row)

decks = []
for i in range(0,len(file_list)):
    for j in range(0,len(file_list[i])):
        if i == 0 and j>0:
            decks.append(file_list[i][j])

deck_list = {}
for i in decks:
    deck_list[i]={}
      
card_list = []
for i in file_list:
    print(i[0])
    card_list.append(i[0])

card_list.pop(0)

counter=0
for line in file_list:
    if counter>0:
        #print(line)
        card = line[0]
        for d in range(0,len(decks)):
            #print(decks[d],line[0],line[d])
            deck_list[decks[d]][card]=float(line[d+1])
    counter+=1

for k,v in deck_list.items():
    for j,w in v.items():
        if j=="Abrade":
            print(k,j,w)

#%%
json_decklists = json.dumps(deck_list)
loaded_decks = json.loads(json_decklists)
print(loaded_decks)
filename = "cards_by_deck.json"
with open(filename, 'w') as f:
    json.dump(loaded_decks, f)