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


def create_image_data(char_matrix):
    '''
    This function outputs a human-viewable copy of an input from matrix form
    '''
    data = np.zeros( (len(char_matrix),len(char_matrix[0]),3), dtype=np.uint8 )
    for row in range(len(char_matrix)):
        for col in range(len(char_matrix[row])):
            #print(col,row,len(char_matrix),len(char_matrix[0]))
            val = 255 - char_matrix[col][row]
            data[row,col] = [val,val,val]
    return(data)


def create_large_image(data_dict):
    '''
    This function just creates an image from the data using 10 of each
    input variable and all ten inputs for a 10x10 image instead of a single
    input
    '''
    shortest = 1000000
    for k,v in data_dict.items():
        if len(v) < shortest:
            shortest = len(v)
    big_matrix_data = []
    for m in range(10):
        medium_matrix_data = []
        for i in range(28):
            medium_matrix_data.append([])
        for i in range(10):
            random_num = random.randint(0,shortest-1)
            array = data_dict[m][random_num]
            for j in range(len(array)):
                medium_matrix_data[j%28].append((array[j]*255))
        for i in medium_matrix_data:
            big_matrix_data.append(i)
    big_image = create_image_data(big_matrix_data)
    image = Image.fromarray(big_image)
    image.show()


def randomize_data_arrays(data_dict):
    '''
    This function is a hold-over from the NN I created; it needed randomized
    data. While the Naive Bayes classifier doesn't need the data to be 
    randomized, I kept this so that my sets would be easier to spot check
    a number of different features easily. In practice, I would remove this
    to reduce the computational expense of the algorithm.
    '''
    data_array = []
    data_result = []
    for k,v in data_dict.items():
        for i in v:
            data_result.append(k)
            data_array.append(i)
    random_index = []
    for i in range(len(data_array)):
        random_index.append(random.random())
    random_index_copy = copy.deepcopy(random_index)
    rand_data_array = []
    rand_data_result = []
    for i in range(len(random_index)):
        min_val = min(random_index_copy)
        random_index_copy.pop(random_index_copy.index(min_val))
        index_val = random_index.index(min_val)
        rand_data_array.append(data_array[index_val])
        rand_data_result.append(data_result[index_val])
    data_array = rand_data_array
    data_result = rand_data_result
    return(data_array,data_result)


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

    def update_probas(self,array,target):
        pos_count_dict,neg_count_dict = {},{}
        count_0,count_1 = 0,0
        
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
    
class naive_bayes:
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
            self.pixels[i].update_probas(data[i],target)
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
            p_e = self.pixels[i].pixel_proba
            if array[i] == 1:
                p_p = self.pixels[i].outcome_proba
            else:
                p_p = self.pixels[i].outcome_proba_neg
                p_e = 1-p_e
            for j in range(len(posteriors)):
                posteriors[j] = posteriors[j] * p_p[j]
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


#%%

        
'''
Data Import
Denom is a variable used to determine how much of the data to import: 1/denom
The string values 'train' and 'test' are for the filenames.
'''
denom = 1
data_dict = data_import_loop('train',denom)
denom = 2
test_dict = data_import_loop('test',denom)



'''
Check Data Import
This prints the counts of observations in the training and test sets by class,
as well as the length of each for verification.
'''
for k,v in data_dict.items():
    print(k,len(v),len(v[0]))
print()
for k,v in test_dict.items():
    print(k,len(v),len(v[0]))
    


'''
Create sample image of data: I used this just to help me visualize the data
'''
create_large_image(data_dict)



'''
Randomize the order of the data
This is a hold-over from the NN data handling, but randomizing the data made it
simpler for the to test individual observations of various characters while
prototyping, so I kept it.
'''
data_array,data_result = randomize_data_arrays(data_dict)
test_array,test_result = randomize_data_arrays(test_dict)


'''
Reshaping the data for the Naive Bayes classifier
The data needed to be rotated in order to reduce the loops needed to train.
'''
data_reshaped = reshape_data(data_array)
test_reshaped = reshape_data(test_array)

'''Instantiating the naive bayes Python Class object'''
nb_clf = naive_bayes(data_reshaped,data_result)

#%%
''' A loop to run the Naive Bayes classifier on the test data and stores
various forms out output data'''
classified_as  = []
for i in range(10):
    row  = []
    for j in range(10):
        row.append(0)
    classified_as.append(row)

correct = 0
correct_dict = {}
totals_dict = {}
tested = len(test_result)
for i in range(len(test_result)):
    if test_result[i] not in totals_dict:
        totals_dict[test_result[i]]=1
    else:
        totals_dict[test_result[i]]+=1
    result = nb_clf.classify(test_array[i])
    output = result.index(max(result))
    if output == test_result[i]:
        correct +=1
        if output not in correct_dict:
            correct_dict[output] = 1
        else:
            correct_dict[output] += 1
    classified_as[test_result[i]][output]+=1
#%%
'''Print a confusion matrix: rows are actual classes (by index) and columns are
classifications by the model'''
for i in classified_as:
    print(i)

#%%
x = []
y = []
yerr = []

'''Printing the output of the Naive Bayes classifier'''

print("\nOut of",tested,"tests,",correct,"were correct, a ratio of",str(correct/tested)+".\n")
print("Class  Total  Correct  Ratio      95% Confidence Interval")
for k,v in sorted(totals_dict.items()):
    ratio = correct_dict[k]/v
    interval = 1.96*math.sqrt((ratio*(1-ratio))/v)
    print("%5d  %5d    %5d  %f    %f-to-%f"%\
          (k,v,correct_dict[k],ratio,ratio-interval,ratio+interval))
    x.append(k)
    y.append(ratio)
    yerr.append(interval)
print()


'''Print a visualization of the resulting errors'''
plt.errorbar(x, y, yerr=yerr,fmt='o')
plt.ylim(0.6,1)
plt.xticks(x)


#plt.legend(loc='lower right')
plt.show()