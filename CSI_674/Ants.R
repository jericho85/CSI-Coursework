#Ants example
#Data from Weber, 1946, "Dimorphism in the African Oecophyulla Worker and an Anomaly
#http://antbase.org/ants/publications/10434/10434.pdf

lengthCounts <- c(8,41,52,7,6,11,32,56,59,23,5)
lengths <- c(4.0,4.5,5.0,5.5,6.0,6.5,7.0,7.5,8.0,8.5,9.0)

barplot(lengthCounts,names.arg=lengths,main="Ant Lengths",col="lightblue")

# Mixture model
mu1 <- 4.8
sd1 <- 0.36
mu2 <- 7.7
sd2 <- 0.61
pr1 <- 0.36
pr2 <- (1-pr1)

xvals <- 350:1100/100
mixDens <- pr1*dnorm(xvals,mu1,sd1)+pr2*dnorm(xvals,mu2,sd2)

# Sample Frequencies and Mixture Density Plot 
plot(xvals,mixDens,col="red",type="l",main="",ylab="",xlab="Body Length (mm)")
lines(lengths,lengthCounts/(300*.5),col="darkcyan",type="h",lwd=3)
legend(8.2,0.42,c("Mixture Density","Sample Frequency"),col=c("red","darkcyan"),lty=c(1,1),lwd=c(1,3))

numSim <- 10000

# Gibbs sampling

xval <- mu1  #Starting value
xG <- NULL
zG <- NULL
for (i in 1:numSim) {
	likz1 <- pr1*dnorm(xval,mu1,sd1)
	likz2 <- pr2*dnorm(xval,mu2,sd2)
	prz1 <- likz1/(likz1+likz2)
	zval <- rbinom(1,1,prz1)
	if (zval==1) zG[i] <- 1 else zG[i] <- 2
	if (zval==1) xval <- rnorm(1,mu1,sd1) else xval <- rnorm(1,mu2,sd2)
	xG[i] <- xval
}

# Trace plot, Histogram, and ACF
plot(1:numSim,xG,main="",ylab="Simulated Body Length (mm)",xlab="Iteration")
histogram(xG,xlab="Gibbs Simulated Body Length (mm)",ylab="Frequency")
acf(xG, main="")

effectiveSize(xG)


# Direct Monte Carlo

xD <- NULL
zD <- NULL
for (i in 1:numSim) {
	zval <- rbinom(1,1,pr1)
	if (zval==1) zD[i] <- 1 else zD[i] <- 2
	if (zval==1) xD[i] <- rnorm(1,mu1,sd1) else xD[i] <- rnorm(1,mu2,sd2)
	}
	
# Trace plot, Histogram, and ACF
plot(1:numSim,xD,main="",ylab="Simulated Body Length (mm)",xlab="Iteration")
histogram(xD,xlab="Direct MC Simulated Body Length (mm)",ylab="Frequency")
acf(xD,main="")

	
plot(density(xD),main="",ylab="Kernel Density Estimate for Direct MC")
lines(xvals,mixDens,col="red")



minor=rnorm(100000*pr1,mu1,sd1)
plot(density(minor))
lines(xvals,dnorm(xvals,mu1,sd1),col="red")

major=rnorm(100000*pr2,mu2,sd2)
plot(density(major))
lines(xvals,dnorm(xvals,mu2,sd2),col="red")

plot(density(c(major,minor)))
lines(xvals,pr1*dnorm(xvals,mu1,sd1)+pr2*dnorm(xvals,mu2,sd2),col="red")