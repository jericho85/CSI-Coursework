### Bayesian Inference and Decision Theory ###

# Anorexia Example (in-class exercise and extensions)

library(MASS)  # Load MASS package (contains anorexia data set)

# Extract family therapy cases
cases_FT = which(anorexia[,1]=="FT")
gain_FT = anorexia[cases_FT,3]-anorexia[cases_FT,2]

# Extract cognitive behavioral therapy cases
cases_CBT = which(anorexia[,1]=="CBT")
gain_CBT = anorexia[cases_CBT,3]-anorexia[cases_CBT,2]

# Extract control group cases
cases_Cont = which(anorexia[,1]=="Cont")
gain_Cont = anorexia[cases_Cont,3]-anorexia[cases_Cont,2]

# Questions to consider:
# 1. Are observations normally distributed?

qqnorm(gain_Cont)
qqline(gain_Cont)
qqnorm(gain_CBT)  # Definitely not normal!
qqline(gain_CBT)
lines(c(-2,1.3),c(-8,15),col="red") # Try a different line
qqnorm(gain_FT)
qqline(gain_FT)

# 2. Assume answer to #1 is yes. Assume standard deviation of
#    normal distribution is known and equal to average of
#    the sample standard deviations for the 3 groups
#    Assume mean for each group has normal prior distribution
#    with mu0 = 0 and standard deviation tau0 = 5
#    What is posterior distribution of the three group means?

# Estimate overall standard deviation (pretend it's known)
SD = mean(sd(gain_FT),sd(gain_CBT),sd(gain_Cont))

# Prior hyperparameters
mu0=0    # Expected mean weight gain is zero
tau0=5   # There is a wide range (+/- 10lbs) around this estimate

# Control group posterior hyperparameters
tau_Cont=1/sqrt(1/tau0^2+length(gain_Cont)/SD^2)
mu_Cont = (mu0/tau0^2+sum(gain_Cont)/SD^2) /
  (1/tau0^2+length(gain_Cont)/SD^2)

#CBT posterior hyperparameters
tau_CBT=1/sqrt(1/tau0^2+length(gain_CBT)/SD^2)
mu_CBT = (mu0/tau0^2+sum(gain_CBT)/SD^2) / 
  (1/tau0^2+length(gain_CBT)/SD^2)

# Family therapy posterior hyperparameters
tau_FT=1/sqrt(1/tau0^2+length(gain_FT)/SD^2)
mu_FT = (mu0/tau0^2+sum(gain_FT)/SD^2) / 
  (1/tau0^2+length(gain_FT)/SD^2)

# 3.Plot all 3 posterior density functions on the same axes
theta=seq(from=-20, to=25, length=200)
plot(theta, dnorm(theta,mu_FT,tau_FT), type="l",col="blue",
     ylim=c(0,0.33), 
     main="Posterior Density for Treatment Mean - known var",
     xlab="Mean Weight Gain (lbs)", ylab="Probability Density")
lines(theta, dnorm(theta,mu_Cont,tau_Cont), type="l",col="red")
lines(theta, dnorm(theta,mu_CBT,tau_CBT), type="l",col="green")
legend(10,0.25,
       c("Control","CBT","Family"),col=c("red","green","blue"),
       lty=c(1,1,1))

#4. Predictive distribution for sample of size 10 and size 1 (individual girl)

nobs=1   # Number of observations (set to 10 and repeat for 1)
pred_mean_Cont = mu_Cont
pred_SD_Cont = sqrt(SD^2/nobs + tau_Cont^2)
pred_mean_CBT = mu_CBT
pred_SD_CBT = sqrt(SD^2/nobs + tau_CBT^2)
pred_mean_FT = mu_FT
pred_SD_FT = sqrt(SD^2/nobs + tau_FT^2)

theta=seq(from=-20, to=25, length=200)
plot(theta, dnorm(theta,pred_mean_Cont,pred_SD_Cont),
     type="l",col="red",
     ylim=c(0,0.33),
     main="Predictive Distribution for Sample Mean",
     xlab = "Sample Mean Weight Gain (lbs)", ylab="Probability Density")
lines(theta, dnorm(theta,pred_mean_CBT,pred_SD_CBT), type="l",col="green")
lines(theta, dnorm(theta,pred_mean_FT,pred_SD_FT), type="l",col="blue")

#5. The unknown variance case

# We will use a prior that is similar to our known-variance prior
# Expected mean weight gain is zero. Use small virtual sample size
# alpha0 = 1. The expected observation precision is alpha0*beta0 = 0.02
# This corresponds to a standard deviation 1/sqrt(precision) of
# around 7, which is similar to our assumed known variance.
# Then we use k0 = 0.7, which gives about 5 as the center of
# our distribution for the standard deviation of theta.

mu0 = 0       # Expected mean weight gain is zero
alpha0 = 1    # Small virtual sample size for precision (SD about 7)
beta0 = 0.02  # Expected precision is 0.02
k0 = 0.7      # Precision multiplier 0.7

# Control group posterior hyperparameters
n_Cont=length(gain_Cont)
mu_Cont=(k0*mu0+sum(gain_Cont))/(k0+n_Cont)
k_Cont=k0+n_Cont
alpha_Cont=alpha0+n_Cont/2
beta_Cont=( 1/beta0 + 0.5*sum((gain_Cont-mean(gain_Cont))^2) + 
              0.5*k0*n_Cont/(k0+n_Cont)*(mean(gain_Cont)-mu0)^2 )^-1
spread_Cont <- sqrt(1/(k_Cont*alpha_Cont*beta_Cont))

#CBT posterior hyperparameters
n_CBT=length(gain_CBT)
mu_CBT=(k0*mu0+sum(gain_CBT))/(k0+n_CBT)
k_CBT=k0+n_CBT
alpha_CBT=alpha0+n_CBT/2
beta_CBT=( 1/beta0 + 0.5*sum((gain_CBT-mean(gain_CBT))^2) + 
              0.5*k0*n_CBT/(k0+n_CBT)*(mean(gain_CBT)-mu0)^2 )^-1
spread_CBT <- sqrt(1/(k_CBT*alpha_CBT*beta_CBT))

# Family therapy posterior hyperparameters
n_FT=length(gain_FT)
mu_FT=(k0*mu0+sum(gain_FT))/(k0+n_FT)
k_FT=k0+n_FT
alpha_FT=alpha0+n_FT/2
beta_FT=( 1/beta0 + 0.5*sum((gain_FT-mean(gain_FT))^2) + 
              0.5*k0*n_FT/(k0+n_FT)*(mean(gain_FT)-mu0)^2 )^-1
spread_FT <- sqrt(1/(k_FT*alpha_FT*beta_FT))


# Plot posterior density functions for 3 unknown means
theta=seq(from=-20, to=25, length=200)
std_Cont = (theta - mu_Cont)/spread_Cont  # Transform to center 0 spread 1 
t_dens_Cont = dt(std_Cont,df=2*alpha_Cont)/spread_Cont
std_CBT = (theta - mu_CBT)/spread_CBT  # Transform to center 0 spread 1 
t_dens_CBT = dt(std_CBT,df=2*alpha_CBT)/spread_CBT
std_FT = (theta - mu_FT)/spread_FT  # Transform to center 0 spread 1 
t_dens_FT = dt(std_FT,df=2*alpha_FT)/spread_FT

plot(theta, t_dens_Cont, type="l",col="red",
     ylim=c(0,0.33),
     main="Posterior Density for Treatment Mean - unknown var",
     xlab="Mean Weight Gain (lbs)", ylab="Probability Density")
lines(theta, t_dens_CBT, type="l",col="green")
lines(theta, t_dens_FT, type="l",col="blue")
legend(10,0.25,
       c("Control","CBT","Family"),col=c("red","green","blue"),
       lty=c(1,1,1))

# Plot posterior density functions for 3 unknown precisions
rho=seq(from=.005, to=0.05, length=200)
g_dens_Cont = dgamma(rho,shape=alpha_Cont,scale=beta_Cont)
g_dens_CBT = dgamma(rho,shape=alpha_CBT,scale=beta_CBT)
g_dens_FT = dgamma(rho,shape=alpha_FT,scale=beta_FT)

plot(rho, g_dens_Cont, type="l",col="red",
     main="Posterior Density for Precision",
     xlab = "Precision",ylab="Probability Density")
lines(rho, g_dens_CBT, type="l",col="green")
lines(rho, g_dens_FT, type="l",col="blue")
legend(0.03,60,
       c("Control","CBT","Family"),col=c("red","green","blue"),
       lty=c(1,1,1))

#5. Evaluating differences between treatments using direct Monte Carlo

#Simulate means and precisions

#Set simulation sample size
numSim <- 10000
# Simulate directly from the posterior distribution for (rho,theta)
rhoMC_Cont <- rgamma(numSim,shape=alpha_Cont,scale=beta_Cont) 
thetaMC_Cont <- rnorm(numSim,mean=mu_Cont,
                      sd=1/sqrt(k_Cont*rhoMC_Cont))
rhoMC_CBT <- rgamma(numSim,shape=alpha_CBT,scale=beta_CBT) 
thetaMC_CBT <- rnorm(numSim,mean=mu_CBT,
                      sd=1/sqrt(k_CBT*rhoMC_CBT))
rhoMC_FT <- rgamma(numSim,shape=alpha_FT,scale=beta_FT) 
thetaMC_FT <- rnorm(numSim,mean=mu_FT,
                      sd=1/sqrt(k_FT*rhoMC_FT))

# Plot all 3 data sets
plot(thetaMC_Cont,rhoMC_Cont,col="red",pch=".",
     xlim=c(-10,20),ylim=c(0,0.05),
     main="Posterior Monte Carlo Sample for Mean & Precision",
     xlab="Theta",ylab="Rho")
points(thetaMC_CBT,rhoMC_CBT,col="green",pch=".")
points(thetaMC_FT,rhoMC_FT,col="blue",pch=".")

# Arrange data in data frame
MCdata=as.data.frame(thetaMC_FT)
MCdata$CBT=thetaMC_CBT
MCdata$Cont=thetaMC_Cont
bestmean=pmax(thetaMC_FT,thetaMC_CBT,thetaMC_Cont)  # mean of best treatment
MCdata$Best=1    # Fill this column with treatment that's best
MCdata$Best[which(thetaMC_CBT==bestmean)]=2     # rows for which CBT is best
MCdata$Best[which(thetaMC_Cont==bestmean)]=3   # rows for which Cont is best

# Plot matrix of means for different treatments color-coded by which is best
pairs(MCdata[ , 1:3],
      col = c("blue", "green", "red")[MCdata$Best],   # Change color by group
      pch = ".",                                      # Change points by group
      labels = c("FT", "CBT", "Cont"),
      main = "Plot Matrix of Group Means")

# Estimate probability each treatment has highest mean weight gain
p_FT_Best = sum((thetaMC_FT>thetaMC_CBT)&(thetaMC_FT>thetaMC_Cont))/numSim
p_CBT_Best = sum((thetaMC_CBT>thetaMC_FT)&(thetaMC_CBT>thetaMC_Cont))/numSim
p_Cont_Best = sum((thetaMC_Cont>thetaMC_FT)&(thetaMC_Cont>thetaMC_CBT))/numSim


p_FT_Best_std = sum((1/sqrt(rhoMC_FT)>1/sqrt(rhoMC_CBT))&(1/sqrt(rhoMC_FT)>1/sqrt(rhoMC_Cont)))/numSim
p_CBT_Best_std = sum((1/sqrt(rhoMC_CBT)>1/sqrt(rhoMC_FT))&(1/sqrt(rhoMC_CBT)>1/sqrt(rhoMC_Cont)))/numSim
p_Cont_Best_std = sum((1/sqrt(rhoMC_Cont)>1/sqrt(rhoMC_FT))&(1/sqrt(rhoMC_Cont)>1/sqrt(rhoMC_CBT)))/numSim

print(p_FT_Best_std)
print(p_CBT_Best_std)
print(p_Cont_Best_std)
print(p_FT_Best_std+p_CBT_Best_std+p_Cont_Best_std)

p_FT_Best_std = sum((rhoMC_FT<rhoMC_CBT)&(rhoMC_FT<rhoMC_Cont))/numSim
p_CBT_Best_std = sum((rhoMC_CBT<rhoMC_FT)&(rhoMC_CBT<rhoMC_Cont))/numSim
p_Cont_Best_std = sum((rhoMC_Cont<rhoMC_FT)&(rhoMC_Cont<rhoMC_CBT))/numSim

print(p_FT_Best_std)
print(p_CBT_Best_std)
print(p_Cont_Best_std)
print(p_FT_Best_std+p_CBT_Best_std+p_Cont_Best_std)

mean(thetaMC_FT)
mean(thetaMC_CBT)
mean(thetaMC_Cont)

#simulating marginally
gainMC_FT <- rnorm(numSim,thetaMC_FT,1/sqrt(rhoMC_FT))
gainMC_CBT <- rnorm(numSim,thetaMC_CBT,1/sqrt(rhoMC_CBT))
gainMC_Cont <- rnorm(numSim,thetaMC_Cont,1/sqrt(rhoMC_Cont))
mean(gainMC_FT)
mean(gainMC_CBT)
mean(gainMC_Cont)

plot(density(gainMC_FT),col='blue',main='Predictive Density for one Girl weight gain')
lines(density(gainMC_CBT),col='green')
lines(density(gainMC_Cont),col='red')

p_FT_Best = sum((gainMC_FT>gainMC_CBT)&(gainMC_FT>gainMC_Cont))/numSim
p_CBT_Best = sum((gainMC_CBT>gainMC_FT)&(gainMC_CBT>gainMC_Cont))/numSim
p_Cont_Best = sum((gainMC_Cont>gainMC_FT)&(gainMC_Cont>gainMC_CBT))/numSim
p_FT_Best
p_CBT_Best
p_Cont_Best