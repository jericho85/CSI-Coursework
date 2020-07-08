library(MASS)
# Extract family therapy cases
cases_FT = which(anorexia[,1]=="FT")
gain_FT = anorexia[cases_FT,3]-anorexia[cases_FT,2]

# Extract cognitive behavioral therapy cases
cases_CBT = which(anorexia[,1]=="CBT")
gain_CBT = anorexia[cases_CBT,3]-anorexia[cases_CBT,2]

# Extract cognitive behavioral therapy cases
cases_Cont = which(anorexia[,1]=="Cont")
gain_Cont = anorexia[cases_Cont,3]-anorexia[cases_Cont,2]

# Estimate overall standard deviation
SD = mean(sd(gain_FT),sd(gain_CBT),sd(gain_Cont))

SD

sample_sd = sd(gain_CBT)
sample_sd
hist(gain_CBT)
# Questions to consider:
# 1. Are observations normally distributed?
# 2. Assume answer to #1 is yes. Assume standard deviation of
#    normal distribution is known and equal to average of
#    the sample standard deviations for the 3 groups
#    Assume mean for each group has normal prior distribution
#    with mu0 = 0 and standard deviation tau0 = 5
#    What is posterior distribution of the three group means?
# 3. We will plot all 3 posterior density functions on the same
#    axes

#sample_sd = sd(gain_FT)
#sample_sd
#hist(gain_FT)
#
#sample_sd = sd(gain_CBT)
#sample_sd
#hist(gain_CBT)


sample_sd = sd(gain_Cont)
sample_sd
hist(gain_Cont)

qqnorm(gain_CBT,pch=1,frame=FALSE)
qqline(gain_CBT,col='green')


# Q1: No, not normal
mu <- 0
tau <- 5

mu_star_cont <- ((mu/tau^2) + (sum(gain_Cont)/var(gain_Cont))) / ((1/tau^2) + (length(gain_Cont)/var(gain_Cont)))
mu_star_cont
tau_star_cont <- (1/tau^2 + length(gain_Cont)/var(gain_Cont))^-0.5
tau_star_cont


mu_star_CBT <- ((mu/tau^2) + (sum(gain_CBT)/var(gain_CBT))) / ((1/tau^2) + (length(gain_CBT)/var(gain_CBT)))
mu_star_CBT
tau_star_CBT <- (1/tau^2 + length(gain_CBT)/var(gain_CBT))^-0.5
tau_star_CBT


mu_star_FT <- ((mu/tau^2) + (sum(gain_FT)/var(gain_FT))) / ((1/tau^2) + (length(gain_FT)/var(gain_FT)))
mu_star_FT
tau_star_FT <- (1/tau^2 + length(gain_FT)/var(gain_FT))^-0.5
tau_star_FT


x = seq(-10,20,by=0.2)
cont = dnorm(x,mu_star_cont,tau_star_cont)



cbt = dnorm(x,mu_star_CBT,tau_star_CBT)
ft = dnorm(x,mu_star_FT,tau_star_FT)
plot(x,cbt,'l',col='green')
lines(x,cont,'l',col='blue')
lines(x,ft,'l',col='red')


##### Predicting the sample mean for 10 girls (page 14)
marginal_likelihood_FT <- sqrt((tau^2/10)+tau_star_FT)
marginal_likelihood_FT

ft_marg_10 <- dnorm(x,mu_star_FT,marginal_likelihood_FT)
plot(x,ft_marg_10,'l')

##### Predict sample mean for 1 girl, own daughter (n=1)

marginal_likelihood_FT <- sqrt((tau^2/1)+tau_star_FT)
marginal_likelihood_FT

ft_marg_1 <- dnorm(x,mu_star_FT,marginal_likelihood_FT)
plot(x,ft_marg_1,'l')

#######
plot(x,ft,'l',col='red')
lines(x,ft_marg_10,'l',col='green')
lines(x,ft_marg_1,'l',col='blue')

