# data specification.  Alter your input datafile: xxxxxxxxxx.csv
# import the data. Note: the data are stages(timing) in rows x genes in columns
setwd("~/Documents/buzz/data/rearranged/new/")
getwd()

d <- read.csv('AllTurnoverOldCerrado.csv', header = TRUE, check.names=FALSE)

head(d)
str(d)
d$SpeciesTurnover
logSpeciesTurnover <- log(d$SpeciesTurnover)
logSpeciesTurnover
# X11()
model <- lm(PlantTurnover ~ Avgprecips*Avgtemps, data= d)

plot.new()
par(mfrow=c(2,2), mar=c(3,3,1,1), mgp=c(2, 0.8,0))
plot(model)


