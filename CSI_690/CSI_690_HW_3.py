# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 16:22:44 2018

@author: jmcle
"""

import numpy as np
a = np.array([[1,10],[1,15],[1,20]])
b = np.array([[11.6],[11.85],[12.25]])
x = np.linalg.lstsq(a,b, rcond=None)
print(x)

#%%

a = np.array([[1,0],[1,1],[1,3]])
aT = a.transpose()
b = np.array([[1],[2],[3]])
ata = np.dot(aT,a)
atb = np.dot(aT,b)
L = np.linalg.cholesky(ata)

strings = ("A","A Transpose","A Transpose * A","A Transpose * B","Cholesky Lower")
variables = (a,aT,ata,atb,L)
for i in range(0,len(strings)):
    print(strings[i])
    print(variables[i])
    print()
    
#%%
# Polynomial Regression
# Finding summations of x^n and yx^n:

x = [1,2,3,4,5,6,7,8,9]
y = [1, 1.5, 2, 3, 4, 5, 8, 10, 13]

x_power = {'sumx0':0,'sumx':0,'sumx2':0,'sumx3':0,'sumx4':0}
xy_power = {'sumx0y':0,'sumx1y':0,'sumx2y':0}

def sumpowerx(sum_,n):
    for i in x:
        sum_+=i**n
#    print(sum_)
    return(sum_)

def sumpowerxy(sum_,n):
    for i in x:
#        print(i)
        sum_ += i**n * y[i-1]
    return(sum_)

for k,v in x_power.items():
    n = list(x_power.keys()).index(k)
    x_power[k] = sumpowerx(v,n)
for k,v in xy_power.items():
    n = list(xy_power.keys()).index(k)
    xy_power[k] = sumpowerxy(v,n)

print(x_power)
print(xy_power)

#%% Solving the linear system:
a = np.matrix([[9,45,285],[45,285,2025],[285,2025,15333]])
b = np.matrix([[47.5],[325],[2438]])
x = np.linalg.solve(a,b)
print(x)
#%%
import numpy as np
import matplotlib.pyplot as plt

t_array = np.array([0.0,1.0,2.0,3.0,4.0,5.0])
y_array = np.array([1.0,2.7,5.8,6.6,7.5,9.9])

def fit_plot(i):
    z = np.polyfit(t_array,y_array,i)
    print("polynomial order",i)
    print("expression coefficients:",z)
    p = np.poly1d(z)
    
    xp = np.linspace(0,10,100)
    plt.plot(t_array, y_array,'.',xp,p(xp),'-',label=i)
    plt.ylim(0,12)
    plt.xlim(0,6)
#    plt.legend()
    plt.show

#for i in range(0,6):
#    fit_plot(i)
    
fit_plot(5)
#%%

a = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1],[1,-1,0,0],[1,0,-1,0],[1,0,0,-1],[0,1,-1,0],[0,1,0,-1],[0,0,1,-1]])
b = np.array([2.95,1.74,-1.45,1.32,1.23,4.45,1.61,3.21,0.45,-2.75])

x_lstsq = np.linalg.lstsq(a,b,rcond=None)[0]
print(x_lstsq)