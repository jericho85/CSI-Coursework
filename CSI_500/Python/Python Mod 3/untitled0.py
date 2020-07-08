#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 17:45:34 2019

@author: jmcleod
"""

import csv

dat = []
with open('cryptocurrency.csv',encoding='utf-8-sig') as csvfile:
    csvreader = csv.reader(csvfile,delimiter=',')
    for row in csvreader:
        dat.append(row)


# Calculate total market value for each crypto currency
for i in dat:                           #iterate through rows
    for j in i:                         #iterate through columns
        try:                            #if field is a number, convert to number, if not, pass
            j=float(j)
        except: pass
    try:                                #if row is not text, 4th column = 2nd col * 3rd col value
        i[3] = round(float(i[2])*float(i[1]), 2)
    except:
        pass

# Calculate market values
count=0                                 # Row counter variable
for i in dat[-1]:                       # Iterate through bottom row
    if i == "":                         # If the cell is empty, calculate it
        temp=0                          # Summation variable
        for x in dat:                   # Iterate through prior rows
            if count>0:                 # But skip the first one
                try:                    # Adding up the values in rows after the first row with the current column position
                    temp+=float(x[count])
                except: pass            # Except for the first column
        dat[-1][count]=round(temp,2)    # Writing the values to list of lists dataframe
    count+=1                            # Update row counter variable


for i in dat:                           #Check output
    print(i)

with open('cryptocurrency_calc.csv','w',encoding='utf-8-sig') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    for i in dat:
        csvwriter.writerow(i)
        
        
#%%