### Bayesian Inference and Decision Theory ###

# This code produces the triplot for the transmission error example from Unit 3
# Prior distribution is Gamma with shape 2 and scale 0.48
# There are 5 errors in 6 observations

# The data
errors <- c(1,0,1,2,1,0)

# Continuous version of the transmission errors example -- page 15-17 of Unit 3
alpha0=2; beta0=0.48                  # prior shape and scale
alpha1=alpha0+sum(errors)             # posterior shape
beta1=1/(1/beta0+length(errors))      # posterior scale


# Do a triplot
lambda=seq(length=100,from=0.03,to=3)
priorDens=dgamma(lambda,shape=alpha0,scale=beta0) # Prior density
postDens=dgamma(lambda,shape=alpha1,scale=beta1)  # Posterior density
normLikC=dgamma(lambda,               # Normalized Likelihood is Gamma(6,1/6)
                shape=sum(errors)+1,scale=1/length(errors))    

plot(lambda,priorDens,type="l",col="blue",main="Triplot for Transmission Error Rate (Continuous)",
     xlab="Error Rate (errors per hour)",ylab="Probability Density",
     xlim=c(0,3),ylim=c(0,1.3))
lines(lambda,normLikC,col="green")
lines(lambda,postDens,col="red")
legend(2.0,1.0,c("Prior","Norm Lik","Posterior"),col=c("blue","green","red"),lty=c(1,1,1))

# Posterior quantities (using properties of gamma distribution)
alpha1*beta1          # posterior mean
sqrt(alpha1*beta1^2)  # posterior standard deviation
(alpha1-1)*beta1      # posterior mode
qgamma(0.5, shape=alpha1, scale=beta1) # posterior median
qgamma(c(0.025,0.975), shape=alpha1, scale=beta1) # posterior 95% interval

