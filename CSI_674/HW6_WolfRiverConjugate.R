############  SYST 664 - Bayesian Inference and Decision Theory  #######

# Assignment 6
# Wolf River Pollutant Concentration Data Analysis 

# The data 
wolf.surface=c(3.74, 4.61, 4.00, 4.67, 4.87, 5.12, 4.52, 5.29, 5.74, 5.48)
wolf.bottom=c(5.44, 6.88, 5.37, 5.44, 5.03, 6.48, 3.89, 5.85, 6.85, 7.16)

# Sufficient statistics for mean
xs=wolf.surface
sums=sum(wolf.surface)
xb=wolf.bottom
sumb=sum(wolf.bottom)
n <- length(xs)

##########  Problem 1  ############

# Conjugate unknown var - Separate priors for surface & bottom

# Prior hyperparameters
mus=0         # prior mean is 0
ks=0          # prior precision multiplier is 0
alphas=-0.5   # Shape of Jeffreys prior for precision
betas=Inf     # Infinite scale for Jeffreys prior
mub=0         # prior mean is 0
kb=0          # prior precision multiplier is 0
alphab=-0.5   # Shape of Jeffreys prior for precision
betab=Inf     # Infinite scale for Jeffreys prior

# Posterior hyperparameters
mus.star=(ks*mus+sum(xs))/(ks+n)
ks.star=ks+n
alphas.star=alphas+n/2
betas.star=( 1/betas + 0.5*sum((xs-mean(xs))^2) + 
              0.5*ks*n/(ks+n)*(mean(xs)-mus)^2 )^-1
mub.star=(kb*mub+sum(xb))/(kb+n)
kb.star=kb+n
alphab.star=alphab+n/2
betab.star=( 1/betab + 0.5*sum((xb-mean(xb))^2) + 
               0.5*kb*n/(kb+n)*(mean(xb)-mub)^2 )^-1

# 90% Posterior intervals on means precisions
qgamma(c(0.05,0.95),shape=alphas.star,scale=betas.star)
qgamma(c(0.05,0.95),shape=alphab.star,scale=betab.star)
mus.star+qt(c(0.05,0.95),2*alphas.star)/sqrt(ks.star*alphas.star*betas.star)
mub.star+qt(c(0.05,0.95),2*alphab.star)/sqrt(kb.star*alphab.star*betab.star)

# Plots
rhogrid = seq(length=200, from=0.2, to=5.5)
plot(rhogrid, dgamma(rhogrid,shape=alphas.star,scale=betas.star),col="blue",
     type="l",ylim=c(0,1),xlab="rho",ylab="Probability Density",
     main="Marginal Density of Surface and Bottom Precision")
lines(rhogrid, dgamma(rhogrid,shape=alphab.star,scale=betab.star),col="red")
legend(3.5,0.85,c("Surface","Bottom"),col=c("blue","red"),lty=c(1,1))


thetagrid = seq(length=200, from=4.1, to=6.6)   # range for theta
spreads=1/sqrt(ks.star*alphas.star*betas.star)  # surface spread
dens=dt((thetagrid-mus.star)/spreads,alphas.star*2)/spreads
plot(thetagrid, dens, col="blue",
     type="l",main="Marginal Density of Surface and Bottom Means",
     xlab="theta",ylab="Probability Density")
spreadb=1/sqrt(kb.star*alphab.star*betab.star)  # bottom spread
dens=dt((thetagrid-mub.star)/spreadb,alphab.star*2)/spreadb
lines(thetagrid, dens, col="red")
legend(5.93,1.92,c("Surface","Bottom"),col=c("blue","red"),lty=c(1,1))

##########  Problem 2  ############

# Direct Monte Carlo
numsim=5000
rhob=rgamma(numsim,shape=alphab.star,scale=betab.star)
thetab=rnorm(numsim,mub.star,1/sqrt(kb.star*rhob))
rhos=rgamma(numsim,shape=alphas.star,scale=betas.star)
thetas=rnorm(numsim,mus.star,1/sqrt(ks.star*rhos))

# Monte Carlo quantiles
quantile(rhos,c(0.05,0.95))
quantile(thetas,c(0.05,0.95))
quantile(rhob,c(0.05,0.95))
quantile(thetab,c(0.05,0.95))

##########  Problem 3  ############
# Plots and credible intervals generated above can be used 
# to evaluate whether surface and bottom means and SDs differ

# Estimate probability that bottom concentration is larger
sum(thetab>thetas)/numsim        # Estimated prob bottom mean is larger
sd(thetab>thetas)/sqrt(numsim)   # Standard error of estimate
quantile(thetab-thetas, c(0.05,0.95))  # 90% credible interval

# Estimate probability that bottom  precision is smaller
sum(rhob>rhos)/numsim        # Estimated prob bottom precision is larger
sd(rhob>rhos)/sqrt(numsim)   # Standard error of estimate
quantile(rhob-rhos, c(0.05,0.95))  # 90% credible interval

# Estimate probability that bottom standard deviation is larger
sigmab=1/sqrt(rhob)         # bottom standard deviation
sigmas=1/sqrt(rhos)         # surfact standard deviation
sum(sigmab>sigmas)/numsim    # Estimated prob bottom std dev is larger
sd(sigmab>sigmas)/sqrt(numsim)   # Standard error of estimate
quantile(sigmab-sigmas, c(0.05,0.95))  # 90% credible interval

##########  Problem 4  ############
# Evaluate normality - normal qq-plots
par(mfrow=c(1,2))   # 2 plots on a page
qqnorm(xs,main="Normal Q-Q Plot for Surface Data")
qqline(xs)
qqnorm(xb,main="Normal Q-Q Plot for Bottom Data")
qqline(xb)
par(mfrow=c(1,1))   # back to 1 plot on a page
qqnorm(c(xs-mean(xs),xb-mean(xb)),main="Normal Q-Q Plot for Combined Data")
qqline(c(xs-mean(xs),xb-mean(xb)))

# Evaluate normality - Shapiro Wilk Test
shapiro.test(xs)
shapiro.test(xb)
shapiro.test(c(xs-mean(xs),xb-mean(xb)))







