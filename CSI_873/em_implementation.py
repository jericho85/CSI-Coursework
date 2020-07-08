#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 15:43:34 2019

@author: jmcleod
"""

import csv,random, math
import matplotlib.pyplot as  plt


'''
Implement EM algorithm to estimate 2 means, mu_1 and mu_2, for normal distributions
with  sigma = 1. Assume that an equal number of points belongs to each distribution.
Include code and results with report.
'''
#%%

data = []
with open('McLeod.txt') as txtfile:
    txt_r =  csv.reader(txtfile,delimiter=' ')
    for r in txt_r:
        data.append(r)

#%%
data_float = []
counter = 0
for i in data:
    for  j in i:
        try:
            data_float.append(float(j))
        except:
            print('error converting  ->',j,'<- input.')

mixdata = data_float
#%%

for i in range(len(mixdata)):
    plt.scatter(float(i),mixdata[i])
plt.show()

#%%
mu_1,mu_2 = random.random(),-random.random()
h = [mu_1,mu_2]
sigma = 1

def calc(sigma,mu,val):
    out = math.e**(-(1/(2*(sigma**2)))*((mu-val)**2))
    return(out)

def em_step1(h,sigma,data):
    data_expanded = []
    for i in data:
        x_1 = calc(sigma,h[0],i)
        x_2 = calc(sigma,h[1],i)
        e_1 = x_1 / (x_1+x_2)
        e_2 = x_2 / (x_1+x_2)
        data_expanded.append([i,e_1,e_2])
    return(data_expanded)

def em_step2(data):
    h1,h2 = [0,0],[0,0]
    for i in data:
        h1[0] += i[0]*i[1]
        h1[1] += i[1]
        h2[0] += i[0]*i[2]
        h2[1] += i[2]
    h = [h1[0]/h1[1],h2[0]/h2[1]]
    return(h)
#%%
    
def print_colors_initial(data):
    rgb = (.5,.5,.5)
    for i in range(len(data)):
        plt.scatter(float(i),data[i],color=[rgb],marker='.')
    plt.show()
    

def print_colors_expanded(data_expanded):        
    for i in range(len(data_expanded)):
        r = random.random()
        if r > data_expanded[i][1]:
            rgb = (0,0,1)
        else:
            rgb = (1,0,0)
        plt.scatter(float(i),data_expanded[i][0],color=[rgb],marker='.')
    plt.show()

print_colors_initial(mixdata)

print(h)
stop = 0
h_old = h
counter = 0
while stop == 0:
    data_expanded = em_step1(h,sigma,mixdata)
    #if counter == 0:
        #print_colors_expanded(data_expanded)
    h_new =  em_step2(data_expanded)
    if h_new[0]-h_old[0] < 0.00001:
        if h_new[1]-h_old[1] < 0.00001:
            stop+=1
    h_old = h
    h = h_new
    counter+=1
#%%
print(h)
print_colors_expanded(data_expanded)


#%%
solve_iters = 0
n = 100
for l in range(n):
    mu_1,mu_2 = random.random(),-random.random()
    h = [mu_1,mu_2]
    sigma = 1
    stop = 0
    h_old = h
    counter = 0
    while stop == 0:
        data_expanded = em_step1(h,sigma,mixdata)
        #if counter == 0:
            #print_colors_expanded(data_expanded)
        h_new =  em_step2(data_expanded)
        if h_new[0]-h_old[0] < 0.00001:
            if h_new[1]-h_old[1] < 0.00001:
                stop+=1
        h_old = h
        h = h_new
        counter+=1
    solve_iters+=counter

print(solve_iters/n)
    
#%%
x = []
y = []
h1_lab = str(h[0])[0:4]
h2_lab = str(h[1])[0:4]


for i in data_expanded:
    r = random.random()
    if r<i[1]:
        x.append(i[0])
    else:
        y.append(i[0])

plt.hist([mixdata],bins=50,label=['data'])
plt.show()
plt.figure(figsize=(12,6))
plt.hist([mixdata,x,y],bins=50,label=['All',h1_lab,h2_lab])
plt.legend(loc='upper left')
plt.show()

#%%
def print_colors_proba(data_expanded):        
    for i in range(len(data_expanded)):
        min_value = min(data_expanded[i][1],data_expanded[i][2])
        rgb = (data_expanded[i][1],min_value,data_expanded[i][2])
        plt.scatter(float(i),data_expanded[i][0],color=[rgb],marker='.')
    plt.show()
print_colors_proba(data_expanded)
