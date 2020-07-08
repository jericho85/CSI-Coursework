#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 16:44:39 2019

@author: jmcleod
"""
import math

data = [['Sky',   'AirTemp', 'Humidity',  'Wind',    'Water',   'Forecast', 'EnjoySport'],\
        ['Sunny', 'Warm',    'Normal',    'Strong',  'Warm',    'Same',     'Yes'],\
        ['Sunny', 'Warm',    'High',      'Strong',  'Warm',    'Same',     'Yes'],\
        ['Rainy', 'Cold',    'High',      'Strong',  'Warm',    'Change',   'No'],\
        ['Sunny', 'Warm',    'High',      'Strong',  'Cool',    'Change',   'Yes']]

#%%
data_dict = {}
for i in range(len(data)):
    if i == 0:
        for j in range(len(data[i])):
            data_dict[data[i][j]]=[]
    else:
        for j in range(len(data[i])):
            data_dict[data[0][j]].append(data[i][j])
#%%

target = 'EnjoySport' #target must be binary

#%%

def attr_entropy(attr):
    entropy_dict = {}
    attr_entropy = 0
    attr_len = len(attr)
    for i in attr:
        if i in entropy_dict:
            entropy_dict[i] += 1
        else: 
            entropy_dict[i] = 1
    for k,v in entropy_dict.items():
        frac = v/attr_len
        updated_v = -frac*math.log2(frac)
        attr_entropy+=updated_v
        entropy_dict[k]=updated_v
    return(attr_entropy)
    
def attr_gain(attr,target):   
    entropy = attr_entropy(target)
    gain = entropy
    attr_counts = {}
    attr_subset = {}
    attr_len = len(attr)
    for i in range(len(attr)):
        if attr[i] not in attr_counts:
            attr_counts[attr[i]] = 1
        else:
            attr_counts[attr[i]] += 1
        if attr[i] not in attr_subset:
            attr_subset[attr[i]]=[target[i]]
        else:
            attr_subset[attr[i]].append(target[i])
    for k,v  in attr_subset.items():
        subset_len = len(v)
        k_entropy = attr_entropy(v)
    #    print(k,k_entropy,subset_len,attr_len)
        gain = gain - ((subset_len/attr_len)*k_entropy)
    #print('Gain',gain)
    return(entropy,gain)
    

sample1=['Warm','Warm','Cold','Warm','Cold','Warm','Warm','Warm']
outcome1=['Yes','Yes','No','Yes','Yes','No','Yes','Yes']
entropy, gain = attr_gain(sample1,outcome1)
print('\nGain:',gain,'Entropy:',entropy)
#init_entropy = (-0.75*math.log2(0.75))+(-0.25*math.log2(0.25))


#%%
classification = ['+','+','-','+','-','-']
a1 = ['T','T','T','F','F','F']
a2 = ['T','T','F','F','T','T']

class_ent = attr_entropy(classification)
a1_ent = attr_entropy(a1)
a2_ent = attr_entropy(a2)

print(class_ent,a1_ent,a2_ent)
entropy2,gain2 = attr_gain(a2,classification)
print(entropy2,gain2)

#%%


print(math.log2(.5))
print(2**-1)