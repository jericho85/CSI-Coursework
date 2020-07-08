

data <-read.table("reactiontimes.csv",quote="",comment.char="",stringsAsFactors=FALSE)
data <- log(data)
colnames(data) <- c(s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,ns1,ns2,ns3,ns4,ns5,ns6)
dataNS <- data[1:11]
dataS  <- data[12:17]

sum(dataNS)

n <- 11
ns <- 30
sigma <- 0
mean <- 0 
for (i in dataNS){
  sigma <- sigma + sd(i)
  mean <- mean + mean(i)
  print(sum(i)/length(i))
}
sigma <- sigma/length(dataNS)
mean <- mean/length(dataNS)

theta_means <- c(5.732187,5.896382,5.710294,5.70498,5.570268,5.798883,
                 5.867212,5.580695,5.541406,5.77762,5.716292)

sd(theta_means)

# Priors
mu_mean0 <- 5.52
mu_st0 <- 0.22
tau_alpha0 <- 0.5
tau_beta0 <- 50
theta_mean0 <- mean
theta_sd0 <- sigma

# Posteriors
# Define functions for updates

mu_mean_update <- function(n,th,t,m,sd){
  mu_m <- (((n*th)/t^2)+(m/sd^2)) / ((n/t^2)+(1/sd^2))
  return(mu_m)
}

mu_sd_update <- function(n,t,sd){
  mu_sd <- (n/t^2+1/sd^2)
  return(mu_sd)
}

thetas_var <- function(theta_array,mean) {
  var <- sum((theta_array-mean)^2)
  return(var)
}

t_beta_update <- function(bp,tv){
  beta <- 1/sqrt( 1/bp+1/2*var )
  return(beta)
}

theta_mean_update <- function(ys,s,m,t){
  th_m <- ( sum(ys)/s^2 + m/t^2 ) / ( length(ys)/s^2 + 1/t^2 )
  return(th_m)
}

