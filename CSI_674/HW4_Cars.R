# OR 664 / SYST 664 / CSI 674 Spring 2020
# Assignment 4 
# Continued analysis of automobile arrival data

# The data
carCounts <- c(3, 5, 7, 3, 3)  # Counts were given as inputs for HW 4

# Parameter values (for plotting)

# Problem 1 - "Uniform" prior
# Use shape 1 and scale infinity

alpha0=1
beta0=Inf
alpha1=alpha0+sum(carCounts*c(0:4))
beta1=1/(1/beta0 + sum(carCounts))

post.mean = alpha1*beta1              # Posterior mean
post.sdev = sqrt(alpha1*beta1^2)      # Posterior standard deviation
post.median = qgamma(0.5, shape=alpha1, scale=beta1)  # posterior median
post.mode = (alpha1-1)*beta1          # posterior mode

lower.val = qgamma(0.025, shape=alpha1, scale=beta1)  # lower bound on 95% interval
upper.val = qgamma(0.975, shape=alpha1, scale=beta1)  # lower bound on 95% interval


# The problem did not ask for a triplot, but we can do one
lambda=seq(length=200,from=0.03,to=5)  # This is the range of lambda values for plot
priorDens=dgamma(lambda,shape=alpha0,scale=beta0)  # Prior
postDens=dgamma(lambda,shape=alpha1,scale=beta1)  # Posterior
normLikC=dgamma(lambda,shape=1+sum(carCounts*c(0:4)),
                scale=1/sum(carCounts))    # Normalized Likelihood is a Gamma(6,1/6)

plot(lambda,priorDens,type="l",col="blue",
     main="Triplot for Vehicle Traffic Rate (Uniform Prior)",
     xlab="Rate (vehicles per 15 seconds)",ylab="Probability Density",
     xlim=c(0,max(lambda)),ylim=c(0,max(postDens)))
lines(lambda,normLikC,col="green")
lines(lambda,postDens,col="red")
legend(3.5,1.0,c("Prior","Norm Lik","Posterior"),col=c("blue","green","red"),
       lty=c(1,1,1))

# Problem 2 - Fit Gamma distribution parameters to expert quantiles

# Define a function to evaluate fit between expert quantiles
# and Gamma quantiles by computing sum of squared deviations
#    param - shape and scale of gamma
#    pvals - probability points to evaluate
#    exqu - expert provided quantiles at probability points
gamma.fit = function(param,pvals,exqu) {         
  alpha=param[1]
  beta=param[2]
  sum((exqu-qgamma(pvals,shape=alpha,scale=beta))^2)
}

# Find best fit for expert inputs 
fit = optim(c(1,1),         # starting values for shape and scale
      function(ab)          # pass function evaluating fit to gamma distribution
        {gamma.fit(ab,                # shape and scale are parameters to optimize
                   c(0.1,0.5,0.9),    # points for which we have judgments
                   c(1.5,3.75,7))})   # the expert-provided quantiles

# Informative prior using expert judgments
alpha0=fit$par[1]      # optimal shape is first returned argument
beta0=fit$par[2]       # optimal scale is second returned argument

# can also use get.gamma.par in the rriskdistributions package, which gives a similar result
library(rriskDistributions)
get.gamma.par(c(0.1,0.5,0.9), c(1.5, 3.75, 7))

# Problem 3 - Find posterior distribution (using result of optim fit)

priorDens=dgamma(lambda,shape=alpha0,scale=beta0)  # Prior from Problem 2
alpha1=alpha0+sum(carCounts*c(0:4))
beta1=1/(1/beta0 + sum(carCounts))  # carCounts is a bad name for this
postDens=dgamma(lambda,shape=alpha1,scale=beta1)  # Posterior
normLikC=dgamma(lambda,shape=1+sum(carCounts*c(0:4)),
                scale=1/sum(carCounts))    # Normalized Likelihood is a Gamma(6,1/6)

post.mean = alpha1*beta1              # Posterior mean
post.sdev = sqrt(alpha1*beta1^2)      # Posterior standard deviation
post.median = qgamma(0.5, shape=alpha1, scale=beta1)  # posterior median
post.mode = (alpha1-1)*beta1          # posterior mode

lower.val = qgamma(0.025, shape=alpha1, scale=beta1)  # lower bound on 95% interval
upper.val = qgamma(0.975, shape=alpha1, scale=beta1)  # lower bound on 95% interval

# Problem 4 - Triplot

plot(lambda,priorDens,type="l",col="blue",
     main="Triplot for Vehicle Traffic Rate (Informative Prior)",
     xlab="Rate (vehicles per 15 seconds)",ylab="Probability Density",
     xlim=c(0,max(lambda)),ylim=c(0,max(postDens)))
lines(lambda,normLikC,col="green")
lines(lambda,postDens,col="red")
legend(3.5,1.0,c("Prior","Norm Lik","Posterior"),col=c("blue","green","red"),
       lty=c(1,1,1))

####
# Alternative solution to Problem 2
# We can find the best values alpha0 and beta0 by brute force

dv = 10000        # initialize deviation to large number

for (a in seq(from=0.5,to=7,length=200)) {     # loop through many alpha values
  for (b in seq(from=0.5,to=10,length=200)) {    # loop through many beta values
    d=sum((c(1.5,3.75,7) # sum of squared deviations between expert and gamma quantiles
       - qgamma(c(0.1,0.5,0.9),shape=a,scale=b))^2)
    if (d<dv) {            # If smallest so far, save the value
      dv = d
      alpha0 = a
      beta0 = b
    } } }
