#############
# Problem 1 #
#############
#R<- c(12.8,21.6,14.8,23.1,34.6,19.7,22.6,29.6,16.4,20.3,29.3,14.9,27.3,22.4,27.5,20.3,38.7,26.4,23.7,26.1,29.5,38.6,44.4,23.2,23.6)
#S<- c(38.4,32.9,48.5,20.9,11.6,22.3,30.2,33.4,26.7,39,12.8,14.6,12.2,23.1,29.4,16,20.1,23.3,22.9,22.5,15.1,31,16.9,16.1,10.8)
#N<- c(35.4,27.4,19.3,41.8,20.3,37.6,36.9,37.3,28.2,23.4,33.7,29.2,41.7,22.6,40.4,34.4,30.4,14.9,51.8,33.8,37.9,29.5,42.4,36.6,47.4)
library(data1.table)
data1 <- fread('https://www2.stat.duke.edu/courses/Spring03/sta113/Data/Hand/fruitfly.dat')
head(data1)
R <- data1$V1
S <- data1$V2
N <- data1$V3

all <- c(R,S,N)

len <- length(R)

qqnorm(R,main='Resistant Normal Q-Q Plot')
qqline(R)
qqnorm(S,main='Susceptible Normal Q-Q Plot')
qqline(S)
qqnorm(N,main='Non-Selected Normal Q-Q Plot')
qqline(N)

qqnorm(all,main='All Fruit Flies Normal Q-Q Plot')
qqline(all)

sumR <- sum(R)
sumS <- sum(S)
sumN <- sum(N)

# Estimate Mean
mu_0 <- mean(c(mean(R),mean(S),mean(N)))

# Estimate the sample precisions
pR0 <- 1/var(R)
pS0 <- 1/var(S)
pN0 <- 1/var(N)

# Estimate mean of aB
ab_mean0 <- mean(c(pR0, pS0, pN0))

# Estimate the variance aB^2
ab2_var0 <- var(c(pR0, pS0, pN0))

# Solving for alpha and beta (shape = sh, scale=sc)
sh <- ab_mean0^2/ab2_var0
sc <- ab2_var0/ab_mean0

# Estimate K
# Sample means
mean_R <- mean(R)
mean_S <- mean(S)
mean_N <- mean(N)

# Sample means Var
means_var <- var(c(mean_R,mean_S,mean_N))

# Precision of Means
means_prec <- 1/means_var

# Estimate K
k <- means_prec / mean(c(pR0,pS0,pN0))

print(c(mu_0,k,sh,sc))

# Now that we have Mu, K, Alpha, and Beta empirical Bayesian Estimates,
# we need to update them for the samples (Unit 5 page 26/27)

r_alpha1 <- sh + n/2
s_alpha1 <- sh + n/2
n_alpha1 <- sh + n/2
r_beta1 <- 1 / (1/sc + 0.5*sum(R-mean_R)^2 + ((n*k)/(2*(n+k)))*(mean_R - mu_0)^2 )
s_beta1 <- 1 / (1/sc + 0.5*sum(S-mean_S)^2 + ((n*k)/(2*(n+k)))*(mean_S - mu_0)^2 )
n_beta1 <- 1 / (1/sc + 0.5*sum(N-mean_N)^2 + ((n*k)/(2*(n+k)))*(mean_N - mu_0)^2 )
r_mu1 <- (k*mu_0 + n*mean_R) / (k+n)
s_mu1 <- (k*mu_0 + n*mean_S) / (k+n)
n_mu1 <- (k*mu_0 + n*mean_N) / (k+n)
r_k1 <- k+n
s_k1 <- k+n
n_k1 <- k+n

# Printing off the results:
print(c(r_mu1,r_k1,r_alpha1,r_beta1))
print(c(s_mu1,s_k1,s_alpha1,s_beta1))
print(c(n_mu1,n_k1,n_alpha1,n_beta1))

# Creating a density plot to review the results
# First, calculating the spread for each theta
r_spread <- sqrt(1/(k*r_alpha1*r_beta1))
s_spread <- sqrt(1/(k*s_alpha1*s_beta1))
n_spread <- sqrt(1/(k*n_alpha1*n_beta1))

# Then updating the input array using the mean and spread
vals <- seq(1,50,length=500)
stdval_r <- (vals-r_mu1)/r_spread
stdval_s <- (vals-s_mu1)/s_spread
stdval_n <- (vals-n_mu1)/n_spread

# Calculating density across inputs
theta_r <- dt(stdval_r,2*r_alpha1)/r_spread
theta_s <- dt(stdval_s,2*s_alpha1)/s_spread
theta_n <- dt(stdval_n,2*n_alpha1)/n_spread

# Plotting the results
plot(vals,theta_r,type='l',col='blue',main="Joint Density Plot",xlab='Values',ylab='Density')
lines(vals,theta_s,col='green')
lines(vals,theta_n,col='red')
legend(0,0.105,c("Resis",'Susceptible','Non-Selected'),
       col=c('blue','green','red'),lty=c(1,1,1))

# And finally, calculating the 90
proba <- c(0.025,0.975)

r_ci <- (qt(proba,2*r_alpha1)*r_spread)+r_mu1
s_ci <- (qt(proba,2*s_alpha1)*s_spread)+s_mu1
n_ci <- (qt(proba,2*n_alpha1)*n_spread)+n_mu1

print(r_ci)
print(s_ci)
print(n_ci)


#############
# Problem 2 #
#############
print(c(r_mu1,r_k1,r_alpha1,r_beta1))
print(c(s_mu1,s_k1,s_alpha1,s_beta1))
print(c(n_mu1,n_k1,n_alpha1,n_beta1))
# Part 1: draw MC samples
numSim <- 100000
r_rho  <- rgamma(numSim,shape=r_alpha1,scale=r_beta1)
r_sigma <- 1/sqrt(r_rho)
r_theta <- rnorm(numSim,mean=mean_R,sd=r_sigma/sqrt(n))

s_rho  <- rgamma(numSim,shape=s_alpha1,scale=s_beta1)
s_sigma <- 1/sqrt(s_rho)
s_theta <- rnorm(numSim,mean=mean_S,sd=s_sigma/sqrt(n))

n_rho  <- rgamma(numSim,shape=n_alpha1,scale=n_beta1)
n_sigma <- 1/sqrt(n_rho)
n_theta <- rnorm(numSim,mean=mean_N,sd=n_sigma/sqrt(n))

# Plot densities
plot(density(r_theta),col='blue',xlim=c(18,38),main="Mean Fecundity of Fruit Flies",xlab='Fecundity',ylab='Probability')
lines(density(s_theta),col='green')
lines(density(n_theta),col='red')

posterior_nonselected <- sum(n_theta>max(r_theta,s_theta))/length(n_theta)

# Part 2: Draw MC samples from Gamma -> T distributions
numSim <- 1000000

# Calculate the spreads
r_spread <- 1/sqrt((k/k+1)*r_alpha1*r_beta1)
s_spread <- 1/sqrt((k/k+1)*s_alpha1*s_beta1)
n_spread <- 1/sqrt((k/k+1)*n_alpha1*n_beta1)

# dMC
r_theta_t <- r_mu1+rt(numSim,df=2*r_alpha1)*r_spread
s_theta_t <- s_mu1+rt(numSim,df=2*s_alpha1)*s_spread
n_theta_t <- n_mu1+rt(numSim,df=2*n_alpha1)*n_spread

# Plotting Densities
plot(density(r_theta_t),col='blue',xlim=c(5,50),main="Fecundity of Single Fruit Flies",xlab='Fecundity',ylab='Probability')
lines(density(s_theta_t),col='green')
lines(density(n_theta_t),col='red')

# Calculate exact percentages. 
posterior_nonselected_1 <- sum((n_theta_t>s_theta_t)&(n_theta_t>r_theta_t))/length(n_theta_t)
n_r<-sum(n_theta_t>r_theta_t )/length(n_theta_t)
n_s<-sum(n_theta_t>s_theta_t)/length(n_theta_t)

# Plot collected Densities
plot(density(r_theta),col='blue',xlim=c(10,50),main="Fecundity of Fruit Flies",xlab='Fecundity',ylab='Probability')
lines(density(s_theta),col='green')
lines(density(n_theta),col='red')
lines(density(r_theta_t),col='darkblue')
lines(density(s_theta_t),col='darkgreen')
lines(density(n_theta_t),col='darkred')

#############
# Problem 3 #
#############
require(rmutil)
acc <- 0.9
tp_alpha0 <- 4.5
tp_beta0 <- 0.5
fp_alpha0 <- 0.5
fp_beta0 <- 4.5

tp_alpha1 <- tp_alpha0 + 28
tp_beta1 <- tp_beta0 +(30-28)

fp_alpha1 <- fp_alpha0 + 7
fp_beta1 <- fp_beta0 + (50-7)

thetas <- seq(0,1,length=1001)

tp_p <- tp_alpha1 / (tp_alpha1+tp_beta1)
tp_m <- tp_alpha1+tp_beta1

fp_p <- fp_alpha1 / (fp_alpha1+fp_beta1)
fp_m <- fp_alpha1+fp_beta1

tp_dens <- dbeta(thetas,tp_alpha1,tp_beta1)
fp_dens <- dbeta(thetas,fp_alpha1,fp_beta1)

plot(thetas,tp_dens,type='l',col='blue',main='True and False Positive Posterior',xlab='Probability',ylab='Density')
lines(thetas,fp_dens,col='green')
legend(0.36,10,c("True Positive","False Positive"),col=c("blue","green"),lty=c(1,1))

pv <- c(0.025, 0.975)
tp_ci <- qbeta(pv,tp_alpha1,tp_beta1)
fp_ci <- qbeta(pv,fp_alpha1,fp_beta1)
tp_ci
fp_ci
#############
# Problem 4 #
#############

alpha0 <- 0.5
beta0 <- Inf
alpha1 <- alpha0 + 123
beta1 <- 1/(1/beta0 + 60)

thetas <- seq(1,3,length=101)
dens <- dgamma(thetas,shape=alpha1,scale=beta1)
plot(thetas,dens,type='l')

#############
# Problem 5 #
#############
x <- dnbinom(seq(0,100,length=101),size=alpha1,prob=1/(1+15*beta1))
plot(seq(0,100,length=101),x,typ='l')

p <- 1-pnbinom(40,size=alpha1,prob=1/(1+15*beta1))
print(p)
#############
# Problem 6 #
#############

nW <- 5
nC <- c(9,23,11,31,17)

numSim <- 1000

aGrid <-  seq(1,50,length=50)       # Alpha
aPrior <- 1/uGrid
aPrior <- mPrior/sum(mPrior)
mGrid <-  seq(4,40,length=50)       # M
mPrior <- seq(0.02,0.02,length=50)   

aMC <- sample(aGrid,1,prob=aPrior)
mMC <- sample(mGrid,1,prob=mPrior)

lam <- rgamma(1,shape=aMC,scale=(mMC/aMC))

q <- array(0, dim=c(numSim,nW))   # Allocate space for simulated CRIMES RATES --- Lambda
q[1,] <- rgamma(nW,shape=aMC,scale=mMC/aMC)  # Initialize crime rate probabilities

for (k in 2:numSim) {
  # Posterior Gamma dist conditional on Data
  alpha1 = aMC[k-1] + (sum(nC))
  beta1  = 1/(1/(mMC[k-1] / aMC[k-1]) + nW)
  
  # Simulated Lambdas
  q[k,] <- rgamma(nW,shape=alpha1,scale=beta1)
  
  
  # These aren't right; not sure how to update the likelihoods of alpha and M
  #update aMC
  aLik <- 1
  for (j in 1:nW) {
    aLik <- aLik * dgamma(q[k,j],aGrid,mGrid/aGrid)
  }
  aPost <- aPrior*aLik/sum(aPrior*aLik)
  
  #update mMC
  mLik <- 1
  for (j in 1:nW) {
    mLik <- mLik * dgamma(q[k,j],aGrid,mGrid/aGrid)
  }
  
  # Draw new values
  aMC[k] <- sample(aGrid,1,prob=aPrior)
  mMC[k] <- sample(mGrid,1,prob=mPrior)
}

quantile(q[,1],c(0.025,0.975))
quantile(q[,2],c(0.025,0.975))
quantile(q[,3],c(0.025,0.975))
quantile(q[,4],c(0.025,0.975))
quantile(q[,5],c(0.025,0.975))

########################
# Problem 6: Attempt 2 #
########################


# Create prior dist (alpha and beta)
# sample new lambdas from that
# from new lambdas get alpha and m likelihoods

# find conditional for lambdas given A and B
# then find posterior and sample from it

nW <- 5
nC <- c(9,23,11,31,17)

numSim <- 100000


aGrid <-  seq(1,50,length=50)       # Alpha
aPrior <- 1/aGrid
aPrior <- aPrior/sum(aPrior)
mGrid <-  seq(4,40,length=50)       # M
mPrior <- seq(0.02,0.02,length=50)   

aMC <- sample(aGrid,1,prob=aPrior)
mMC <- sample(mGrid,1,prob=mPrior)

lam <- array(0, dim=c(numSim,nW))   # Allocate space for simulated CRIMES RATES --- Lambda
lam[1,] <- rgamma(nW,shape=aMC,scale=mMC/aMC)

for (k in 2:numSim) {
  
  # This doesn't seem to work right; getting roughly the same lambdas at the end. 
  # Trying instead to sample from posteriors given data individually by Lambda
  #alpha1 = aMC[k-1] + (sum(nC))
  #beta1  = 1/(1/(mMC[k-1] / aMC[k-1]) + nW)
  
  # sample new lambdas from alpha and beta priors
  #lam[k,] <- rgamma(nW,shape=alpha1,scale=beta1)
  
  
  # Sample new lambdas from individually updated gamma distributions
  for (j in 1:nW){
    alpha1 <- aMC[k-1] + nC[j]
    beta1  <- 1/(1/(mMC[k-1] / aMC[k-1]) + 1)
    lam[k,j] <- rgamma(1,shape=alpha1,scale=beta1)
  }
  
  # from new lambdas get alpha likelihoods
  aLik <- 1
  for (j in 1:nW) {
    aLik <- aLik * dgamma(lam[k-1,j],aMC[k-1]*aPrior,(mMC[k-1]*mPrior)/(aMC[k-1]*aPrior))
  }
  # find conditional for lambdas given A and B
  # then find posterior and sample from it
  aPost <- aPrior*aLik/sum(aPrior*aLik)
  aMC[k] <- sample(aGrid,1,prob=aPost)
  
  # from new lambdas get beta likelihoods
  mLik <- 1
  for (j in 1:nW) {
    mLik <- mLik * dgamma(lam[k-1,j],aMC[k]*aPrior,(mMC[k-1]*mPrior)/(aMC[k]*aPrior))
  }
  # find conditional for lambdas given A and B
  # then find posterior and sample from it
  mPost <- mPrior*mLik/sum(mPrior*mLik)
  mMC[k] <- sample(mGrid,1,prob=mPost)
  
}


quantile(lam[,1],c(0.025, 0.975))
quantile(lam[,2],c(0.025, 0.975))
quantile(lam[,3],c(0.025, 0.975))
quantile(lam[,4],c(0.025, 0.975))
quantile(lam[,5],c(0.025, 0.975))

plot(density(lam[,1]),col='dark blue',xlim=c(0,45),main='Density of Lambda by Ward',ylab='Density','xlab'='Lambda')
lines(density(lam[,2]),col='purple')
lines(density(lam[,3]),col='dark green')
lines(density(lam[,4]),col='dark orange')
lines(density(lam[,5]),col='dark red')
legend(32,0.15,c("Ward 1",'Ward 2','Ward 3','Ward 4','Ward 5'),
       col=c('dark blue','purple','dark green','dark orange','dark red'),lty=c(1,1,1,1,1))

##########################
# Problem 6: no comments #
##########################

nW <- 5
nC <- c(9,23,11,31,17)
numSim <- 100000
aGrid <-  seq(1,50,length=50)       
aPrior <- 1/aGrid
aPrior <- aPrior/sum(aPrior)
mGrid <-  seq(4,40,length=50)       
mPrior <- seq(0.02,0.02,length=50)   
aMC <- sample(aGrid,1,prob=aPrior)
mMC <- sample(mGrid,1,prob=mPrior)
lam <- array(0, dim=c(numSim,nW))   
lam[1,] <- rgamma(nW,shape=aMC,scale=mMC/aMC)

for (k in 2:numSim) {
  for (j in 1:nW){
    alpha1 <- aMC[k-1] + nC[j]
    beta1  <- 1/(1/(mMC[k-1] / aMC[k-1]) + 1)
    lam[k,j] <- rgamma(1,shape=alpha1,scale=beta1)
  }
  aLik <- 1
  for (j in 1:nW) {
    aLik <- aLik * dgamma(lam[k-1,j],aMC[k-1]*aPrior,(mMC[k-1]*mPrior)/(aMC[k-1]*aPrior))
  }
  aPost <- aPrior*aLik/sum(aPrior*aLik)
  aMC[k] <- sample(aGrid,1,prob=aPost)
  mLik <- 1
  for (j in 1:nW) {
    mLik <- mLik * dgamma(lam[k-1,j],aMC[k]*aPrior,(mMC[k-1]*mPrior)/(aMC[k]*aPrior))
  }
  mPost <- mPrior*mLik/sum(mPrior*mLik)
  mMC[k] <- sample(mGrid,1,prob=mPost)
}






#############
# Problem 7 #
#############

cost_fp <- 0.05
cost_fn <- 1

p <- seq(0,1,length=101)

# Actual  Test  Action  Loss  Probability
# Ok      Ok    None    0     0.92*(1-P)
# Ok      Def   flag    0.05  0.08*(1-P)
# Def     Ok    None    1     0.12*P
# Def     Def   flag    0     0.88*P

follow_test <- p*0.12*1 + (1-p)*0.08*0.05
always_flag <- (1-p)*0.05
never_flag  <- p*1

plot(follow_test,type='l',col='blue',ylim=c(0,.1),xlim=c(0,50))
lines(always_flag,col='red')
lines(never_flag,col='green')
legend(30,.10,c("Follow Test","Always Flag",'Never Flag'),col=c("blue","red","green"),lty=c(1,1,1))

print(follow_test)
print(never_flag)
print(always_flag)

for (i in seq(1,100,length=100)) {
  print(c(i,follow_test[i],always_flag[i]))
}
#############
# Problem 8 #
#############

library(data.table)
data8 <- fread('https://www2.stat.duke.edu/courses/Spring03/sta113/Data/Hand/icecream.dat')
head(data8)

y <- data8$V2 # Consumption
x <- data8$V5 # Temperature F
x <- x[-length(x)]
y <- y[-length(y)] 
n = length(x)

xbar <- mean(x)
ybar <- mean(y)

b <- sum( (x-xbar) * (y-ybar)) / sum( (x-xbar)^2 ) 
a <- ybar - b*xbar

sxx <- sum( (x-xbar)^2 )
syy <- sum( (y-ybar)^2 )
sxy <- sum( (x-xbar) * (y-ybar) )
see <- sum( (y-ybar-b*(x-xbar))^2)

#posteriors
rho_alpha <- (n-2)/2
rho_beta  <- 2/see

eta_center <- ybar
eta_spread <- (n*(n-2)/see)^-0.5
eta_degf   <- n-2

beta_center <- b
beta_spread <- (see*(n-2)/see)^-0.5
beta_degf   <- n-2

s2<- see/(n-2)
s <- sqrt(s2)

print(mean(y))
print(mean(x))

fit=lm(y ~ x)
summary(fit)  # Summary of regression results
plot(fit)     # Diagnostic plots from lm object

qnorm(c(0.025, 0.975),mean=0.2068621,sd=0.0247002) #intercept
qnorm(c(0.025, 0.975),mean=0.0031074,sd=0.0004779) #slope

temps <- seq(20,80,length=61)
min_vals <- sort(temps*0.002170733 + 0.1584506)
max_vals <- sort(temps*0.004044067 + 0.2552736)
plot(x,y,ylim=c(0.1,0.6))
lines(temps,min_vals)
lines(temps,max_vals)
print(max_vals)
#############
# Problem 9 #
#############
# Posterior predictive distribution for temps
xlow = 46
xhigh = 98

predlow.center = a + b*xlow
predlow.spread = sqrt(((xhigh-xbar)^2/sxx + 1/n + 1)*see/(n-2))
predlow.df = n-2

predhigh.center = a + b*xhigh
predhigh.spread = sqrt(((xhigh-xbar)^2/sxx + 1/n + 1)*see/(n-2))
predhigh.df = n-2

# Exact credible interval for prediction @ 19 mg 
predlow.center + qt(c(0.05,0.95),predlow.df)*predlow.spread
predhigh.center + qt(c(0.05,0.95),predhigh.df)*predhigh.spread

##############
# Problem 10 #
##############

# Beta binomial?
# Priors
beta_e <- c(1,1)
beta_d <- c(1,1)
beta_u <- c(1,1) 

# Posteriors
beta_e <- c(10,22)
beta_d <- c(16,16)
beta_u <- c(7,25) 

e_ci <- qbeta(c(0.05,0.95),shape1=beta_e[1],shape2=beta_e[2])
d_ci <- qbeta(c(0.05,0.95),shape1=beta_d[1],shape2=beta_d[2])
u_ci <- qbeta(c(0.05,0.95),shape1=beta_u[1],shape2=beta_u[2])
e_ci
d_ci
u_ci

e_ci <- qbeta(c(.5),shape1=beta_e[1],shape2=beta_e[2])
d_ci <- qbeta(c(.5),shape1=beta_d[1],shape2=beta_d[2])
u_ci <- qbeta(c(.5),shape1=beta_u[1],shape2=beta_u[2])
v <- c(e_ci,d_ci,u_ci)
v <- v/sum(v)
print(v)


#
l_h <- 8
c_p <- 170.1-7.5 + l_h
c_t <- 190

ex <- seq(1,100,length=100)
t_p <- ex + c_p
f_g <- t_p / (c_t+100)

for (i in 1:100){
  print(c(ex[i],f_g[i]))
}

