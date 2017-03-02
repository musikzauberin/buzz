#Script to combine Cerrado pollination network data wth climate data

rm(list=ls()) # clear objects
graphics.off() #close all open figures and graphics objects

NetData <- as.matrix(read.table("../Data/PolliNets.txt",
                                header = TRUE, fill = TRUE,sep = "\t",strip.white = TRUE))
ClimData<- as.matrix(read.table("../Data/Clima.txt",
                                header = TRUE, fill = TRUE,sep = "\t",strip.white = TRUE))
coln<-list() #create empty list to hold column indices
coln$NetSeas <- match("Season", colnames(NetData)) #get column indices
coln$NetMnth <- match("Month", colnames(NetData))
coln$NetDay <- match("Day", colnames(NetData))
coln$NetYr <- match("Year", colnames(NetData))
coln$NetBee <- match("Bee", colnames(NetData))
coln$NetPlnt <- match("Plant", colnames(NetData))
coln$ClimMnth <- match("Month", colnames(ClimData))
coln$ClimDay <- match("Day", colnames(ClimData))
coln$ClimYr <- match("Year", colnames(ClimData))
coln$Precip <- match("Precipitation..mm.", colnames(ClimData))
coln$Tmax <- match("Temp..Max.", colnames(ClimData))
coln$Tmin <- match("Temp..Min.", colnames(ClimData))
coln$Humid <- match("Humidity", colnames(ClimData))

#First aggregate daily link-specific visitations  
TmpLst <- as.matrix(paste(NetData[,coln$NetDay],NetData[,coln$NetMnth],NetData[,coln$NetYr],
                          NetData[,coln$NetBee],NetData[,coln$NetPlnt]))# obtain unique day and bee-plant link combinations
LnkLst <- unique(TmpLst) #Extract unique day-bee-plant link combinations
OutData <- matrix(data = "",length(LnkLst),length(colnames(NetData))+5,dimnames = 
  list(NULL,c(colnames(NetData),"Visits","Precip","Tmax","Tmin","Humid"))) #Preallocate empty array

for(i in 1:nrow(LnkLst)){
  tmpIx <-which(TmpLst==LnkLst[i])
  OutData[i,1:length(colnames(NetData))]<-NetData[tmpIx[1],,drop = FALSE] 
  OutData[i,length(colnames(NetData))+1]<-length(tmpIx) #number of instances of that link on that day
  for(j in 1:nrow(ClimData)){ #Add climatic data
    if (ClimData[j,coln$ClimDay] == as.numeric(NetData[tmpIx[1],coln$NetDay]) &&
      ClimData[j,coln$ClimMnth] == as.numeric(NetData[tmpIx[1],coln$NetMnth]) &&
      ClimData[j,coln$ClimYr] == as.numeric(NetData[tmpIx[1],coln$NetYr])) { 
      OutData[i,length(colnames(NetData))+2] <- ClimData[j, coln$Precip]
      OutData[i,length(colnames(NetData))+3] <- ClimData[j, coln$Tmax]
      OutData[i,length(colnames(NetData))+4] <- ClimData[j, coln$Tmin]
      OutData[i,length(colnames(NetData))+5] <- ClimData[j, coln$Humid]
      break
    }
  }
}
write.csv(OutData,"ClimNetDataLnx.csv")

#Now aggregate daily bee(node)-specific visitations  
TmpLst <- as.matrix(paste(NetData[,coln$NetDay],NetData[,coln$NetMnth],NetData[,coln$NetYr],NetData[,coln$NetBee]))# obtain unique day-bee combinations
LnkLst <- unique(TmpLst) #Extract unique day-bee-plant link combinations
OutData <- matrix(data = "",length(LnkLst),length(colnames(NetData))+5,dimnames = 
  list(NULL,c(colnames(NetData),"Visits","Precip","Tmax","Tmin","Humid"))) #Preallocate empty array
for(i in 1:nrow(LnkLst)){
  tmpIx <-which(TmpLst==LnkLst[i])
  tmpDat <- NetData[tmpIx,,drop = FALSE] 
  OutData[i,1:length(colnames(NetData))-1]<-tmpDat[1,1:length(colnames(NetData))-1,drop = FALSE] #transfer all data except plant id
  OutData[i,length(colnames(NetData))] <-paste(tmpDat[,coln$NetPlnt],collapse = ";") # list IDs of all plants visted by that bee
  OutData[i,length(colnames(NetData))+1]<-length(tmpIx)
  for(j in 1:nrow(ClimData)){ #Add climatic data
    if (ClimData[j,coln$ClimDay] == as.numeric(NetData[tmpIx[1],coln$NetDay]) &&
      ClimData[j,coln$ClimMnth] == as.numeric(NetData[tmpIx[1],coln$NetMnth]) &&
      ClimData[j,coln$ClimYr] == as.numeric(NetData[tmpIx[1],coln$NetYr])) { 
      OutData[i,length(colnames(NetData))+2] <- ClimData[j, coln$Precip]
      OutData[i,length(colnames(NetData))+3] <- ClimData[j, coln$Tmax]
      OutData[i,length(colnames(NetData))+4] <- ClimData[j, coln$Tmin]
      OutData[i,length(colnames(NetData))+5] <- ClimData[j, coln$Humid]
      break
    }
  }
}
write.csv(OutData,"../Results/ClimNetDataBee.csv")

#Now summarize bee-specific data... 

