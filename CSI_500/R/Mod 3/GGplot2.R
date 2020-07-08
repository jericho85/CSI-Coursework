library(ggplot2)
library(MASS)
mycrabs=MASS::crabs

ggplot(mycrabs,aes(mycrabs$CW,mycrabs$CL)) +geom_point()

ggplot(mycrabs,
       aes(mycrabs$sp,mycrabs$BD)) +geom_boxplot()

ggplot( mycrabs,
        aes(mycrabs$CL, mycrabs$CW, color=mycrabs$sex)) + geom_point() + facet_wrap(~mycrabs$sp)

# make the new "key"
mycrabs$spsex = paste(mycrabs$sp, mycrabs$sex, sep="")
# do the plot
ggplot(mycrabs, aes(mycrabs$spsex, mycrabs$BD)) + geom_boxplot()


# use the new "key"
mycrabs$spsex = paste(mycrabs$sp, mycrabs$sex, sep="")
# do the plot
ggplot(mycrabs, aes(mycrabs$spsex, mycrabs$BD)) + geom_violin()

ggplot( mycrabs, aes( mycrabs$BD)) + geom_histogram()
ggplot( mycrabs, aes( mycrabs$BD)) + geom_freqpoly()

ggplot( mycrabs, aes( mycrabs$BD, color = mycrabs$sp)) + geom_freqpoly()
ggplot( mycrabs, aes( mycrabs$BD, fill = mycrabs$sp)) + geom_histogram() +
  facet_wrap(~mycrabs$sp, ncol = 1)
