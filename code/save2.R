library(fmsb)
library(car)
library(nlme)

setwd("~/Documents/buzz/data/rearranged/new/")
getwd()
d <- read.csv('AllTurnoverOldCerrado.csv', header = TRUE, check.names=FALSE)
head(d)
str(d)

X11()
# plant turnover vs avgprecips*avgtemps
plantavgmodel<- lm(PlantTurnover ~ Avgprecips*Avgtemps*Season, data= d)
par(mfrow=c(2,2), mar=c(3,3,1,1), mgp=c(2, 0.8,0))
plot(plantavgmodel)
# still okay
anova(plantavgmodel)
summary(plantavgmodel)
vif(plantavgmodel)
# not great, nothing significant, low explanatory power

# minimise plantavgmodel
drop.scope(plantavgmodel)
plantavgmodel2 <- update(plantavgmodel, .~. -Avgprecips:Avgtemps:Season)
anova(plantavgmodel, plantavgmodel2)
anova(plantavgmodel2)
summary(plantavgmodel2)
vif(plantavgmodel2)

drop.scope(plantavgmodel2)
plantavgmodel3 <- update(plantavgmodel2, .~. -Avgprecips:Avgtemps)
anova(plantavgmodel2, plantavgmodel3)
anova(plantavgmodel3)
summary(plantavgmodel3)
vif(plantavgmodel3)

drop.scope(plantavgmodel3)
plantavgmodel4 <- update(plantavgmodel3, .~. -Avgprecips:Season)
anova(plantavgmodel4, plantavgmodel3)
anova(plantavgmodel4)
summary(plantavgmodel4)
vif(plantavgmodel4)

drop.scope(plantavgmodel4)
plantavgmodel5 <- update(plantavgmodel4, .~. -Avgtemps:Season)
anova(plantavgmodel4, plantavgmodel5)
anova(plantavgmodel5)
summary(plantavgmodel5)
vif(plantavgmodel5)

drop.scope(plantavgmodel5)
plantavgmodel6 <- update(plantavgmodel5, .~. -Season)
anova(plantavgmodel5, plantavgmodel6)
vif(plantavgmodel6)
summary(plantavgmodel6)

plantavgmodel7 <- update(plantavgmodel6, .~. -Avgprecips)
anova(plantavgmodel6, plantavgmodel7)
vif(plantavgmodel7)
summary(plantavgmodel7)

save(plantavgmodel5, file='plantavgmodelfinalOld.Rda')


# plant turnover vs diffprecips*difftemps*Season
plot.new()
plantdiffmodel<- lm(PlantTurnover ~ diffprecips*difftemps*Season, data= d)
par(mfrow=c(2,2), mar=c(3,3,1,1), mgp=c(2, 0.8,0))
plot(plantdiffmodel)
# still okay
anova(plantdiffmodel)
summary(plantdiffmodel)
# not great, nothing significant, low explanatory power

# minimise plandiffgmodel
drop.scope(plantdiffmodel)
plantdiffmodel2 <- update(plantdiffmodel, .~. -diffprecips:difftemps:Season)
anova(plantdiffmodel, plantdiffmodel2)
anova(plantdiffmodel2)
summary(plantdiffmodel2)
vif(plantdiffmodel2)

drop.scope(plantdiffmodel2)
plantdiffmodel3 <- update(plantdiffmodel2, .~. -diffprecips:Season)
anova(plantdiffmodel2, plantdiffmodel3)
anova(plantdiffmodel3)
summary(plantdiffmodel3)
vif(plantdiffmodel3)

drop.scope(plantdiffmodel3)
plantdiffmodel4 <- update(plantdiffmodel3, .~. -diffprecips:difftemps)
anova(plantdiffmodel4, plantdiffmodel3)
anova(plantdiffmodel4)
summary(plantdiffmodel4)
vif(plantdiffmodel4)

drop.scope(plantdiffmodel4)
plantdiffmodel5 <- update(plantdiffmodel4, .~. -difftemps:Season)
anova(plantdiffmodel4, plantdiffmodel5)
anova(plantdiffmodel5)
summary(plantdiffmodel5)
vif(plantdiffmodel5)

drop.scope(plantdiffmodel5)
plantdiffmodel6 <- update(plantdiffmodel5, .~. -Season)
anova(plantdiffmodel5, plantdiffmodel6)
anova(plantdiffmodel6)
summary(plantdiffmodel6)

drop.scope(plantdiffmodel6)
plantdiffmodel7 <- update(plantdiffmodel6, .~. -difftemps)
anova(plantdiffmodel7, plantdiffmodel6)
anova(plantdiffmodel7)
summary(plantdiffmodel7)

drop.scope(plantdiffmodel7)
plantdiffmodel8 <- update(plantdiffmodel7, .~. -diffprecips)
anova(plantdiffmodel7, plantdiffmodel8)
anova(plantdiffmodel8)
summary(plantdiffmodel8)
save(plantdiffmodel8, file='plantdiffmodelfinalOld.Rda')

