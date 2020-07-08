### Example of using JAGS from Unit 6

# install.packages("R2jags")   # only run this once
# install.packages("superdiag")   # only run this once

require(R2jags)    # running JAGS from r
require(superdiag) # mcmc diagnostics
require(coda)
require(lattice)   # for some of the plots 

# set.seed(12345)  # set seed for reproducibility

# The data 
reaction.times=c(5.743, 5.606, 5.858, 5.656, 5.591, 5.793, 5.697, 
                 5.875, 5.677, 5.73, 5.69, 5.919, 5.981, 5.996, 
                 5.635, 5.799, 5.537, 5.642, 5.858, 5.793, 5.805, 
                 5.73, 5.677, 5.553, 5.829, 5.489, 5.724, 5.793, 5.684, 5.606)
n <- length(reaction.times)

rt.data  <- list("reaction.times", "n")

rt.params <- c("theta", "rho")

rt.inits <- function(){
 list("theta"=c(6), "rho"=c(25))
 }

# Fit the JAGS model
# Make sure working directory is set to location of file "reaction.time.model.jags"
reaction.times.fit <- jags(data=rt.data, inits=rt.inits,
 rt.params, n.chains=4, n.iter=9000, n.burnin=1000,
 model.file="reaction.time.model.jags")
 
# Process output with coda package
reaction.times.fit.mcmc<-as.mcmc(reaction.times.fit) # convert to R MCMC object
# Note: default thinning gave a thinning interval of 8
summary(reaction.times.fit.mcmc)    # Summary table of MCMC outputs 
plot(reaction.times.fit.mcmc)       # Plots of MCMC results
acfplot(reaction.times.fit.mcmc)

 
#Additional plots
xyplot(reaction.times.fit.mcmc)      # trace plots in lattice package
densityplot(reaction.times.fit.mcmc) # density plots in lattice package


#Diagnostics
superdiag(reaction.times.fit.mcmc, burnin=10)
