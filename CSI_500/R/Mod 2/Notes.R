my_data =  c(1,3,5,7,9)


my_info = data.frame(id=numeric(0),gender=character(0),age=numeric(0))
my_info
my_data2= edit(my_info)

#import csv
myframe = read.csv("name.csv", header=TRUE, sep=",",comment.char="#")

#import excel
myframe = read.xlsx(file="name.xlsx",sheetIndex=1,header=TRUE,startRow=2)

h = c(1,2,3,4,5)
w = c(100,110,120,130,140)
a = c(25,26,27,28,29)
data_=data.frame(h,w,a)
data_
write.table(x=data_,
            file='student_info.csv',
            sep=',',
            col.names=TRUE,
            row.names=FALSE,
            quote=FALSE,
            eol='\n')

idlist = seq(1,4)
genderlist = c('M','F','M','F')
agelist=c(27,26,33,29)
myframe = data.frame(
  id=idlist,
  gender=genderlist,
  age=agelist
)
myframe

myframe$car=c('Y','Y','N','N')
myframe
myframe$age.pct = myframe$age/mean(myframe$age)
myframe
myframe[order(myframe$age.pct),]
myframe
myframe[order(myframe$id),]
myframe

fix(myframe)
