#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSI500, Python Assignment 2

Jericho McLeod

Note to Dr. Scott,

Thank you for the kind remarks on the prior assignments. I use Python 
professionally, and took this course primarily for the exposure to LaTex and 
NetLogo, though I am relatively weak in R compared to Python.

Also, again for grading ease, I have the output at the tops of each segment of 
code so that if the function is run you don't get an 'Output: ...." copy of
my inline samples. 

Cheers,
Jericho
"""
#%% Problem 1 using zip()

'''
Output for leap year:
('Jan', 31)
('Feb', 29)
('Mar', 31)
('Apr', 30)
('May', 31)
('Jun', 30)
('Jul', 31)
('Aug', 31)
('Sep', 30)
('Oct', 31)
('Nov', 30)
('Dec', 31)
'''

#Defining variables
months = ('Jan','Feb','Mar','Apr','May','Jun',\
          'Jul','Aug','Sep','Oct','Nov','Dec')
days = (31,28,31,30,31,30,31,31,30,31,30,31)

# Zipping tuples
months_days = zip(months,days)

# Converting to list
months_days = list(months_days)

# Print list data structure transparently to match with intended output
for i in months_days: print(i)

#%% Problem #1 given no redundant input data

    
'''
Output for leap year:
('Jan', 31)
('Feb', 29)
('Mar', 31)
('Apr', 30)
('May', 31)
('Jun', 30)
('Jul', 31)
('Aug', 31)
('Sep', 30)
('Oct', 31)
('Nov', 30)
('Dec', 31)
'''

# Variables defined
months = ('Jan','Feb','Mar','Apr','May','Jun',\
          'Jul','Aug','Sep','Oct','Nov','Dec')
days = (31,30,29,28)
days_31 = (1,3,5,7,8,10,12)
days_30 = (4,6,9,11)
input_done = 0
months_days = []

# Get and sanity check user input for leap year status
while input_done ==0:
    leap = input("Is it a leap year? Input 'y' or 'n' \nInput: ")
    if leap == 'y' or leap == 'n':
        input_done+=1

# Put combined tuples in list data structure for later user
for i in months:
    if months.index(i)+1 in days_31: 
        new_tup=(i,days[0])
    elif months.index(i)+1 in days_30:
        new_tup=(i,days[1])
    elif leap=='y':
        new_tup=(i,days[2])
    elif leap=='n':
        new_tup=(i,days[3])
    months_days.append(new_tup)

# Print list data structure transparently to match with intended output
for i in months_days: print(i)


#%% Problem #2

''' 
Sample of output:
shall 3
i 1
compare 1
thee 2
to 3
a 2
summers 2
day 1
 ...
 ...
 ...
this 2
gives 1
life 1


Archaic words found:
thee
thou
hath
thou
owst (ow'st)
growst (grow'st)
wandrest (wand'rest)
'''

# I used regex to parse; this is the import of the library
import re

#sonnet 18
text =  "Shall I compare thee to a summer's day?\
 Thou art more lovely and more temperate.\
 Rough winds do shake the darling buds of May,\
 And summer's lease hath all too short a date.\
 Sometime too hot the eye of heaven shines,\
 And often is his gold complexion dimmed;\
 And every fair from fair sometime declines,\
 By chance or nature's changing course untrimmed.\
 But thy eternal summer shall not fade\
 Nor lose possession of that fair thou ow'st,\
 Nor shall Death brag thou wand'rest in his shade,\
 When in eternal lines to time thou grow'st.\
 So long as men can breathe or eyes can see,\
 So long lives this, and this gives life to thee."

# Regex to remove punctuation
text = re.sub(r'[^\w\s]','',text)

# Empty data structure for split string
words = []

# Splitting into words list
for w in text.split(' '):
    w = w.lower()
    words.append(w)

# Empty dictionary for historgram
word_freq = dict()

# Populating histogram by checking for keys, 
#incrementing if present, 
#creating at count==1 if not present
for word in words:
    if word in word_freq.keys():
        word_freq[word]+=1
    else: word_freq[word]=1

#printing the dictionary
for k,v in word_freq.items():
    print(k,v)
    

#%% Problem #3

'''Output of function:
The converted temperature of 0 C is 32 F

The converted temperature of 32 F is 0 C

The converted temperature of 100 C is 212 F

The converted temperature of 212 F is 100 C
'''

# Input desired parameters into lists
temp= [0,32,100,212]
scale=['c','f','c','f']

# Convert temps function
def convert_temp(temp,scale):
    if scale == 'c':
        temp2=temp*1.8+32
        print('\nThe converted temperature of',temp,'C','is',int(temp2),'F')
    elif scale == 'f':
        temp2=(temp-32)/1.8
        print('\nThe converted temperature of',temp,'F','is',int(temp2),'C')

# Iterate through input lists to find input variables for conversion function
for i in range(0,len(temp)):
    convert_temp(temp[i],scale[i])



#%% Problem #4

'''
Function output:
For iteration 1 pin 5 output is 0 and pin 6 output is 1 

For iteration 2 pin 5 output is 0 and pin 6 output is 1 

For iteration 3 pin 5 output is 0 and pin 6 output is 1 

For iteration 4 pin 5 output is 1 and pin 6 output is 0 
'''

# input data
pin_1 = [0,0,1,1]
pin_2 = [0,1,0,1]
pin_3 = [0,0,1,1]
pin_4 = [0,1,0,1]

# Defining pin 5 logic
def pin_5(pin1,pin2):
    if pin1 == 1 and pin2 == 1:
        pin5 = 1
    else: pin5 = 0
    return(pin5)

# defining pin 6 logic
def pin_6(pin3,pin4):
    if pin3 == 1 and pin4==1:
        pin6 = 0
    else: pin6 = 1
    return(pin6)

# call pin functions iteratively for values in lists
for i in range(0,len(pin_1)):
    pin1,pin2,pin3,pin4 = pin_1[i],pin_2[i],pin_3[i],pin_4[i]
    pin5,pin6=pin_5(pin1,pin2),pin_6(pin3,pin4)
    print('For iteration',i+1,'pin 5 output is',pin5,\
          'and pin 6 output is',pin6,'\n')
    


#%% Problem #5

''' I prefer using a loop with a conditional end to using recursion. 
    
while len(fib) < target:
    print(len(fib),target)
    fib.append(fib[len(fib)-2]+fib[len(fib)-1])
print(fib)

To follow directions, the following function is recursive, and has the 
following output:
0
1
1
2
3
5
8
13
21
34
55
89
144
233
377
610
987
1597
2584
4181
'''

# Beginning sequence in list form
fib =[0,1]
target = 20 # number of numbers in fibonnaci sequence to calculate

# Function that calls itself
def recurs_fib(list_,t,target):
    if t==target-2: 
        for i in list_: print(i)
    else:
        t+=1
        list_.append(list_[len(list_)-2]+list_[len(list_)-1])
        recurs_fib(list_,t,target)

# First call to instantiate
recurs_fib(fib,0,target)


