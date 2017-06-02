library(fmsb)
library(car)

# data specification.  Alter your input datafile: xxxxxxxxxx.csv
# import the data. Note: the data are stages(timing) in rows x genes in columns
setwd("~/Documents/buzz/data/rearranged/new/")
getwd()

d <- read.csv('AllTurnoverOldCerrado.csv', header = TRUE, check.names=FALSE)

head(d)
str(d)
# X11()
# B_os vs avgprecips*avgtemps
plot.new()
osavgmodel<- lm(B_os ~ Avgprecips*Avgtemps*Season, data= d)
par(mfrow=c(2,2), mar=c(3,3,1,1), mgp=c(2, 0.8,0))
plot(osavgmodel)
# still okay
anova(osavgmodel)
summary(osavgmodel)
vif(osavgmodel)

# minimise osavgmodel
drop.scope(osavgmodel)
osavgmodel2 <- update(osavgmodel, .~. -Avgprecips:Avgtemps:Season)
anova(osavgmodel, osavgmodel2)

save(osavgmodel, file='osavgmodelfinalOld.Rda')

vif(osavgmodel, data = d)
osavgmodel2 <- update(osavgmodel, .~. -Avgprecips:Avgtemps:Season)
vif(osavgmodel2, data = d)
osavgmodel3 <- update(osavgmodel2, .~. -Season)
vif(osavgmodel3, data = d)
osavgmodel4 <- update(osavgmodel3, .~. -Avgprecips:Avgtemps)
vif(osavgmodel4, data = d)
osavgmodel5 <- update(osavgmodel4, .~. -Avgprecips:Season)
vif(osavgmodel5, data = d)
anova(osavgmodel5)
summary(osavgmodel5)
osavgmodel6 <- update(osavgmodel5, .~. -Avgprecips)
vif(osavgmodel6, data = d)
anova(osavgmodel6)
summary(osavgmodel6)

drop.scope(osavgmodel6)
osavgmodel7 <- update(osavgmodel6, .~. -Avgtemps:Season)
anova(osavgmodel6, osavgmodel7)
anova(osavgmodel7)
summary(osavgmodel7)


# os turnover vs diffprecips*difftemps*Season
plot.new()
osdiffmodel<- lm(B_os ~ diffprecips*difftemps*Season, data= d)
par(mfrow=c(2,2), mar=c(3,3,1,1), mgp=c(2, 0.8,0))
plot(osdiffmodel)
# not very okay
anova(osdiffmodel)
summary(osdiffmodel)
# not great, nothing significant, low explanatory power

# minimise osdiffgmodel
drop.scope(osdiffmodel)
osdiffmodel2 <- update(osdiffmodel, .~. -diffprecips:difftemps:Season)
anova(osdiffmodel, osdiffmodel2)
anova(osdiffmodel2)
summary(osdiffmodel2)

drop.scope(osdiffmodel2)
osdiffmodel3 <- update(osdiffmodel2, .~. -diffprecips:difftemps)
anova(osdiffmodel2, osdiffmodel3)
anova(osdiffmodel3)
summary(osdiffmodel3)

drop.scope(osdiffmodel3)
osdiffmodel4 <- update(osdiffmodel3, .~. -diffprecips:Season)
anova(osdiffmodel4, osdiffmodel3)
anova(osdiffmodel4)
summary(osdiffmodel4)

drop.scope(osdiffmodel4)
osdiffmodel5 <- update(osdiffmodel4, .~. -diffprecips)
anova(osdiffmodel4, osdiffmodel5)
anova(osdiffmodel5)
summary(osdiffmodel5)

drop.scope(osdiffmodel5)
osdiffmodel6 <- update(osdiffmodel5, .~. -difftemps:Season)
anova(osdiffmodel5, osdiffmodel6)
anova(osdiffmodel6)
summary(osdiffmodel6)

drop.scope(osdiffmodel6)
osdiffmodel7 <- update(osdiffmodel6, .~. -difftemps)
anova(osdiffmodel7, osdiffmodel6)
anova(osdiffmodel7)
summary(osdiffmodel7)

drop.scope(osdiffmodel7)
osdiffmodel8 <- update(osdiffmodel7, .~. -Season)
anova(osdiffmodel7, osdiffmodel8)
anova(osdiffmodel8)
summary(osdiffmodel8)
save(osdiffmodel8, file='osdiffmodelfinalOld.Rda')


vif(osdiffmodel, data = d)
drop.scope(osdiffmodel)
osdiffmodel2 <- update(osdiffmodel, .~. -diffprecips:difftemps:Season)
vif(osdiffmodel2, data = d)

osdiffmodel3 <- update(osdiffmodel2, .~. -diffprecips:Season)
vif(osdiffmodel3, data = d)
anova(osdiffmodel3)
summary(osdiffmodel3)

drop.scope(osdiffmodel3)
osdiffmodel4 <- update(osdiffmodel3, .~. -diffprecips:difftemps)
anova(osdiffmodel4)
summary(osdiffmodel4)
