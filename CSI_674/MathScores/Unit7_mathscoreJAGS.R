############  SYST 664 - Bayesian Inference and Decision Theory  #######

# Math test scores example from Unit 7
# Working directory should be set to directory containing file 
#  Data in file Y.school.mathscore and JAGS model in file mathscore.model.jags

# install.packages("MCMCvis")
library(MCMCvis)

# Read in the data and define the variables 
Y.school.mathscore<-dget("Y.school.mathscore") # math score data
school = Y.school.mathscore[,1]                # 1st column is school
score = Y.school.mathscore[,2]                 # 2nd column is score
nS = length(unique(school))                    # number of schools
n = length(score)                             # total number of observations

school.means = aggregate(score, by=list(school), FUN="mean")[,2]  # find means for schools
school.sd = aggregate(score, by=list(school), FUN="sd")[,2]  # find SDs for schools
school.size = aggregate(score, by=list(school), FUN="length")[,2] # number of students 

library(R2jags)        # JAGS

#Gibbs sample

math.data <- list("nS","n","school","score")

math.params <- c("mu","lambda","rho","theta")

math.inits <- function(){
 list("mu"=c(50), "lambda"=c(0.01),"rho"=c(0.01), "theta"=array(50,nS))
 }

# The jags function takes data and starting values as input. It automatically writes
# a jags script, calls the model, and saves the simulations for easy access in R.
math.fit <- jags(data=math.data, inits=math.inits, math.params, n.chains=2, 
                n.iter=5000, n.burnin=100,model.file="mathscore.model.jags",
                n.thin=1)

math.fit.mcmc <- as.mcmc(math.fit)        # change to mcmc object
MCMCsummary(math.fit.mcmc, round=2)       # show summary of JAGS object

# MCMCpstr function extracts summary from MCMC output
# Better to use on JAGS output than as.mcmc version because it retains structure
# of original data, whereas mcmc object orders school means lexicographically on index
paramMeans=MCMCpstr(math.fit,          # find parameter means
                    func = mean,
                    type = 'summary')

# Extract effective sample sizes for all variables
effSiz = MCMCpstr(math.fit,          # find parameter means
                  func = effectiveSize,
                  type = 'summary')
histogram(effSiz$theta,xlab="Effective Sample Size for School Means")

# Shrinkage plots
par(mfrow=c(1,1))
plot(school.means,paramMeans$theta,
     ylab=expression(hat(theta)),xlab=expression(bar(y)))
lines(school.means,school.means)

plot(school.size,(school.means-paramMeans$theta),
     ylab="Amount of Shrinkage",xlab="School Size")
lines(c(min(school.size),max(school.size)), c(0,0))

# Use MCMCvis package to do caterpillar plot for school means 
MCMCplot(math.fit,              
         params = 'theta',
         ref_ovl = TRUE,
         ref=50,
         horiz = FALSE
         )


