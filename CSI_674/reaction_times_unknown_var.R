### Bayesian Inference and Decision Theory ###

# Reaction Time Example from Unit 5
# Analysis with unknown standard deviation

# Prior hyperparameters
mu=0         # prior mean is 0
k=0          # prior precision multiplier is 0
alpha=-0.5   # Shape of prior for precision
beta=Inf     # Infinite scale 
spread5=Inf  # Spread of predictive distribution for 1st 5 obs

# The data (only the first subject)
reaction.times=c(5.743, 5.606, 5.858, 5.656, 5.591, 5.793, 5.697, 5.875, 5.677, 5.73, 5.69, 5.919, 5.981, 5.996, 5.635, 5.799, 5.537, 5.642, 5.858, 5.793, 5.805, 5.73, 5.677, 5.553, 5.829, 5.489, 5.724, 5.793, 5.684, 5.606)

# Process observations in batches of 5 to find posterior hyperparameters
for (b in 1:6) {
	batch=reaction.times[((b-1)*5+1):(b*5)]  # next batch of data
	# Posterior hyperparameters
	mu[b+1]=(k[b]*mu[b]+sum(batch))/(k[b]+5)
	k[b+1]=k[b]+5
	alpha[b+1]=alpha[b]+5/2
	beta[b+1]=( 1/beta[b] + 0.5*sum((batch-mean(batch))^2) + 
                0.5*k[b]*5/(k[b]+5)*(mean(batch)-mu[b])^2 )^-1
}

# Plot predictive distributions for 5-observation batches (starting w 2nd batch)
spread=1/sqrt((k*5/(k+5))*alpha*beta)  # spread of predictive distr for next 5 obs
for (b in 2:6) {
  xbar=seq(length=101,from=5.4,to=6.0)
  pred.known.var=dnorm(xbar,mean=mu[b],sd=spread[b])
  pred.unk.var=dt((xbar-mu[b])/spread[b],df=alpha[b]*2)/spread[b]
  plot(xbar,pred.unk.var,type="l",col="blue",ylim=c(0,8.5),xlim=c(5.4,6),
       main=paste("Predict Obs ",(b-1)*5+1, " to ", b*5, "- Unknown Variance"),
       xlab="Sample Mean",
       ylab="Probability Density")
  lines(xbar,pred.known.var,col="red")
  nextobs=mean(reaction.times[((b-1)*5+1):(b*5)])
  lines(c(nextobs,nextobs),
        c(0,dt((nextobs-mu[b])/spread[b],df=alpha[b]*2)/spread[b]),
                   col="green")
  legend(5.4,8,c("Predictive (t)","Predictive (normal)",
                 paste("Avg Obs ",(b-1)*5+1, "-", b*5)),
                 col=c("blue","red","green"),lty=c(1,1,1))	
}

# Posterior credible intervals for mean, variance, precision and standard deviation
# Note: NaNs produced for prior quantiles
theta025=mu+qt(0.025,2*alpha)/sqrt(k*alpha*beta)  # 0.025 quantile for mean
theta975=mu+qt(0.975,2*alpha)/sqrt(k*alpha*beta)  # 0.975 quantile for mean
rho025=qgamma(0.025,alpha,scale=beta)             # 0.025 quantile for precision
rho975=qgamma(0.975,alpha,scale=beta)             # 0.975 quantile for precision
var025=1/rho975                                   # 0.025 quantile for variance
var975=1/rho025                                   # 0.975 quantile for variance
std025=sqrt(var025)                               # 0.025 quantile for std dev
std975=sqrt(var975)                               # 0.975 quantile for std dev

# Quantiles for sample mean (predictive quantiles for next 5 observations)
xbar025=mu+qt(0.025,2*alpha)/sqrt((k*5/(k+5))*alpha*beta)  # 0.025 quantile for mean
xbar975=mu+qt(0.975,2*alpha)/sqrt((k*5/(k+5))*alpha*beta)  # 0.975 quantile for mean

##################################
# Contour plot of the joint posterior distribution 

# Inverse gamma density parameterized by shape and scale
dinvgamma<-function(x,shp,scl) {
ld<- shp*log(1/scl) -lgamma(shp) -(shp+1)*log(x)  -1/(scl*x) 
exp(ld)
                            }

gs<-200
theta<-seq(5.65,5.82,length=gs)
is2<-seq(30,110 ,length=gs)       # precision
s2g<-seq(0.008,0.026,length=gs)    # variance

ld.th.is2<-ld.th.s2<-matrix(0,gs,gs)
b=7    # Plot final posterior after all 30 observations
for(i in 1:gs) { for(j in 1:gs) {
    ld.th.is2[i,j]<- dnorm(theta[i],mu[b],1/sqrt( is2[j]*k[b]) ) *
                   dgamma(is2[j],shape=alpha[b],scale=beta[b] )
    ld.th.s2[i,j]<- dnorm(theta[i],mu[b],sqrt(s2g[j]/k[b]) ) *
                    dinvgamma(s2g[j],alpha[b],beta[b])
                     }} 

par(mfrow=c(1,2),mar=c(3,3,1,1),mgp=c(1.75,.75,0))
grays<- gray( (10:0)/10)
image(theta,is2,ld.th.is2,col=grays,xlab="Mean",
       ylab="Precision" ) 
image(theta,s2g,ld.th.s2, col=grays,xlab="Mean",
       ylab="Variance" )
par(mfrow=c(1,1))


##################################
# Perspective plots

persp(theta,is2,ld.th.is2,theta=30,phi=5,xlab="Mean",
       ylab="Precision",zlab="Probability Density",
       xlim=theta[c(1,gs)] ,ylim=is2[c(1,gs)]) 
persp(theta,s2g,ld.th.s2,theta=30,phi=5,xlab="Mean",
       ylab="Variance",zlab="Probability Density" )

##################################
# Slices

plot(0,xlab="Mean",ylab="Probability Density",xlim=c(5.65, 5.82),ylim=c(0,0.42),
     main="Slices of Joint Density")
cc=c("purple","blue","green","orange","red")
legend(5.65,0.35,c("rho=37","rho=54","rho=70","rho=86","rho=102"),
       col=cc,lty=c(1,1))
for (i in 1:5) {
  indx = 20+(i-1)*40
  lines(theta,ld.th.is2[,indx],col=cc[i])
}

##################################
# Conditionals

plot(0,xlab="Mean",ylab="Probability Density",xlim=c(5.65, 5.82),ylim=c(0,23),
     main="Conditional Density of Mean Given Precision")
legend(5.65,18,c("rho=37","rho=54","rho=70","rho=86","rho=102"),
       col=cc,lty=c(1,1))
cc=c("purple","blue","green","orange","red")
for (i in 1:5) {
  indx = 20+(i-1)*40
  dth=theta[2]-theta[1]
  f = ld.th.is2[,indx]/(sum(ld.th.is2[,indx])*dth)
  lines(theta,f,col=cc[i])
}

