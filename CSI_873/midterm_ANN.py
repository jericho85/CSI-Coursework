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
"""

import csv,random,math,decimal,copy
import numpy as np
from PIL import Image
decimal.getcontext().prec = 100


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

def create_large_image(data_dict):
    '''This function creates an NxN image of 10 examples of 10 classes'''
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
    ''' This is a function to randomize the order of training and test data'''
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

class neuron:
    def __init__(self,input_count,starting_weight,learn_rate):
        self.weights = [starting_weight]*(input_count+1)
        self.delta_weights = [0]*(input_count+1)
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
    def back_prop(self,t_o,inputs,momentum):
        error = self.output * (1 - self.output) * (t_o - self.output)
        for i in range(len(self.weights)):
            try: xji = inputs[i-1]
            except: xji = 1
            prior_weight_delta = self.delta_weights[i]
            self.weights[i] = (self.learn_rate * error * xji) + self.weights[i] + (momentum * prior_weight_delta)
            self.delta_weights[i] = self.learn_rate * error * xji

class hidden_neuron(neuron): 
    def feed_forward(self,input_array):
        x = self.weights[0]
        for i in range(len(input_array)):
            x += float(input_array[i])*float(self.weights[i+1])
        x_out = decimal.Decimal(1)/(decimal.Decimal(1)+(decimal.Decimal(math.e)**(decimal.Decimal(-x)))) # Sigmoid output
        x_out = float(round(x_out,16))
        self.output = x_out
        return(x_out)
    def back_prop(self,w_e_term,inputs,momentum):
        error = w_e_term * self.output*(1-self.output)
        for i in range(len(self.weights)):
            try: xji = inputs[i-1]
            except: xji = 1
            prior_weight_delta = self.delta_weights[i]
            self.weights[i]= (self.learn_rate * error * xji) + self.weights[i] + (prior_weight_delta * momentum)
            self.delta_weights[i] = self.learn_rate * error * xji

class neural_network:
    def __init__(self,dataset,classes,hidden_neurons,output_neurons,\
                 starting_weight=0.1,learn_rate=0.3,momentum = 0.6):
        self.inputs =  len(dataset[0])
        self.dataset = dataset
        self.classes = classes
        self.starting_weight = starting_weight
        self.learn_rate = learn_rate
        self.momentum = momentum
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
        delta_weights = []
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
                delta_weights.append(delta_w)
                neuron.weights[w] += (delta_w + self.momentum * neuron.delta_weights[w])
                neuron.delta_weights[w] = delta_w
        for n in range(len(self.hidden_layer)):
            neuron =  self.hidden_layer[n]
            for w in range(len(neuron.weights)):
                try: xji = self.dataset[(iteration%len(self.dataset))][w-1]
                except: xji = 1
                delta_w = neuron.learn_rate * hidden_errors[n] * xji #self.output_errors[n]
                delta_weights.append(delta_w)
                neuron.weights[w] += (delta_w + self.momentum * neuron.delta_weights[w])
                neuron.delta_weights[w] = delta_w
        return(delta_weights)

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

def measure_model(test_set,test_answers,model):
    '''This function determines the accuracy of a model by classifying the
    test data'''
    total = 0
    correct  = 0
    for n in range(len(test_answers)):
        rando = random.random()
        if rando > 0: #set to higher value to subset data
            classification = model.classify(test_set[n])
            actual_class = test_answers[n]
            if classification == actual_class:
                correct+=1
            total+=1
    return(correct/total)

def conf_matrix_shell():
    '''This function just returns an empty NxN matrix'''
    matrix = []
    for i in range(10):
        row=[]
        for j in range(10):
            row.append(0)
        matrix.append(row)
    return(matrix)

def get_conf_matrix(test_set,test_answers,model):
    '''This function uses the NxN matrix created above and adds
    observed classifications'''
    matrix = conf_matrix_shell()
    for n in range(len(test_answers)):
        rando = random.random()
        if rando > 0: #adjust to subset data
            classification = model.classify(test_set[n])
            actual_class = test_answers[n]
            matrix[actual_class][classification]+=1
    return(matrix)

def get_weights_image_vector(model): 
    hidden_weights = []
    output_weights = []
    pixel_weights = {}
    for i in model.hidden_layer:
        hidden_weights.append(i.weights[1:])
    for i in model.output_layer:
        output_weights.append(i.weights[1:])

    for out in range(len(output_weights)):
        vector = []
        for i in range(len(hidden_weights[0])):
            vals,val = [],0
            for h in hidden_weights:
                vals.append(h[i])

            for o in range(len(output_weights[out])): #
                vals[o] = vals[o] * output_weights[out][o] #
            for v in vals:
                val += v
            vector.append(val)
        pixel_weights[out] = vector
    return(pixel_weights)

def min_max_array(array):
    out = []
    for i in array:
        v = (i-min(array)) / (max(array)-min(array))
        out.append(v)
    return(out)


def alt_min_max(array):
    out,temp = [],[]
    for i in array:
        if i>=0:
            temp.append(i)
        else:
            temp.append(i*-1)
    for i in temp:
        v = (i-min(temp)) / (max(temp)-min(temp))
        out.append(v)
    return(out)



    
def create_small_image_data(char_matrix):
    ''' Create an image of a specific input
    Useful after the above classification command 
    in order to see the image being classified'''
    data = np.zeros( (len(char_matrix),len(char_matrix[0]),3), dtype=np.uint8 )
    for row in range(len(char_matrix)):
        for col in range(len(char_matrix[row])):
            #print(col,row,len(char_matrix),len(char_matrix[0]))
            val = 255- (255 * char_matrix[row][col])
            data[row,col] = [val,val,val]
    return(data)


def create_image(data_array,name):
    matrix = []
    for i in range(int(len(data_array)/28)):
        row = data_array[i*28:i*28+28]
        matrix.append(row)
    image_matrix = create_small_image_data(matrix)
    image = Image.fromarray(image_matrix)
    filename = str(name)+'.jpg'
    image.save(filename)

    

def create_single_array(model,i):
    ''' Creates the array for weights images'''
    pixel_weights = get_weights_image_vector(model)
    blank_row = [0]*28
    temp_vec1 = min_max_array(pixel_weights[0])
    temp_vec2 = min_max_array(pixel_weights[1])
    temp_vec3 = min_max_array(pixel_weights[2])
    temp_vec4 = min_max_array(pixel_weights[3])
    temp_vec5 = min_max_array(pixel_weights[4])
    temp_vec6 = min_max_array(pixel_weights[5])
    temp_vec7 = min_max_array(pixel_weights[6])
    temp_vec8 = min_max_array(pixel_weights[7])
    temp_vec9 = min_max_array(pixel_weights[8])
    temp_vec10 = min_max_array(pixel_weights[9])
    temp_array = temp_vec1+blank_row+\
                 temp_vec2+blank_row+\
                 temp_vec3+blank_row+\
                 temp_vec4+blank_row+\
                 temp_vec5+blank_row+\
                 temp_vec6+blank_row+\
                 temp_vec7+blank_row+\
                 temp_vec8+blank_row+\
                 temp_vec9+blank_row+\
                 temp_vec10+blank_row
    create_image(temp_array,i)


def main():
    '''Data Import'''
    denom = 1
    data_dict = data_import_loop('train',denom)
    denom = 1
    test_dict = data_import_loop('test',denom)
    '''Create sample image of data'''
    create_large_image(data_dict)
    '''Randomize the order of the data'''
    data_array,data_result = randomize_data_arrays(data_dict)
    test_array,test_result = randomize_data_arrays(test_dict)
    file_output = []
    for i in range(2,11):
        prior_ann = 0
        prior_accuracy = 0
        prior_accs = []
        stop = 0
        powers = 8
        data_instance = 0
        ann = neural_network(data_array,data_result,i,10)
        name = str(i)+'_nodes_'+str(data_instance)+'_iters'
        create_single_array(ann,name)
        while stop < 1:
            for n in range(2**powers-data_instance):
                ann.feed_forward(data_instance)
                ann.back_prop(data_instance)
                data_instance+=1
            name = str(i)+'_nodes_'+str(data_instance)+'_iters'
            create_single_array(ann,name)
            result = measure_model(test_array,test_result,ann)
            prior_accs.append(result)
            print('Nodes: %d  Iterations: %d   Accuracy: %4f'%(i,data_instance,result))
            file_output.append(['Nodes: %d  Iterations: %d   Accuracy: %4f'%(i,data_instance,result)])
            powers+=1
            delta_acc = result - prior_accuracy
            print(result,prior_accuracy,delta_acc)
            if delta_acc < 0: delta_acc = delta_acc * -1
            if delta_acc < .005 and data_instance > 8200: #stopping condition on drop in accuracy
                stop+=1
            elif len(prior_accs) > 2:
                if prior_accs[-1]<prior_accs[-2] and  prior_accs[-2] < prior_accs[-3]: #stopping condition for 10% decrease in accuracy with rewind to prior ANN
                    stop+=1
                    ann = prior_ann
            else:
                prior_accuracy = result
            prior_ann = copy.deepcopy(ann)
            if powers > 15: #upper bound on iterations to train
                stop+=1
        confusion_matrix = get_conf_matrix(test_array,test_result,ann)
        print()
        print('Hidden Nodes:',i)
        print('Accuracy:',result)
        print('Confusion Matrix:')
        for i in confusion_matrix:
            print(i)
        print()
        file_output.append([])
        file_output.append(['Hidden Nodes:',i])
        file_output.append(['Accuracy:',result])
        file_output.append(['Confusion Matrix:'])
        for i in confusion_matrix:
            file_output.append(i)
        file_output.append([])
        
    with open('output_filename.csv', mode='w') as csvfile:
        csv_r = csv.writer(csvfile,delimiter=',')
        for row in file_output:
            csv_r.writerow(row)
    
if __name__ == '__main__':
    main()