#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 14:05:17 2019

@author: jmcleod
"""

import csv,random,copy,math 
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
#from importlib import reload   # not needed for python 2
#reload(plt)
#%%



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
    
denom = 1
data_dict = data_import_loop('train',denom)
denom = 2
test_dict = data_import_loop('test',denom)


data_matrix,results_array = reshape_data(data_dict)
test_matrix,test_results_array = reshape_data(test_dict)

#%%
class pixel:
    '''
    This class is used to learn and store the probabilities for each input
    attribute.
    '''
    def __init__(self):
        self.outcomes = [] # just a list of the possible classes
        self.pixel_proba = [] # probability of the evidence
        self.outcome_proba = [] # posterior probability
        self.outcome_proba_neg = [] # posterior probability if evidence is (1-p)
        for i in range(10):
            self.outcomes.append(i)
            self.outcome_proba.append(0)
            self.outcome_proba_neg.append(0)

    def update_probas(self,prior,array,target):
        if prior == 0:
            pos_count_dict,neg_count_dict = {},{}
        else:
            pos_count_dict_0,pos_count_dict_1,neg_count_dict_0,neg_count_dict_1 = {},{},{},{}
        count_0,count_1 = 0,0
        if prior == 0:
            '''Adds up counts to use to calculate probabilities of the evidence
            and posterior probabilities'''
            for i in self.outcomes:
                pos_count_dict[i],neg_count_dict[i]=0,0
            for i in range(len(array)):
                if array[i] == 0:
                    neg_count_dict[target[i]]+=1
                    count_0+=1
                else:
                    pos_count_dict[target[i]]+=1
                    count_1+=1
            self.pixel_proba = count_1 / (count_1+count_0)
            '''
            Calculate the outcome likelihoods given a positive or negative value 
            for this pixel. As in, what is the probability the actual image is
            a 1 given this pixel being 0 or 1, and what is the probability it is
            a 2 given this pixel being 0 or 1. '''
            for k,v in pos_count_dict.items():             
                try: 
                    self.outcome_proba[k] = v / (v+neg_count_dict[k]) 
                    
                except:
                    print("Error: more outcomes allowed than are present in data")
            for k,v in neg_count_dict.items():
                try:
                    self.outcome_proba_neg[k] = v / (v+pos_count_dict[k])
                except:
                    print("Error: more outcomes allowed than are present in data")
        else:
            for i in self.outcomes:
                pos_count_dict_0[i],pos_count_dict_1[i],neg_count_dict_0[i],neg_count_dict_1[i]=0,0,0,0
            for i in range(len(array)):
                if array[i] == 0:
                    if prior[i]==0:
                        neg_count_dict_0[target[i]]+=1
                    else:
                        neg_count_dict_1[target[i]]+=1
                    count_0+=1
                else:
                    if prior[i]==0:
                        pos_count_dict_0[target[i]]+=1
                    else:
                        pos_count_dict_1[target[i]]+=1
                    count_1+=1
            self.pixel_proba = count_1 / (count_1+count_0)
            '''This is an altered version of the function that converts
            probabilities of the evidence based on the prior observations'''

            count_11,count_01,total_count = 0,0,0
            for i in range(len(array)):
                total_count +=1
                if prior[i] == 1:
                    if array[i] == 1:
                        count_11 +=1
                elif prior[i] == 0:
                    if array[i] == 1:
                        count_01 +=1
            
            
            self.pixel_proba = [count_01/total_count,count_11/total_count]

            '''
            Calculate the outcome likelihoods given a positive or negative value 
            for this pixel. As in, what is the probability the actual image is
            a 1 given this pixel being 0 or 1, and what is the probability it is
            a 2 given this pixel being 0 or 1. 
            '''
            for k,v in pos_count_dict_0.items():  
                
                #try: 
                try:
                    proba_0 = pos_count_dict_0[k] / (pos_count_dict_0[k]+ neg_count_dict_0[k])
                except:
                    proba_0 = 0
                try:
                    proba_1 = pos_count_dict_1[k] / (pos_count_dict_1[k]+ neg_count_dict_1[k])
                except:
                    proba_1 = 0
                #print(proba_0,proba_1)
                self.outcome_proba[k] = [proba_0,proba_1]
                try:
                    proba_0 = neg_count_dict_0[k] / (pos_count_dict_0[k]+ neg_count_dict_0[k])
                except:
                    proba_0 = 0
                try:
                    proba_1 = neg_count_dict_1[k] / (pos_count_dict_1[k]+ neg_count_dict_1[k])
                except:
                    proba_1 = 0
                #print(proba_0,proba_1)
                self.outcome_proba_neg[k] = [proba_0,proba_1]
                #except:
                #    print("Error: more outcomes allowed than are present in data")
    
class bayesian_network:
    '''
    This is the setup of the classifieer. It creates a set of objects
    representing the inputs and then learns the likelihood of the outputs 
    for each
    '''
    def __init__(self,data,target):
        self.pixels = {}
        self.target_proba = [1]*10
        for i in range(len(data)):
            self.pixels[i]=pixel()
            if i  == 0:
                self.pixels[i].update_probas(0,data[i],target)
            else: 
                self.pixels[i].update_probas(data[i-1],data[i],target)
        temp = {}
        for i in target:
            if i not in temp:
                temp[i]=1
            else:
                temp[i]+=1
        for i in range(len(self.target_proba)):
            self.target_proba[i]=temp[i]/len(target)
        
    '''
    This function makes classifications given a new input array by
    Calculating the likelihood of the evidence given the outcome for each
    pixel, divided by the likelihood of the evidence.
    The  output is an arrray of probabilities for each digit. The highest of
    these is the class returned by the model.
    '''
    def classify(self,array):
        posteriors,evidence,results = [1]*10, [1]*10, []
        for i in range(len(array)):
            if i  == 0:
                p_e = self.pixels[i].pixel_proba
                if array[i] == 1:
                    p_p = self.pixels[i].outcome_proba
                else:
                    p_p = self.pixels[i].outcome_proba_neg
                    p_e = 1-p_e
                for j in range(len(posteriors)):
                    #print(len(posteriors))
                    #print(len(p_p))
                    #print(j)
                    #print(p_p[j])
                    try:
                        posteriors[j] = posteriors[j] * p_p[j]
                    except:
                        print('posteriors:',posteriors,'\n','p_p:',p_p,'\n','j:',j)
                    evidence[j] = evidence[j] * p_e
            else:
                '''This is a new step to determine the probability of the
                evidence based on the prior evidence's observed value.
                Uncomment the following print lines to see that  the probability
                of the evidence is being updated'''
                #print(array[i],array[i-1],self.pixels[i].pixel_proba)
                p_e = self.pixels[i].pixel_proba[int(array[i-1])]
                #print(p_e)
            
                
                if array[i] == 1:
                    if array[i-1] == 0:
                        p_p = self.pixels[i].outcome_proba
                    else:
                        p_p = self.pixels[i].outcome_proba
                else:
                    if array[i-1]  == 0:
                        p_p = self.pixels[i].outcome_proba_neg
                    else:
                        p_p = self.pixels[i].outcome_proba_neg
                    p_e = 1-p_e
                for j in range(len(posteriors)):
                    try:
                        if array[i-1] == 0:
                            posteriors[j] = posteriors[j] * p_p[j][0]
                        else:
                            posteriors[j] = posteriors[j] * p_p[j][1]
                    except:
                        print('posteriors:',posteriors,'\n','p_p:',p_p,'\n','j:',j)
                    evidence[j] = evidence[j] * p_e
        for i in range(len(posteriors)):
            try:
                results.append((posteriors[i]*self.target_proba[i])/evidence[i])
            except:
                results.append(0)
        summation = 0
        for i in results:
            summation+=i
        if summation == 0:
            summation =1
        for i in range(len(results)):
            results[i] = results[i]/summation
        return(results)


bn_clf = bayesian_network(data_matrix,results_array)

#%%
def reshape_data(data):
    '''
    This function rotates a matrix 90 degrees. 
      [[x,x],[y,y]] ->  [[x,y],[x,y]]
    '''
    data_reshaped = []
    for i in range(len(data[0])):
        data_reshaped.append([])
    for i in range(len(data)):
        for j in range(len(data[i])):
            data_reshaped[j].append(data[i][j])
    return(data_reshaped)

test_data = reshape_data(test_matrix)
#%%

confusion_matrix =  [[0,0,0,0,0,0,0,0,0,0],\
                     [0,0,0,0,0,0,0,0,0,0],\
                     [0,0,0,0,0,0,0,0,0,0],\
                     [0,0,0,0,0,0,0,0,0,0],\
                     [0,0,0,0,0,0,0,0,0,0],\
                     [0,0,0,0,0,0,0,0,0,0],\
                     [0,0,0,0,0,0,0,0,0,0],\
                     [0,0,0,0,0,0,0,0,0,0],\
                     [0,0,0,0,0,0,0,0,0,0],\
                     [0,0,0,0,0,0,0,0,0,0],]

correct = 0
incorrect = 0
for i in range(len(test_data)):
    actual  = test_results_array[i]
    class_proba = bn_clf.classify(test_data[i])
    classified_as = class_proba.index(max(class_proba))
    confusion_matrix[int(actual)][(classified_as)]+=1
    if actual == classified_as:
        correct+=1
    else:
        incorrect+=1

#%%
for i in confusion_matrix:
    print(i)
print()
print(correct/(correct+incorrect))