### Bayesian Inference and Decision Theory ###

# Reaction time example from Unit 5 and 6

# Log reaction time data (log reaction times) for first non-schizophrenic subject
reaction.times=c(5.743, 5.606, 5.858, 5.656, 5.591, 5.793, 5.697, 5.875, 5.677, 5.73, 
                 5.69, 5.919, 5.981, 5.996, 5.635, 5.799, 5.537, 5.642, 5.858, 5.793, 
                 5.805, 5.73, 5.677, 5.553, 5.829, 5.489, 5.724, 5.793, 5.684, 5.606)

require(coda)   # load the coda package - Output Analysis and Diagnostics for MCMC

x = reaction.times
xbar = mean(x)
n = length(x)

#####
# First consider conjugate model of Unit 5
#   Assume non-informative prior distribution
#   Normal-Gamma with mu0=0, k0=0, alpha0=-1/2, beta0=infinity
#   Posterior hyperparameters mu1, k1, alpha1, beta1 
mu0=0
k0=0
alpha0=-0.5
beta0=Inf

mu1 <- (mu0*k0+xbar*n)/(k0+n)
k1 <- k0+n
alpha1 <- alpha0 + n/2
beta1 <- 1/(1/beta0 + 0.5*sum((x-xbar)^2 + k0*n/(k0+n)*(xbar-mu0)))

spread1 <- sqrt(1/(k1*alpha1*beta1))

thetaVals <- 5.64+(0:100)/500
stdVals <- (thetaVals - mu1)/spread1
thetaMargDens <- dt(stdVals,df=2*alpha1)/spread1
normDens <- dnorm(thetaVals,mu1,spread1)
dens <- cbind(thetaMargDens,normDens)
matplot(thetaVals,dens,type=c("l","l"),col=c("red","blue"),
        xlab="Theta",ylab="Probability Density")
legend(5.76,15,c("Unknown SD (t)","Known SD (Normal)"),
       col=c("red","blue"),lty=c(1,2))

# Monte Carlo Simulation - Direct Monte Carlo and Gibbs Sampling
# Set simulation sample size
numSim <- 10000

# Simulate directly from the posterior distribution 
rhoDirect <- rgamma(numSim,shape=alpha1,scale=beta1)
sigmaDirect <- 1/sqrt(rhoDirect)
thetaDirect <- rnorm(numSim,mean=mu1,sd=sigmaDirect/sqrt(k1))

####
# Now use Gibbs sampling for semi-conjugate distribution (equations Unit 6 p.12)

#Prior hyperparameters (all but tau0 are same as normal-gamma model)
mu0 = 0
tau0 = Inf     # SD of Theta
alpha0=-0.5
beta0=Inf

# Initialize rho (don't need to initialize theta because it is sampled first)
rGprev <- 1/var(x)     # Initial guess for precision
rhoGibbs = thetaGibbs = sigmaGibbs = NULL   # Initialize variables for simulation
for (k in 1:numSim) {
  muG = (mu0/tau0^2 + n*rGprev*xbar) /   # reduces to xbar when tau = Inf
    (1/tau0^2 + n*rGprev)
  tauG = 1/sqrt(1/tau0^2 + n*rGprev)     # reduces to sigmaGibbs/sqrt(n) when tau = Inf
  thetaGibbs[k] <- rnorm(1,mean=muG,sd=tauG)    # simulate new value for theta
  alphaG<-alpha0 + n/2    # This could be set outside the loop because alpha1 does not change
  betaG<-1/(1/beta0 + 0.5*sum((x-thetaGibbs[k])^2)) # update scale given current theta
  rhoGibbs[k]<-rgamma(1,shape=alphaG,scale=betaG)   # sample new value for rho
  sigmaGibbs[k]<-1/sqrt(rhoGibbs[k])                # calculate new value of sigma
  rGprev = rhoGibbs[k]    # previous value of rho
}


#Plot theoretical and Monte Carlo density functions
plot(density(thetaDirect),col="darkgreen",lty=2,main="",xlab="Theta")
lines(density(thetaGibbs),col="blue",lty=3)
lines(thetaVals,thetaMargDens,col="red")
legend(5.76,15,c("Direct MC KD","Gibbs KD","Theoretical t"),col=c("darkgreen","blue","red"),lty=c(2,3,1))

#Plot theoretical and Monte Carlo density functions
plot(density(sigmaDirect),col="darkgreen",lty=2,main="",xlab="Sigma")
lines(density(sigmaGibbs),col="blue",lty=3)
legend(.18,20,c("Direct MC KD","Gibbs KD"),col=c("darkgreen","blue"),lty=c(2,3))

#Plot theoretical and Monte Carlo density functions
plot(density(rhoDirect),col="darkgreen",lty=2,main="",xlab="Rho")
lines(density(rhoGibbs),col="blue",lty=3)
legend(100,0.02,c("Direct MC KD","Gibbs KD"),col=c("darkgreen","blue"),lty=c(2,3))


#Quantiles
quantile(thetaGibbs, c(0.025,0.975))
quantile(sigmaGibbs, c(0.025,0.975))

#Calculate effective sample size
effectiveSize(thetaDirect)
effectiveSize(thetaGibbs)
effectiveSize(sigmaDirect)
effectiveSize(sigmaGibbs)

# Trace plot
traceplot(as.mcmc(thetaGibbs), main="Traceplot for Gibbs Sampling Estimate of Theta")
traceplot(as.mcmc(sigmaGibbs), main="Traceplot for Gibbs Sampling Estimate of Sigma")

# ACF
acf(thetaGibbs)
acf(sigmaGibbs)

