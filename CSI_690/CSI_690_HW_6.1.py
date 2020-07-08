# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 12:00:41 2018

@author: jmcle
"""
import numpy as np
import math
import sys

k=0

x_1=0
y_1=0

x_2=1.2
y_2=0

x_3=0
y_3=1.2



def newton_raphson(x_1,y_1,x_2,y_2,x_3,y_3):
# Evaluate partial derivatives for iteration K
    def calc_dfx2():
        if x_1 == x_2 and x_2 == x_3:
            dfx2 = 0
        elif x_1==x_2:
            dfx2=4*((((-12*(x_2-x_3 ))**(-13))-(-6*(x_2-x_3 )**(-7) )))
        elif x_2==x_3:
            dfx2=4*(((-12*(x_1-x_2 )**(-13))-(-6*(x_1-x_2 )**(-7))))
        else:
            dfx2=4*(((-12*(x_1-x_2 )**(-13))-(-6*(x_1-x_2 )**(-7)))+(((-12*(x_2-x_3 ))**(-13))-(-6*(x_2-x_3 )**(-7) )))
        return(dfx2)
    
    def calc_dfx3():
        if x_1 == x_3 and x_2 == x_3:
            dfx3 = 0
        elif x_1==x_3:
            dfx3=4*((((-12*(x_2-x_3 ))**(-13))-(-6*(x_2-x_3 )**(-7) )))
        elif x_2==x_3:
            dfx3=4*(((-12*(x_1-x_3 )**(-13))-(-6*(x_1-x_3 )**(-7))))
        else:
            dfx3=4*(((-12*(x_1-x_3 )**(-13))-(-6*(x_1-x_3 )**(-7)))+(((-12*(x_2-x_3 ))**(-13))-(-6*(x_2-x_3 )**(-7) )))
        return(dfx3)
    
    def calc_dfy2():
        if y_1 == y_2 and y_2 == y_3:
            dfy2 = 0
        elif y_1==y_2:
            dfy2=4*((((-12*(y_2-y_3 ))**(-13))-(-6*(y_2-y_3 )**(-7) )))
        elif y_2==y_3:
            dfy2=4*(((-12*(y_1-y_2 )**(-13))-(-6*(y_1-y_2 )**(-7))))
        else:
            dfy2=4*(((-12*(y_1-y_2 )**(-13))-(-6*(y_1-y_2 )**(-7)))+(((-12*(y_2-y_3 ))**(-13))-(-6*(y_2-y_3 )**(-7) )))
        return(dfy2)
    
    def calc_dfy3():
        if y_1 == y_3 and x_2 == y_3:
            dfy3 = 0
        elif y_1==y_3:
            dfy3=4*((((-12*(y_2-y_3 ))**(-13))-(-6*(y_2-y_3 )**(-7) )))
        elif y_2==y_3:
            dfy3=4*(((-12*(y_1-y_3 )**(-13))-(-6*(y_1-y_3 )**(-7))))
        else:
            dfy3=4*(((-12*(y_1-y_3 )**(-13))-(-6*(y_1-y_3 )**(-7)))+(((-12*(y_2-y_3 ))**(-13))-(-6*(y_2-y_3 )**(-7) )))
        return(dfy3)
    
    dfx2=calc_dfx2()
    dfx3=calc_dfx3()
    dfy2=calc_dfy2()
    dfy3=calc_dfy3()
    #print(dfx2,dfx3,dfy2,dfy3)
    
    # Calculate second partial derivatives:
    def calc_df_x22(x_1,x_2,x_3):
        if x_1 == x_2 and x_2 == x_3:
            df_x22 = 0
        elif x_1 == x_2:
            df_x22 = 4*((156*(x_2-x_3)**-14)-(42*(x_2-x_3)**-8))
        else:
            df_x22 = 4*(((156*(x_1-x_2)**-14)-(42*(x_1-x_2)**-8)) + ((156*(x_1-x_2)**-14)-(42*(x_1-x_2)**-8)))
        return(df_x22)
    
    def calc_df_x23(x_1,x_2,x_3):
        if x_2 == x_3:
            df_x23 = 0
        else:
            df_x23 = df_x23 = 4*((156*(x_2-x_3)**-14)-(42*(x_2-x_3)**-8))
        return(df_x23)
    
    def calc_df_x33(x_1,x_2,x_3):
        if x_1 == x_2 and x_2 == x_3:
            df_x33 = 0
        elif x_1 == x_3:
            df_x33 = 4*((156*(x_2-x_3)**-14)-(42*(x_2-x_3)**-8))
        else:
            df_x33 = 4*(((156*(x_1-x_3)**-14)-(42*(x_1-x_3)**-8)) + ((156*(x_2-x_3)**-14)-(42*(x_2-x_3)**-8)))
        return(df_x33)
    
    df_x2x2 = calc_df_x22(x_1,x_2,x_3)
    df_x2x3 = calc_df_x23(x_1,x_2,x_3)
    df_x3x3 = calc_df_x33(x_1,x_2,x_3)
    df_y2y2 = calc_df_x22(y_1,y_2,y_3)
    df_y2y3 = calc_df_x23(y_1,y_2,y_3)
    df_y3y3 = calc_df_x33(y_1,y_2,y_3)
    
    # Construct the hessian and gradient
    gradient = np.array([dfx2,dfx3,dfy2,dfy3])
    gradient_T = np.matrix.transpose(gradient)
    minus_gradient_T = gradient_T * -1
    
    hessian = np.matrix([[df_x2x2,df_x2x3,0,0],
                         [df_x2x3,df_x3x3,0,0],
                         [0,0,df_y2y2,df_y2y3],
                         [0,0,df_y2y3,df_y3y3]
                         ])
#    print(hessian)
#    print()
#    print(gradient_T)
#    print()
#    print(minus_gradient_T)
#    print()
    
#    hessian_T = np.matrix.transpose(hessian)
#    aTa = np.dot(hessian, hessian_T)
#    atb = np.dot(hessian_T,minus_gradient_T)
#    atb = np.matrix.transpose(atb)

    s = np.linalg.solve(hessian,minus_gradient_T)
#    s = np.linalg.solve(aTa,atb)
#    print(s)
    return(s)



def iterating_nr(x_1,y_1,x_2,y_2,x_3,y_3,k):
    place_holder_var =0
    old_val_var = 0
    new_val_var=0
    while place_holder_var ==0:# and k<50:
        print("K:",k)
        print("x1:",x_1,"y1:",y_1,"\n",
              "x2:",x_2,"y2:",y_2,"\n",
              "x3:",x_3,"y3:",y_3,"\n")
        new_vals = newton_raphson(x_1,y_1,x_2,y_2,x_3,y_3)
        x_2 = x_2 - float(new_vals[0])
        x_3 = x_3 - float(new_vals[1])
        y_2 = y_2 - float(new_vals[2])
        y_3 = y_3 - float(new_vals[3])
        k +=1
        old_val_var = new_val_var
        new_val_var = 0
        for i in new_vals:
            new_val_var += i**2
        new_val_var = math.sqrt(float(new_val_var))
        error = new_val_var - old_val_var
        print("Est. Error:",error)
        print()
        if error > 2:
            print("Diverging Solution!!!!")
            print()
            sys.exit()
        if new_val_var < 0.001: place_holder_var += 1
    
    return(x_1,y_1,x_2,y_2,x_3,y_3,k)

iterating_nr(x_1,y_1,x_2,y_2,x_3,y_3,k)
#s = newton_raphson(x_1,y_1,x_2,y_2,x_3,y_3)
#a = np.savetxt(sys.stdout,s)


#%%

import matplotlib.pyplot as plt
x = (0,.96,.96)
y = (0,1.12,-1.12)
#a = (0,0)
#b = (0.967918,-1.12393)
#c = (0.934927,1.12102)
#plt.figure()
#plt.plot(x,y,lw=3)
plt.scatter(x,y,s=120)

