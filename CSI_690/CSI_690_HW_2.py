# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 11:34:59 2018

@author: jmcle
"""
# Solving system for X using NumPy
import numpy as np
# Input Matrices
A = np.matrix([[2,3,-2],[-1,1,1],[1,3,4]])
b = np.matrix([[2],[4],[8]])

# Use Numpy to solve for X vector
x=np.linalg.solve(A,b)
print(x)

# Use Numpy to verify X vector is a valid solution
function  = np.allclose(np.dot(A,x),b)
print(function)

#%%

# Input Matrices
A = np.matrix([[2.0,3.0,-2.0],[-1.0,1.0,1.0],[1.0,3.0,4.0]])
b = np.matrix([[2.0],[4.0],[8.0]])

# Solve for X algorithmically
n=len(A)
for k in range(0,n-1):
    for i in range(k+1,n):
        factor = A[i,k]/A[k,k]
        for j in range(k+1,n):
            A[i,j]=A[i,j]-(factor*A[k,j])
        b[i]=b[i]-(factor*b[k])
for i in range(n-1,1,-1):
    sum_=b[i]
    for j in range(i+1,n):
        sum_=sum_-A[i,j]*(b[j]/A[j,j])
    x[i]=sum_/A[i,i]
print(x)

# source: Numerical Methods for Engineers, 7th Ed, by Chapra and Canale, pg254

#%%
#% LU Factorization using Scipy
import scipy

A = scipy.array([[2.0,3.0,-2.0],[-1.0,1.0,1.0],[1.0,3.0,4.0]])
P, L, U = scipy.linalg.lu(A)
print(A)
print()
print(P)
print()
print(L)
print()
print(U)

#%%
A = np.array([[2.0,3.0,-2.0],[-1.0,1.0,1.0],[1.0,3.0,4.0]])
B = np.array([2.0,4.0,8.0])
X = np.array([-1.2,2,0.8])
Residual = np.dot(A,X) - B
print(Residual)