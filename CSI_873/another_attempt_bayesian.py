#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 13:42:32 2019

@author: jmcleod
"""

import csv,random,copy,math 
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def data_import(file):
    '''
    This function imports the data from a particular file
    and returns an array of arrays
    NOTE: I am normalizing pixel values to simply be 0 and 1: no in between.
    '''
    data = []
    with open(file, 'r') as csvfile:
        csv_r = csv.reader(csvfile,delimiter=' ')
        for row in csv_r:
            row_nums = []
            for i in range(len(row)):
                try:
                    val = float(row[i])
                    if i > 0:
                        val = round(val/255,4)
                        if val > 0: # making inputs binary for simplicity
                            val =1
                        # The above line scales the data imported
                    row_nums.append(val)
                except:
                    print('ERROR on import: non-numerical data')
                    print(row[i])
                    break                    
            data.append(row_nums)
    return(data)


def data_import_loop(string,denom):
    '''
    This function loops the data import across all files of the chosen type,
    which is specified by the string argument passed to the function.
    It then uses the first value in the set to add the imported arrays
    to the correct dictionary key, created with values 0-9. 
    The resulting dictionary is returned.
    '''
    files = []
    data_dict = {}
    for i in range(10):
        file_name = string+str(i)+'.txt'
        files.append(file_name)
        data_dict[i]=[]
    for i in files:
        data = data_import(i)
        for j in range(len(data)):
            if j%denom==0: # SUBSET data to 1/5th
                data_dict[data[j][0]].append(data[j][1:])
    return(data_dict)
    

def reshape_data(data_dict):
    results = []
    sideways =  []
    for k,v in data_dict.items():
        for i in range(len(v)):
            sideways.append(v[i])
            results.append(k)
    print(len(sideways),len(sideways[0]))
    data_reshaped = []
    for i in range(len(sideways[0])):
        data_reshaped.append([])
    for i in range(len(sideways)):
        for j in range(len(sideways[i])):
            data_reshaped[j].append(sideways[i][j])
    return(data_reshaped,results)
    



denom = 200
data_dict = data_import_loop('train',denom)
denom = 100
test_dict = data_import_loop('test',denom)

for k,v in data_dict.items():
    print(k,len(v))

print()
for k,v in test_dict.items():
    print(k,len(v))

data_matrix,results_array = reshape_data(data_dict)
test_matrix,test_results_array = reshape_data(test_dict)