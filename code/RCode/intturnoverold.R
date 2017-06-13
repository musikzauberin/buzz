library(fmsb)
library(car)
library(nlme)

# data specification.  Alter your input datafile: xxxxxxxxxx.csv
# import the data. Note: the data are stages(timing) in rows x genes in columns
setwd("~/Documents/buzz/data/rearranged/new/")
getwd()

d <- read.csv('AllTurnoverOldCerradox.csv', header = TRUE, check.names=FALSE)

head(d)
str(d)
X11()

plot.new()
intavgmodel<- lm(InteractionTurnover ~ Avgprecips*Avgtemps*Season, data= d)
par(mfrow=c(2,2), mar=c(3,3,1,1), mgp=c(2, 0.8,0))
plot(intavgmodel)
# still okay
anova(intavgmodel)
summary(intavgmodel)
vif(intavgmodel)

drop.scope(intavgmodel)
intavgmodel2 <- update(intavgmodel, .~. -Avgprecips:Avgtemps:Season)
anova(intavgmodel, intavgmodel2)
anova(intavgmodel2)
summary(intavgmodel2)
vif(intavgmodel2)

drop.scope(intavgmodel2)
intavgmodel3 <- update(intavgmodel2, .~. -Avgprecips:Avgtemps)
anova(intavgmodel2, intavgmodel3)
anova(intavgmodel3)
summary(intavgmodel3)
vif(intavgmodel3)

drop.scope(intavgmodel3)
intavgmodel4 <- update(intavgmodel3, .~. -Avgprecips:Season)
anova(intavgmodel3, intavgmodel4)
anova(intavgmodel4)
summary(intavgmodel4)
vif(intavgmodel4)

drop.scope(intavgmodel4)
intavgmodel5 <- update(intavgmodel4, .~. -Avgprecips)
anova(intavgmodel4, intavgmodel5)
anova(intavgmodel5)
summary(intavgmodel5)
vif(intavgmodel5)

drop.scope(intavgmodel5)
intavgmodel6 <- update(intavgmodel5, .~. -Avgtemps:Season)
anova(intavgmodel5, intavgmodel6)
anova(intavgmodel6)
summary(intavgmodel6)
vif(intavgmodel6)

drop.scope(intavgmodel6)
intavgmodel7 <- update(intavgmodel6, .~. -Season)
anova(intavgmodel6, intavgmodel7)
anova(intavgmodel7)
summary(intavgmodel7)

drop.scope(intavgmodel7)
intavgmodel8 <- update(intavgmodel7, .~. -Avgtemps)
anova(intavgmodel7, intavgmodel8)
anova(intavgmodel8)
summary(intavgmodel8)

##diff model

plot.new()
intdiffmodel<- lm(InteractionTurnover ~ diffprecips*difftemps*Season, data= d)
par(mfrow=c(2,2), mar=c(3,3,1,1), mgp=c(2, 0.8,0))
plot(intdiffmodel)
# still okay
anova(intdiffmodel)
summary(intdiffmodel)
vif(intdiffmodel)

drop.scope(intdiffmodel)
intdiffmodel2 <- update(intdiffmodel, .~. -diffprecips:difftemps:Season)
anova(intdiffmodel, intdiffmodel2)
anova(intdiffmodel2)
summary(intdiffmodel2)
vif(intdiffmodel2)

drop.scope(intdiffmodel2)
intdiffmodel3 <- update(intdiffmodel2, .~. -diffprecips:Season)
anova(intdiffmodel2, intdiffmodel3)
anova(intdiffmodel3)
summary(intdiffmodel3)
vif(intdiffmodel3)

drop.scope(intdiffmodel3)
intdiffmodel4 <- update(intdiffmodel3, .~. -diffprecips:difftemps)
anova(intdiffmodel3, intdiffmodel4)
anova(intdiffmodel4)
summary(intdiffmodel4)
vif(intdiffmodel4)

drop.scope(intdiffmodel4)
intdiffmodel5 <- update(intdiffmodel4, .~. -diffprecips)
anova(intdiffmodel4, intdiffmodel5)
anova(intdiffmodel5)
summary(intdiffmodel5)
vif(intdiffmodel5)

drop.scope(intdiffmodel5)
intdiffmodel6 <- update(intdiffmodel5, .~. -difftemps:Season)
anova(intdiffmodel5, intdiffmodel6)
summary(intdiffmodel6)

drop.scope(intdiffmodel6)
intdiffmodel7 <- update(intdiffmodel6, .~. -Season)
anova(intdiffmodel6, intdiffmodel7)
summary(intdiffmodel7)

drop.scope(intdiffmodel7)
intdiffmodel8 <- update(intdiffmodel7, .~. -difftemps)
anova(intdiffmodel7, intdiffmodel8)
summary(intdiffmodel8)

X11()
plot.new()
intplantavgmodel<- lm(InteractionTurnover~PlantTurnover, data= d)
par(mfrow=c(2,2), mar=c(3,3,1,1), mgp=c(2, 0.8,0))
plot(intplantavgmodel)
# still okay
anova(intplantavgmodel)
summary(intplantavgmodel)
str(d)
