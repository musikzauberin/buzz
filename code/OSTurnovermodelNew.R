# data specification.  Alter your input datafile: xxxxxxxxxx.csv
# import the data. Note: the data are stages(timing) in rows x genes in columns
setwd("~/Documents/buzz/data/rearranged/new/")
getwd()

d <- read.csv('AllTurnoverNewCerrado.csv', header = TRUE, check.names=FALSE)

head(d)
str(d)
# X11()
# B_os vs avgprecips*avgtemps
plot.new()
osavgmodel<- lm(B_os ~ Avgprecips*Avgtemps*Season, data= d)
par(mfrow=c(2,2), mar=c(3,3,1,1), mgp=c(2, 0.8,0))
plot(osavgmodel)
# really bad
anova(osavgmodel)
summary(osavgmodel)
# a few sig

# minimise osavgmodel
drop.scope(osavgmodel)
osavgmodel2 <- update(osavgmodel, .~. -Avgprecips:Avgtemps:Season)
anova(osavgmodel, osavgmodel2)
anova(osavgmodel2)
summary(osavgmodel2)

drop.scope(osavgmodel2)
osavgmodel3 <- update(osavgmodel2, .~. -Avgprecips:Season)
anova(osavgmodel3, osavgmodel2)
anova(osavgmodel3)
summary(osavgmodel3)

drop.scope(osavgmodel3)
osavgmodel4 <- update(osavgmodel3, .~. -Avgprecips:Avgtemps)
anova(osavgmodel3, osavgmodel4)
anova(osavgmodel4)
summary(osavgmodel4)

drop.scope(osavgmodel4)
osavgmodel5 <- update(osavgmodel4, .~. -Avgprecips)
anova(osavgmodel5, osavgmodel4)
anova(osavgmodel5)
summary(osavgmodel5)

drop.scope(osavgmodel5)
osavgmodel6 <- update(osavgmodel5, .~. -Avgtemps:Season)
anova(osavgmodel5, osavgmodel6)
save(osavgmodel5, file='osavgmodelfinalNew.Rda')

# os turnover vs diffprecips*difftemps*Season
plot.new()
osdiffmodel<- lm(B_os ~ diffprecips*difftemps*Season, data= d)
model<- gls(B_os ~ diffprecips*difftemps*Season, data= d)
par(mfrow=c(2,2), mar=c(3,3,1,1), mgp=c(2, 0.8,0))
plot(osdiffmodel)
# very bad
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
save(osdiffmodel8, file='osdiffmodelfinalNew.Rda')
summary(osavgmodel)
plot(osavgmodel)
