x = rnorm(10000,mean=0,sd=1)
mean(x)
sd(x)
max(x)
min(x)
hist(x,main="Histogram of random data")

x = c(1, 1, 2, 3, 5, 8)#,13,21,34,55,89)

#c(1, 1, 2, 3, 5, 8, ) -> x
#x<-c(1,1,2,3,5,8)

1/x

y=c(x, 0, x)
y
z = x*x
z

q = x + 1
q
q = 2*x+3
q
q=sin(x)
q

test = paste(c("x","y"), 1:10, sep="-")
test

x = 3:8
x
y = 5:2
y

# sequences
z=seq(from=2,to=12,by=2)
z
w= seq(length=8,from=0,by=3)
w
rep(3,times=5)
rep(y,each=2)

x = c(1:5,NA,NA,NA,8:10)
x
y=is.na(x)
y
is.nan(0/0) # true
is.infinite(1/0) # true
is.infinite(0/0) # true
is.nan(1/0) # true

zones = c("Eastern", "Central","Mountain","Western","Alaska","Hawaii","Samoa")
labs = paste(c("X","Y"),1:10,sep="-")
labs


x = c(1:2,NA,4:5)
x
!is.na(x)
x[!is.na(x)]
x=1:10
x[2:5]
x[-c(1,3,5,7)]

basket=c(1,3,4)
basket
names(basket)=c('apple','orange','banana')
basket
basket['orange']

#cleaning NA values in dataset
x = c(1:4,NA,6:10)
x
y = x[!is.na(x)]
y
mean(y)
x[is.na(x)]=mean(y)
x



x=c(1,2.3,4.5,6.789)
x
mode(x)
length(x)
y=c(1,'happy',sqrt(9))
mode(y)
length(y)

x=numeric()
x
length(x)
mode(x)
x[1]=5
x[2]=7
x[5]=13
x
x=11:13
x

x=1:8
x
class(x)
y=2.5*x
y
class(y)
z=matrix(nrow=2,ncol=4,data=x)
z         
class(z)
attributes(z)

x=1:4
x
attributes(x)
xmat=matrix(nrow=2,ncol=2,data=x)
xmat
attributes(xmat)

resp_data = c(3,4,4,3,3,5,4,5,5,3,3,4,3,3,5,1,2,2,1,2)
resp_data
q_text=c("very_low",'low','medium','high','very_high')
q_text
resp_factor=factor(resp_data,labels=q_text,order=TRUE)
resp_factor
plot(resp_factor)
grid()


x=1:12
attributes(x)
dim(x)=c(3,4)
x
dim(x)=c(4,3)
x
dim(x)=c(2,3,2)
x



e = list(name="my first list", nums=1:10, airports=c('JFK','ORD','LAX'),data=matrix(2,2,data=4:7))
e


pid = sample(1:10000,10)
pid
diag_code = trunc(abs(rnorm(10)*100000))/100
diag_code
gender = sample(1:2,10,replace=TRUE)
gender
med.frame=data.frame(pid=pid,diag_code=diag_code,gender=gender)
med.frame
attach(med.frame)
gf = factor(gender,levels=1:2,c('M','F'))
table(gf)
detach(med.frame)
med.frame


y = rnorm(200,0,1)
y
stem(y)

x = seq(0,99)
x = rnorm(100,0,1)
y=rnorm(100,0,1)
plot(x,y)


boxplot(y)


hist(y)

plot(x,sort(y))

plot(density(y))


# Options for graphs
# main="Title of your graph"
# xlab="title of your X axis"
# ylab="title of your y axis"
# xlim=c(low,high) # define X limits if needed
# ylim=c(low,high)# define Y limits if needed
# lty=n # define line type, solid, dashed, dash-dot, etc
# lwd=n # define line width, default is 1.0
# col="color" # define color
# pch=n # define point character (dot, triangle, etc.)

plot(x,y,main='Example Scatter Plot',xlab='X label',ylab='Y Label',ylim=c(-5,5),xlim=c(-25,125),col='blue',pch=7)



x = c(1,.9,.8,.7,.6,.5,.4,.3,.2,.1,.01,.001,.0001)
y = 1/x
y

