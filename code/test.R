library(fmsb)
library(car)
library(nlme)

# data specification.  Alter your input datafile: xxxxxxxxxx.csv
# import the data. Note: the data are stages(timing) in rows x genes in columns
setwd("~/Documents/buzz/data/rearranged/new/")
getwd()

d <- read.csv('AllTurnoverOldCerrado.csv', header = TRUE, check.names=FALSE)

head(d)
str(d)
X11() # new window
# B_os vs avgprecips*avgtemps
plot.new()
osavgmodel<- lm(B_os ~ Avgprecips*Avgtemps*Season, data= d)
par(mfrow=c(2,2), mar=c(3,3,1,1), mgp=c(2, 0.8,0))
plot(osavgmodel)
# still okay
summary(osavgmodel)
vif(osavgmodel, data=d)

drop.scope(osavgmodel)
osavgmodel2 <- update(osavgmodel, .~. -Avgprecips:Avgtemps:Season)
vif(osavgmodel2, data=d)

drop.scope(osavgmodel2)
osavgmodel3 <- update(osavgmodel2, .~. -Avgtemps:Season)
vif(osavgmodel3, data=d)

drop.scope(osavgmodel3)
osavgmodel4 <- update(osavgmodel3, .~. -Avgprecips:Avgtemps)
vif(osavgmodel4, data=d)

drop.scope(osavgmodel4)
osavgmodel5 <- update(osavgmodel4, .~. -Avgprecips:Season)
vif(osavgmodel5, data=d)

drop.scope(osavgmodel5)
osavgmodel6 <- update(osavgmodel5, .~. -Season)
vif(osavgmodel6, data=d)
summary(osavgmodel6)

osavgmodel<- lm(B_os ~ Avgprecips*Avgtemps, data= d)
par(mfrow=c(2,2), mar=c(3,3,1,1), mgp=c(2, 0.8,0))
plot(osavgmodel)
# still okay
summary(osavgmodel)
vif(osavgmodel, data=d)

drop.scope(osavgmodel)
osavgmodel2 <- update(osavgmodel, .~. -Avgprecips:Avgtemps)
vif(osavgmodel2, data=d)
summary(osavgmodel2)

osavgmodel3 <- update(osavgmodel2, .~. -Avgprecips)
summary(osavgmodel3)

osdiffmodel<- lm(B_os ~ diffprecips*difftemps, data= d)
vif(osdiffmodel, data=d)
summary(osdiffmodel)
