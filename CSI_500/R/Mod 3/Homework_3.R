# Problem 1

# 1.1: Computing the damping expression y = (sin(x)/x) 

# declare function
myfun=function(x=0) {
  return(sin(x)/(x))
}

# declare vector
yvals = c()

# populate vector with data from running sequential 
# numbers through declared function
for(i in seq(1:100)) {
  y=myfun(i);
  yvals<-c(yvals,y)
}

# 1.2 Line plot of output
plot(yvals,type="l")

# 1.3:  Instantiating a vector of range 1:100
xvals = c(seq(1:100))

#1.4: Applying damping function using sapply
new_yvals = sapply(xvals,myfun)
plot(new_yvals,type="l")

# To be honest, the efficiency of sapply() didn't 
# click until I did this and compared my code 
# for my own function and the sapply() function.

#########################################################

# Problem 2
xAxis = c(seq(1:10)) # 2.1: X Axis creation
yAxis = c(seq(1:10)) # 2.2: Y Axis creation

# Z Axis random distribution
zData <- rnorm(100, mean=0, sd=1)

# 2.3: Converting Z data to Matrix
zMatrix = matrix(nrow=10, ncol=10,
           byrow=TRUE,
           data=zData)

# 2.4: Plotting Contour
contour(xAxis,yAxis,zMatrix,
        main="Contour plot",
        col="blue",
        lty=5,
        lwd=2,
        xlab="X",
        ylab="Y")

# 2.5: perspective plot
persp(xAxis,yAxis,zMatrix,
            main="Random Data Plotted",
            xlab="X",
            ylab="Y",
            zlab="Z",
            theta=42, #angle of rotation on Z axis
            phi=30, #angle of elevation above X-Y plane
            col="green",
            shade=.2)

#########################################################

# Problem 3: 

# Results: 
#  3.1: 
#  Starting from a rainy day appears to slow down convergence
#  by one iteration. Otherwise, there is no effect. This may
#  just be an artifact of starting on a less-likely point in
#  the model.

# Creating a Sunny/Rainy markhov model in R
printf = function(s,...){ #print function
  cat(paste0(sprintf(s,...)),"\n")}

mpow = function(m,p) { #setting up a matrix power function
  # %*% is the operator in R for matrix multiplication
  val = m
  for (i in 1:(p-1)) {
    val = m %*% val
  }
  return(val)
}

# probabilities created and then populated in matrix
p_sun_sun = .8
p_sun_rain = .2
p_rain_sun = .9
p_rain_rain = .1

M = matrix(nrow=2, ncol=2,
           byrow=TRUE,
           data=c(p_sun_sun,p_sun_rain,p_rain_sun,p_rain_rain))

P0 = c(0,1)
tmax = 20 # Iterations
trange = seq(from=1, to=tmax, by=1)
printf("%8s %8s %8s","time","p(sun)","p(rain)")

for (i in trange) {
  Mt=P0 %*% mpow(M,i)
  printf("%8d %8.4f %8.4f",i,Mt[1],Mt[2])
}


# 3.2 and 3.3

# Results: beta = 0.08 and gamma = 0.25 are relatively 
# representative of market observations. It may be 
# possible to get more refined results by comparing
# the adopters population with the true dataset and
# coming up with some error margin factor that is used
# to tune parameters. 

# Defining the transition matrix for 3 class population

beta = 0.08
gamma = 0.25

M = matrix(
  nrow=3,
  ncol=3,
  byrow=TRUE,
  data = c(-1*beta, 0,0,
           beta,-1*gamma,0,
           0,gamma,0)
)

num.potential = 99
num.adopters = 1
num.disposers = 0

# N = initial pop vector dist
N = c(num.potential,num.adopters,num.disposers)

# print title and column headers
printf("Population over Time")
printf("%4s%5s%8s%5s%8s%5s%8s",
       "time"," ",
       "potential"," ",
       "adopters"," ",
       "disposers")
printf("%4d   %8.2f    %8.2f     %8.2f",
       0, N[1], N[2], N[3])

#tracking populations over time
pop.hist.potentials = c(num.potential)
pop.hist.adopters = c(num.adopters)
pop.hist.disposers = c(num.disposers)

# set up time range
tmax=24
trange=seq(from=1,t=tmax,by=1)

# Actual model

#iterate and compute pop changes over time

for (i in trange) {
  Nt = M %*% N
  N = N + Nt
  #print current iteration output
  printf("%4d   %8.2f    %8.2f     %8.2f",
         0, N[1], N[2], N[3])
  #track history for plotting afterward
  pop.hist.potentials=c(pop.hist.potentials,N[1])
  pop.hist.adopters=c(pop.hist.adopters,N[2])
  pop.hist.disposers=c(pop.hist.disposers,N[3])
}

# plotting model
plot(
  trange,
  pop.hist.potentials[1:tmax +1],
  ty="l",
  lwd=2,
  col="blue",
  ylim=c(0,max(pop.hist.potentials,
               pop.hist.adopters,
               pop.hist.disposers)),
  main="Diffusion of Innovation Model",
  xlab="Time",
  ylab="Adoption Rate"
)
lines(trange,
      pop.hist.adopters[1:tmax+1],
      ty="l",
      lwd=2,
      col="green")
lines(trange,
      pop.hist.disposers[1:tmax+1],
      ty="l",
      lwd=2,
      col="red")
legend("right",
       legend=c("Poten.","Adopt.","Dispo."),
       col=c("blue","green","red"),
       pt.cex=1.0,
       cex=0.75,
       lwd=c(rep(3,1.0)),
       bty="y",
       inset=c(0.02,0.02),
       y.intersp-0.75)
grid()
