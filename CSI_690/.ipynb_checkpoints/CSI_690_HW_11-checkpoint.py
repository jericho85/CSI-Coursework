# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 19:10:58 2018

@author: jmcle
"""

import numpy as np

plate = [[0,0,0],\
         [0,0,0],\
         [0,0,0]]

def return_neighbors(i,j):
    bott = [i+1,j]
    top = [i-1,j]
    right = [i,j+1]
    left = [i,j-1]
    return(top,bott,left,right)


def calc_temp(neighbors): #pass neighbor temps as a list
    temp = 0
    for i in neighbors:
        temp+=i
    temp=temp/4
    return(temp)


def fetch_temp(i,j,plate):
    if i < 0: temp = 0
    elif i > 2: temp = 150
    elif j > 2: temp = 50
    elif j < 0:
        j = 1
        temp = plate[i][j]
    else: temp = plate[i][j]
    return(temp)  


def update_plate(plate):
    tempplate = [[0,0,0],[0,0,0],[0,0,0]]
    for i in range(len(plate)):
        for j in range(len(plate)):
            top,bott,left,right = return_neighbors(i,j)
            temp_list = []
            temp_list.append(fetch_temp(top[0],top[1],plate))
            temp_list.append(fetch_temp(bott[0],bott[1],plate))
            temp_list.append(fetch_temp(right[0],right[1],plate))
            temp_list.append(fetch_temp(left[0],left[1],plate))
            new_temp = calc_temp(temp_list)
            tempplate[i][j]=new_temp
    return(tempplate)


def iterate_updates(plate):
    stop=0
    error = [[1,1,1],[1,1,1],[1,1,1]]
    while stop == 0:
        old_aij = plate
        plate = update_plate(plate)
        npplate = np.matrix(plate)
        print('\n',npplate)
        new_aij = plate
        error_list = []
        for i in range(0,3):
            for j in range(0,3):
                try:
                    error[i][j]= abs((new_aij[i][j]-old_aij[i][j])/new_aij[i][j])
                    error_list.append(error[i][j])
                except: 
                    error[i][j]=1
                    error_list.append(1)
        if max(error_list) < 0.01:
            stop+=1
        print(error)
    return(plate)


plate = iterate_updates(plate)

npplate = np.matrix(plate)
print('\n',npplate)
print(plate)

#%%
import math

plate =[[150,150,150,150,150],\
        [102.87671299, 105.57117807, 102.87671299, 90.73201739,50],\
        [65.83726878, 67.41672103, 65.83726878, 60.4940746,50],\
        [33.64596359, 33.45581769, 33.64596359, 35.9243372,50],\
        [0,0,0,0,0]]

def calc_qx(plate,i,j):
    qx = -(plate[i+1][j]-plate[i-1][j])/2
    return(qx)
    
def calc_qy(plate,i,j):
    qy = -(plate[i][j+1]-plate[i][j-1])/2
    return(qy)

def calc_qn_dir(plate,i,j):
    qx,qy = calc_qx(plate,i,j),calc_qy(plate,i,j)
    qx2_qy2 = qx**2+qy**2
    qn = qx2_qy2**.5
    if qx > 0:
        theta = math.atan(qy/qx)
    elif qx < 0:
        theta = math.atan(qy/qx) + math.pi
    return(qn,theta)

for i in range(1,4):
    for j in range(1,4):
        qn,theta = calc_qn_dir(plate,i,j)
        theta_d = theta*180/math.pi
        print(plate[i][j],qn,theta_d)
        print()

#%% 29.8

plate = [[0,0,0],\
         [0,0,0],\
         [0,0,0]]

def return_neighbors(i,j):
    bott = [i+1,j]
    top = [i-1,j]
    right = [i,j+1]
    left = [i,j-1]
    return(top,bott,left,right)


def calc_temp(neighbors): #pass neighbor temps as a list
    temp = 0
    for i in neighbors:
        temp+=i
    temp=temp/4
    return(temp)


def fetch_temp(i,j,plate):
    if i < 0: 
        i = 1
        temp = plate[i][j]
    elif i > 2: temp = 100
    elif j > 2: temp = 50
    elif j < 0: temp = 75
    else: temp = plate[i][j]
    return(temp)  


def update_plate(plate):
    tempplate = [[0,0,0],[0,0,0],[0,0,0]]
    for i in range(len(plate)):
        for j in range(len(plate)):
            top,bott,left,right = return_neighbors(i,j)
            temp_list = []
            temp_list.append(fetch_temp(top[0],top[1],plate))
            temp_list.append(fetch_temp(bott[0],bott[1],plate))
            temp_list.append(fetch_temp(right[0],right[1],plate))
            temp_list.append(fetch_temp(left[0],left[1],plate))
            new_temp = calc_temp(temp_list)
            tempplate[i][j]=new_temp
    return(tempplate)


def iterate_updates(plate):
    stop=0
    error = [[1,1,1],[1,1,1],[1,1,1]]
    while stop == 0:
        old_aij = plate
        plate = update_plate(plate)
        npplate = np.matrix(plate)
        print('\n',npplate)
        new_aij = plate
        error_list = []
        for i in range(0,3):
            for j in range(0,3):
                try:
                    error[i][j]= abs((new_aij[i][j]-old_aij[i][j])/new_aij[i][j])
                    error_list.append(error[i][j])
                except: 
                    error[i][j]=1
                    error_list.append(1)
        if max(error_list) < 0.01:
            stop+=1
        print(error)
    return(plate)


plate = iterate_updates(plate)

npplate = np.matrix(plate)
print('\n',npplate)
print(plate)

#%%
import math

plate =[[100,100,100,100,100],\
        [75,83.19997657,82.31144446,74.06536559,50],\
        [75,75.99209901,72.87589586,64.45364555,50],\
        [75,73.98924026,69.98003443,61.9700183,50],\
        [75,75.99209901,72.87589586,64.45364555,50]]


def calc_qx(plate,i,j):
    qx = -(plate[i+1][j]-plate[i-1][j])/2
    return(qx)
    
def calc_qy(plate,i,j):
    qy = -(plate[i][j+1]-plate[i][j-1])/2
    return(qy)

def calc_qn_dir(plate,i,j):
    qx,qy = calc_qx(plate,i,j),calc_qy(plate,i,j)
    qx2_qy2 = qx**2+qy**2
    qn = qx2_qy2**.5
    if qx > 0:
        theta = math.atan(qy/qx)
    elif qx < 0:
        theta = math.atan(qy/qx) + math.pi
    else:
        theta = 1.5708
    return(qn,theta)


for i in range(1,4):
    for j in range(1,4):
        qn,theta = calc_qn_dir(plate,i,j)
        theta_d = theta*180/math.pi
        print(plate[i][j],qn,theta_d)
        print()

#%% Ch-C 30.10
    
k_prime = 0.49 # cal/(s * cm * degrees C)
length = 10 # cm
delta_x = 2 # cm
delta_t = 0.1 # seconds
t0 = 0 # rod temp at start is 0
T0 = 100 # temp in C at rod position 0cm
T10 = 50 # temp in C at rod position 10cm
iter_ = 4

""" Note that rod is aluminum with C = 0.2174 cal/(g* C) and p = 2.7g/cm^3.
Therefore, k = 0.49 / (2.7*0.2174) = 0.835 cm^2/s and lambda - 0.835(0.1)/2^2
= 0.020875"""

k = 0.835
lambda_ = 0.020875
A = np.matrix([[1.04175,    -0.020875,  0,          0],\
               [-0.020875,  1.04175,    -0.020875,  0],\
               [0,          -0.020875,  1.04175,    -0.020875],\
               [0,          0,          -0.020875,  1.04175]])
b = np.array([2.0875,0,0,1.04375])

def solve_system(a,b):
    x = np.linalg.solve(a,b)
    return(x)
    
for i in range(0,iter_):
    x = solve_system(A,b)
    print(x)
    b=x+b
    print(b)
    print()

#%% CH-C 30.11
    
k_prime = 0.49 # cal/(s * cm * degrees C)
length = 10 # cm
delta_x = 2 # cm
delta_t = 0.1 # seconds
t0 = 0 # rod temp at start is 0
T0 = 100 # temp in C at rod position 0cm
T10 = 50 # temp in C at rod position 10cm
iter_ = 4

""" Note that rod is aluminum with C = 0.2174 cal/(g* C) and p = 2.7g/cm^3.
Therefore, k = 0.49 / (2.7*0.2174) = 0.835 cm^2/s and lambda - 0.835(0.1)/2^2
= 0.020875"""

k = 0.835
lambda_ = 0.020875
A = np.matrix([[2.04175,    -0.020875,  0,          0],\
               [-0.020875,  2.04175,    -0.020875,  0],\
               [0,          -0.020875,  2.04175,    -0.020875],\
               [0,          0,          -0.020875,  2.04175]])
b = np.array([4.175,0,0,2.0875])

def solve_system(a,b):
    x = np.linalg.solve(a,b)
    return(x)

for i in range(0,iter_):
    x = solve_system(A,b)
    print(x)
    b = x*4
    print(b)
    print()

#%%
