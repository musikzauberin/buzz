import csv
import operator
import decimal
import numpy as np
import matplotlib.pyplot as pl
import calendar
import sys
import os.path
import networkx as nx

def longest(l):
  if(not isinstance(l, list)): 
    return(0)
  else:
    return(max([len(subl) for subl in l]))

def maxValue(inputlist):
  return max([sublist[-1] for sublist in inputlist])


with open('../data/rearranged/testtrial.csv') as csvfile:
   reader = csv.DictReader(csvfile, delimiter=',')
   rows = list(reader)
   beeplants = []
   for row in rows:
      i = []
      i.append(row['Bee']) # Your data columns
      i.append(row['Plant'])
      beeplants.append(map(float, i)) # convert to float

h = open('../data/rearranged/testtrial.csv','rb')
data = csv.reader(h)

months = []
bees = []
plants = []

for column in data:
  months.append(column[0])
  bees.append(column[3])
  plants.append(column[4])

h.close()

#remove header
for i in [months, bees, plants]:
  del i[0]

datalen = len(months)

startofmonths = [0]
for i in range(1, datalen):
  if months[i] != months[i-1]:
    startofmonths.append(i)
startofmonths.append(len(months))

# shifting data downwards

bees[:] = [int(x) - ((min(int(s) for s in bees)) - 1) for x in bees]
plants[:] = [int(x) - ((min(int(s) for s in plants)) - 1) for x in plants]

beelists = []
plantlists = []
noofmonths = 1
rangeofmonths = range(0, len(startofmonths) - noofmonths, noofmonths)
for x in rangeofmonths:
  startindex = startofmonths[x]
  nextindex = startofmonths[x + noofmonths]
  beelist = []
  plantlist = []
  for i in range(startindex, nextindex):
    if bees[i] not in beelist:
      beelist.append(bees[i])
    if plants[i] not in plantlist:
      plantlist.append(plants[i])
  beelists.append(beelist)
  plantlists.append(plantlist)

# totalnoofmonthsx4
upperbound = 12

e = 0
beedots = [[-10] for i in range(upperbound)]
for i in range(0, upperbound, 4):
  beedots[i] = beelists[e]
  e += 1

ideallen = longest(beedots)

for beedot in beedots:
  while len(beedot) < ideallen:
    beedot.append(-10)
    
e = 0
plantdots = [[-10] for i in range(upperbound)]
for i in range(2, upperbound, 4):
  plantdots[i] = plantlists[e]
  e += 1

print plantdots
print beedots

ideallen = longest(plantdots)

for plantdot in plantdots:
  while len(plantdot) < ideallen:
    plantdot.append(-10)

pl.axis([-1, 24, 0, 200])


# beeplants[:][:] = [int(beeplant[0]) - ((min(int(s) for s in bees)) - 1) for beeplant[0] in beeplants]
# #   beeplant[1] = [int(x) - ((min(int(s) for s in plants)) - 1) for x in plants]

print beeplants[:][:]
print startofmonths


pl.plot(beedots, 'mo')
pl.plot(plantdots, 'go')
pl.show()