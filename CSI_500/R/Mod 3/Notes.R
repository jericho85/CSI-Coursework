# Groups in R
print( { x=1; y=2; z=3})
# these get treated as a group of variables and the last value is returned
print({x=1; y=2; z=3; k=111})

# Loops in R
# For
for (i in range(1,3)) {print("Hello")}
# While
i=0
while (i<3) {print("hello");i=i+1}
# Repeat
i=0
repeat{print("hello"); i=i+1; if (i>3) break;}

# Next and Break
for (i in seq(0,5)) { if(i==3) break; print(i);}
for(i in seq(0,5)) { if(i==3) next(); print(i);}

# Defining Functions
mysum = function(x=0,y=0) {return(x+y)} #zeros are default values if none passed
mysum(3,5)

# Ignoring additional parameters passed to a function that aren't needed:
mysum = function(x=0,y=0,...){print(x+y)}
mysum(3,5,formatted=FALSE)

# Mapping functions to vectors
# sapply is 'simple apply'
# lapply returns a list
sapply(1:3, sqrt)
lapply(1:3,sqrt)
#you can use your own functions in these
myfun=function(x) {return(sin(x)/(x+1))}
sapply(1:3,myfun)

# 3D Graphing in R
#setting up function
zfun = function(x,y) {
  val = x^2 + y^2
  return(val)
}
# setup contour data
xvals = seq(-5,5,1)
yvals = seq(-5,5,1)
xlen = length(xvals)
ylen = length(yvals)

zvals = outer(xvals,yvals,zfun) #uses vector algebra function "outer"

# Plot the contour
persp(xvals,yvals,zvals)

contour(xvals,yvals,zvals,
        main="Contour plot",
        col="red",
        lty=3,
        lwd=2,
        xlab="X",
        ylab="Y")

persp(xvals,yvals,zvals,
      main="3d Perspective Plot",
      xlab="X",
      ylab="Y",
      zlab="Z",
      theta=30, #angle of rotation on Z axis
      phi=20, #angle of elevation above X-Y plane
      col="wheat",
      shade=.2)


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

P0 = c(1,0)
tmax = 20 # Iterations
trange = seq(from=1, to=tmax, by=1)
printf("%8s %8s %8s","time","p(sun)","p(rain)")

for (i in trange) {
  Mt=P0 %*% mpow(M,i)
  printf("%8d %8.4f %8.4f",i,Mt[1],Mt[2])
}

# Modeling Diffusion of Innovation
# Defining the transition matrix for 3 class population

beta = 0.15
gamma = 0.1

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
tmax=28
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
  ylab="Population Size"
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
       legend=c("Potential","Adopters","Disposers"),
       col=c("blue","green","red"),
       pt.cex=1.0,
       cex=0.75,
       lwd=c(rep(3,1.0)),
       bty="y",
       inset=c(0.02,0.02),
       y.intersp-0.75)

grid()
