# Problem 1

wolf.surface=c(3.74, 4.61, 4.00, 4.67, 4.87, 5.12, 4.52, 5.29, 5.74, 5.48)
wolf.bottom=c(5.44, 6.88, 5.37, 5.44, 5.03, 6.48, 3.89, 5.85, 6.85, 7.16)

s_n <- length(wolf.surface)
b_n <- length(wolf.bottom)

s_xbar <- mean(wolf.surface)
b_xbar <- mean(wolf.bottom)

#Theta Parameters
mu0 <- 6 
tau0 <- 1.5

#Rho parameters
alpha0 <- 4.5
beta0 <- 0.19

# Standard deviations of input data
b_sigma0 <- sd(wolf.bottom)
s_sigma0 <- sd(wolf.surface)

# Describing the precision as the inverse of the variance
b_rho0 <- 1/b_sigma0^2
s_rho0 <- 1/s_sigma0^2
b_lambda0 <- 1/tau0^2
s_lambda0 <- 1/tau0^2

# Conditional Distribution for Theta:
s_mu1 <- ((mu0/tau0^2)+(sum(wolf.surface)/s_sigma0)) / 
  ((1/tau0^2)+(length(wolf.surface)/s_sigma0))
b_mu1 <- ((mu0/tau0^2)+(sum(wolf.bottom)/b_sigma0)) / 
  ((1/tau0^2)+(length(wolf.bottom)/b_sigma0))
s_tau1 <- (1/tau0^2 + length(wolf.surface)*s_rho0)^-.5
b_tau1 <- (1/tau0^2 + length(wolf.bottom)*b_rho0)^-.5

# Conditional Distribution for Rho
b_var_theta <- sum((b_n-b_mu1)^2)
s_var_theta <- sum((s_n-s_mu1)^2)
b_alpha1 <- alpha0 + b_n/2
s_alpha1 <- alpha0 + s_n/2
b_beta1 <- 1/(1/beta0 + b_var_theta/2)
s_beta1 <- 1/(1/beta0 + s_var_theta/2)

# Print parameters for report out
s_mu1
b_mu1
s_tau1
b_tau1
b_var_theta
s_var_theta
b_alpha1
s_alpha1
b_beta1
s_beta1


# Problem 2

numSim <- 10000

# Initialize rho (don't need to initialize theta because it is sampled first)

# Initial guess for precision
#b_rGprev <- 1/b_var_theta    
#s_rGprev <- 1/s_var_theta     

# Alternatively, do a random draw for the initial precisions
s_rGprev<-rgamma(1,shape=s_alpha1,scale=s_beta1)   
b_rGprev<-rgamma(1,shape=b_alpha1,scale=b_beta1)  

# Initialize variables for simulation
#b_rhoGibbs = b_thetaGibbs = b_sigmaGibbs = NULL   
#s_rhoGibbs = s_thetaGibbs = s_sigmaGibbs = NULL


##### TEST PRIORS ######
#mu1 <- 6 
#tau1 <- 1.5
#alpha1 <- 4.5
#beta1 <- 0.19
#s_mu1 <-mu0
#b_mu1 <-mu0
#s_tau1<-tau0
#b_tau1<-tau0
#b_sigma1 <- sd(wolf.bottom)
#s_sigma1 <- sd(wolf.surface)
#b_rho1 <- 1/b_sigma0^2
#s_rho1 <- 1/s_sigma0^2
#b_lambda1 <- 1/tau0^2
#s_lambda1 <- 1/tau0^2
#s_alpha1 <- alpha1
#b_alpha1 <- alpha1
#s_beta1 <- beta1
#b_beta1 <- beta1


########################


for (k in 1:numSim) {
  # reduces to xbar when tau = Inf
  s_muG = (mu0/tau0^2 + s_n*s_rGprev*s_xbar) /
    (1/tau0^2 + s_n*s_rGprev)
  b_muG = (mu0/tau0^2 + b_n*b_rGprev*b_xbar) /
    (1/tau0^2 + b_n*b_rGprev)

  # reduces to sigmaGibbs/sqrt(n) when tau = Inf
  s_tauG = 1/sqrt(1/tau0^2 + s_n*s_rGprev)
  b_tauG = 1/sqrt(1/tau0^2 + b_n*b_rGprev)

  # simulate new value for theta
  s_thetaGibbs[k] <- rnorm(1,mean=s_muG,sd=s_tauG)
  b_thetaGibbs[k] <- rnorm(1,mean=b_muG,sd=b_tauG)

  # update scale given current theta
  s_betaG<-1/(1/beta0 + 0.5*sum((wolf.surface-s_thetaGibbs[k])^2))
  b_betaG<-1/(1/beta0 + 0.5*sum((wolf.bottom-b_thetaGibbs[k])^2))

  # sample new value for rho
  s_rhoGibbs[k]<-rgamma(1,shape=s_alpha1,scale=s_betaG)
  b_rhoGibbs[k]<-rgamma(1,shape=b_alpha1,scale=b_betaG)

  # calculate new value of sigma
  s_sigmaGibbs[k]<-1/sqrt(s_rhoGibbs[k])
  b_sigmaGibbs[k]<-1/sqrt(b_rhoGibbs[k])

  # previous value of rho
  s_rGprev = s_rhoGibbs[k]
  b_rGprev = b_rhoGibbs[k]
}



# for (k in 1:numSim) {
#   # reduces to xbar when tau = Inf
#   s_muG = (s_mu1/s_tau1^2 + s_n*s_rGprev*s_xbar) /
#     (1/s_tau1^2 + s_n*s_rGprev)
#   b_muG = (b_mu1/b_tau1^2 + b_n*b_rGprev*b_xbar) /
#     (1/b_tau1^2 + b_n*b_rGprev)
# 
#   # reduces to sigmaGibbs/sqrt(n) when tau = Inf
#   s_tauG = 1/sqrt(1/s_tau1^2 + s_n*s_rGprev)
#   b_tauG = 1/sqrt(1/b_tau1^2 + b_n*b_rGprev)
# 
#   # simulate new value for theta
#   s_thetaGibbs[k] <- rnorm(1,mean=s_muG,sd=s_tauG)
#   b_thetaGibbs[k] <- rnorm(1,mean=b_muG,sd=b_tauG)
# 
#   # update scale given current theta
#   s_betaG<-1/(1/s_beta1 + 0.5*sum((wolf.surface-s_thetaGibbs[k])^2))
#   b_betaG<-1/(1/b_beta1 + 0.5*sum((wolf.bottom-b_thetaGibbs[k])^2))
# 
#   # sample new value for rho
#   s_rhoGibbs[k]<-rgamma(1,shape=s_alpha1,scale=s_betaG)
#   b_rhoGibbs[k]<-rgamma(1,shape=b_alpha1,scale=b_betaG)
# 
#   # calculate new value of sigma
#   s_sigmaGibbs[k]<-1/sqrt(s_rhoGibbs[k])
#   b_sigmaGibbs[k]<-1/sqrt(b_rhoGibbs[k])
# 
#   # previous value of rho
#   s_rGprev = s_rhoGibbs[k]
#   b_rGprev = b_rhoGibbs[k]
# }

# Calculate Quantiles
s_thetaGibbs_Q <- quantile(s_thetaGibbs,c(0.05,0.95))
b_thetaGibbs_Q <- quantile(b_thetaGibbs,c(0.05,0.95))
s_sigmaGibbs_Q <- quantile(1/sqrt(s_rhoGibbs),c(0.05,0.95))
b_sigmaGibbs_Q <- quantile(1/sqrt(b_rhoGibbs),c(0.05,0.95))


theta_diff <- b_thetaGibbs-s_thetaGibbs
theta_diff_Q <- quantile(theta_diff,c(0.05,0.95))

# print quantiles for report out
s_thetaGibbs_Q
b_thetaGibbs_Q
s_sigmaGibbs_Q 
b_sigmaGibbs_Q 
theta_diff_Q

# Plots to verify
plot(density(s_thetaGibbs),col='blue',type='l',xlim=c(3.5,7.5),main='Θ Density')
lines(density(b_thetaGibbs),col="green")
legend(6.2,1.4,c("Θ Surface ","Θ Bottom"),col=c("blue","green"),lty=c(1,1))

plot(density(1/sqrt(s_rhoGibbs)),col='blue',type='l',xlim=c(0.5,2),ylim=c(0,3),main='Σ Density')
lines(density(1/sqrt(b_rhoGibbs)),col="green")
legend(1.5,3,c("Σ Surface ","Σ Bottom"),col=c("blue","green"),lty=c(1,1))

plot(density(theta_diff),col='blue',type='l',xlim=c(-1,3.5),main='Θ Differences')

# Problem 3
require(coda) 
library(coda)
traceplot(as.mcmc(theta_diff), main="Traceplot for Gibbs Sampling Theta_B-Theta_S")
acf(theta_diff)
effectiveSize(theta_diff)

# Problem 4
s_rhoGibbs_Q <- quantile(s_rhoGibbs,c(0.05,0.95))
b_rhoGibbs_Q <- quantile(b_rhoGibbs,c(0.05,0.95))
s_rhoGibbs_Q
b_rhoGibbs_Q
