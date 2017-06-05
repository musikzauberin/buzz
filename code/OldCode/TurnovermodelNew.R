# data specification.  Alter your input datafile: xxxxxxxxxx.csv
# import the data. Note: the data are stages(timing) in rows x genes in columns
setwd("~/Documents/buzz/data/rearranged/new/")
getwd()

d <- read.csv('AllTurnoverNewCerrado.csv', header = TRUE, check.names=FALSE)

head(d)
str(d)
# X11()
# plant turnover vs avgprecips*avgtemps
plot.new()
plantavgmodel<- lm(PlantTurnover ~ Avgprecips*Avgtemps*Season, data= d)
par(mfrow=c(2,2), mar=c(3,3,1,1), mgp=c(2, 0.8,0))
plot(plantavgmodel)
# really bad
anova(plantavgmodel)
summary(plantavgmodel)
# everything significant, and high explanatory....

# minimise plantavgmodel
drop.scope(plantavgmodel)
plantavgmodel2 <- update(plantavgmodel, .~. -Avgprecips:Avgtemps:Season)
anova(plantavgmodel, plantavgmodel2)
anova(plantavgmodel2)
summary(plantavgmodel2)

drop.scope(plantavgmodel2)
plantavgmodel3 <- update(plantavgmodel2, .~. -Avgtemps:Season)
plantavgmodel3 <- update(plantavgmodel2, .~. -Avgprecips:Season)
plantavgmodel3 <- update(plantavgmodel2, .~. -Avgprecips:Avgtemps)
anova(plantavgmodel2, plantavgmodel3)
# cannot drop anything
save(plantavgmodel2, file='plantavgmodelfinalNew.Rda')

# plant turnover vs diffprecips*difftemps*Season
plot.new()
plantdiffmodel<- lm(PlantTurnover ~ diffprecips*difftemps*Season, data= d)
par(mfrow=c(2,2), mar=c(3,3,1,1), mgp=c(2, 0.8,0))
plot(plantdiffmodel)
# really bad
anova(plantdiffmodel)
summary(plantdiffmodel)
# not great, nothing significant, low explanatory power

# minimise plandiffgmodel
drop.scope(plantdiffmodel)
plantdiffmodel2 <- update(plantdiffmodel, .~. -diffprecips:difftemps:Season)
anova(plantdiffmodel, plantdiffmodel2)
anova(plantdiffmodel2)
summary(plantdiffmodel2)

drop.scope(plantdiffmodel2)
plantdiffmodel3 <- update(plantdiffmodel2, .~. -diffprecips:difftemps)
anova(plantdiffmodel2, plantdiffmodel3)
anova(plantdiffmodel3)
summary(plantdiffmodel3)

drop.scope(plantdiffmodel3)
plantdiffmodel4 <- update(plantdiffmodel3, .~. -diffprecips:Season)
anova(plantdiffmodel4, plantdiffmodel3)
anova(plantdiffmodel4)
summary(plantdiffmodel4)

drop.scope(plantdiffmodel4)
plantdiffmodel5 <- update(plantdiffmodel4, .~. -diffprecips)
anova(plantdiffmodel4, plantdiffmodel5)
anova(plantdiffmodel5)
summary(plantdiffmodel5)

drop.scope(plantdiffmodel5)
plantdiffmodel6 <- update(plantdiffmodel5, .~. -difftemps:Season)
anova(plantdiffmodel5, plantdiffmodel6)
anova(plantdiffmodel6)
summary(plantdiffmodel6)

drop.scope(plantdiffmodel6)
plantdiffmodel7 <- update(plantdiffmodel6, .~. -Season)
anova(plantdiffmodel7, plantdiffmodel6)
anova(plantdiffmodel7)
summary(plantdiffmodel7)

drop.scope(plantdiffmodel7)
plantdiffmodel8 <- update(plantdiffmodel7, .~. -difftemps)
anova(plantdiffmodel7, plantdiffmodel8)
anova(plantdiffmodel8)
summary(plantdiffmodel8)
save(plantdiffmodel8, file='plantdiffmodelfinalNew.Rda')

