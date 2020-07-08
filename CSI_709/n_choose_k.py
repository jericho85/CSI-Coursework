# -*- coding: utf-8 -*-
"""
@author: Jericho
n choose k calculator
n! / k! (n-k)!
"""
import math

#%%

# this can be used to determine the number of possible links in a graph

n= 4
k= 2

def n_choose_k(n,k):
    n_choose_k = math.factorial(n)/(math.factorial(k)*math.factorial(n-k))
    return(n_choose_k)

n_choose_k(n,k)


#%%

# This can be used to determine the sample space of a graph if k=2, otherwise 
# use next function

n= 4
k= 2

def n_choose_k_choose_k(n,k):
    m = math.factorial(n)/(math.factorial(k)*math.factorial(n-k))
    choose = math.factorial(m)/(math.factorial(k)*math.factorial(m-k))
    return(choose)

n_choose_k_choose_k(n,k)

#%%
# ((N Choose 2) Choose K)

n= 4
k= 2

def n_choose_k_choose_k(n,k):
    m = math.factorial(n)/(math.factorial(2)*math.factorial(n-2))
    choose = math.factorial(m)/(math.factorial(k)*math.factorial(m-k))
    return(choose)

n_choose_k_choose_k(n,k)

#%%
# Probability of Ksub-i in an Erdos Renyi Graph
# Or, the probability of a node having a specific degree
#incomplete at the moment
#n= 4
#k= 2
#
#def n_choose_k_choose_k(n,k):
#    m = math.factorial(n)/(math.factorial(2)*math.factorial(n-2))
#    choose = math.factorial(m)/(math.factorial(k)*math.factorial(m-k))
#    return(choose)
#
#n_choose_k_choose_k(n,k)