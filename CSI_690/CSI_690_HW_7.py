# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 17:29:17 2018

@author: jmcle
"""

# Bisection

def f(x):
    fx = 6 + (10*x) + (9*(x**2)) + (16*(x**3))
    return(fx)
    
def bisect(xl,xu):
    xr,iter_ = 0,0
    es = .001
    imax = 1000
    fl = f(xl)
    while iter_<imax:
        xrold = xr
        xr = (xl + xu)/2
        fr = f(xr)
        iter_+=1
        if xr != 0:
            ea = abs((xr - xrold)/xr)*100
        test = fl*fr
        if test < 0:
            xu=xr
        elif test > 0:
            xl = xr
            fl = fr
        else: ea = 0
        if ea < es: iter_+=imax
        print(xl, xr, xu, ea)
    return(xr)
xr= bisect(-2,1)
fxr = 3 + (6*xr) + (5*(xr**2)) + (3*(xr**3)) + (4*(xr**4))
print()
print(fxr)
#%%

# Newton's Method
def iter_(x):
    num = 6 + 10*x + (9*(x**2)) + (16*(x**3))
    den = 10 + 18*x + (48*(x**2))
    xi_plus = x - (num/den)
    return(xi_plus)

def error(xi_plus,xi):
    err = abs((xi_plus-xi)/xi_plus)
    return(err)

def newton(x0,es):
    err = 1
    xi = x0
    while err > es:
        xi_plus = iter_(xi)
        err = error(xi_plus,xi)
        print(xi_plus,err)
        xi = xi_plus
    return(xi)

xi = newton(-1,.01)
fxi = 3 + (6*xi) + (5*(xi**2)) + (3*(xi**3)) + (4*(xi**4))
print()
print(fxi)
        
        
#%%
# Newton's Method wither finite difference approximation

def eval_x(x):
    fx = 3 + (6*x) + (5*(x**2)) + (3*(x**3)) + (4*(x**4))
    return(fx)

def eval_dx(x):
    fx = 6 + 10*x + (9*(x**2)) + (16*(x**3))
    return(fx)


def iter_2(x):
    pf = x*.01
    x_plus = x + pf
    x_minus = x - pf
    fx_plus = eval_x(x_plus)
    fx_minus = eval_x(x_minus)
    fx = eval_x(x)
    num = (fx_plus - fx_minus)/(2 *pf)
    den = (fx_plus - (2*fx) + fx_minus) / (pf**2)
    xi_plus = x - (num/den)
    return(xi_plus)

def error2(xi_plus,xi):
    err = abs((xi_plus-xi)/xi_plus)
    return(err)

def newton2(x0,es):
    err = 1
    xi = x0
    while err > es:
        xi_plus = iter_2(xi)
        err = error2(xi_plus,xi)
        print(xi_plus,err)
        xi = xi_plus
    return(xi)

xi = newton2(-1,.01)
fxi = 3 + (6*xi) + (5*(xi**2)) + (3*(xi**3)) + (4*(xi**4))
print()
print(xi)
print()
print(fxi)
        
        #%%

#Optimize problem with multiple variables

#import sympy
from sympy import symbols, diff
import numpy as np
import math


y,t = np.array([1.81945517,1.84768883,1.85922616,1.87857847,\
           1.94678403,2.04153268,2.11669564,2.10190186,\
           2.20970561,2.18723323,2.3130484,2.40119457,\
           2.34998155,2.38172234]),\
           np.array([0.001,0.003,0.0055,0.01,0.03,0.072,0.139,\
           0.1,0.24,0.2,0.3,0.469,0.4,0.5])

jacobian = []
for i in range(len(y)):
    q = y[i]
    p = t[i]
    a,b,c = symbols('a b c', real=True)
    func = +c + a*(p**b)
    dfa = diff(func,a)
    dfb = diff(func,b)
    dfc = diff(func,c)
    temp_array = [dfa,dfb,dfc]
    jacobian.append(temp_array)

#for i in jacobian:
#    print(i)
    
#jacobian = [[0.001**b, -6.90775527898214*a*0.001**b, 1],
#                [0.003**b, -5.80914299031403*a*0.003**b, 1],
#                [0.0055**b, -5.20300718674371*a*0.0055**b, 1],
#                [0.01**b, -4.60517018598809*a*0.01**b, 1],
#                [0.03**b, -3.50655789731998*a*0.03**b, 1],
#                [0.072**b, -2.63108915996608*a*0.072**b, 1],
#                [0.139**b, -1.97328134585145*a*0.139**b, 1],
#                [0.1**b, -2.30258509299405*a*0.1**b, 1],
#                [0.24**b, -1.42711635564015*a*0.24**b, 1],
#                [0.2**b, -1.6094379124341*a*0.2**b, 1],
#                [0.3**b, -1.20397280432594*a*0.3**b, 1],
#                [0.469**b, -0.757152510535858*a*0.469**b, 1],
#                [0.4**b, -0.916290731874155*a*0.4**b, 1],
#                [0.5**b, -0.693147180559945*a*0.5**b, 1]]


def eval_jacobian(a,b,c):
#    print(a,b,c,'Jacobian evaluation')
    eval_jac = []
    for i in jacobian:
        temp_list = []
        for j in i:
     #       print("to evaluate:",j,a,b,c)
            j = str(j)
            answer = eval(j)
     #       print("solution:",answer)
            temp_list.append(answer)
        eval_jac.append(temp_list)
 #   print(eval_jac)
#    print()
    return(eval_jac)



def calc_residual(y,t,a,b,c):
    resid = y - (c + a*(t**b))
#    print(resid)
    return(resid)

def residual_array(eval_jac):
    resid_array =[]
    for i in range(len(y)):        
         y_var = y[i]
         t_var = t[i]
         a = eval_jac[i][0]
         b = eval_jac[i][1]
         c = eval_jac[i][2]
         resid=calc_residual(y_var,t_var,a,b,c)
         resid_array.append(resid)
    return(resid_array)

def iterations():
#    a,b,c =.913,.51,1.81
    a,b,c = 0.914,.51,1.81
#    stop = 0
    for i in range(2):
        eval_jac=eval_jacobian(a,b,c)
        residuals = np.matrix(residual_array(eval_jac))
        residuals_T = np.transpose(residuals)
        eval_jac_T = np.transpose(eval_jac)
#        print(residuals)
#        print()
#        jtj = np.dot(eval_jac_T,eval_jac)
#        jtr = np.dot(-eval_jac_T,residuals_T)
#        jtr=-jtr
#        print(jtj)
#        print()
        residuals_T = residuals_T.getA1()*-1
        sol=np.linalg.lstsq(eval_jac,residuals_T) #,rcond=None)
        print(eval_jac)
        print()
        print(residuals_T)
        print()
        print(sol)
        print()
  #      sol=np.linalg.lstsq(jtj,jtr,rcond=None)
#        print(sol[0])
#        print()
#        old_a,old_b,old_c = a,b,c
        a = a +float(sol[0][0])
        b = b +float(sol[0][1])
        c = c +float(sol[0][2])
#        print(old_a,a)
        print("a,b,c:",a,b,c)
    print(a,b,c,"solution")
    print(sol)
iterations()
#%%

#2nd attempt at Gaussian Newton Raphson method

from sympy import symbols, diff
import numpy as np
import math


y,t = np.array([1.81945517,1.84768883,1.85922616,1.87857847,\
           1.94678403,2.04153268,2.11669564,2.10190186,\
           2.20970561,2.18723323,2.3130484,2.40119457,\
           2.34998155,2.38172234]),\
           np.array([0.001,0.003,0.0055,0.01,0.03,0.072,0.139,\
           0.1,0.24,0.2,0.3,0.469,0.4,0.5])

jacobian = []
for i in range(len(y)):
    q = y[i]
    p = t[i]
    a,b,c = symbols('a b c', real=True)
    func = +c + a*(p**b)
    dfa = diff(func,a)
    dfb = diff(func,b)
    dfc = diff(func,c)
    temp_array = [dfa,dfb,dfc]
    jacobian.append(temp_array)

#for i in jacobian:
#    print(i)
    
#jacobian = [[0.001**b, -6.90775527898214*a*0.001**b, 1],
#                [0.003**b, -5.80914299031403*a*0.003**b, 1],
#                [0.0055**b, -5.20300718674371*a*0.0055**b, 1],
#                [0.01**b, -4.60517018598809*a*0.01**b, 1],
#                [0.03**b, -3.50655789731998*a*0.03**b, 1],
#                [0.072**b, -2.63108915996608*a*0.072**b, 1],
#                [0.139**b, -1.97328134585145*a*0.139**b, 1],
#                [0.1**b, -2.30258509299405*a*0.1**b, 1],
#                [0.24**b, -1.42711635564015*a*0.24**b, 1],
#                [0.2**b, -1.6094379124341*a*0.2**b, 1],
#                [0.3**b, -1.20397280432594*a*0.3**b, 1],
#                [0.469**b, -0.757152510535858*a*0.469**b, 1],
#                [0.4**b, -0.916290731874155*a*0.4**b, 1],
#                [0.5**b, -0.693147180559945*a*0.5**b, 1]]


def eval_jacobian(a,b,c):
    eval_jac = []
    for i in jacobian:
        temp_list = []
        for j in i:
            j = str(j)
            answer = eval(j)
            temp_list.append(answer)
        eval_jac.append(temp_list)
    return(eval_jac)



def calc_residual(y,t,a,b,c):
    resid = y - (c + a*(t**b))
    print(resid)
    return(resid)

def residual_array(eval_jac):
    resid_array =[]
    for i in range(len(y)):        
         y_var = y[i]
         t_var = t[i]
         a = eval_jac[i][0]
         b = eval_jac[i][1]
         c = eval_jac[i][2]
         resid=calc_residual(y_var,t_var,a,b,c)
         print(y_var,t_var,a,b,c)
         resid_array.append(resid)
         print("calc residual:",resid)
    return(resid_array)

def iterations():
#    a,b,c =.913,.51,1.81
    a,b,c = 1,.5,1.5
    print("a,b,c:",a,b,c)
    for i in range(1):
        eval_jac=eval_jacobian(a,b,c)
        residuals = np.matrix(residual_array(eval_jac))
        residuals_T = np.transpose(residuals)
        eval_jac_T = np.transpose(eval_jac)
        jtj = np.dot(eval_jac_T,eval_jac)
        jtr = np.dot(eval_jac_T,residuals_T)*-1
        sol=np.linalg.lstsq(jtj,jtr,rcond=None)
        a = a +float(sol[0][0])
        b = b +float(sol[0][1])
        c = 1.81 #c +float(sol[0][2])

        print("a,b,c:",a,b,c)
    print(a,b,c,"solution")
    print(sol)
iterations()

#%%
import scipy.optimize as optimize

def fun(x,a,b,c):
    return(a*(x**b+c))
    
optimize.minimize(fun,10,args=(1,.5,2))

#%%
import random
import time

t0=time.time()
y,x = np.array([1.81945517,1.84768883,1.85922616,1.87857847,\
           1.94678403,2.04153268,2.11669564,2.10190186,\
           2.20970561,2.18723323,2.3130484,2.40119457,\
           2.34998155,2.38172234]),\
           np.array([0.001,0.003,0.0055,0.01,0.03,0.072,0.139,\
           0.1,0.24,0.2,0.3,0.469,0.4,0.5])
    
def eval_fun(a,b,c):
    squares = 0
    for i in range(len(x)):
        fun = (c + a*(i**b))
        squares += (y[i]-fun)**2
    return(squares)
    
resid = y - (c + a*(x**b))
#c=1.797, a=.913, b=.507
def guess():
    a=float(random.randrange(90000, 92000))/100000
    b=float(random.randrange(50000, 52000))/100000
    c=float(random.randrange(178500, 180000))/100000
    abs_resid = eval_fun(a,b,c)
    return(a,b,c,abs_resid)

def iter_guess():
    a,b,c,abs_resid =0.90009 , 0.50002 , 1.78518 , 52.13998148799598
    for i in range(10):
        new_a,new_b,new_c,abs_resid_guess = guess()
        if abs_resid_guess<abs_resid:
            a,b,c,abs_resid=new_a,new_b,new_c,abs_resid_guess
    print(a,",",b,",",c,",",abs_resid)

iter_guess()
t1=time.time()
time_taken=t1-t0
print("This operation took:",time_taken,"seconds.")

#%%

# Random search for morse potential
#fun = D_e * ( 1 - math.e**(-B*((R/R_0)-1))**2) - D_e
import random
import time
import pandas as pd
import math
R = [1.2655,1.2755,1.2855,1.2955,1.3055,1.3155,1.3255,1.3355,1.3455,1.3555,\
     1.3655,1.3755,1.3855,1.3955,1.4055,1.4155,1.4255,1.4355,1.4455,1.4555,\
     1.4655,1.4755,1.4855,1.4955,1.5055,1.5155,1.5255,1.5355,1.5455,1.5555,\
     1.5655,1.5755,1.5855,1.5955,1.6055,1.6155,1.6255,1.6355,1.6455,1.6555,\
     1.6655,1.6655,1.6755,1.6855,1.6955,1.7055]

U_R = [0.026123136,-0.149391684,-0.315926676,-0.474026072,-0.623961988,\
       -0.765734424,-0.900159728,-1.0272379,-1.147513172,-1.260713428,\
       -1.367927132,-1.468610052,-1.563578536,-1.652832584,-1.736644312,\
       -1.815285836,-1.889029272,-1.95787462,-2.022093996,-2.081959516,\
       -2.13747118,-2.188901104,-2.23679352,-2.280604196,-2.32114948,\
       -2.358157256,-2.39189964,-2.422648748,-2.45040458,-2.475167136,\
       -2.497480648,-2.516800884,-2.533944192,-2.548638456,-2.561155792,\
       -2.571224084,-2.579387564,-2.585646232,-2.590000088,-2.592449132,\
       -2.593537596,-2.593537596,-2.592721248,-2.590272204,-2.58646258,\
       -2.581292376]



def eval_fun(D_e, Beta, R_0):
    squares = 0
    for i in range(len(R)):
        try:
            fun = D_e * (( 1 - (math.e**(-Beta*((R[i]/R_0)-1))))**2) - D_e
        except:
            fun = 1000000
        try:
            squares += (U_R[i]-fun)**2
        except:
            squares = 1000000
    squares = squares**(.5)
    return(squares)
    

def guess():
    D_e=float(random.randrange(-5000, 5000))/1000
    Beta=float(random.randrange(-5000, 5000))/1000
    R_0=float(random.randrange(-5000, 5000))/1000
    abs_resid = eval_fun(D_e, Beta, R_0)
    return(D_e, Beta, R_0,abs_resid)

    
def save(D_e, Beta, R_0,abs_resid):
    file = open('C:\\Users\\jmcle\\Desktop\\Output\\Output_data.txt','w')
    file.write("D_e, Beta, R_0,abs_resid"+" ")
    file.write(str(D_e)+" ") 
    file.write(str(Beta)+" ") 
    file.write(str(R_0)+" ")
    file.write(str(abs_resid)+" ")

def iter_guess(D_e, Beta, R_0,abs_resid):
    for i in range(1000000):
        #new_D_e,new_Beta,new_R_0,abs_resid_guess = guess()
        D_e_guess=float(random.randrange(25800, 26000))/10000
        Beta_guess=float(random.randrange(28800, 29000))/10000
        R_0_guess=float(random.randrange(16600, 16700))/10000
       # print(D_e_guess, Beta_guess, R_0_guess)
        abs_resid_guess = eval_fun(D_e_guess, Beta_guess, R_0_guess)
        if abs_resid_guess<abs_resid:
            D_e, Beta, R_0,abs_resid=D_e_guess, Beta_guess, R_0_guess,abs_resid_guess
            #save(D_e, Beta, R_0,abs_resid)

            print("Updated values:",D_e, Beta, R_0,abs_resid)
    print(D_e,",",Beta,",",R_0,",",abs_resid)
    return(D_e, Beta, R_0,abs_resid)

abs_resid=1000
D_e, Beta, R_0 =   0.008, -1.582, -3.142
t2=time.time()
iter_guess(D_e, Beta, R_0,abs_resid)
t3=time.time()
time_taken2=t3-t2
print("This operation took:",time_taken2,"seconds.")

def repeat_iter():
    abs_resid=1000
    D_e, Beta, R_0 =   0.008, -1.582, -3.142
    df = pd.DataFrame(columns = ["D_e", "Beta", "R_0","abs_resid"])
    for i in range(10000):
        t2=time.time()
        print("Iteration number",i)
        D_e, Beta, R_0,abs_resid = iter_guess(D_e, Beta, R_0,abs_resid)
        temp_list=[[str(D_e), str(Beta), str(R_0),str(abs_resid)]]
        df=df.append(pd.DataFrame(temp_list,columns=["D_e", "Beta", "R_0","abs_resid"]),ignore_index=True)
        df.to_csv('C:\\Users\\jmcle\\Desktop\\Output\\Output_data.csv')
        t3=time.time()
        time_taken2=t3-t2
        print("This operation took:",time_taken2,"seconds.")
        print()

#repeat_iter()
#%%
R = [1.2655,1.2755,1.2855,1.2955,1.3055,1.3155,1.3255,1.3355,1.3455,1.3555,\
     1.3655,1.3755,1.3855,1.3955,1.4055,1.4155,1.4255,1.4355,1.4455,1.4555,\
     1.4655,1.4755,1.4855,1.4955,1.5055,1.5155,1.5255,1.5355,1.5455,1.5555,\
     1.5655,1.5755,1.5855,1.5955,1.6055,1.6155,1.6255,1.6355,1.6455,1.6555,\
     1.6655,1.6655,1.6755,1.6855,1.6955,1.7055]

for i in R:
    D_e, Beta, R_0,abs_resid=2.5942 , 2.8814 , 1.6684 , 0.006905517375262224
    fun = D_e * (( 1 - (math.e**(-Beta*((i/R_0)-1))))**2) - D_e
    print(fun)