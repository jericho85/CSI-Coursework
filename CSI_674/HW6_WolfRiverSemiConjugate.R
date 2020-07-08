############  SYST 664 - Bayesian Inference and Decision Theory  #######

# Assignment 8
# Wolf River Pollutant Concentration Data Analysis 
# Perform Gibbs sampling of joint posterior distribution of means and precisions

# The data 
wolf.surface=c(3.74, 4.61, 4.00, 4.67, 4.87, 5.12, 4.52, 5.29, 5.74, 5.48)
wolf.bottom=c(5.44, 6.88, 5.37, 5.44, 5.03, 6.48, 3.89, 5.85, 6.85, 7.16)

# Sufficient statistics for mean
xs=wolf.surface
sums=sum(wolf.surface)
xb=wolf.bottom
sumb=sum(wolf.bottom)
n <- length(xs)     # same sample size for both surface and bottom

##########  Problem 6B  ############

# Assume independent priors for mean and precision
mu=6      # Prior mean of HCB concentration
tau=1.5   # Prior SD of HCB concentration
alpha=4.5
beta=0.19

#Set simulation sample size
numSim <- 10000

# Gibbs sample initialization 
thetasGibbs = mean(xs)    # Initial guess for surface mean
thetabGibbs = mean(xb)    # Initial guess for bottom mean
sigmasGibbs = sd(xs)      # Initial guess for surface SD
sigmabGibbs = sd(xb)      # Initial guess for bottom SD
rhosGibbs = 1/sd(xs)^2    # Initial guess for surface precision
rhobGibbs = 1/sd(xb)^2    # Initial guess for bottom precision

# Draw the Gibbs samples
for (k in 2:numSim) {
  tau.star.s=1/sqrt(1/tau^2+n*rhosGibbs[k-1])
  mu.star.s=(mu/tau^2 + sum(xs)*rhosGibbs[k-1])/(1/tau^2+n*rhosGibbs[k-1])
	thetasGibbs[k]<-rnorm(1,mean=mu.star.s,sd=tau.star.s)
	tau.star.b=1/sqrt(1/tau^2+n*rhobGibbs[k-1])
	mu.star.b=(mu/tau^2 + sum(xb)*rhobGibbs[k-1])/(1/tau^2+n*rhobGibbs[k-1])
	thetabGibbs[k]<-rnorm(1,mean=mu.star.b,sd=tau.star.b)
	
	alpha.star.s = alpha.star.b = alpha+n/2     # alpha1 does not change 
	beta.star.s<-1/(1/beta + 0.5*sum((xs-thetasGibbs[k])^2))
	beta.star.b<-1/(1/beta + 0.5*sum((xb-thetabGibbs[k])^2))
	rhosGibbs[k]<-rgamma(1,shape=alpha.star.s,scale=beta.star.s)
	rhobGibbs[k]<-rgamma(1,shape=alpha.star.b,scale=beta.star.b)
	}

sigmasGibbs = 1/sqrt(rhosGibbs)    # get sample of standard deviations
sigmabGibbs = 1/sqrt(rhobGibbs)

#####  Plots of Gibbs Sampler Output ####

#Scatterplot of rho vs theta and sigma vs theta
plot(thetasGibbs,rhosGibbs,pch=".", col="blue",
     xlab=expression(theta),ylab=expression(rho),
     main="Gibbs Sample for Means and Precisions",
     xlim=c(3.5,7))  # set limits to show all points
points(thetabGibbs,rhobGibbs,pch=".", col="red")
legend(6.3,2.7,c("Surface","Bottom"),col=c("blue","red"),pch=c(16,16))

plot(thetasGibbs,sigmasGibbs,pch=".", col="blue",
     xlab=expression(theta),ylab=expression(sigma),
     main="Gibbs Sample for Means and Standard Deviations",
     xlim=c(3.5,7))  # set limits to show all points
points(thetabGibbs,sigmabGibbs,pch=".", col="red")
legend(6.3,2.2,c("Surface","Bottom"),col=c("blue","red"),pch=c(16,16))


plot(density(thetasGibbs),col="blue",
     main="Posterior Density Estimates for Means",
     xlab=expression(theta),ylab="Probability Density",
     xlim=c(3.5,7))
lines(density(thetabGibbs),col="red")
legend(6.3,1.2,c("Surface","Bottom"),col=c("blue","red"),lty=c(1,1))

plot(density(sigmasGibbs),col="blue",
     main="Posterior Density Estimates for Standard Deviations",
     xlab=expression(sigma),ylab="Probability Density")
lines(density(sigmabGibbs),col="red")
legend(1.6,2,c("Surface","Bottom"),col=c("blue","red"),lty=c(1,1))


#Quantiles of the sample - endpoints of 90% credible intervals
quantile(thetasGibbs, c(0.05,0.95))  # Mean concentration, surface
quantile(rhosGibbs, c(0.05,0.95))    # Precision of concentration, surface
quantile(sigmasGibbs, c(0.05,0.95))  # SDev of concentration, surface
quantile(thetabGibbs, c(0.05,0.95))  # Mean concentration, bottom
quantile(rhobGibbs, c(0.05,0.95))    # Precision of concentration, bottom
quantile(sigmabGibbs, c(0.05,0.95))  # SDev of concentration, bottom
quantile(thetabGibbs-thetasGibbs, c(0.05,0.95))  # Difference in means

#Does bottom have higher pollutant concentration? Larger standard deviation?

theta.diff = thetabGibbs - thetasGibbs  # differences in means 
sigma.diff = sigmabGibbs - sigmasGibbs  # differences in SDevs
sum(theta.diff>0)/length(theta.diff)
sum(sigma.diff>0)/length(sigma.diff)


# Posterior point estimates
mean(thetasGibbs)
mean(thetabGibbs)
mean(sigmasGibbs)
mean(sigmabGibbs)
mean(rhosGibbs)
mean(rhobGibbs)
mean(theta.diff)
mean(sigma.diff)

##########  Problem 6C  ############


# Traceplot
library(coda)
diff.mcmc=as.mcmc(theta.diff)   # make into MCMC object
traceplot(diff.mcmc,main="Traceplot of Difference in Means")      # argument must be MCMC object

# Autocorrelation
acf(theta.diff,main="Autocorrelation Plot for Difference in Means")

#Diagnostics
effectiveSize(thetasGibbs)
effectiveSize(thetabGibbs)
effectiveSize(rhosGibbs)
effectiveSize(rhobGibbs)
effectiveSize(sigmasGibbs)
effectiveSize(sigmabGibbs)
effectiveSize(theta.diff)


