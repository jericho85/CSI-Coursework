# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 15:40:33 2018

@author: Jericho
"""
from sympy import *

a,b,c,x = symbols('a b c x', real=True)
fx = c+a*x**b
print(diff(fx,a))
print(diff(fx,b))
print(diff(fx,c))

#%%

a,b,c = symbols('a b c', real=True)
x=.0001

fx = c+a*x**b
print(diff(fx,a))
print(diff(fx,b))
print(diff(fx,c))

d = -9.21034037197618*0.0001**.5*1.82
print(d)