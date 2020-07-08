# -*- coding: utf-8 -*-
"""
Ebb3: Given the attached dataset of ball bearing properties with 11
properties and
210 samples, perform the PCA analysis of this problem:
    a) Form the correlation matrix (DONE))
    b) Solve the eigenvalue problem for the correlation matrix by finding
    the eigenvalues and eigenvectors (DONE)
    c) Sort eigenvalues and eigenvectors from largest (number 1) to
    smallest (number 11) eigenvalue (DONE)
    d) Check that the eigenvectors are orthonormal (DONE))
    e) Determine how many PCs give at least 80% of the variance (DONE))
    f) Specify which are the predominant original properties of PC1 and
    PC2 (hint: largest coefficients in absolute value)
    g) Project the original data on each eigenvector pertaining to the
    subset found in (e)
    h) Plot the projected data in plots PC1-PC2, PC1-PC3 and PC2-PC3.
"""

import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
input_df = pd.read_csv("C:\\Users\\Jericho\\Google Drive\\School\\CSI 690\\ballbearings.csv",header=0)
import numpy as np
from mpl_toolkits.mplot3d import Axes3D 

"""Normalizing the data"""
df = (input_df-input_df.mean())/ (input_df.max()-input_df.min())

"""My function that creates a correlation matrix:"""
def correlation_matrix(df):
    cols = list(df)
    df[cols[1]]
    corr_matrix = []
    for i in range(0,len(cols)):
        row = []
        for j in range(0,len(cols)):
            if j>i:pass
            row.append(df[cols[i]].corr(df[cols[j]]))
        corr_matrix.append(row)
    
    for i in corr_matrix:
        print(i)

#correlation_matrix(df)

"""Using a library for correlation matrix to save re-importing it to dataframe"""
def correlation_matrix_lib(df):
    corr_matrix = df.corr()
#    print(corr_matrix) #shows correlations
#    print(pd.plotting.scatter_matrix(df)) #shows symmetrical plot
    return(corr_matrix)

corr_matrix=correlation_matrix_lib(df)

def correlation_matrix_graphic(df):
    plt.pyplot.matshow(df.corr())
    plt.pyplot.colorbar()

#correlation_matrix_graphic(df)



#print(corr_matrix)

eig_vals,eig_vectors = np.linalg.eig(corr_matrix)

#print(eig_vectors)
#print()
eig_vectors = np.transpose(eig_vectors)
#print(eig_vectors)
#print()
#print()
#print("Eigen values:")
#print(eig_vals)
#print()
#print("Eigen vectors:")
#print(eig_vectors)

"""Sorting Eigen values and eigen vectors by eigen value size"""
order= eig_vals.argsort()[::-1]
eig_vals = eig_vals[order]
eig_vectors = eig_vectors[order]

#print()
#print("Sorted Eigen values:")
#print(eig_vals)
#print()
#print("Sorted Eigen vectors:")
#print(eig_vectors)
#print()

"""Checking for orthonormal eigenvectors"""
ortho = np.dot(eig_vectors,eig_vectors.T)
#print("Orthonormal test:")
#print(ortho)

"""Check the number of Principal components needed to capture 80% of the variance"""
total_eig_val = sum(eig_vals)
counter = 1
cum_sum = 0
for i in eig_vals:
    percent = (i/total_eig_val)
    cum_sum+=percent
#    print("PCA",counter,percent,cum_sum)
    counter+=1
    
"""Answer: 6 principal components will capture 86% of the variance"""    
#print(eig_vectors,eig_vals)
#print()


"""Which original properties are predominant to which PCA?"""
def identify_predominant_properties(eig_vectors):
    counter =1
    for i in eig_vectors:
        max_val = abs(max(i))
        subcounter =1
        for j in i:
            if j==max_val:
                print("For PCA",counter,"feature",subcounter,"was the most predominant.")
            subcounter+=1
        counter+=1

def project_pca(eig_vectors,input_df): # PROBLEM HERE: NEED TO TRIM EIG VECTORS T
    sig_pca = 6
    sig_eig_vectors = eig_vectors[:sig_pca]
    return(sig_eig_vectors)
    
sig_eig_vectors=project_pca(eig_vectors,input_df)
#print(sig_eig_vectors)

sig_eig_vectors=np.array(sig_eig_vectors)
#print()
#print(sig_eig_vectors[0][0])
input_df=np.array(input_df)
df=np.array(df)

def transform_data(sig_eig_vectors,input_df): 
    transformed_data = pd.DataFrame()
    pca_tracker =0
    pca_name=["PCA1","PCA2","PCA3","PCA4","PCA5","PCA6"]
    for x in sig_eig_vectors:
        temp_list=[]
        counter=0
        for i in range(0,len(input_df)):
            temp_val=0
            for j in input_df:
                var = counter%11
                temp_val += x[var] * input_df[i][j] #PROBLEM IS HERE: input_df[j][i] does not return the value
        #        if pca_tracker == 0: 
        #            if var==1:print(x[var],input_df[j][i])
                counter+=1
#                if pca_tracker == 0: print(temp_val)
            temp_list.append(temp_val)
#            if pca_tracker==0:print(temp_val)
        transformed_data[pca_name[pca_tracker]]=np.array(temp_list)
        pca_tracker+=1
            
    return(transformed_data)
                
#transformed_data=transform_data(sig_eig_vectors,input_df)


def transform_updated_data(sig_eig_vectors,input_df):
    transformed_data= pd.DataFrame()
    pca_tracker=0
    pca_name=["PCA1","PCA2","PCA3","PCA4","PCA5","PCA6"]
    pca_array = []
    for x in input_df: #iterate through data columns
#        print(x)
        temp_list = []
        for i in range(0,len(pca_name)):
#            print()
#            print(i)
            temp_val=0
            for j in range(0,11):
                temp_val += x[j]*sig_eig_vectors[i][j]
                #print(temp_val)
            temp_list.append(temp_val)
        pca_array.append(temp_list)
    return(pca_array)
pca_array=transform_updated_data(sig_eig_vectors,df)

#print(eig_vals)
#print()
#print(eig_vectors)
print(pca_array)
print()
transformed = pd.DataFrame(pca_array)
print(transformed)
#transformed.to_csv('C:\\Users\\Jericho\\Google Drive\\School\\CSI 690\\test.csv',sep=',')
#transformed.plot.scatter(x=transformed[0],y=transformed[1])
#print()
#print(input_df)

#threedee.scatter(transformed.index, transformed)

#transformed_data.plot.scatter(x='PCA1',y='PCA2')
#transformed_data.plot.scatter(x='PCA1',y='PCA3')
#transformed_data.plot.scatter(x='PCA2',y='PCA3')



#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#x=transformed_data['PCA2']
#y=transformed_data['PCA1']
#z=transformed_data['PCA3']
#ax.scatter(x,y,z,c='b',marker='o')
#ax.set_xlabel('PCA2')
#ax.set_ylabel('PCA1')
#ax.set_zlabel('PCA3')
#
#
#plt.show()
#
#transformed_data.plot.scatter(x='PCA1',y='PCA2')
#transformed_data.plot.scatter(x='PCA1',y='PCA3')
#transformed_data.plot.scatter(x='PCA1',y='PCA4')
#transformed_data.plot.scatter(x='PCA1',y='PCA5')
#transformed_data.plot.scatter(x='PCA1',y='PCA6')
#transformed_data.plot.scatter(x='PCA2',y='PCA3')
#transformed_data.plot.scatter(x='PCA2',y='PCA4')
#transformed_data.plot.scatter(x='PCA2',y='PCA5')
#transformed_data.plot.scatter(x='PCA2',y='PCA6')
#transformed_data.plot.scatter(x='PCA3',y='PCA4')
#transformed_data.plot.scatter(x='PCA3',y='PCA5')
#transformed_data.plot.scatter(x='PCA3',y='PCA6')
#transformed_data.plot.scatter(x='PCA4',y='PCA5')
#transformed_data.plot.scatter(x='PCA4',y='PCA6')
#transformed_data.plot.scatter(x='PCA6',y='PCA6')
#%%