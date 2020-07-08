theta <- seq(length=20,from=0.025,to=0.975)
priorDist <- array(1/20,20)
barplot(priorDist,main=expression("Prior Dist for"~theta),
        xlab=expression(~theta),ylab="Prior Probability",names.arg=theta,
        border="darkblue",col="lightblue",ylim=c(0,0.15))

numobs=5
numd=1
postDist<-priorDist*theta^numd*(1-theta)^(numobs-numd)
postDist<-postDist/sum(postDist)

barplot(postDist,main=expression("Prior Dist for"~theta),
        xlab=expression(~theta),ylab="Prior Probability",names.arg=theta,
        border="darkblue",col="lightblue",ylim=c(0,0.15))
