"""
e^x = 1 - x + x^2/2 - x^3/3!
"""
import math

x = 5

def errors(n):
    target = 0.006737947
    true_error = target-n
    relative_error = true_error/target
    return(true_error,relative_error)

def e_power_1(x):
    print("For the first given function:")
    n = 0
    count = 0
    while count < 20:
        q = (x**count)/math.factorial(count)
        if count%2 == 0:
            n+=q
        else:
            n-=q
        true_error,rel_error = errors(n)
        print("On the addition of term",count+1,"the true error is",true_error)
        print("and the approximate relative error is",rel_error)
        print()
        count+=1
    return(n)
    
def e_power_2(x):
    print()
    print("For the second given function:")
    n = 0
    count = 0
#    n+=1
    while count < 20:
        q = (x**count)/math.factorial(count)
        n+=q
        temp_n = 1/n
        true_error,rel_error=errors(temp_n)
        print("On the addition of term",count+1,"the true error is",true_error)
        print("and the approximate relative error is",rel_error)
        print()
        count+=1
    n=1/n
    return(n)
    
    
epower=e_power_1(x)
epower2=e_power_2(x)
print("First Function:",epower)
print("Second Function:",epower2)
print("Actual Answer:",.006737947)

#testing python's built in math.e functions
e = math.e
eval_e = e ** -5
print("Python's math library gives the following solution:",eval_e)

#%%
"""
cos_x = 1 - x^2/2 + x^4/4! - x^6/6! + x^8/8!
"""
x = math.pi * 0.3
def cos_x(x):
    count=0
    n=0
    end = False
    while end == False:
        q=(x**count)/math.factorial(count)
        if count%4==0:
            n+=q
        else:
            n-=q
        count+=2
        if q < 0.0000005:
            end = True
    print(n)
    print("The necessary terms to reach 8 significant digits is:")
    print(count/2)

cosx = math.cos(x)
print(cosx)
cos_x=cos_x(x)

#%%


import pandas as pd
import math
import time

df=pd.read_csv("C:\\Users\\jmcle\\Google Drive\\School\\CSI 690\\"
               +"data_mean_std.csv",delim_whitespace=True)

col1 = df["P1"]
col2 = df["P2"]
col3 = df["P3"]
col_list = (col1,col2,col3)


def moving_stdv(sample):
    m = 0
    s = 0
    N = len(sample)
    leng=range(1,N+1)
    for i in leng:
        t0=time.time()
        x=sample.iloc[i-1]
        oldm=m
        m=m+(x-m)/i
        s=s+(x-m)*(x-oldm)
        t1=time.time()
    iter_time=t1-t0
    print(iter_time,"Iteration time")
    s=s/N-1
    mov_stdev = math.sqrt(s)
    return(mov_stdev)

def standard_stdv(sample):
    for n in sample:
        sum_all = 0
        for i in sample <=n:
            sum_all+=i
        xbar = sum_all/n+1
        sumvar=0
        for i in sample:
            sumvar+= (i-xbar)**2
        var = sumvar/len(sample)-1
        stddev= math.sqrt(var)
    return(stddev)
    # for an effective standard deviation implementation, remove the 
    # line containing "for n in sample:" and then de-indent the rest of this
    # function. This particular version was created in order to test the
    # effficacy of re-calculating the standard deviation each time a new value
    # was obtained.

counter=0
for i in col_list:
    counter+=1
    t0=time.time()
    mv_stdv = moving_stdv(i)
    t1=time.time()
    stdv = standard_stdv(i)
    t2=time.time()
    diff = stdv - mv_stdv
    time1=t1-t0
    time2=t2-t1
    string = "P"+str(counter)
    print("For",string,"the single pass algorithm  for standard deviation "\
          +"returns",mv_stdv)
    print("while the traditional algorithm returns",stdv)
    print("and the difference between the two is",diff)
    print()
    print("The time for the single pass algorithm to run is",time1, "seconds.")
    print("The traditional algorithm's time to run is",time2, "seconds.")
    print()
    print()
    print()
    