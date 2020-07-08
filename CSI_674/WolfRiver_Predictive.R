############  SYST 664 - Bayesian Inference and Decision Theory  #######

# Assignment 7
# Wolf River Pollutant Concentration Prediction of Future Sample 

# The data 
wolf.surface=c(3.74, 4.61, 4.00, 4.67, 4.87, 5.12, 4.52, 5.29, 5.74, 5.48)
wolf.bottom=c(5.44, 6.88, 5.37, 5.44, 5.03, 6.48, 3.89, 5.85, 6.85, 7.16)

# Sufficient statistics for mean
xs=wolf.surface
sums=sum(wolf.surface)
xb=wolf.bottom
sumb=sum(wolf.bottom)
n <- length(xs)

##########  Find Postrior Distribution (from Assignment 6)  ############

# Conjugate unknown var - Separate priors for surface & bottom

# Prior hyperparameters
mus=0         # prior mean is 0
ks=0          # prior precision multiplier is 0
alphas=-0.5   # Shape of Jeffreys prior for precision
betas=Inf     # Infinite scale for Jeffreys prior
mub=0         # prior mean is 0
kb=0          # prior precision multiplier is 0
alphab=-0.5   # Shape of Jeffreys prior for precision
betab=Inf     # Infinite scale for Jeffreys prior

# Posterior hyperparameters
mus.star=(ks*mus+sum(xs))/(ks+n)
ks.star=ks+n
alphas.star=alphas+n/2
betas.star=( 1/betas + 0.5*sum((xs-mean(xs))^2) + 
               0.5*ks*n/(ks+n)*(mean(xs)-mus)^2 )^-1

mub.star=(kb*mub+sum(xb))/(kb+n)
kb.star=kb+n
alphab.star=alphab+n/2
betab.star=( 1/betab + 0.5*sum((xb-mean(xb))^2) + 
               0.5*kb*n/(kb+n)*(mean(xb)-mub)^2 )^-1

##########  Problem 1  ############

# Predictive distribution for samples of size 10 and 40
# Nonstandard t distribution 

ssize = 40    # number of observations to predict (10 or 40)
pred.spread.s =   # spread of predictive t distribution
  1/sqrt(ks.star*ssize/(ks.star+ssize)*alphas.star*betas.star)
mus.star+qt(c(0.025,0.975),2*alphas.star)*pred.spread.s  # interval for sample mean

ssize = 10    # number of observations to predict (10 or 40)
pred.spread.b =   # spread of predictive t distribution
  1/sqrt(kb.star*ssize/(kb.star+ssize)*alphab.star*betab.star)
mub.star+qt(c(0.025,0.975),2*alphab.star)*pred.spread.b  # interval for sample mean

##########  Problem 2  ############

# We do this two different ways and verify that they give the same results to
# within sampling error. First draw samples of Theta and Rho, draw ssize observations,  
# compute the sample mean, and average.

numsim=5000
rhob=rgamma(numsim,shape=alphab.star,scale=betab.star) # sample bottom precision
thetab=rnorm(numsim,mub.star,1/sqrt(kb.star*rhob))     # sample surface precision
rhos=rgamma(numsim,shape=alphas.star,scale=betas.star) # sample bottom mean
thetas=rnorm(numsim,mus.star,1/sqrt(ks.star*rhos))     # sample surface mean
diff = 0     # Difference in sample means - initialize to 0
dd=0
for (i in 1:ssize) {
  diff = diff + 
    rnorm(numsim,thetab,1/sqrt(rhob)) -    # sample bottom observation
    rnorm(numsim,thetas,1/sqrt(rhos))      # sample surface observation and subtrace
  }
diff = diff / ssize    # Calculate average - divide sum by number of observations

quantile(diff, c(0.025,0.975))   # quantiles
plot(density(diff),              # kernel density plot
     main=paste("Density for Difference in Sample Means for m =",ssize))

# We can also sample from the t distribution (need two independent samples,
# one for surface and one for bottom)
diff1 = mub.star + rt(numsim,2*alphab.star)*pred.spread.b -
  mus.star + rt(numsim,2*alphas.star)*pred.spread.s 
quantile(diff1,c(0.025,0.975))  # Compare with quantiles from full sampling method

##########  Problem 3  ############

# Known standard deviation model

mu0=0           # prior mean for theta is 0
tau0=Inf        # prior SD of theta is infinite

sigmas = sd(xs) # observation SD is assumed known and equal to sample SD
sigmab = sd(xb) # observation SD is assumed known and equal to sample SD

mus.star =      # Posterior mean for surface
  (mu0/tau0^2 + sum(xs)/sigmas^2)/(1/tau0^2+n/sigmas^2)
taus.star =     # Posterior SD of surface mean
  (1/tau0^2+n/sigmas^2)^(-1/2)
mub.star =      # Posterior mean for bottom
  (mu0/tau0^2 + sum(xb)/sigmab^2)/(1/tau0^2+n/sigmab^2)  
taub.star =     # Posterior SD of surface mean
  (1/tau0^2+n/sigmab^2)^(-1/2)

# Predictive intervals

qnorm(c(0.025,0.975),    # Surface, sample size 10
      mus.star,sqrt(taus.star^2 + sigmas^2/10))
qnorm(c(0.025,0.975),    # Surface, sample size 40
      mus.star,sqrt(taus.star^2 + sigmas^2/40))
qnorm(c(0.025,0.975),    # Surface, sample size 10
      mub.star,sqrt(taub.star^2 + sigmab^2/10))
qnorm(c(0.025,0.975),    # Surface, sample size 40
      mub.star,sqrt(taub.star^2 + sigmab^2/40))


# Kernel density plot
plot(density(diff),main=paste("Density for Difference in Sample Means"))
lines(density(diff),col="blue")
legend(-1.2,0.55,c("m=10","m=40"),col=c("blue","black"),lty=c(1,1))
