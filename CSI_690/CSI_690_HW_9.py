# Heath, 9.4 Euler's Method

def function(t,y):
    fun = (-5*y)
    return(fun)

t,y = 0,1
h = 0.5
n = 20

for i in range(0,n):
    m = function(t,y)
    y1 = y + h*m
    t1 = t + h
    print(t1,y1)
    t,y = t1,y1

#%%
    
# Heath, 9.4 Backward Euler's Method with fixed point iteration

def function(t,y):
    fun = (-5*y)
    return(fun)

t,y = 0,1
h = 0.5
n = 20

for i in range(0,n):
    m = function(t,y)
    y1k0 = y + h*m
    t1k0 = t + h
    #print(t1,y1)
    m1 = function(t1k0,y1k0)
    y1 = y + h*m1
    t1 = t+h
    print(t1,y1)
    t,y = t1,y1

#%%
    
# Heath, 9.4 Backward Euler's Method with Newton-Raphson

def function(t,y):
    fun = (-5*y)
    return(fun)

def der_fun(t,y):
    fun = -5
    return(fun)

t,y = 0,1
h = 0.5
n = 20

for i in range(0,n):
    m0 = function(t,y)
    m1 = der_fun(t,y)
   # print(m0,m1)
    mk = m0/m1
    fm = y-mk
    y1k0 = y + h*fm
   # print(y1k0)
    t1k0 = t + h
    #print(t1,y1)
    m1 = function(t1k0,y1k0)
    y1 = y + h*m1
    t1 = t+h
    print(t1,y1)
    t,y = t1,y1


#%%
import random
# EBB7

def update_x(xt,vt,h):
    xtk1 = (xt+h) - (vt+h)*h
    return(xtk1)

def update_v(vt,k,x,m):
    vtk1 = vt+(k*x)/m
    return(vtk1)

def osc_freq(k,m):
    freq = (k/m)**.5 # k and m are constants
    return(freq)

def random_num():
    num=random.random()
    return(num)

# parameters
xt = 0
v = .5
m = 1
k = 2
h = .001
t = 0
w = osc_freq(k,m)
print(w)

for i in range(0,400):
    new_v = update_v(v,k,xt,m)
    new_x = update_x(xt,v,h)
    t+=1
    print(t,new_x,new_v)
    xt = new_x
    v = new_v