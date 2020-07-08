
#simple monte carlo
numSim <- 10000000
lambda1 <- rgamma(numSim,shape=7,scale=1/11)
lambda2 <- rgamma(numSim,shape=16,scale=1/11)

mean(lambda1)
mean(lambda2)
sd(lambda1)
sd(lambda2)
diff <- lambda2-lambda1
sum(diff>0)/numSim

#density estimates
plot(density(lambda1),col='red')
lambda<-seq(from=0.01,to=1.6,length=20)
lines(lambda,dgamma(lambda,shape=7,scale=1/11),col='blue')


# Doing more stuff

numSim <- 1000
lambda1 <- rgamma(numSim,shape=7,scale=1/11)
lambda2 <- rgamma(numSim,shape=16,scale=1/11)

mean(lambda1)
mean(lambda2)
sd(lambda1)
sd(lambda2)
diff <- lambda2-lambda1

h <- diff>0

meanMC <- mean(h)
sdevMC <- sqrt(var(h)/numSim) # standard dev


# Simulating defects on the next day

defect.1.next = rpois(numSim,lambda1)
barplot(table(defect.1.next)/numSim)
table(defect.1.next)/numSim

defect.2.next = rpois(numSim,lambda2)
barplot(table(defect.2.next)/numSim)
table(defect.2.next)/numSim



diff.obs <- defect.2.next - defect.1.next
barplot(table(diff.obs)/numSim)
sum(diff.obs>0)/numSim
sum(diff.obs==0)/numSim
sum(diff.obs<0)/numSim

###
x <- seq(0.1,9.3,0.1)
wave = sin(x)+1.5
wave_inv <- 1/wave
plot(x,wave,
     type='l',
     xlim=c(0,10),
     ylim=c(0,3))
lines(x,wave_inv)

