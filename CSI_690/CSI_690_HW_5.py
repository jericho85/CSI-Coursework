# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 10:21:52 2018

@author: Jericho
"""

import matplotlib.pyplot as plt
import numpy as np

def graph( x_range):
    x = np.array(x_range)
    y = eval("-25+(82*x)-(90*x**2)+(44*x**3)-(8*x**4)+(.7*x**5)")
    plt.plot(x,y)
    plt.grid(True)
    plt.show()

graph(np.linspace(0,1,num=100))
print()
graph(np.linspace(0.55,0.6,num=10))

#%%

def solver(x):
    y=-25+(82*x)-(90*x**2)+(44*x**3)-(8*x**4)+(.7*x**5)
    print(y)
    
solver(0.5625)

#%%
def error_est(u,l):
    num = abs(u-l)
    den = abs(u+l)
    err = num/den
    return(err)

error_est(0.5625,.59375)

#%% updated error est
xr_new=0.579556
xr_old=0.580537
error = (xr_new-xr_old)/xr_new
print(error)

#%%
def solver(x):
    y=-25+(82*x)-(90*x**2)+(44*x**3)-(8*x**4)+(.7*x**5)
    return(y)

def false_position(xl,xu):
    num = solver(xu) * (xl-xu)
    den = solver(xl)-solver(xu)
    frac = num/den
    solution = xu-frac
    return(solution)
xl = 0.5
xu = .580537
xr = false_position(xl,xu)

prod_l = solver(xl)*solver(xr)
prod_u = solver(xu)*solver(xr)
new_val=solver(xr)

print("xl:",xl,"f(xl):",solver(xl))
print()
print("xu:",xu,"f(xu):",solver(xu))
print()
print("xr:",xr,"f(xr):",solver(xr))
print()
print("Prod_L",prod_l)
print("Prod_U",prod_u)


#%%
pi = 3.1415926535897
r=1
# Volume of a 1 meter R sphere:
vol = (4/3)*pi*r**3
print(vol)
mass = vol *200
print()
print(mass)

fluid_density = 1000
fluid_displacement = mass/fluid_density
print()
print(fluid_displacement)
vol_above = vol-fluid_displacement
print()
print(vol_above)
print(vol_above*3)

print()
def expression(x,pi):
    y = pi*x**3 - 3*pi*x**2 + 10.05309649148704
    return(y)

expression(1,pi)
hl = 1.421875
hu = 1.4296875
hr = (hl+hu)/2
fhl = expression(hl,pi)
fhu = expression(hu,pi)
fhr = expression(hr,pi)
print(hl,fhl)
print(hu,fhu)
print(hr,fhr)
print(fhl*fhr)
print()
xr_new=1.42578125
xr_old=1.4296875
error = (xr_new-xr_old)/xr_new
print(error)

#%%
def graph( x_range):
    x = np.array(x_range)
    y = eval("-1 +5.5*x -4*x**2 + 0.5*x**3")
    plt.plot(x,y)
    plt.grid(True)
    plt.show()

graph(np.linspace(-5,10,num=100))
print()
graph(np.linspace(0.21,0.22,num=10))
graph(np.linspace(1.4,1.6,num=10))
graph(np.linspace(6.2,6.4,num=10))

#%%

def evaluate(x):
    y = -1 +(5.5*x) -(4*x**2) + (0.5*x**3)
    return(y)

def eval_derivative(x):
    y = 5.5 - 8*x + 1.5*x**2
    return(y)

def calculate_xi_plus1(xi_1):
    num = evaluate(xi_1)
    den = eval_derivative(xi_1)
    solution = xi_1 - (num/den)
    return(solution)
    
def error(xi,xi_1):
    if xi != 0:
        err = (xi-xi_1)/xi
        if err < 0: err = err * -1
        return(err)
    else: return("no prior xi value")

xi,xi_1 = 1.4,1.4
for i in range(10):
    xi_1=xi
    xi=calculate_xi_plus1(xi)
    
    err = error(xi,xi_1)
    print("xi",xi)
    print("xi_1",xi_1)
    print("error",err)
    print()
#%%
def secant(x,x_1,y_1):
    y = 2 + (-x**2 - 2*x +15 )**0.5
#    y = 2 - (-x**2 - 2*x +15 )**0.5
    xk_plus1 = x - y*(x-x_1)/(y-y_1)
    return(xk_plus1,y)

x = 3
xk_1= 0.5
y_1 = 2 + (-xk_1**2 - 2*xk_1 +15 )**0.5
y#_1 = 2 - (-xk_1**2 - 2*xk_1 +15 )**0.5
for i in range(10):
    new_x,new_y=secant(x,xk_1,y_1)
    error = (new_x-x) / new_x
    print(new_x,error)
    xk_1=x
    x=new_x
    y_1=new_y
#%%
x,y = 1.6,3.5
for i in range(20):
    
    u_exp = "5 - (x-4)**2 - (y-4)**2"
    v_exp = "16 - x**2 - y**2"
    
    vy = -2*y
    uy = -2*(y-4)
    vx = -2*x
    ux = -2*(x-4)
    
    u = 5 - (x-4)**2 - (y-4)**2
    v = 16 - x**2 - y**2
    
    det = ux * vy - uy*vx
    
    x_plus = x - (u*vy - v*uy)/det
    y_plus = y - (v*ux - u*vx)/det
    
    print(x_plus,", ",y_plus)
    x,y=x_plus,y_plus