############  SYST 664 - Bayesian Inference and Decision Theory  #######

# Assignment 7
# Wolf River Pollutant Concentration Data Analysis 
# Use JAGS to do MCMC simulation of joint posterior distribution of means and precisions

# The data 
wolf.surface=c(3.74, 4.61, 4.00, 4.67, 4.87, 5.12, 4.52, 5.29, 5.74, 5.48)
wolf.bottom=c(5.44, 6.88, 5.37, 5.44, 5.03, 6.48, 3.89, 5.85, 6.85, 7.16)


##########  Problem 6B  ############
# Use JAGS to do Gibbs sampling from joint posterior distribution

library(R2jags)    # running JAGS from r
library(superdiag) # mcmc diagnostics
library(coda)
library(lattice)   # for some of the plots 
library(MCMCvis)   # visualization functions


# Fit the JAGS model
# Make sure working directory is set to location of file "wolfriver.model.jags"

## Fit surface posterior distribution
n=length(wolf.surface)  # number of observations
x=wolf.surface          # observations
surface.fit <- jags(data=list("x", "n"), 
                           inits=function(){list("theta"=c(mean(x)), "rho"=c(1/var(x)))},
                           parameters.to.save = c("theta", "rho"), 
                           n.chains=1, n.iter=10000, n.burnin=0,n.thin=1,
                           model.file="wolfriver.model.jags")

surface.fit         # summary of output
plot(as.mcmc(surface.fit))   # traceplots and densities 

## Fit bottom posterior distribution
n=length(wolf.bottom)  # number of observations
x=wolf.bottom          # observations
bottom.fit <- jags(data=list("x", "n"), 
                    inits=function(){list("theta"=c(mean(x)), "rho"=c(1/var(x)))},
                    parameters.to.save = c("theta", "rho"), 
                    n.chains=1, n.iter=10000, n.burnin=0,n.thin=1,
                    model.file="wolfriver.model.jags")

bottom.fit                 # summary of output 
plot(as.mcmc(bottom.fit))   # traceplots and densities 

# Find posterior credible intervals for parameters

surface.chains=as.data.frame(MCMCchains(surface.fit))  # extract the chains to data frame
quantile(surface.chains$theta,c(0.05,0.95))
quantile(1/sqrt(surface.chains$rho),c(0.05,0.95))
bottom.chains=as.data.frame(MCMCchains(bottom.fit))  # extract the chains to data frame
quantile(bottom.chains$theta,c(0.05,0.95))
quantile(1/sqrt(bottom.chains$rho),c(0.05,0.95))
quantile(bottom.chains$theta - surface.chains$theta,c(0.05,0.95))

##########  Problem 6C  ############
# Traceplot, acf, and effective sample size

traceplot(as.mcmc(bottom.chains$theta - surface.chains$theta),
          main="Traceplot of Surface Minus Bottom Mean")
acf(bottom.chains$theta - surface.chains$theta,
    main="ACF of Surface Minus Bottom Mean")
effectiveSize(bottom.chains$theta - surface.chains$theta)
