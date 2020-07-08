# OR 664 / SYST 664 / CSI 674 Spring 2019
# Assignment 3 
# Analysis of automobile arrivals

# Set up the data
carIntervals=c(12, 2, 6, 2, 19, 5, 34, 4, 1, 4, 8, 7, 1, 21, 
               6, 11, 8, 28, 6, 4, 5, 1, 18, 9, 5, 1, 21, 1, 
               1, 5, 3, 14, 5, 3, 4, 5, 1, 3, 16, 2)
summary(carIntervals)            # Summary statistics for car interrival times 

# Part a: Evaluate fit of exponential distribution using a Q-Q plot
exp.quantiles = qexp(ppoints(length(carIntervals)))
qqplot(exp.quantiles,carIntervals,
       main="Exponential Q-Q Plot of Car Interarrival Times",
       xlab="Exponential Quantiles",ylab="Empirical Quantiles")
lines(exp.quantiles,exp.quantiles*mean(carIntervals))  # Overlay a line

# Goodness of fit based on exponential distribution
qq=c(0:8)/8                            # exponential quantiles
br=qexp(qq,rate=1/mean(carIntervals))  # bin boundaries
oo=hist(carIntervals,br,plot=F)$counts # counts in the bins

# With 8 bins we use chisquare test with degrees of freedom 6
# 8 equally likely bins means expected count of 5 in each bin
sum((oo-5)^2/5)       # chisquare test statistic
qchisq(0.95,6)        # critical value for test statistic


# Part b: Compare empirical and theoretical distributions for arrivals by 15-second interval
carTimes = cumsum(carIntervals)           # Cumulative sums
Which15Sec <- ceiling(carTimes/15)        # Minute during which each car passed
CarsBy15Sec <- tabulate(Which15Sec)       # Count number of cars in each 15 second interval
ObservedCounts <- table(CarsBy15Sec)      # Counts of intervals with 0, 1, 2 etc. cars

ObservedCounts[6]=0                       # No intervals with more than 5 cars

# Sample mean is total number of events divided by total number of time periods
# Here we assume 40 cars in 21 15-second intervals (ignoring the fact that the
# last interval is slightly shorter than 15 seconds) 
ArrivalRate=sum(CarsBy15Sec)/length(CarsBy15Sec)  # Estimate Poisson rate by 40 cars in 21 intervals
ExpectedCounts=dpois(0:4,ArrivalRate)*length(CarsBy15Sec)    # Expected counts for Poisson distribution
ExpectedCounts[6]=(1-ppois(4,ArrivalRate))*length(CarsBy15Sec)

# Plot the data
ObsExp <- rbind(ObservedCounts,ExpectedCounts) # bind into matrix for plotting
barplot(ObsExp,main="Distribution of Arrivals per 15-second Block", 
        xlab="Number of Cars (in 15-second Block)", 
        ylab="Empirical Count (of 15-second Blocks)", col=c("lightblue","pink"), 
        border=c("darkblue","red"),names=c(0:4,"5+"), beside=TRUE,
        legend=c("Observed","Expected"))


# Chi-squared test
oc = c(ObservedCounts[1:4],sum(ObservedCounts[5:6]))
ec = c(ExpectedCounts[1:4],sum(ExpectedCounts[5:6]))

# With 5 bins we use chisquare test with degrees of freedom 3
sum((oc-ec)^2/ec)             # Test statistic
qchisq(0.95,3)                # 95th percentile of chisq distribution


# Part c: Find the posterior distribution from first 10 observations
lambda=seq(from=0.2,to=4,by=0.2)
priorDist = array(1,length(lambda))/length(lambda)
lik = array(1,length(lambda))   # initialize likelihood to all 1's
for (i in 1:10) {               # multiply likelihoods of first 10 observations
  lik = lik*dpois(CarsBy15Sec[i],lambda)
}
postDist=priorDist*lik/sum(priorDist*lik)  # posterior distribution
barplot(postDist,
        main=expression(paste("Posterior Distribution for",~Lambda,
                        " after 10 Observations")),
        col=c("mediumpurple"), border=c("purple4"),
        xlab=expression(lambda), ylab="Probability",
        names=lambda)

# Posterior mean and standard deviation
postMean = sum(lambda*postDist)
postVar = sum(((lambda-postMean)^2)*postDist)
postSD = sqrt(postVar)

# Quantiles of posterior distribution
# Quantile q is smallest value of lambda for which the posterior cdf is >= q
# To find quantile q: first we count how many values of posterior cdf are less than q,
# then we add 1 to find the index of the first value that is greater than or equal to q, 
# then we find the value of lambda corresponding to this index
postmed = lambda[sum(cumsum(postDist)<0.5)+1]  # Median
q025=lambda[sum(cumsum(postDist)<0.025)+1]     # 0.025 quantile
q95=lambda[sum(cumsum(postDist)<0.95)+1]       # 0.95 quantile
q975=lambda[sum(cumsum(postDist)<0.975)+1]     # 0.975 quantile

# Verify quantiles using the qdiscrete function in e1071 package
library(e1071)
qdiscrete(c(0.025, 0.5, 0.95, 0.975), postDist, lambda)

postmode = lambda[which(postDist==max(postDist))]  # Mode of the posterior distribution

## Plot the cumulative distribution function
plot(lambda,cumsum(postDist),type="s",     # type "s" means a step function
     main="Cumulative Distribution Function for Rate After 10 Obs",
     xlab="Lambda",ylab="Cumulative Probability")
lines(c(0.0,postmed,postmed), c(0.5,0.5,0),col="red",lty=2)
lines(c(0.0,q95,q95),c(0.95,0.95,0),col="blue",lty=4)
legend(2.6,0.5,c("Median","95%"),col=c("red","blue"),lty=c(2,4))


# Part d: Find the posterior distribution from all observations
priorDist = postDist            # use posterior distribution from part b as prior
lik = array(1,length(lambda))   # initialize likelihood to all 1's
for (i in 11:length(CarsBy15Sec)) {               # multiply likelihoods of first 10 observations
  lik = lik*dpois(CarsBy15Sec[i],lambda)
}
postDist=priorDist*lik/sum(priorDist*lik)  # posterior distribution
barplot(postDist,
        main=expression(paste("Posterior Distribution for",~Lambda,
                              " after All 21 Observations")),
        col=c("mediumpurple"), border=c("purple4"),
        xlab=expression(lambda), ylab="Probability",
        names=lambda)

# Posterior mean and standard deviation
postMean = sum(lambda*postDist)
postVar = sum(((lambda-postMean)^2)*postDist)
postSD = sqrt(postVar)

# Quantiles of posterior distribution
# Quantile q is smallest value of lambda for which the posterior cdf is >= q
# To find quantile q: first we count how many values of posterior cdf are less than q,
# then we add 1 to find the index of the first value that is greater than or equal to q, 
# then we find the value of lambda corresponding to this index
postmed = lambda[sum(cumsum(postDist)<0.5)+1]  # Median
q025=lambda[sum(cumsum(postDist)<0.025)+1]     # 0.025 quantile
q95=lambda[sum(cumsum(postDist)<0.95)+1]       # 0.95 quantile
q975=lambda[sum(cumsum(postDist)<0.975)+1]     # 0.975 quantile

# Verify quantiles using the qdiscrete function in e1071 package
qdiscrete(c(0.025, 0.5, 0.95, 0.975), postDist, lambda)

postmode = lambda[which(postDist==max(postDist))]  # Mode of the posterior distribution

## Plot the cumulative distribution function
plot(lambda,cumsum(postDist),type="s",     # type "s" means a step function
     main="Cumulative Distribution Function for Rate After 21 Observations",
     xlab="Lambda",ylab="Cumulative Probability")
lines(c(0.0,postmed,postmed), c(0.5,0.5,0),col="red",lty=2)
lines(c(0.0,q95,q95),c(0.95,0.95,0),col="blue",lty=4)
legend(2.6,0.5,c("Median","95%"),col=c("red","blue"),lty=c(2,4))

# Part e: Predictive distribution

# We calculate the predictive distribution for k events 
# by multiplying Poisson probability for k events given lambda
# times posterior probability of lambda and adding the result

predDist=NULL
for (i in 0:5) {
  predDist[i+1] = sum(postDist*dpois(i,lambda))
}

predDist[6]=1-sum(predDist[1:5])
pointPred=dpois(0:5,sum(lambda*postDist))
pointPred[6]=1-sum(pointPred[1:5])

# Plot the data
predcmp <- rbind(predDist,pointPred) # bind into matrix for plotting
barplot(predcmp,main="Predictive Distribution for Vehicle Counts", 
        xlab="Number of Cars (in 15-second Block)", 
        ylab="Probability", col=c("lightblue","pink"), 
        border=c("darkblue","red"),names=c(0:5), beside=TRUE,
        legend=c("Predictive",expression(paste("Poisson ",~lambda,"=1.95"))))
