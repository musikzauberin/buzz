library(fmsb)
library(car)
library(nlme)

# data specification.  Alter your input datafile: xxxxxxxxxx.csv
# import the data. Note: the data are stages(timing) in rows x genes in columns
setwd("~/Documents/buzz/data/rearranged/new/")
getwd()

d <- read.csv('AllTurnoverOldCerradoWet.csv', header = TRUE, check.names=FALSE)

head(d)
str(d)
X11()
# B_os vs avgprecips*avgtemps
plot.new()
plantavgmodelwet<- lm(PlantTurnover ~ Avgprecips*Avgtemps, data= d)
par(mfrow=c(2,2), mar=c(3,3,1,1), mgp=c(2, 0.8,0))
plot(plantavgmodelwet)
# still okay
anova(plantavgmodelwet)
summary(plantavgmodelwet)
vif(plantavgmodelwet)


