# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 15:20:25 2018

@author: jmcle
"""
#%% Lotka-Volterra model

import numpy
import matplotlib.pyplot as plt


alpha1 = 1.
beta1 = 0.1
alpha2 = 0.5
beta2 = .02

def f(u):
    y1 = u[0]
    y2 = u[1]
    return numpy.array([y1*(alpha1 - beta1*y2), y2*(-alpha2+beta2*y1)])

def euler_step(u, f, dt):
    return(u + dt * f(u))

T = 25.0 
h = 0.01 
n = int(T/h) + 1 
y1_init = 100.0
y2_init = 10.0
T_init = 0.0
u_euler = numpy.empty((n, 2))
u_euler[0] = numpy.array([y1_init, y2_init])

for i in range(n-1):
    u_euler[i+1] = euler_step(u_euler[i], f, h)
    time = numpy.linspace(0.0, T,n)
    y1_euler = u_euler[:,0]
    y2_euler = u_euler[:,1]

plt.plot(time, y1_euler, label = 'Prey ')
plt.plot(time, y2_euler, label = 'Predator')
plt.xlabel('time')
plt.ylabel('populations')
plt.legend()
plt.show()

plt.plot(y1_euler,y2_euler,label='Phase Portrait')
plt.xlabel('Prey')
plt.ylabel('Predator')
plt.legend()
plt.show()

#%% Leslie-Gower model

alpha1 = 1.
beta1 = 0.1
alpha2 = 0.5
beta2 = 10

def f(u):
    y1 = u[0]
    y2 = u[1]
    return numpy.array([y1*(alpha1 - beta1*y2), y2*(alpha2-beta2*y2/y1)])

def euler_step(u, f, dt):
    return(u + dt * f(u))

T = 25.0 
h = 0.01 
n = int(T/h) + 1 
y1_init = 100.0
y2_init = 10.0
T_init = 0.0
u_euler = numpy.empty((n, 2))
u_euler[0] = numpy.array([y1_init, y2_init])

for i in range(n-1):
    u_euler[i+1] = euler_step(u_euler[i], f, h)
    time = numpy.linspace(0.0, T,n)
    y1_euler = u_euler[:,0]
    y2_euler = u_euler[:,1]

plt.plot(time, y1_euler, label = 'Prey ')
plt.plot(time, y2_euler, label = 'Predator')
plt.xlabel('time')
plt.ylabel('populations')
plt.legend()
plt.show()

plt.plot(y1_euler,y2_euler,label='Phase Portrait')
plt.xlabel('Prey')
plt.ylabel('Predator')
plt.legend()
plt.show()

#%%

import numpy as np
import matplotlib.pyplot as plt
import math

def f(x,t):
    x1 = math.exp(.25*(-3*math.cos(t)+math.cos(t*3)/3)+(2/3))
    return(x1)

def heun(f,x0,t):
    n = len( t )
    x = np.array([x0]*n)
    temp_list=[]
    temp_list2=[]
    for i in range(0,n-1):
        h = 1
        k1 =h*f(x[i],t[i])
        k2 =h*f(x[i]+k1,t[i+1])
        xs =x[i]+(k1+k2)/2.0 
        temp_list.append(k2)
        temp_list2.append(k1)
    return(temp_list,temp_list2)

t=[]
t0=0
h =0.1
tupper = 3
steps = tupper/h +1
for i in range(0,31):
    j=i*h
    t.append(j)
print(t)

k2, k1 =heun(f,1,t)
print(k1,k2)

#%%

import numpy as np
import matplotlib.pyplot as plt
import math

def f(x,t):
    x1 = math.exp(.25*(-3*math.cos(t)+math.cos(t*3)/3)+(2/3))
    return(x1)

def ralston( f, x0, t ):

    n = len( t )
    x = np.array( [x0] * n )
    temp_list=[]
    temp_list2=[]
    for i in range(0, n - 1 ):
        h = .1
        k1 = f( x[i], t[i] ) #*h
        k2 = f(x[i]+.75*h, t[i+1]+.75*k1*h )
        yi = x[i] + ( (1/3)*k1 + (2/3)*k2 ) * h
        print(yi)
        temp_list.append(k2)
        temp_list2.append(k1)
    return(temp_list,temp_list2)

t=[]
t0=0
h =0.1
tupper = 3
steps = tupper/h +1
for i in range(0,31):
    j=i*h
    t.append(j)
#print(t)

k2, k1 =ralston(f,1,t)
print(k1,k2)

#%%

import numpy as np
import matplotlib.pyplot as plt
import math

def f(x,t):
    x1 = -2*x+5*math.exp(-t)
    return(x1)
    
def f2(x,t):
    x1 = -(t*x**2)/2
    return(x1)

def rk4( f, x0, t ):
    n = len( t )
    x = []
    x.append(x0)
    for i in range( n - 1 ):
        h = t[i+1] - t[i]
        k1 = h * f( x[i], t[i] )
        k2 = h * f( x[i] + 0.5 * k1, t[i] + 0.5 * h )
        k3 = h * f( x[i] + 0.5 * k2, t[i] + 0.5 * h )
        k4 = h * f( x[i] + k3, t[i+1] )
        x_plus = x0 + (( k1 + k2 + k3 + k4 ) / 6.0)
        x.append(x_plus)
        x0=x_plus
    return x

t = [0.0,0.1,0.2,0.3,0.4]
y = rk4(f,2,t)
z = rk4(f2,4,y)

print(t)
print(y)
print(z)