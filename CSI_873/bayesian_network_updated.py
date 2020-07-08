#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 13:44:27 2019

@author: jmcleod
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 17:53:47 2019

@author: jmcleod

This is a Naive Bayes classifier that resuses the data import from the ANN. It
was also used to classify NMIST data. This system is relatively trivial to
implement compared to ANNs, so far fewer problems were encountered.

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
    
#%%

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
    

#%%
    
class first_pixel:
    def __init__(self):
        self.proba = [[],[],[],[],[],[],[],[],[],[]]
    
    def update_proba(self,current,outcome,outcome_probas):
        counts = [0,0] # [0,1]
        o_c = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
        for i in range(len(current)):
            if current[i]==1:
                counts[1]+=1
                o_c[outcome[i]][1]+=1
            else:
                counts[0]+=1
                o_c[outcome[i]][0]+=1
        final = []
        for i in o_c:
            a = i[0]/(i[0]+i[1])
            b = i[1]/(i[0]+i[1])
            final.append([a,b])
        self.proba = final
        

class pixel:
    def __init__(self):
        self.proba = []
    
    def update_probas(self,current,prior,outcome,outcome_probas):
        p_c = [0,0] # [p0,p1] p_c = prior counts
        c_c = [0,0,0,0] # [p0c0,p1c0,p0c1,p1c1] c_c = current probabilities
        o_c = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],\
                          [0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]] 
                            # [0[p0c0,p1c0,p0c1,p1c1], 1[p0c0,p1c0,p0c1,p1c1] ]
        for i in range(len(current)):
            if prior[i] == 0: 
                p_c[0] +=1
                if current[i] == 0:
                    c_c[0] +=1
                    o_c[outcome[i]][0] +=1
                elif current[i] == 1:
                    c_c[2] +=1
                    o_c[outcome[i]][2] +=1
            elif prior[i] == 1:
                p_c[1] +=1
                if current[i] == 0:
                    c_c[1] +=1
                    o_c[outcome[i]][1] +=1
                elif current[i] ==1:
                    c_c[3] +=1
                    o_c[outcome[i]][3] +=1
        #print(c_c)
        #print(o_c)
        final = []
        for i in o_c:
            temp = [0,0,0,0]
            try:
                temp[0] = i[0]/(i[0]+i[2])
            except: i[0]=0
            try:
                temp[1] = i[1]/(i[1]+i[3])
            except: i[1]=0
            try:
                temp[2] = i[2]/(i[0]+i[2])
            except: i[2]=0
            try:
                temp[3] = i[3]/(i[1]+i[3])
            except:
                temp[3] = 0
            final.append(temp)
        #print(final)
        '''
        for i in o_c:
            temp = [0,0,0,0]
            try:
                i[0] = i[0]/c_c[0]
            except: i[0]=0
            try:
                i[1] = i[1]/c_c[1]
            except: i[1]=0
            try:
                i[2] = i[2]/c_c[2]
            except: i[2]=0
            try:
                i[3] = i[3]/c_c[3]

        try:
            c_c[0]=c_c[0]/p_c[0]
        except: c_c[0]=0
        try:
            c_c[1]=c_c[1]/p_c[1]
        except: c_c[1]=0
        try:
            c_c[2]=c_c[2]/p_c[0]
        except: c_c[2]=0
        try:
            c_c[3]=c_c[3]/p_c[1]
        except: c_c[3]=0

        #c_p = [c_c[0]/p_c[0],c_c[1]/p_c[1],c_c[2]/p_c[0],c_c[3]/p_c[1]]
        o_p = []
        for i in range(len(o_c)):
            current_out = []
            for j in range(len(o_c[i])):
                try:
                    post = o_c[i][j]/(c_c[j])
                    apr = outcome_probas[i]
                    current_out.append(post/apr)
                except:
                    current_out.append(0)
            o_p.append(current_out)
            '''
#        print('outcome probabilities',outcome_probas)
#        print()
#        print('prior counts',p_c)
#        print()
#        print('current probas',c_c)
#        print()
#        print(o_c)
#        print()
        #for i in o_p:
        #    print(i)
        #print(o_p)
        self.proba = final
            

class bayesian_network:
    def __init__(self,data_matrix,results_array):
        self.prior_probas=[]
        self.data_matrix = data_matrix
        self.results_array = results_array
        self.pixels = []
    
    def calc_prior_proba(self):
        outcome_probas = []
        counts_dict = {}
        for i in self.results_array:
            if i not in counts_dict:
                counts_dict[i]=1
            else:
                counts_dict[i]+=1
        for k,v in sorted(counts_dict.items()):
            outcome_probas.append(v/len(results_array))
        self.prior_probas = outcome_probas
    
    def fit_pixels(self):
        for i in range(len(self.data_matrix)):
            if i == 0:
                pix = first_pixel()
                pix.update_proba(self.data_matrix[i],self.results_array,self.prior_probas)
            else:
                pix = pixel()
                pix.update_probas(self.data_matrix[i],self.data_matrix[i-1],self.results_array,self.prior_probas)
            self.pixels.append(pix)
    
    def classify(self,input_array):
        numerator = [0,0,0,0,0,0,0,0,0,0]
        denominator =  [0,0,0,0,0,0,0,0,0,0]
        probabilities = [[],[],[],[],[],[],[],[],[],[]]
        for i in range(len(input_array)):
            if i == 0:
                for j in range(len(self.pixels[i].proba)):
                    vals = self.pixels[i].proba[j]
                    cur_val = int(input_array[i])
                    numerator[j]=(vals[cur_val])
                    denominator[j]=((vals[cur_val]+vals[1-cur_val]))
            else: #[p0c0,p1c0,p0c1,p1c1]
                #print(self.pixels[i].proba)
                for j in range(len(self.pixels[i].proba)):
                    vals =  self.pixels[i].proba[j]
                    cur_val  = int(input_array[i])
                    pr_val = int(input_array[i-1])
                    if pr_val == 0:
                        den = vals[0]+vals[2]
                        if cur_val  == 0:
                            num = vals[0]
                        elif cur_val ==1:
                            num = vals[2]
                    elif pr_val == 1:
                        den = vals[1]+vals[3]
                        if cur_val == 0:
                            num =vals[1]
                        elif cur_val ==1:
                            num = vals[3]
                            
                    #print(num,den)
                    if num !=1:
                    
                    #print(numerator[j],denominator[j])
                    #print('before',numerator[j],denominator[j])
                        numerator[j] =  numerator[j] * num
                        denominator[j]= denominator[j] * den
                    #print('after',numerator[j],denominator[j],'\n')
        print(numerator,denominator)
                    
        
        
bn = bayesian_network(data_matrix,results_array)
bn.calc_prior_proba()
bn.fit_pixels()
bn.classify(test_matrix[91])
#%%
pix = pixel()
pix.update_probas(data_matrix[100],data_matrix[99],results_array,outcome_probas)
#for i in pix.proba:
#    print(i)
fpix = first_pixel()
fpix.update_proba(data_matrix[0],results_array,outcome_probas)
fpix.proba
bn = bayesian_network(data_matrix,results_array)
bn.calc_prior_proba()
bn.fit_pixels()
#%%
for i in bn.pixels:
    print(i.proba)
        
#%%

denom = 200
data_dict = data_import_loop('train',denom)
denom = 100
test_dict = data_import_loop('test',denom)

for k,v in data_dict.items():
    print(k,len(v))

print()
for k,v in test_dict.items():
    print(k,len(v))
#%%
data_matrix,results_array = reshape_data(data_dict)
test_matrix,test_results_array = reshape_data(test_dict)
#%%
outcome_probas = []
counts_dict = {}
for i in results_array:
    if i not in  counts_dict:
        counts_dict[i]=1
    else:
        counts_dict[i]+=1
for k,v in sorted(counts_dict.items()):
    outcome_probas.append(v/len(results_array))
    

#%%
pix = pixel()
pix.update_probas(data_matrix[200],data_matrix[199],results_array,outcome_probas)
#%%
pix.proba