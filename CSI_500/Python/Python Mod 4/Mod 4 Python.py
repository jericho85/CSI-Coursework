#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 13:48:00 2019

@author: jmcleod
"""

#%% Problem 1.1: Heights of students by year and gender

import matplotlib.pyplot as plt


infile = open('student_data.csv',mode='r')
header=infile.readline()
file_data=infile.readlines()

student_dat = []

for i in file_data:
    i = i.strip()
    gender,height,year = i.split(',')
    gender = gender.strip()
    height = int(height)
    year = year.strip()
    student_dat.append((gender,height,year))


m_heights = []
f_heights = []

for i in student_dat:
    gender = i[0]
    height = i[1]
    year = i[2]
    if gender == 'male':
        m_heights.append(height)
    elif gender == 'female':
        f_heights.append(height)
    else: print('Error: non-binary gender option not yet available')
    

x1 = range(len(m_heights))
x2 = range(len(f_heights))

plt.plot(x1,m_heights,'-b',label='Male')
plt.plot(x2,f_heights,'-r',label='Female')
plt.title('Student Height by Gender')
plt.xlabel('Student Number')
plt.ylabel('Height in Inches')


plt.legend()
plt.show()


#assigning 8 lists of male/female + year in school
m_fr,m_so,m_ju,m_se,f_fr,f_so,f_ju,f_se=[],[],[],[],[],[],[],[]

for i in student_dat:
    gender = i[0]
    height = i[1]
    year = i[2]
    
    if gender =='male':
        if year == 'freshman':
            m_fr.append(height)
        elif year == 'sophomore':
            m_so.append(height)
        elif year == 'junior':
            m_ju.append(height)
        else: m_se.append(height)
    if gender =='female':
        if year == 'freshman':
            f_fr.append(height)
        elif year == 'sophomore':
            f_so.append(height)
        elif year == 'junior':
            f_ju.append(height)
        else: f_se.append(height)
        
height_data = [m_fr,m_so,m_ju,m_se,f_fr,f_so,f_ju,f_se]
height_labels = ['m_fr','m_so','m_ju','m_se','f_fr','f_so','f_ju','f_se']
plt.boxplot(height_data,labels=height_labels)
plt.title('Student Heights by Gender and Class')
plt.ylabel('Height in Inches')
plt.show()

#%% Problem 1.2: Diffusion of Innovation, iPad Sales over Time


infile = open('ipad_sales.csv',mode='r')
header=infile.readline()
file_data=infile.readlines()


sales_data = []
for i in file_data:
    i = i.strip()
    quarter,sales = i.split(',')
    quarter = quarter.strip()
    sales = float(sales)
    sales_data.append((quarter,sales))

quarter = []
sales = []
for i in sales_data:
    quarter.append(i[0])
    sales.append(i[1])


fig, ax = plt.subplots()
plt.setp(ax.get_xticklabels(), rotation=90, horizontalalignment='right')
plt.plot(quarter,sales)
fig.set_size_inches(10,4)
plt.title('iPad Sales: Q3 2010 to Q4 2018')
plt.ylabel('Sales (millions)')
plt.xlabel('Quarter and Year')
plt.show()

#%% Problem 2

'''
The Population Size has two direct impacts: time it takes to compute the model
and the smoothness of the curves that result. For instance, the model is very
fast with N=10, but made up of very distinct 90 degree angles rather than 
curves. When N=100000, the model takes a perceptible amount of time to run,
but the resulting plots are very smooth.

Beta is the adoption rate in the model. Thus, at 1, all adoption happens in
iteration 1, and at adoption rate 0.0001, the adoption rate is very low. This
is reflected in the model by changes to the curve for adoption; for beta==1, 
all adoption is immediate, and as beta approaches 0, the adoption curve moves
right, or further out in time. 

Gamma is, essentially, the exact same thing as Beta, except for disposal rates.
It is noteworthy that Gamma is also dependent on Beta: if Beta = 0, Gamma is
irrelevant, and at all other points, Beta acts as a multiplier for Gamma. 

Time periods do not effect the behavior of the model, merely the amount of
observation of the model that is conducted. If a model appears to be just a
set of straight lines or very steep curves, altering the time period may be
helpful in understanding the input beta and gamma.

There are diffusion parameters that correpsond with iPad sales. Please note,
however, that the periodicity for iPad sales that I used corresponds with a 
longer period than was initially used in class. The current market appears to
have a decrease of Gamma somewhat. In order to properfly reflect this in the
model, I would want to provide for updates of gamma and beta that correspond
with new product releases.  Alternatively, considering the iPad Pro a new
product altogether, and measuring it separately from the iPad, would provide
a simpler solution to the change in observed market performance. 

That said, the values that correspond with current iPad sales are:
    model = DOI_Model(N=10000,beta=0.003,gamma=0.008,max_time=1000)

'''


#%% Problem 3: in PDF

#%% Problem 4:

'''
4.1
Setosa petal [x,y]: [0.246,1.462]
Versicolor petal [x,y]: [1.326,4.26]
Virginica petal [x,y]: [2.026,5.552]

4.2
Setosa sepal [x,y]: [5.006,3.428]
Versicolor sepal [x,y]: [5.936,2.77]
Virginica sepal [x,y]: [6.588,2.974]    

4.3
Setosa is easily distinguished. Versicolor and Virginica can be distinguished
approximately, but using only sepal means there will be some edge case
ambiguity. 

4.4
Petals will result in similar issues identifying species along the same lines. 
It is possible to distinguish species to some degree, especially for Setosa,
but Virginica and Versicolor are very close in proximity and will have some
overlap. 
'''