
# coding: utf-8

# # Vectors
# 
# ### Various calculations that begin with the assumption that e1 = [1,0] and e2 = [0,1] as the basis vectors

# __First we must import libraries__

# In[110]:


import math


# __Assign Initial Vectors__

# In[225]:


def assign_vector_r():
    vector_r = [2,1]
    print("Vector R: ",vector_r)
    return(vector_r)

def assign_vector_s():
    vector_s = [3,-4]
    print("Vector S: ",vector_s)
    return(vector_s)

def verified_vectors():
    vector_r, vector_s = assign_vector_r(),assign_vector_s()
    if len(vector_r) == len(vector_s):
        return(vector_r,vector_s)
    else: 
        print("Error: the vectors do not have the same length!")


# __Calculate dot product of vectors R and S__
# 
# $$
# r*s
# $$

# In[226]:


def dot_product(vector_r,vector_s):
    
    dot_prod=0
    for r,s in zip(vector_r,vector_s):
        dot_prod+=r*s
    print("Dot-product equals: ",dot_prod)
    if dot_prod == 0:
        print("These vectors are orthogonal!")
    return(dot_prod)

vector_r,vector_s=verified_vectors()
dot_product(vector_r,vector_s)


# __Calculate the Length of R__
# 
# $$
# | r |
# $$

# In[234]:


def vector_length(vector):
    temp_sum=0
    for i in vector:
        temp_sum=temp_sum + i*i
    mod_vector = math.sqrt(temp_sum)
    print("The length of the input vector is: ",mod_vector)
    return(mod_vector)

vector_r,vector_s = verified_vectors()
vector_length(vector_s)


# __Calculate Mod Vector of R__
# 
# _Edit the function call to change the vector for which you want to calculate the mod vector._
# 
# 
# $$
# | r |^2
# $$

# In[233]:


def modular_vector(vector):
    temp_sum=0
    for i in vector:
        temp_sum=temp_sum + i*i
#    mod_vector = math.sqrt(temp_sum)
    mod_vector = temp_sum
    print("The mod of the input vector is: ",mod_vector)
    return(mod_vector)

vector_r,vector_s = verified_vectors()
modular_vector(vector_s)


# Calculate Scalar Projection
# 
# $$
# \frac{r*s}{|r|}
# $$

# In[237]:


def scalar_projection(vector_r,vector_s):
    dot_prod = dot_product(vector_r,vector_s)
    mod_vector = vector_length(vector_r)
    scalar_projection = dot_prod / mod_vector
    print("The scalar projection is: ",scalar_projection)
    return(scalar_projection)
vector_r,vector_s=verified_vectors()
scalar_projection(vector_r,vector_s)


# __Calculate Vector Projections__
# 
# 
# 
# $$
# \frac{r*s}{|r|^2}
# $$

# In[228]:


def vector_projection(vector_r,vector_s):
    dot_prod = dot_product(vector_r,vector_s)
    vector_length = vector_length(vector_r)
    vector_projection = dot_prod / mod_vector
    print("The vector projection is: ",vector_projection)
    return(vector_projection)
vector_r,vector_s=verified_vectors()
vector_projection(vector_r,vector_s)


# __Defining new Basis Vectors__
# 
# In order to change basis we must first define new vectors in terms of the original basis vectors.

# In[223]:


def basis_vector_b1():
    vector_b1 = [-3,1]
    print("Vector B1: ",vector_b1)
    return(vector_b1)

def basis_vector_b2():
    vector_b2 = [1,3]
    print("Vector B2: ",vector_b2)
    return(vector_b2)

def verified_basis_vectors():
    vector_b1, vector_b2 = basis_vector_b1(),basis_vector_b2()
    if len(vector_b1) == len(vector_b2):
        return(vector_b1,vector_b2)
    else: 
        print("Error: the new basis vectors do not have the same length!")


# __Shift Basis of R with dual value basis vectors__
# 
# $$
# \frac{r*b1}{|b1|^2} ... \frac{r*bn}{|bn|^2}
# $$

# In[224]:


def basis_shift(vector_r,vector_b1,vector_b2):
    value_1 = vector_projection(vector_b1,vector_r)
    value_2 = vector_projection(vector_b2,vector_r)
    new_vector = list()
    new_vector.append(value_1)
    new_vector.append(value_2)
    print("The new vector is: ",new_vector)

vector_r,vector_s = verified_vectors()
vector_b1,vector_b2 = verified_basis_vectors()
basis_shift(vector_r,vector_b1,vector_b2)


# __Shift Basis of R with multiple value basis vectors__
# 
# _Note that R and Basis Vectors are redefined in this cell_

# In[231]:


def basis_vectors():
    basis_vectors={}
#    basis_vectors['bvector1']=[-4,-3,8]
    basis_vectors['bvector2']=[1,2,3]
    basis_vectors['bvector3']=[-2,1,0]
    basis_vectors['bvector4']=[-3,-6,5]
    return(basis_vectors)

def basis_shift_2(vector_r,basis_vectors):
    new_values = {}
#    for x in range(0,len(vector_r)):
#        new_values["value{0}".format(x)]=""
    for key in new_values:
        print(key)
    counter =1
    for k,v in basis_vectors.items():
        print(k,v)
        temp_val = vector_projection(v,vector_r)
        temp_name = "Value"+str(counter)
        new_values[temp_name]=temp_val
        counter+=1
    return(new_values)
#    print("The new vector is: ",new_vector)

vector_r = [-4,-3,8]
basis_vectors = basis_vectors()
basis_shift_2(vector_r,basis_vectors)

