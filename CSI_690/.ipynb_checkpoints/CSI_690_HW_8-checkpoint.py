# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 14:31:43 2018

@author: jmcle
"""
import math
e = math.e



x_list = [1, 1.5, 1.6, 2.5, 3.5]
fx = [0.6767, 0.3734, 0.3261, 0.08422, 0.01596]
x=2.5

#input the values near which to calculate the derivative estimate
input_list = [1.6,2.5,3.5]


def eval_func(x):
    fx_calc = 5*(e**(-2*x))*x
    print(fx_calc)
    return(fx_calc)

def eval_frac(a,b,c,d):
    num = 2*a - b - c
    den = (d - b) * (d - c)
    frac = num/den
#    print(frac, "fraction")
#    print("a:",a,"b:",b,"c:",c,"d:",d)
    return(frac)

def eval_der(x,xi,xipl,ximin):
#    fx_ximin = eval_func(ximin)
#    fx_xipl = eval_func(xipl)
#    fx_xi = eval_func(xi)
    ximin_index = x_list.index(ximin)
    xi_index = x_list.index(xi)
    xipl_index = x_list.index(xipl)
    fx_ximin = fx[ximin_index]
    fx_xipl = fx[xipl_index]
    fx_xi = fx[xi_index]
    
    ximin_frac = eval_frac(x,xi,xipl,ximin)
    xi_frac = eval_frac(x,ximin,xipl,xi)
    xipl_frac = eval_frac(x,ximin,xi,xipl)
    fprimex = fx_ximin*ximin_frac + fx_xipl*xipl_frac + fx_xi*xi_frac
    return(fprimex)

def calc_der(x):
    der = e**(-2*x) * (5-10*x)
    return(der)

fprimex = eval_der(x,input_list[0],input_list[1],input_list[2])
print(fprimex)
der = calc_der(x)
#print(der)

#%%
from scipy import integrate
x2 = lambda x: 20 * math.pi * x * (1-x/.75)**(1/7)
integrate.quad(x2,0,0.75)

#%%
from scipy import integrate
from scipy.special import erf
gaussian = lambda x: 20 * math.pi * x * (1-x/.75)**(1/7)
result = integrate.romberg(gaussian,0,.75,show=True)

#%%
import matplotlib.pyplot as plt
x_list = []
Fx_list = []
xprime = 30
nprime = 1.44
Gx = []
def calc_Fx(x):
    Fx = 1 - math.e**(-(x/xprime)**nprime)
    return(Fx)

for i in range(0,101):
    x = i
    Fx = calc_Fx(x)
    Fx_list.append(Fx)
    x_list.append(x)
#    print(x,Fx)
fx_list = []
for i in range(0,100):
    if i == 0: fx_list.append(0)
    else: fx_list.append( Fx_list[i+1] - Fx_list[i-1] )
#print(fx_list)
#fake_fx_list=[]
#for i in range(1316,1318):
#    fake_fx_list.append(fx_list[i])

#plt.plot(x_list)
#plt.plot(Fx_list)
plt.plot(fx_list)
#plt.plot(fake_fx_list)
plt.show()

for i in range(0,100):
    if i>0:Gx.append(fx_list[i]/x_list[i])
plt.plot(Gx)
plt.show()