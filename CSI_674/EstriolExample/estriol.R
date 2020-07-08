## Regression model for dependence of baby's birthweight on estriol in mother's blood

# Read in the data (make sure working directory is set to location of file)
estriol=read.table("estriol.txt",header=TRUE)

# Plot birthweight against estriol
plot(estriol$Estriol,estriol$Birthweight,xlab="Estriol(mg)",ylab="Birthweight (gx100)",main="Birthweight vs Estriol")

# Use lm to fit regression line
fit=lm(estriol$Birthweight ~ estriol$Estriol)
summary(fit)  # Summary of regression results
plot(fit)     # Diagnostic plots from lm object

# Residual plot "by hand"
plot(estriol$Estriol,fit$residuals,xlab="Estriol(mg)",ylab="Residuals",main="Residual Plot")
qqnorm(fit$residuals)   #Normal linear model
qqline(fit$residuals)

# Statistics calculated 
x=estriol$Estriol
y=estriol$Birthweight
xbar=mean(x)
ybar=mean(y)
n=length(x)
sxx=sum((x-xbar)^2)
sxy=sum((x-xbar)*(y-ybar))

b = sxy/sxx            # slope estimate calculated "by hand"
a = ybar - b*xbar      # intercept estimate calculated "by hand"
see = sum((y - a - b*x)^2)   # error sum of squares

# Posterior predictive distribution for baby if mother has 19mg estriol
xnew = 19
pred.center = a + b*xnew
pred.spread = sqrt(((xnew-xbar)^2/sxx + 1/n + 1)*see/(n-2))
pred.df = n-2

### Three different predictive intervals; all should be very similar

# Exact credible interval for prediction @ 19 mg 
pred.center + qt(c(0.05,0.95),pred.df)*pred.spread

# Simulate predictive distribution for x=19 using t distribution
pred_19a = 33.08 + 3.89*rt(1000,29)
quantile(pred_19a,c(0.05,0.95))

# Simulate predictive distribution for x=19 using gamma and normal
rho=rgamma(1000,shape=14.5,scale=0.0047)
eta=rnorm(1000,32,sqrt(1/(31*rho)))
beta=rnorm(1000, 0.608, sqrt(1/(677.42*rho)))
pred_19b=rnorm(1000,eta+beta*(19-17.23),sqrt(1/rho))
quantile(pred_19b,c(0.05,0.95))



