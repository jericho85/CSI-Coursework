# Jericho McLeod
# CSI 500
# R Mod 1 Assignment

# Problem One

company = c('Hewlett-Packard','IBM','Google','Amazon')
n_shares = c(1000,350,250,500)
close_price = c(18.79,160.26,1134.42,1571.68)
c_value = n_shares*close_price
portf_value = sum(c_value)
portf_value
# Value: 1143326

sales = c(0,100,50,0)
n_shares = n_shares-sales
c_value = n_shares*close_price
portf_value = sum(c_value)
portf_value
# Value: 1071579

increase = 0.0625
close_price = close_price * (1+increase)
c_value = n_shares*close_price
portf_value = sum(c_value)
portf_value
# Value: 1138553

# Problem 2
# Supply Line
s_y1=500
s_y2=300
s_x1=1
s_x2=2
s_m = (s_y2-s_y1)/(s_x2-s_x1)
# m = -200/1,000,000, or -0.0002, or -2e-4

# Intercept = y=mx+b, or 700 in this case
s_b=700
s_y2==s_x2*s_m+s_b # verification of intercept

# Formula: y = mx + b
# Equation: y = -200 x + 700

# Demand line
d_y1=100
d_y2=200
d_x1=1
d_x2=2
d_m = (d_y2-d_y1)/(d_x2-d_x1)
# m = 100m

# Intercept = y=mx+b, or 700 in this case
d_b=0
d_y2==d_x2*s_m+d_b

# Formula: y = mx + b
# Equation: y = 100 x + 0

A = c(-s_m,1,-d_m,1)
A = matrix(nrow=2,ncol=2,data=A,byrow=TRUE)
A
b = c(s_b,d_b)
b = matrix(nrow=2,ncol=1,data=b,byrow=TRUE)
b
det(A)!=0 # verify not singular
AI = solve(A)
AI

# A^-1 is:
#  1/300    -1/300
#  1/3      2/3

A%*%AI
# Output is:
#   1.000000e+00    0
#  -5.551115e-17    1
# Close enough to identity matrix for me! Machine precision accounts for variance

# I actually didn't look up the vector * matrix syntax, but just created b as a ncol=1 nrow=2 matrix
# Thus, multiplying them in R is the same as multiplying any other two matrices
AI%*%b

# X solution, or quantity of zipfits to produce with the expectation of selling 
# them at market equilibrium, is 2.3333... (million)
# Y solution, or the price at which to sell them, is $233.33

# Problem 3

data_one = rnorm(100,mean=0,sd=1)
data_two = rnorm(100,mean=0.8,sd=2.5)
stem(data_one)
hist(data_two)
scatter(data_one)
plot(data_one)
plot(density(data_two)) 
boxplot(data_one,data_two)
     