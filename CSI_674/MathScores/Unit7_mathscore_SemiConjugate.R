############  SYST 664 - Bayesian Inference and Decision Theory  #######

# Math test scores example from Unit 7
# Working directory should be set to directory containing file 
#  Data in file Y.school.mathscore 

# install.packages("MCMCvis")
library(MCMCvis)

# Read in the data and define the variables 
Y.school.mathscore<-dget("Y.school.mathscore") # math score data
school = Y.school.mathscore[,1]                # 1st column is school
score = Y.school.mathscore[,2]                 # 2nd column is score
nS = length(unique(school))                    # number of schools
n = length(score)                              # total number of observations

# calculate sufficient statistics
school.means = aggregate(score, by=list(school), FUN="mean")[,2]  # find means for schools
school.sd = aggregate(score, by=list(school), FUN="sd")[,2]  # find SDs for schools
school.size = aggregate(score, by=list(school), FUN="length")[,2] # number of students 
school.SSQ = aggregate(score^2, by=list(school), FUN="sum")[,2]  # sum of squares for schools


# Estimate model using Gibbs sampling

# Prior hyperparameters
mu.mean.0 = 50     # prior mean of school means
mu.SD.0 = 25         # this gives 95% credible interval of [162,385] ms
tau.sh.0 = sig.sh.0 = 1/2    # Use small virtual sample size
tau.sc.0 = sig.sc.0 = 50     # prior scale gives expected precision of 25

## Initialize Gibbs sample variables
numSim = 5000               # size of sample to draw
thetaG = matrix(nrow = numSim, ncol = nS)
thetaG[1,] = school.means   # initial value for theta
muG = mean(school.means)    # initial value for mu
tauG = sd(school.means)     # initial value for tau
sigG = mean(school.sd)      # initial value for sigma

# Draw the Gibbs samples
for (k in 2:numSim) {
  mu.mean.1 =    # mean of mu
    (mu.mean.0/mu.SD.0^2+sum(thetaG[k-1,])/tauG[k-1]^2)/(1/mu.SD.0^2+nS/tauG[k-1]^2)
  mu.SD.1 = (1/mu.SD.0^2+nS/tauG[k-1]^2)^-(1/2)  # SD of mu
  muG[k]=rnorm(1,mu.mean.1, mu.SD.1)             # sample new mu
  
  tau.sh.1 = tau.sh.0 + 0.5*nS  # shape for 1/tau^2 (same every iteration)
  tau.sc.1 = (1/tau.sc.0 + 0.5*sum((thetaG[k-1,]-muG[k])^2))^-1 # scale for 1/tau^2
  tauG[k] = rgamma(1,shape=tau.sh.1,scale=tau.sc.1)^(-1/2)  # sample new tau
  
  sig.sh.1 = sig.sh.0 + 0.5*sum(school.size)  # shape for 1/sigma^2 (same every iteration)
  sig.sc.1 = (1/sig.sc.0 +                    # scale for 1/sigma^2
                0.5*sum((score-thetaG[k-1,school])^2))^-1 
  sigG[k] = rgamma(1,shape=sig.sh.1,scale=sig.sc.1)^(-1/2)  # sample new sigma^2
  
  mu.1 = (muG[k]/tauG[k]^2+school.means*school.size/sigG[k]^2)/
    (1/tauG[k]^2+school.size/sigG[k]^2)         # vector of posterior means
  tau.1 = (1/tauG[k]^2+school.size/sigG[k]^2)^(-1/2)  # vector of posterior SDs
  thetaG[k,] = rnorm(nS,mu.1,tau.1)   # sample new theta
}

# Means and 95% intervals
theta.hat = colMeans(thetaG)     #  Estimate of posterior means for the 11 subjects
th025=th975=NULL
for (i in 1:nS) {
  th025[i] = quantile(thetaG[,i],0.025)  # lower bound of 95% interval
  th975[i] = quantile(thetaG[,i],0.975)  # upper bound of 95% interval
}

# Table of credible intervals
results=as.data.frame(th025)
results$th975=th975
colnames(results)=c("2.5%","97.5%")
rownames(results) = paste("theta",c(1:11),sep="_")
mu025=quantile(muG,0.025)
mu975=quantile(muG,0.975)
tau025=quantile(tauG,0.025)
tau975=quantile(tauG,0.975)
sig025=quantile(sigG,0.025)
sig975=quantile(sigG,0.975)

results[nS+1,]=c(mu025,mu975)
results[nS+2,]=c(tau025,tau975)
results[nS+3,]=c(sig025,sig975)
rownames(results)[nS+(1:3)] = c("mu","tau","sig")

# write to file for pasting into solution
write.csv(round(results,3),file="results.csv") 

# Caterpillar plot for Theta
plot(school.means,theta.hat,main = "Means for Schools",
     ylab="Posterior Interval",xlab="Sample Mean",ylim = c(min(th025),max(th975)))
lines(school.means,school.means)
for (i in 1:nS) {
  lines(c(school.means[i],school.means[i]),c(th025[i],th975[i]))
}
# Plotting this line shows clearly that means are different
lines(1:nS,array(mean(theta.hat),nS),lty="dashed")

# Normal qq-plot for Theta
qqnorm(theta.hat)
qqline(theta.hat)

# MCMC diagnostics

#### Traceplots

library(coda)  # load package for MCMC functions

par(mfrow=c(3,2))  # 3x2 layout
traceplot(as.mcmc(muG),main="Traceplot for Mu")
traceplot(as.mcmc(tauG),main="Traceplot for Tau")
traceplot(as.mcmc(sigG),main="Traceplot for Sigma")
for (i in 1:nS) {
  traceplot(as.mcmc(thetaG[,1]),main=paste("Traceplot for Theta",i))
}

#### ACF plots

par(mfrow=c(3,2))  # 3x2 layout
acf(muG,main="ACF for Mu")
acf(tauG,main="ACF for Tau")
acf(sigG,main="ACF for Sigma")
for (i in 1:nS) {
  acf(thetaG[,1],main=paste("ACF for Theta",i))
}

par(mfrow=c(1,1))    # Set layout back to single plot

# Effective sample sizes
effectiveSize(muG)
effectiveSize(tauG)
effectiveSize(sigG)
apply(thetaG,2,effectiveSize)

