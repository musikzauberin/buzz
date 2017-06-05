library(fmsb)
library(car)
library(nlme)

# data specification.  Alter your input datafile: xxxxxxxxxx.csv
# import the data. Note: the data are stages(timing) in rows x genes in columns
setwd("~/Documents/buzz/data/rearranged/new/")
getwd()

d <- read.csv('AllTurnoverOldCerradoDry.csv', header = TRUE, check.names=FALSE)

head(d)
str(d)
X11()
plot.new()
plantavgmodeldry<- lm(PlantTurnover ~ Avgprecips*Avgtemps, data= d)
par(mfrow=c(2,2), mar=c(3,3,1,1), mgp=c(2, 0.8,0))
plot(plantavgmodeldry)
# still okay
anova(plantavgmodeldry)
summary(plantavgmodeldry)
vif(plantavgmodeldry)

drop.scope(plantavgmodeldry)
plantavgmodeldry2 <- update(plantavgmodeldry, .~. -Avgprecips:Avgtemps)
anova(plantavgmodeldry, plantavgmodeldry2)
anova(plantavgmodeldry2)
summary(plantavgmodeldry2)

drop.scope(plantavgmodeldry2)
plantavgmodeldry3 <- update(plantavgmodeldry2, .~. -Avgprecips)
anova(plantavgmodeldry2, plantavgmodeldry3)
anova(plantavgmodeldry3)
summary(plantavgmodeldry3)

drop.scope(plantavgmodeldry3)
plantavgmodeldry4 <- update(plantavgmodeldry3, .~. -Avgtemps)
anova(plantavgmodeldry3, plantavgmodeldry4)
anova(plantavgmodeldry4)
summary(plantavgmodeldry4)

save(plantavgmodeldry4, file='plantavgmodelfinalOlddry.Rda')

