# Unit 1 Bayesian Updating Example: Inference about an unknown probability
# Calculate and plot prior and posterior distribution 
# for disease probability:  Discretized prior; 
# sample of 10 cases, 3 having disease

# Assume the unknow probability p can take on one of 20 evenly spaced values 
# between 0.025 and 0.975
pVals <- seq(length=20,from=0.025,to=0.975)

# Prior distribution: choose a prior distribution centered around 0.3 
priorDist <- c(0.033, 0.071, 0.099, 0.116, 0.117, 0.113, 0.103, 
               0.090, 0.074, 0.061, 0.045, 0.024, 0.016,
               0.013, 0.009, 0.006, 0.004, 0.003, 0.002, 0.001)

# Verify that the expected value of p is 0.3
sum(priorDist*pVals)

# Plot the prior distribution as a bar chart 
barplot(priorDist,main="Prior distribution for p",
        xlab="p", ylab="Prior Probability",names.arg=pVals,
        border="darkblue", col="lightblue",ylim=c(0,0.15))

# Calculate the posterior distribution of p after observing sample of 
# 10 cases, 3 having disease
numobs=10    # Number of observations
numd=3       # Number having the disease
lik = pVals^numd*(1-pVals)^(numobs-numd)  # Likelihood of data given p
pl <- priorDist * lik                     # prior times likelihood
postDist <- pl/sum(pl)                    # result of Bayes rule

# Plot the posterior distribution 
barplot(postDist,main="Posterior distribution for p",
xlab="p", ylab="Posterior Probability",names.arg=pVals,
border="darkblue", col="lightblue")

# Expected value of p given the observations
sum(pVals*postDist)

# Poterior cumulative distribution function
cdf = cumsum(postDist)      # calculate cumulative sum
round(rbind(pVals, cdf),4)  # print probability points and cdf at each point

# Prior and posterior probability that disease probabilty is between 0.2 and 0.4
indx = which(pVals>=0.2 & pVals<=0.4)  # Indices for probs between 0.2 and 0.4
sum(priorDist[indx])     # Prior prob that disease probability is between 0.2 and 0.4
sum(postDist[indx])      # Posterior prob that disease probability is between 0.2 and 0.4

