
# Part  1a
interarrival_times <- c(12, 2, 6, 2, 19, 5, 34, 4, 1, 4, 8, 7, 1, 21, 6, 11, 8, 28, 6, 4, 5, 1, 18, 9, 5, 1, 21, 1, 1, 5, 3, 14, 5, 3, 4, 5, 1, 3, 16, 2)

arrival_interval=diff(interarrival_times) 
exponential.quantiles = qexp(ppoints(length(interarrival_times)))

# q-q plot
qqplot(exponential.quantiles, interarrival_times,main="Exponential Q-Q Plot of Arrival Intervals",
       xlab = "Theoretical Exponential Quantiles", ylab = "Empirical Quantiles")
lines(exponential.quantiles,exponential.quantiles*mean(interarrival_times)) 

# standard plot
x <-c(1:40)
y <-sort(interarrival_times)
plot(x,y,main='Exponential Plot',xlab='Sorted Position',ylab='Time')
data.df  <- data.frame(x=x,y=y)
model_expo <- lm(y ~ x + I(x^2), data = data.df)
result <- data.frame(x = seq(1, 40, by = 1))
result$model_expo <- predict(model_expo)
result <-  melt(result, 
                id.vars = "x", 
                variable.name = "model",
                value.name = "fitted")
lines(x,result$fitted)


# Part 1b
actual_counts <- c(2, 2, 1, 1, 0, 4, 3, 0, 2, 1, 1, 1, 4, 0, 2, 2, 3, 2, 4, 3, 2)
interval_hist <- c(3,5,7,3,3)
counts <- c(0:4)
barplot(interval_hist,
        main='Histogram of Arrivals per Period',
        ylab='Count of Cars',
        xlab='Count of Periods with Y cars',
        names.arg=counts)
data.df <- data.frame(period_counts=counts,car_counts=interval_hist)
print(data.df)

poisson <- dpois(0:5, mean(actual_counts))
poisson <- poisson * sum(interval_hist)
print(poisson)
lines(poisson)


# Part 1c
lambda <- seq(length=20,from=0.2,to=4)
priors <-  array(1/20,20)
barplot(priors,
        main="Prior Dist",
        xlab="Counts of Cars per Period",
        ylab="Prior Probability",
        names.arg=lambda,
        border="darkblue",
        col="lightblue",
        ylim=c(0,0.25))
#print(lambda)
#print(priors)


lik <- array(1,length(lambda))         # Initialize likelihood as a constant
for (i in 1:10) {
  lik <- lik*dpois(actual_counts[i],lambda)   # Multiply by Likelihood 
}

# The posterior distribution
postDist <- priors*lik           # Prior times likelihood
postDist <- postDist/sum(postDist)  # Normalize to sum to 1

barplot(postDist,
        main="Posterior Dist",
        xlab="Counts of Cars per Period",
        ylab="Probability",
        names.arg=lambda,
        border="darkblue",
        col="lightblue",
        ylim=c(0,0.3))

# define a function to return medians and  percentiles
# the formula returns the index+1 of the last  value smaller
# than the target percentile, while will always be argmin(f(x)>q) 
# shown on page 19 of unit  2 notes
dist_percentile <- function(distr,percentile){
  postDistCumu <- cumsum(postDist)
  index <- 0
  for (i in 1:length(postDistCumu)) {
    if (postDistCumu[i] < percentile){
      index <- i
    }
  }
  index<-index+1
  return(index)
}

postMean <- sum(lambda*postDist)
postVar <- sum((lambda-postMean)^2*postDist)
postSD <- sqrt(postVar)
postMedian <- lambda[dist_percentile(postDist,.5)]
post95th <- lambda[dist_percentile(postDist,0.95)]


# Part 1d

#lik <- postDist         # Initialize likelihood as a constant
lik <- array(1,length(lambda))    
for (i in 11:20) {
  lik <- lik*dpois(actual_counts[i],lambda)   # Multiply by Likelihood 
}

#postDist <- priors*lik           # Prior times likelihood
postDist <- postDist*lik 
postDist <- postDist/sum(postDist)  # Normalize to sum to 1

barplot(postDist,
        main="2nd Posterior Dist",
        xlab="Counts of Cars per Period",
        ylab=" Probability",
        names.arg=lambda,
        border="darkblue",
        col="lightblue",
        ylim=c(0,0.3))

postMean <- sum(lambda*postDist)
postVar <- sum((lambda-postMean)^2*postDist)
postSD <- sqrt(postVar)
postMedian <- lambda[dist_percentile(postDist,.5)]
post95th <- lambda[dist_percentile(postDist,0.95)]

# Part 1e
pred_label  <- c(0:4)
pred_proba <- rep(0,5)

for(i in 1:20) {
  x <- round(lambda[i])
  y <- match(x,pred_label)
  pred_proba[y] <- pred_proba[y] + postDist[i]
}

barplot(pred_proba,
        main="Predictive Distribution",
        xlab="Counts of Cars per Period",
        ylab=" Probability",
        names.arg=pred_label,
        border="darkblue",
        col="lightblue",
        ylim=c(0,1))

print(pred_proba)
