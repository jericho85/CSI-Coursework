# Beta-Binomial Marginal Likelihood Plot for Unit 3 example
#   alpha/(alpha+beta) = 0.7
#   (alpha+beta) varies from 1 to 16

# # If not already installed, install rmutil package
# for Beta-Binomial functions
#    install.packages("rmutil")  # Install rmutil package (only needs to be run once)

# Load package for Beta-Binomial functions
require(rmutil)         # Load the rmutil package (do this on restarting R if you want to use the package)

bbinom.predict=array(dim=c(5,11))  # 5-dimensional array for the 5 predictive distributions
vcount=c(1,2,4,8,16)               # Virtual counts for the 5 distributions
for (i in 1:5)  {
  bbinom.predict[i,]=dbetabinom(0:10,10,0.7,vcount[i])  # ith beta-binomial mass function
}

# Make the plot
plot.title=expression(paste(               # Title for plot
  "Beta-Binomial Marginal Likelihood with size=10, ",alpha,"/(",alpha,"+",
  beta,") = 0.7"))
lgnd=NULL
for (i in 1:5) {
  lgnd[i]=paste("a",vcount[i]*.7,", b=",vcount[i]*.3)
}

barplot(rbind(bbinom.predict),beside=TRUE,
        main = plot.title,
        ylab="Probability",xlab="Number of Successes",
        legend.text=lgnd,
        args.legend=list(x="topleft"),
        names.arg=0:10,
        col=cm.colors(5))
