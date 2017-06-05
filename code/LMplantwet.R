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
plot.new()
plantavgmodelwet<- lm(PlantTurnover ~ Avgprecips*Avgtemps, data= d)
par(mfrow=c(2,2), mar=c(3,3,1,1), mgp=c(2, 0.8,0))
plot(plantavgmodelwet)
# still okay
anova(plantavgmodelwet)
summary(plantavgmodelwet)
vif(plantavgmodelwet)

drop.scope(plantavgmodelwet)
plantavgmodelwet2 <- update(plantavgmodelwet, .~. -Avgprecips:Avgtemps)
anova(plantavgmodelwet, plantavgmodelwet2)
anova(plantavgmodelwet2)
summary(plantavgmodelwet2)
vif(plantavgmodelwet2)

drop.scope(plantavgmodelwet2)
plantavgmodelwet3 <- update(plantavgmodelwet2, .~. -Avgprecips)
anova(plantavgmodelwet2, plantavgmodelwet3)
anova(plantavgmodelwet3)
summary(plantavgmodelwet3)

drop.scope(plantavgmodelwet3)
plantavgmodelwet4 <- update(plantavgmodelwet3, .~. -Avgtemps)
anova(plantavgmodelwet3, plantavgmodelwet4)


save(plantavgmodelwet3, file='plantavgmodelfinalOldwet.Rda')


