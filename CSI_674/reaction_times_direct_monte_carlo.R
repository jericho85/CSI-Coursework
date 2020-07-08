### Bayesian Inference and Decision Theory ###

# Monte Carlo example from Unit 5

# Reaction time data from Gelman et al.
reaction.times=c(5.743, 5.606, 5.858, 5.656, 5.591, 5.793, 5.697, 5.875, 5.677, 5.73, 
                 5.69, 5.919, 5.981, 5.996, 5.635, 5.799, 5.537, 5.642, 5.858, 5.793, 
                 5.805, 5.73, 5.677, 5.553, 5.829, 5.489, 5.724, 5.793, 5.684, 5.606)
x = reaction.times
xbar = mean(x)
n = length(x)

# Assume non-informative prior distribution
# Normal-Gamma with mu0=0, k0=0, alpha0=-1/2, beta0=infinity
# Posterior hyperparameters mu1, k1, alpha1, beta1
mu1 <- xbar
k1 <- n
alpha1 <- -1/2 + n/2
beta1 <- 1/(0.5*sum((x-xbar)^2))
spread1 <- sqrt(1/(k1*alpha1*beta1))

# Plot t and normal posterior density functions
thetaVals <- 5.64+(0:100)/500
stdVals <- (thetaVals - mu1)/spread1
thetaMargDens <- dt(stdVals,df=2*alpha1)/spread1
normDens <- dnorm(thetaVals,mu1,spread1)
dens <- cbind(thetaMargDens,normDens)
matplot(thetaVals,dens,type=c("l","l"),col=c("red","blue"),xlab="Theta", ylab="Probability Density")
legend(5.76,15,c("Unknown SD (t)","Known SD (Normal)"),col=c("red","blue"),lty=c(1,2))

#Set simulation sample size
numSim <- 10000
# Simulate directly from the posterior distribution
rhoDirect <- rgamma(numSim,shape=alpha1,scale=beta1) 
sigmaDirect <- 1/sqrt(rhoDirect)
thetaDirect <- rnorm(numSim,mean=xbar,sd=sigmaDirect/sqrt(n))
#Plot theoretical and Monte Carlo density functions
plot(density(thetaDirect),col="darkgreen",lty=2,main="",xlab="Theta") 
lines(thetaVals,thetaMargDens,col="red")
legend(5.76,15,c("Monte Carlo","Theoretical t"),col=c("darkgreen","red"),lty=c(2,1))

