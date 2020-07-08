#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 15:41:29 2019

@author: jmcleod

CSI-873: Computational Learning

This is an Artificial Neural Network with a single hidden layer of some
specified size. I used it to classify NMIST data for handwritten digits, thus
this file also contains image generation functions to convert the numeric
arrays back into graphics for human review.

The activation function is sigmoid: 1 / 1  + e ^ -z


Things that I initially did wrong in implementing this, and the problems that
were caused because of them:
    
    1) Initialized all weights to the same value. This caused my hidden 
       outputs to all remain identical to each other.
       
    2) Set unrealistic stopping conditions. This caused my model to train 
       indefinitely or to stop far too soon.
       
    3) Did not train long enough manually. This caused the model to essentially
       be as accurate as random guesses.
       
    4) Used binary outputs for hidden neurons. This causes rapid divergence.
    
    5) Removed thbe activation function from hidden neurons. This was before 
       other problems, so I do not know the actual impact other than the 
       optimization making inappropriate steps
"""

import csv,random,math,decimal,copy
import numpy as np
from PIL import Image
decimal.getcontext().prec = 100
import matplotlib.pyplot as plt

#%%

def data_import(file):
    '''
    This function imports the data from a particular file
    and returns an array of arrays
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
                        # The above line scales the data imported
                    row_nums.append(val)
                except:
                    print('ERROR on import: non-numerical data:',row[i])
                    break                    
            data.append(row_nums)
    return(data)

#%%

def data_import_loop(string,denom):
    '''This function loops the data import across all files of the chosen type,
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
            if j%denom==0: # SUBSET data 
                data_dict[data[j][0]].append(data[j][1:])
    return(data_dict)


#%%


def create_image_data(char_matrix):
    '''
    This function outputs a human-viewable copy of an input from matrix form
    '''
    data = np.zeros( (len(char_matrix),len(char_matrix[0]),3), dtype=np.uint8 )
    for row in range(len(char_matrix)):
        for col in range(len(char_matrix[row])):
            val = 255 - char_matrix[col][row]
            data[row,col] = [val,val,val]
    return(data)


#%%

def create_large_image(data_dict):
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



#%%

def randomize_data_arrays(data_dict):
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

#%%

class neuron:
    def __init__(self,input_count,starting_weight,learn_rate):
        self.weights = [starting_weight]*(input_count+1)
        for i in range(input_count+1):
            rando = random.uniform(-starting_weight,starting_weight)
            self.weights[i] = rando
        self.learn_rate=learn_rate
        self.output = 0
        
class output_neuron(neuron):
    def feed_forward(self,input_array):
        x = self.weights[0]
        for i in range(len(input_array)):
            x += float(input_array[i])*float(self.weights[i+1])
        x_out = decimal.Decimal(1)/(decimal.Decimal(1)+(decimal.Decimal(math.e)**(decimal.Decimal(-x)))) # Sigmoid output
        x_out = float(round(x_out,16))
        self.output = x_out
        return(x_out)
    def back_prop(self,t_o,inputs):
        error = self.output * (1 - self.output) * (t_o - self.output)
        for i in range(len(self.weights)):
            try: xji = inputs[i-1]
            except: xji = 1
            self.weights[i] = (self.learn_rate * error * xji) + self.weights[i]

class hidden_neuron(neuron): 
    def feed_forward(self,input_array):
        x = self.weights[0]
        for i in range(len(input_array)):
            x += float(input_array[i])*float(self.weights[i+1])
        x_out = decimal.Decimal(1)/(decimal.Decimal(1)+(decimal.Decimal(math.e)**(decimal.Decimal(-x)))) # Sigmoid output
        x_out = float(round(x_out,16))
        self.output = x_out
        return(x_out)
    def back_prop(self,w_e_term,inputs):
        error = w_e_term * self.output*(1-self.output)
        for i in range(len(self.weights)):
            try: xji = inputs[i-1]
            except: xji = 1
            self.weights[i]= (self.learn_rate * error * xji) + self.weights[i]

class neural_network:
    def __init__(self,dataset,classes,hidden_neurons,output_neurons,\
                 starting_weight=0.1,learn_rate=0.3):
        self.inputs =  len(dataset[0])
        self.dataset = dataset
        self.classes = classes
        self.starting_weight = starting_weight
        self.learn_rate = learn_rate
        self.hidden_layer = []
        self.output_layer  = []
        self.output_errors = []
        for i in range(hidden_neurons):
            self.hidden_layer.append(hidden_neuron(self.inputs,\
                                               self.starting_weight,\
                                               self.learn_rate))
        for i in range(output_neurons):
            self.output_layer.append(output_neuron(len(self.hidden_layer),\
                                               self.starting_weight,\
                                               self.learn_rate))
        self.hidden_x = []
        self.output_x = []

    def feed_forward(self,epoch):
        data_instance = self.dataset[(epoch % len(self.dataset))]
        self.hidden_x = []
        for n in self.hidden_layer:
            self.hidden_x.append(n.feed_forward(data_instance))
        self.output_x = []
        for n in self.output_layer:
            self.output_x.append(n.feed_forward(self.hidden_x))

    def back_prop(self,iteration):
        self.output_errors = []
        hidden_errors = []
        target_class = self.classes[(iteration%len(self.dataset))]
        target_outputs = [0.01]*len(self.output_layer)
        for i in range(len(self.output_layer)):
            if i==target_class:
                target_outputs[i] +=0.98
        for n in range(len(self.output_layer)):
            neuron = self.output_layer[n]
            self.output_errors.append(neuron.output * (1  - neuron.output) * \
                                 (target_outputs[n] - neuron.output))
        for n in range(len(self.hidden_layer)):
            neuron = self.hidden_layer[n]
            output = neuron.output
            pre_error = output * (1-output)
            wk = 0
            for n2 in range(len(self.output_layer)):
                o_neuron = self.output_layer[n2]
                wk += (o_neuron.weights[n+1] * self.output_errors[n2])
            hidden_errors.append(wk * pre_error)
        for n in range(len(self.output_layer)): 
            neuron = self.output_layer[n]
            for w in range(len(neuron.weights)):
                try: xji = self.hidden_x[w-1]
                except: xji = 1
                delta_w = neuron.learn_rate * self.output_errors[n] * xji
                neuron.weights[w] += delta_w
        for n in range(len(self.hidden_layer)):
            neuron =  self.hidden_layer[n]
            for w in range(len(neuron.weights)):
                try: xji = self.dataset[(iteration%len(self.dataset))][w-1]
                except: xji = 1
                delta_w = neuron.learn_rate * hidden_errors[n] * xji #self.output_errors[n]
                neuron.weights[w] += delta_w

    def classify(self,array):
        self.hidden_x = []
        for n in self.hidden_layer:
            self.hidden_x.append(n.feed_forward(array))
        self.output_x = []
        for n in self.output_layer:
            self.output_x.append(n.feed_forward(self.hidden_x))
        classification = 0
        value = 0
        for i in range(len(self.output_x)):
            if self.output_x[i]>=value:
                classification = i
                value = self.output_x[i]
        return(classification)

#%%

def measure_model(test_set,test_answers,model):
    total = 0
    correct  = 0
    for n in range(len(test_answers)):
        rando = random.random()
        if rando > 0.90:
            classification = model.classify(test_set[n])
            actual_class = test_answers[n]
            if classification == actual_class:
                correct+=1
            total+=1
    return(correct/total)

#%%
        
'''Data Import'''
denom = 2
data_dict = data_import_loop('train',denom)
denom = 2
test_dict = data_import_loop('test',denom)

#%%

'''Check Data Import'''
for k,v in data_dict.items():
    print(k,len(v),len(v[0]))
print()
for k,v in test_dict.items():
    print(k,len(v),len(v[0]))
    
#%%

'''Create sample image of data'''
create_large_image(data_dict)

#%%

'''Randomize the order of the data'''
data_array,data_result = randomize_data_arrays(data_dict)
test_array,test_result = randomize_data_arrays(test_dict)

#%%

'''Instatiate the NN'''
ann = neural_network(data_array,data_result,6,10)

#%%
n=0
#%%
'''Iterate through a small subset of the training data for testing'''
for i in range(1000):
    ann.feed_forward(n)
    ann.back_prop(n)
    n+=1

ann.output_x
#%%
    
'''Iterate through the data n times for better training:'''
# Todo: create loop based on stopping condition instead of specified training amount
n =  len(data_result)*100
prior_result = 0
for i in range(n):
    if i%(len(data_result)/10)==0 and i>0:
        print(i)
    ann.feed_forward(i)
    ann.back_prop(i)
    if i%(len(data_result)/10)==0 and i>0:
        new_result = measure_model(test_array,test_result,ann)
        print('current accuracy:',new_result)
        if new_result > prior_result:
            prior_result = new_result
        else:
            print('it got worse')
        print('done verifying prior')
    #if prior == ann.output_x:
    #    break
    #prior = ann.output_x
    
#%%
    
accuracy_results_dict  = {}
for h_i in range(10,21):
    print('Hidden neurons:',h_i)
    if h_i > 10:
        hidden_count = (h_i-9)*10
    else:
        hidden_count = h_i
    ann = neural_network(data_array,data_result,hidden_count,10)
    accuracy_results_dict[hidden_count] = []
    prior_result = 0
    report = 2
    power = 7
    for i in range((2**14)+1):
        ann.feed_forward(i)
        ann.back_prop(i)
        if i==report**power:
            
            result = measure_model(test_array,test_result,ann)
            accuracy_results_dict[hidden_count].append(result)
            print('Training iterations: %9d  Accuracy: %4f'%(i,result))
            power +=1
#%%
accuracy_results_dict  = {}
for h_i in range(10):
    print('Hidden neurons:',h_i)
    hidden_count = 10
    ann = neural_network(data_array,data_result,hidden_count,10)
    accuracy_results_dict[h_i] = []
    prior_result = 0
    report = 2
    power = 7
    for i in range((2**20)+1):
        ann.feed_forward(i)
        ann.back_prop(i)
        if i==report**power:
            result = measure_model(test_array,test_result,ann)
            accuracy_results_dict[h_i].append(result)
            print('Training iterations: %9d  Accuracy: %4f'%(i,result))
            power +=1
#%%

with open('outputfile3.csv', mode='w') as csvfile:
    csv_r = csv.writer(csvfile,delimiter=',')
    csv_r.writerow(['The output starts at 128 iterations of training and reports at each power of 2'])
    for k,v in accuracy_results_dict.items():
        row = [k]
        for i in v:
            row.append(i)
        csv_r.writerow(row)
#%%
        


#%%
labs = []
for i in range(8):
    labs.append(2**(i+7))
plt.figure(figsize=(15,9))
for k,v in accuracy_results_dict.items():
    if k < 2:
        string = str(k)+' Hidden Neuron'
    else:
        string = str(k)+' Hidden Neurons'
    plt.plot(v,label=string)
plt.xticks(np.arange(8),labs,rotation=45)
plt.legend(loc='upper left')

plt.show()
#%%
        
'''Print weights'''
for i in ann.output_layer:
    print(i.weights)
print()
#for i in ann.hidden_layer:
#    print(max(i.weights))

#%%

n = 1
#%%
classification = ann.classify(data_array[n])
print(classification,data_result[n])
ann.output_x
n+=1
#%%
'''Classify a specific input'''
correct = 0
incorrect = 0
for i in range(len(test_array)):
    if i%(len(test_array)/20) == 0:
        print(i,len(test_array))
    classification = ann.classify(test_array[i])
    if classification ==  test_result[i]:
        correct+=1
    else:
        incorrect+=1

print('Ratio:',correct/(correct+incorrect))
    


#%%

''' Create an image of a specific input
    Useful after the above classification command 
    in order to see the image being classified'''
    
def create_small_image_data(char_matrix):
    # This function outputs a human-viewable copy of an input from matrix form
    data = np.zeros( (len(char_matrix),len(char_matrix[0]),3), dtype=np.uint8 )
    for row in range(len(char_matrix)):
        for col in range(len(char_matrix[row])):
            #print(col,row,len(char_matrix),len(char_matrix[0]))
            val = 255- (255 * char_matrix[row][col])
            data[row,col] = [val,val,val]
    return(data)


def create_image(data_array):
    matrix = []
    #rint(data_array)
    for i in range(28):
        row = data_array[i*28:i*28+28]
        matrix.append(row)
    image_matrix = create_small_image_data(matrix)
    image = Image.fromarray(image_matrix)
    image.show()


create_image(data_array[n])
print(data_result[n])