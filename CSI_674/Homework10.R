library(data.table)
data <- fread('http://www.biostat.umn.edu/~lynn/iid/estriol.dat')
head(data)

x <- data$estriol
y <- data$birthwt
n <- length(x)

xbar <- mean(x)
ybar <- mean(y)

b <- sum( (x-xbar) * (y-ybar)) / sum( (x-xbar)^2 ) 
a <- ybar - b*xbar

sxx <- sum( (x-xbar)^2 )
syy <- sum( (y-ybar)^2 )
sxy <- sum( (x-xbar) * (y-ybar) )
see <- sum( (y-ybar-b*(x-xbar))^2)

#posteriors
rho_alpha <- (n-2)/2
rho_beta  <- 2/see

eta_center <- ybar
eta_spread <- (n*(n-2)/see)^-0.5
eta_degf   <- n-2

beta_center <- b
beta_spread <- (see*(n-2)/see)^-0.5
beta_degf   <- n-2

s2<- see/(n-2)
s <- sqrt(s2)

# Problem 2 Assumptions

fitted <- lm(formula= estriol ~ birthwt,data=data)
plot(fitted)
fitted$residuals

# Problem 3: Predictive Distribution
xnew = 19
pred_center <- xnew*b+a
pred_spread <- sqrt( (((xnew-xbar)^2/sxx)+(1/n)+1) * (see/(n-2)))
pred_df     <- n-2
pred_ci <- qt(c(0.05,0.95),df=pred_df)*pred_spread
pred_ci <- pred_ci + pred_center
pred_ci
plot(x,y)


# Problem 4: MC samples

numSim <- 1000
rho_k  <- rgamma(numSim,shape=((n-2)/2),scale=(2/see))
eta_k  <- rnorm(numSim,mean=ybar,sd=sqrt(1/(n*rho_k)))
beta_k <- rnorm(numSim,mean=b,sd=sqrt(1/(sxx*rho_k)))
y_sim  <- rnorm(numSim,mean=(eta_k+beta_k*(19-xbar)),sd=sqrt(1/rho_k))
quantile(y_sim,c(0.05,0.95))


numSim <- 100000
rho_k  <- rgamma(numSim,shape=((n-2)/2),scale=(2/see))
eta_k  <- rnorm(numSim,mean=ybar,sd=sqrt(1/(n*rho_k)))
beta_k <- rnorm(numSim,mean=b,sd=sqrt(1/(sxx*rho_k)))
y_sim2  <- rnorm(numSim,mean=(eta_k+beta_k*(19-xbar)),sd=sqrt(1/rho_k))
quantile(y_sim,c(0.05,0.95))
density(y_sim)
plot(density(y_sim),col='darkgreen')
lines(density(y_sim2),col='blue')

