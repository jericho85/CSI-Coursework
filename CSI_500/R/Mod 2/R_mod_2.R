# R Module 2
# Jericho McLeod

# Problem 1

id = c(123,245,387)
major = c('Data Science','Pre Med','Public Health')
GPA = c(3.8,3.2,3.4)

df = data.frame(
  id=id,
  major=major,
  GPA=GPA
)

id = c(123,245,387)
dorm = c('N','Y','Y')
in_state = c('Y','Y','N')
df2 = data.frame(
  id=id,
  dorm=dorm,
  in_state=in_state
)

df_merged = merge(df,df2,by='id')
df_merged

df_selected = df_merged[c("major","in_state")]
df_selected

# Problem 2

fib = c(0,1)
for (i in 1:18) {
  fib = c(fib,sum(tail(fib,n=2)))
}
fib

printf = function(s,...){
  cat(paste0(sprintf(s,...)),"\n")
}

for (i in fib){
  printf("value = %d",i)
}

# Problem 3

library(MASS)
crab.data=MASS::crabs
crab.data$wl.ratio = crab.data$CW/crab.data$CL
crab.data.BM <- crab.data[ which(crab.data$sp=='B' & crab.data$sex=='M'), ]
crab.data.BF <- crab.data[ which(crab.data$sp=='B' & crab.data$sex=='F'), ]
crab.data.OM <- crab.data[ which(crab.data$sp=='O' & crab.data$sex=='M'), ]
crab.data.OF <- crab.data[ which(crab.data$sp=='O' & crab.data$sex=='F'), ]
boxplot(crab.data.BM$wl.ratio,
        crab.data.BF$wl.ratio,
        crab.data.OM$wl.ratio,
        crab.data.OF$wl.ratio,
        main='Crab Width/Length Ratios by Gender and Species',
        names=c('BM','BF','OM','OF'))

        