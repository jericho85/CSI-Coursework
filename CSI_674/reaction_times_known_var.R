### Bayesian Inference and Decision Theory ###

# Reaction Time Example from Unit 5
# Analysis assuming standard deviation is known to be 0.127

# The data 
# Data set can be found at 
#    http://www.stat.columbia.edu/~gelman/book/data/schiz.asc 
# The observations are natural logarithms of reaction times of the 
# first non-schizophrenic subject
reaction.times = c(312, 272, 350, 286, 268, 328, 298, 356, 292, 308, 
                   296, 372, 396, 402, 280, 330, 254, 282, 350, 328, 
                   332, 308, 292, 258, 340, 242, 306, 328, 294, 272)
x = log(reaction.times)  # Data - natural log of reaction times
n = length(x)            # Number of observations
xbar = mean(x)

# Prior hyperparameters - noninformative reference prior
mu=0         # prior mean is 0
tau=Inf      # prior standard deviation is infinity
sigma=sd(x)  # treat standard deviation as known and equal to sample standard deviation

# Posterior distribution for reaction times for subject is normal
mu.star = (mu/tau^2+sum(x)/sigma^2)/(1/tau^2+n/sigma^2)  # Posterior mean
tau.star = (1/(tau^2) + n/(sigma^2))^(-1/2)              # Posterior std. dev

# Triplot
th=seq(length=201,from=5.4,to=6.0)
priorDens=dnorm(th,mean=mu,sd=tau)   # prior density (all zeros)
normLik=dnorm(th,mean=xbar,sd=sigma/sqrt(n)) 
postDens=dnorm(th,mean=mu.star,sd=tau.star)
plot(th,priorDens,type="l",col="blue",ylim=c(0,18),
     main=paste("Triplot for Reaction Time Data"),
     xlab="theta",ylab="Probability Density")
lines(th,normLik,col="red")
lines(th,postDens,col="green")
legend(5.4,17,c("Prior","NormLik","Posterior"), col=c("blue","red","green"),lty=c(1,1,1))	

# Posterior credible interval for theta
theta.star.025=qnorm(0.025,mean=mu.star,sd=tau.star)
theta.star.975=qnorm(0.975,mean=mu.star,sd=tau.star)

###################
# Process observations in batches of 5
for (b in 1:6) {
	batch=reaction.times[((b-1)*5+1):(b*5)]  # next batch of data
	# Posterior mean and std dev
	tau[b+1]=(1/tau[b]^2+5/sigma^2)^(-1/2)  
	mu[b+1]=(mu[b]/tau[b]^2+sum(batch)/sigma^2)/(1/tau[b]^2+5/sigma^2)
	# Posterior credible interval for theta
	theta025[b]=qnorm(0.025,mean=mu[b+1],sd=tau[b+1])
	theta975[b]=qnorm(0.975,mean=mu[b+1],sd=tau[b+1])
	# Posterior credible interval for mean of next 5 obs
	xbar025[b]=qnorm(0.025,mean=mu[b+1],sd=sqrt(tau[b+1]^2+sigma^2/5))
	xbar975[b]=qnorm(0.975,mean=mu[b+1],sd=sqrt(tau[b+1]^2+sigma^2/5))
}

# Triplots of Mean Parameter for 5-observation batches
th=seq(length=201,from=5.4,to=6.0)
for (b in 1:6) {
	priorDens=dnorm(th,mean=mu[b],sd=tau[b])
	xbar=mean(reaction.times[((b-1)*5+1):(b*5)])
	normLik=dnorm(th,mean=xbar,sd=sigma/sqrt(5))
	postDens=dnorm(th,mean=mu[b+1],sd=tau[b+1])
	plot(th,priorDens,type="l",col="blue",ylim=c(0,18),main=paste("Triplot for Obs ",(b-1)*5+1, " to ", b*5),xlab="theta",ylab="Probability Density")
	lines(th,normLik,col="red")
	lines(th,postDens,col="green")
	legend(5.4,17,c("Prior","NormLik","Posterior"), col=c("blue","red","green"),lty=c(1,1,1))	
}

# Plot predictive distributions for 5-observation batches (starting w 2nd batch)
for (b in 2:6) {
	xbar=seq(length=101,from=5.4,to=6.0)
	bayespred=dnorm(xbar,mean=mu[b],sd=sqrt(tau[b]^2+sigma^2/5))
	pointpred=dnorm(xbar,mean=mu[b],sd=sigma/sqrt(5))
	plot(xbar,bayespred,type="l",col="blue",ylim=c(0,8),xlim=c(5.4,6),
       main=paste("Predict Obs ",(b-1)*5+1, " to ", b*5, "- Known Variance"),
       xlab="Sample Mean",
       ylab="Probability Density")
	lines(xbar,pointpred,col="red")
	nextobs=mean(reaction.times[((b-1)*5+1):(b*5)])
	lines(c(nextobs,nextobs),c(0,dnorm(nextobs,mean=mu[b],sd=sqrt(tau[b]^2+sigma^2/5))),col="green")
	legend(5.4,8,c("Bayesian Predictive","Point Estimate",paste("Avg Obs ",(b-1)*5+1, " to ", b*5)),col=c("blue","red","green"),lty=c(1,1,1))	
}

