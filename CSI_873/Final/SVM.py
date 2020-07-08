#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 12:44:59 2019

@author: jmcleod
"""

import csv,random,math,decimal,copy, datetime
import numpy as np
from PIL import Image
decimal.getcontext().prec = 100
#from numpy import array
from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt 
import cvxopt


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

def data_import_loop(string,denom):
    '''This function loops the data import across all files of the chosen type,
    which is specified by the string argument passed to the function.
    It then uses the first value in the set to add the imported arrays
    to the correct dictionary key, created with values 0-9. 
    The resulting dictionary is returned.
    '''
    files = []
    results = []
    data_matrix = []
    data_dict = {}
    for i in range(10):
        file_name = string+str(i)+'.txt'
        files.append(file_name)
        data_dict[i]=[]
    for i in files:
        data = data_import(i)
        for j in range(len(data)):
            if j<denom: # SUBSET data 
                data_dict[data[j][0]].append(data[j][1:])
                data_matrix.append(data[j][1:])
                results.append(data[j][0:1][0])
    return(data_dict,results,data_matrix)

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

def subset_data(matrix,array,digits,P,denom):
    matrix_out = []
    array_out = []
    for i in digits:
        bottom = int(denom*i)
        top = bottom + int(denom*P)
        matrix_out = matrix_out +matrix[bottom:top]
        array_out = array_out +array[bottom:top]
    return(matrix_out,array_out)


def subset_test_data(matrix,array,digits,P,denom):
    matrix_out = []
    array_out = []
    for i in digits:
        bottom = int(denom*i)
        top = bottom + int(denom*P)
        matrix_out = matrix_out +matrix[bottom:top]
        array_out = array_out +array[bottom:top]
    return(matrix_out,array_out)

    
def radial_bias(v1,v2):
    x = np.array(v1)-np.array(v2)
    n = math.e**(- 0.05 *(np.linalg.norm(x)**2))
    return(n)

def m_matrix(labels,data):
    m = []
    if len(data) != len(labels):
        print("Error: data length mismatch")
        return(0)
    else:
        for i in range(len(labels)):
            row = []
            for j in range(len(labels)):
                yy = labels[i] * labels[j]
                #print(data[i])
                #print(data[j])
                k = radial_bias(data[i],data[j])
                row.append(yy*k)
            m.append(row)
    #print(m)    
    return(m)

def calc_b(y,alphas,petals):
    alpha_0 = max(alphas)
    alpha_0_index = alphas.index(alpha_0)
    b = 0
    alpha_m = []
    print('Alpha optimal',alpha_0)
    for i in range(len(alphas)):
        if alphas[i]>0.001:

            b +=  y[i] * alphas[i] * radial_bias(petals[i],petals[alpha_0_index])
            alpha_m.append(petals[i])
    b -= y[alpha_0_index]
    return(b,alpha_m)

def clf(ind,b,y,alphas,data,test_data):
    sum_val = 0
    for i in range(len(alphas)):
        if alphas[i] > 0.001:
            sum_val +=  y[i] * alphas[i] * radial_bias(test_data[ind],data[i])
    sum_val -= b
    return(sum_val)

def y_vector(input_vec,target):
    output = []
    for i in input_vec:
        if i == target:
            output.append(1.0)
        else:
            output.append(-1.0)
    return(output)

def qp_vars(data_ys,C,m):
    '''
    This function constructs the Quadratic Program matrices and vectors
    '''
    q = []
    b = []
    G = []
    h = []
    A = []
    P = cvxopt.matrix(m)
    for i in range(len(data_ys)):
        q.append(-1.0)
        b.append(0.0)
        g_row = []
        for  j in range(len(data_ys)):
            if i==j:
                g_row.append(-1.0)
            else: 
                g_row.append(0.0)
        G.append(g_row)
        h.append(0.0)
    for i in range(len(data_ys)):
        row = []
        for j in range(len(data_ys)):
            if i ==j:
                row.append(1.0)
            else: row.append(0.0)
        G.append(row)
        h.append(C)
    q = cvxopt.matrix(q)
    b = cvxopt.matrix(0.0)
    A = cvxopt.matrix(data_ys)
    G = cvxopt.matrix(G)
    G = G.T
    h = cvxopt.matrix(h)
    b  = cvxopt.matrix(b)
    A  = cvxopt.matrix(A)
    A = A.T
    #print(P)
    return(P,q,G,h,A,b)


#%%
'''Data Import'''
denom = 250
data_dict,results,data_matrix = data_import_loop('train',denom)
denom = 250
test_dict,test_results,test_data_matrix = data_import_loop('test',denom)
'''Create sample image of data'''
#create_large_image(data_dict)

#%%

'''This section allows subsetting training examples off'''
subset_matrix,subset_results = subset_data(data_matrix,results,(2,5),1,denom)#(0.5*0.05),denom)
subset_test_matrix,subset_test_results = subset_data(test_data_matrix,test_results,(2,5),1,denom)

#%%
# construct a data matrix and then a vector of y vals
data_m = copy.deepcopy(subset_matrix)
data_ys =  []

for i in subset_results:
    if i==2:
        data_ys.append(1.0)
    else:
        data_ys.append(-1.0)

test_ys = y_vector(subset_test_results,2)
C  = 100
lambda_var = 0.05
m = m_matrix(data_ys,data_m)
m = np.matrix(m)
P,q,G,h,A,b = qp_vars(data_ys,C,m)
sol = cvxopt.solvers.qp(P,q,G,h,A,b)
alphas  = []
for i in sol['x']:
    alphas.append(i)
b,alpha_m  = calc_b(data_ys,alphas,data_m)

# Actual_classified
true_true, true_false, false_true, false_false = 0,0,0,0
for i in range(len(test_ys)):
    y = test_ys[i]
    classification = clf(i,b,data_ys,alphas,subset_matrix,subset_test_matrix)
    if y >= 0:
        if classification >= 0:
            true_true +=1
        else:
            true_false +=1
    else:
        if classification >= 0:
            false_true +=1
        else:
            false_false +=1
    #print(test_ys[i],classification)

print('       True     False')
print('True   ',true_true,'      ',true_false)
print('False  ',false_true,'      ',false_false)
#%%
counter = 0
for i in alphas:
    if i>0.001:
        counter+=1
print(counter)
#%%

'''This section allows eliminating pixels in each training example'''
subset_matrix,subset_results = subset_data(data_matrix,results,(2,5),0.5,denom)
subset_test_matrix,subset_test_results = subset_data(test_data_matrix,test_results,(2,5),1,denom)

keep_one_in = 20

trimmed_subset_matrix = []
trimmed_subset_test_matrix = []
for i in range(len(subset_matrix)):
    row = []
    for j in range(len(subset_matrix[i])):
        if j%keep_one_in == 0:
            row.append(subset_matrix[i][j])
    trimmed_subset_matrix.append(row)
for i in range(len(subset_test_matrix)):
    row = []
    for j in range(len(subset_test_matrix[i])):
        if j%keep_one_in == 0:
            row.append(subset_test_matrix[i][j])
    trimmed_subset_test_matrix.append(row)
subset_matrix = trimmed_subset_matrix
subset_test_matrix = trimmed_subset_test_matrix

# construct a data matrix and then a vector of y vals
data_m = copy.deepcopy(subset_matrix)
data_ys =  []

for i in subset_results:
    if i==2:
        data_ys.append(1.0)
    else:
        data_ys.append(-1.0)

test_ys = y_vector(subset_test_results,2)
C  = 100
lambda_var = 0.05
m = m_matrix(data_ys,data_m)
m = np.matrix(m)
P,q,G,h,A,b = qp_vars(data_ys,C,m)
sol = cvxopt.solvers.qp(P,q,G,h,A,b)
alphas  = []
for i in sol['x']:
    alphas.append(i)
b,alpha_m  = calc_b(data_ys,alphas,data_m)

# Actual_classified
true_true, true_false, false_true, false_false = 0,0,0,0
for i in range(len(test_ys)):
    y = test_ys[i]
    classification = clf(i,b,data_ys,alphas,subset_matrix,subset_test_matrix)
    if y >= 0:
        if classification >= 0:
            true_true +=1
        else:
            true_false +=1
    else:
        if classification >= 0:
            false_true +=1
        else:
            false_false +=1
    #print(test_ys[i],classification)

print('       True     False')
print('True   ',true_true,'      ',true_false)
print('False  ',false_true,'      ',false_false)

#%%

'''This section applies SVD'''
subset_matrix,subset_results = subset_data(data_matrix,results,(2,5),(0.5),denom)
subset_test_matrix,subset_test_results = subset_data(test_data_matrix,test_results,(2,5),1,denom)

# svd  component here:
svd = TruncatedSVD(n_components=(int(784/20)))

svd.fit(subset_matrix)
result = svd.transform(subset_matrix)
subset_matrix = result

svd.fit(subset_test_matrix)
result = svd.transform(subset_test_matrix)
subset_test_matrix = result


# construct a data matrix and then a vector of y vals
data_m = copy.deepcopy(subset_matrix)
data_ys =  []

for i in subset_results:
    if i==2:
        data_ys.append(1.0)
    else:
        data_ys.append(-1.0)

test_ys = y_vector(subset_test_results,2)
C  = 100
lambda_var = 0.05
m = m_matrix(data_ys,data_m)
m = np.matrix(m)
P,q,G,h,A,b = qp_vars(data_ys,C,m)


sol = cvxopt.solvers.qp(P,q,G,h,A,b)
alphas  = []
for i in sol['x']:
    alphas.append(i)
b,alpha_m  = calc_b(data_ys,alphas,data_m)

# Actual_classified
true_true, true_false, false_true, false_false = 0,0,0,0
for i in range(len(test_ys)):
    y = test_ys[i]
    classification = clf(i,b,data_ys,alphas,subset_matrix,subset_test_matrix)
    if y >= 0:
        if classification >= 0:
            true_true +=1
        else:
            true_false +=1
    else:
        if classification >= 0:
            false_true +=1
        else:
            false_false +=1
    #print(test_ys[i],classification)

print('       True     False')
print('True   ',true_true,'      ',true_false)
print('False  ',false_true,'      ',false_false)

#%%
'''This section compares even and odd numbers'''
denom = 500
subset_matrix,subset_results = subset_data(data_matrix,results,(0,1,2,3,4,5,6,7,8,9),.2,denom)
subset_test_matrix,subset_test_results = subset_data(test_data_matrix,test_results,(0,1,2,3,4,5,6,7,8,9),.2,denom)

def modified_y_vector(input_vec,target):
    output = []
    for i in input_vec:
        if i in target:
            output.append(1.0)
        else:
            output.append(-1.0)
    return(output)

# construct a data matrix and then a vector of y vals

data_ys =  modified_y_vector(subset_results,[0,2,4,6,8])
test_ys = modified_y_vector(subset_test_results,[0,2,4,6,8])
#%%
data_m = copy.deepcopy(subset_matrix)
C  = 100
lambda_var = 0.05
m = m_matrix(data_ys,data_m)
m = np.matrix(m)
P,q,G,h,A,b = qp_vars(data_ys,C,m)
sol = cvxopt.solvers.qp(P,q,G,h,A,b)
alphas  = []
for i in sol['x']:
    alphas.append(i)
b,alpha_m  = calc_b(data_ys,alphas,data_m)

# Actual_classified
true_true, true_false, false_true, false_false = 0,0,0,0
for i in range(len(test_ys)):
    y = test_ys[i]
    classification = clf(i,b,data_ys,alphas,subset_matrix,subset_test_matrix)
    if y >= 0:
        if classification >= 0:
            true_true +=1
        else:
            true_false +=1
    else:
        if classification >= 0:
            false_true +=1
        else:
            false_false +=1
    #print(test_ys[i],classification)

print('       True     False')
print('True   ',true_true,'      ',true_false)
print('False  ',false_true,'      ',false_false)
#%%

'''This section compares all different digits and classifies them'''
denom = denom
subset_matrix,subset_results = subset_data(data_matrix,\
                                           results,\
                                           (0,1,2,3,4,5,6,7,8,9),0.2,denom)

subset_test_matrix,subset_test_results = subset_data(test_data_matrix,\
                                                     test_results,\
                                                     (0,1,2,3,4,5,6,7,8,9),\
                                                     0.2,denom)
#%%
def modified_y_vector(input_vec,target):
    output = []
    try:
        for i in input_vec:
            if i in target:
                output.append(1.0)
            else:
                output.append(-1.0)
    except:
        for i in input_vec:
            if i == target:
                output.append(1.0)
            else:
                output.append(-1.0)
    return(output)

# construct a data matrix and then a vector of y vals

data_y_0 =  modified_y_vector(subset_results,0)
data_y_1 =  modified_y_vector(subset_results,1)
data_y_2 =  modified_y_vector(subset_results,2)
data_y_3 =  modified_y_vector(subset_results,3)
data_y_4 =  modified_y_vector(subset_results,4)
data_y_5 =  modified_y_vector(subset_results,5)
data_y_6 =  modified_y_vector(subset_results,6)
data_y_7 =  modified_y_vector(subset_results,7)
data_y_8 =  modified_y_vector(subset_results,8)
data_y_9 =  modified_y_vector(subset_results,9)

data_y_vals  = [data_y_0,data_y_1,data_y_2,data_y_3,\
                data_y_4,data_y_5,data_y_6,data_y_7,\
                data_y_8,data_y_9]

test_y_0 =  modified_y_vector(subset_test_results,0)
test_y_1 =  modified_y_vector(subset_test_results,1)
test_y_2 =  modified_y_vector(subset_test_results,2)
test_y_3 =  modified_y_vector(subset_test_results,3)
test_y_4 =  modified_y_vector(subset_test_results,4)
test_y_5 =  modified_y_vector(subset_test_results,5)
test_y_6 =  modified_y_vector(subset_test_results,6)
test_y_7 =  modified_y_vector(subset_test_results,7)
test_y_8 =  modified_y_vector(subset_test_results,8)
test_y_9 =  modified_y_vector(subset_test_results,9)

test_y_vals = [test_y_0,test_y_1,test_y_2,test_y_3,\
               test_y_4,test_y_5,test_y_6,test_y_7,\
               test_y_8,test_y_9]

data_m = copy.deepcopy(subset_matrix)
#%%
def get_b_alphas(data_ys,data_m):
    C  = 100
    m = m_matrix(data_ys,data_m)
    m = np.matrix(m)
    P,q,G,h,A,b = qp_vars(data_ys,C,m)
    sol = cvxopt.solvers.qp(P,q,G,h,A,b)
    alphas  = []
    for i in sol['x']:
        alphas.append(i)
    b,alpha_m  = calc_b(data_ys,alphas,data_m)
    return(b,alphas)
    
b_alpha_dict = {}
for i in range(0,10):
    b,alpha = get_b_alphas(data_y_vals[i],data_m)
    b_alpha_dict[i] = [b,alpha]

#%%

confusion = []
for i in range(10):
    row = [0]*10
    confusion.append(row)

#%%
all_classifications = []
# Actual_classified
true_true, true_false, false_true, false_false = 0,0,0,0
for i in range(len(test_ys)):
    y = test_ys[i]
    classifications = []
    for k,v in sorted(b_alpha_dict.items()):
        classification = clf(i,b_alpha_dict[k][0],data_y_vals[k],b_alpha_dict[k][1],subset_matrix,subset_test_matrix)
        classifications.append(classification)
    classed = classifications.index(max(classifications))
    #print(subset_test_results[i],classed)
    all_classifications.append(classifications)
    confusion[int(subset_test_results[i])][classed]  +=1
#%%
confusion = []
for i in range(10):
    row = [0]*10
    confusion.append(row)
good =0
bad =0
for i in range(len(all_classifications)):
    classed = all_classifications[i].index(max(all_classifications[i]))
    if classed == subset_test_results[i]:
        good+=1
    else:
        bad+=1
    confusion[int(subset_test_results[i])][int(classed)]  +=1
print(good,bad)
for i in confusion:
    print(i)

#%%
'''
1)  Use the provided discretized hand written digits data sets (both training 
    and testing, scaled between 0 and 1, fractional values are fine).
  DONE

2)  Formulate the dual soft margin SVM in MATLAB by specifying all the required 
    matrices and vectors.
  DONE

3)  Train the dual soft-margin SVM (the one that incorporates a non-separable 
    case) to classify 2s vs. 5s only. Select 500 training data points (250 
    for 2s, 250 for 5s).
    Use the dual radial basis function machine γ = 0.05. Use C = 100 as the 
    penalty parameter. Increase if necessary.
  DONE

4)  Calculate the error/accuracy for testing examples.
  DONE

5)  Reduce the original number of pixels (784) uniformly by 50%, 75%, 90% and 
    95%. Calculate the testing accuracy for all the cases. Describe the 
    observations.
  DONE


6)  Apply the SVD decomposition to the training data to prepare a lower quality 
    data. Reduce the original 784 dimension by 50%, 75%, 90% and 95%. Calculate 
    the testing accuracy for all the cases. Describe the observations.
  DONE

7)  Reduce the original number of number of training examples (500) by 50%, 75%, 
    90% and 95%. Calculate the testing accuracy for all the cases. Describe the 
    observations.
  DONE

8)  Train the dual radial basis function machine γ = 0.05 to classify even vs. 
    odd numbers. Select 1000 training data points (100 for each digit), use all 
    784 pixels. Calculate the error for testing examples.
  DONE

9)  Run 10 SVMs to train to detect a particular digit (e.g. 2) against the rest 
    digits (e.g. 0, 1, 3, 4, 5, 6, 7, 8, 9). In the training use the value 
    y = +1 for a particular digit and y = -1 for the rest of them. Obtain 10 
    different separating hyperplanes h0,...,h9 that separate each 0,1,...,9 
    from the rest digits.

10) While testing the digits you may find out that a particular digit may be 
    classified not uniquely. For example, some tested digit can be on the 
    positive side of h3, h5 and h8, meaning that this digit can be classified 
    as 3, 5 or 8. Alternatively, you may find out that the tested digit is on 
    negative side for all hyperplanes. To resolve the problem classify this 
    digit as the one that corresponds to the hyperplane with the maximum 
    classification number
    
    l
    ∑yα*K(x ,x)−b
    i=1

11) Calculate the error rate. Compare the results with those obtained for the 
    artificial neural network, Bayes naïve classifier, and k-nearest neighbor 
    algorithms.

12) Document your experiments, prepare the report, submit it, and have a great 
    holiday season!



Equations:

Primal:
    
Dual soft margin:
    minimize  0.5(w _dot_ w) +  C*[SUM of E for i=1 to l]
    s.t.
    y_i [(w _dot_ x_i) -b]  >=1-E, for all i
    E >=0
    
    variables: w,b,E
    
Dual:
    max SUM from i=1 to l: alpha_i - .5 SUM i,j to l alpha_i alpha_j y_i y_j (x_i _dot_ x_j)
    s.t.
    SUM i=1 to l a_i y_i = 0
    a_i > 0
    C >= a_i
    
    variables:  a  (which  will be 0 for most vectors but >0 for a few that matter)
    


Optimization Problem:
    min 0.5a^t Ma-e^t a
    s.t.
    y^t a = 0
    a >=  0
    Ce >= a
    
    where M_ij = y_i y_j K (x_i,x_j)
    and K(x_i,x_j) = exp{-||x_i - x_j||^2 } #radial bias function


Explanation of matrix expansions:
    https://math.stackexchange.com/questions/231408/how-to-convert-quadratic-programming-problem-to-matrix-form
    https://stats.stackexchange.com/questions/19181/why-bother-with-the-dual-problem-when-fitting-svm
QP Solver:
    https://pypi.org/project/qpsolvers/
    https://cvxopt.org/examples/tutorial/qp.html
    https://stackoverflow.com/questions/32543475/how-python-cvxopt-solvers-qp-basically-works

Math explanation:
    https://medium.com/@ankitnitjsr13/math-behind-support-vector-machine-svm-5e7376d0ee4d
    https://medium.com/@ankitnitjsr13/math-behind-svm-support-vector-machine-864e58977fdb
    https://math.stackexchange.com/questions/231408/how-to-convert-quadratic-programming-problem-to-matrix-form

'''


#%%
x = ['100%','50%','25%','10%','5%','2.5%','1%','0.5%']
#errors_examples = [8,14,38,124,300]
#errors_pixels = [8,10,23,31,170]
#errors_svd = [8,107,104,93,86,75,121,244]
errors = [8,107,104,93,86,75,121,244]
cis = []
y = []
count = 1000

for i in errors:
    p = 1-(i/count)
    ci = 1.96 * math.sqrt((p*(1-p))/count)
    cis.append(ci)
    y.append(p)
    print('Accuracy:',p)
    print('CI',ci)
    print()
    #print('Lower:',p-ci)
    #print('Upper:',p+ci)
plt.ylim(.5,1)
plt.errorbar(x,y,yerr=cis)
#%%
#p = 1-(66/count)
p = .879
count = 1000
ci = 1.96 * math.sqrt((p*(1-p))/count)

print('Accuracy:',p)
print('CI',ci)
print('Lower:',p-ci)
print('Upper:',p+ci)
#%%
x = ['SVM','KNN','ANN','NB']
y = [0.879,0.922,0.918,0.84]
yerr = [0.879-0.8587864220287451,0.922-0.9167438368975079,0.918-0.9162994698426667,0.84-0.8328145213103092]
plt.errorbar(x,y,yerr=yerr,ls='none',marker='o')






#%%

iris= []
with open('iris.csv',mode='r') as csv_f:
    csv_r = csv.reader(csv_f,delimiter=',')
    for row in csv_r:
        new_row = []
        for i in row:
            try:
                val = float(i)
                new_row.append(val)
            except:
                new_row.append(i)
        iris.append(new_row)
        
sepal_length = []
sepal_width = []
petal_length = []
petal_width = []
species = []
for i in iris[1:]:
    sepal_length.append(i[0])
    sepal_width.append(i[1])
    petal_length.append(i[2])
    petal_width.append(i[3])
    species.append(i[4])

plt.scatter(petal_length[0:50],petal_width[0:50],color='r')
plt.scatter(petal_length[50:100],petal_width[50:100],color='b')
#plt.scatter(petal_length[100:],petal_width[100:],color='g')
plt.show()

small_petal_l = petal_length[0:50] + petal_length[100:]
small_petal_w = petal_width[0:50] + petal_width[100:]
small_species = species[0:50] + species[100:]

plt.scatter(small_petal_l,small_petal_w)

#print(small_species)

y = []
for i in small_species:
    if i == 'setosa':
        y.append(1)
    else:
        y.append(-1)


C  = 100
lambda_var = 0.05



# construct a data matrix and then a vector of y vals
data_matrix = []
data_ys =  []


for i in range(len(small_petal_w)):
    data_matrix.append([small_petal_w[i],small_petal_l[i]])
    if small_species[i] == 'setosa':
        data_ys.append(1)
    else:
        data_ys.append(-1)
        


m = m_matrix(data_ys,data_matrix)
m = np.matrix(m)
print(m)




for i in range(len(y)):
    y[i] = float(y[i])

P = cvxopt.matrix(m)

q = []
b = []
G = []
h = []
A = []
for i in range(len(y)):
    q.append(-1.0)
    b.append(0.0)
    g_row = []
    for  j in range(len(y)):
        if i==j:
            g_row.append(-1.0)
        else: 
            g_row.append(0.0)
    G.append(g_row)
    h.append(0.0)
for i in range(len(y)):
    row = []
    for j in range(len(y)):
        if i ==j:
            row.append(1.0)
        else: row.append(0.0)
    G.append(row)
    h.append(C)


#P = P.T
q = cvxopt.matrix(q)

#b = cvxopt.matrix(b)
b = cvxopt.matrix(0.0)
A = cvxopt.matrix(y)
G = cvxopt.matrix(G)
G = G.T
h = cvxopt.matrix(h)


b  = cvxopt.matrix(b)
A  = cvxopt.matrix(A)
A = A.T

sol = cvxopt.solvers.qp(P,q,G,h,A,b)

print(sol['x'])
print(sol['primal objective'])
for i in range(len(sol['x'])):
    print(i,sol['x'][i])

plt.scatter(small_petal_l,small_petal_w)
plt.show()
a_l = []
a_w = []
for i in range(len(sol['x'])):
    if sol['x'][i]>0:
        a_l.append(small_petal_l[i])
        a_w.append(small_petal_w[i])
plt.scatter(small_petal_l,small_petal_w)
plt.scatter(a_l,a_w,color='b')
plt.scatter(small_petal_l[44],small_petal_w[44],color='r')
plt.scatter(small_petal_l[56],small_petal_w[56],color='r')


alphas  = []
for i in sol['x']:
    alphas.append(i)

b,alpha_m  = calc_b(y,alphas,data_matrix)

for i in range(len(y)):
    classification = clf(i,b,y,alphas,data_matrix)
    print(y[i],classification)

#%%
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    