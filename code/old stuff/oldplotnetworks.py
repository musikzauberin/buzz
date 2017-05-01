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

def maxValue(inputlists):
  return max([sublist[-1] for sublist in inputlists])

def minValue(inputlists):
  return min([sublist[-1] for sublist in inputlists])

filename = 'testtrial.csv'
pathname = '../data/rearranged/' + filename
h = open(pathname,'rb')
data = csv.reader(h)

# with open('../data/rearranged/testtrial.csv') as csvfile:
#    reader = csv.DictReader(csvfile, delimiter=',')
#    rows = list(reader)
#    beeplants = []
#    for row in rows:
#       i = []
#       i.append(row['Bee']) # Your data columns
#       i.append(row['Plant'])
#       beeplants.append(map(float, i)) # convert to float

########## Inputting data into lists ##########

# copy and paste all headers in data three times
headers = 'months, days, years, bees, plants'

[months, days, years, bees, plants] = ([] for i in range(len(next(data))))

headers2 = [months, days, years, bees, plants]

for column in data:
  for j, i in enumerate(headers2):
    i.append(column[j])

h.close()

print maxValue(headers2)


########## Analysing data ##########

def findstartindex(values, timescale_str):
  'Finds starting index of timescale + last index(len(timescale)), returns startoftimescale'
  'require years and months list'
  startofmonths = [0]
  startofyears = [0]
  datalen = len(values)
  if timescale_str == 'months':
    for i in range(1, datalen):
      if values[i] != values[i-1]:
        startofmonths.append(i)
    print 'Total number of months is ' + str(len(startofmonths)) + '.'
    startofmonths.append(len(months))
    return startofmonths
  if timescale_str == 'years':
    for i in range(1, datalen):
      if values[i] != values[i-1]:
        startofyears.append(i)
    print 'Total number of years is ' + str(len(startofyears)) + '.'
    startofyears.append(len(years))
    return startofyears

startofmonths = findstartindex(months, 'months')

# # shifting data downwards
#
# bees[:] = [int(x) - ((min(int(s) for s in bees)) - 1) for x in bees]
# plants[:] = [int(x) - ((min(int(s) for s in plants)) - 1) for x in plants]
#
# beelists = []
# plantlists = []
# noofmonths = 1
# rangeofmonths = range(0, len(startofmonths) - noofmonths, noofmonths)
# for x in rangeofmonths:
#   startindex = startofmonths[x]
#   nextindex = startofmonths[x + noofmonths]
#   beelist = []
#   plantlist = []
#   for i in range(startindex, nextindex):
#     if bees[i] not in beelist:
#       beelist.append(bees[i])
#     if plants[i] not in plantlist:
#       plantlist.append(plants[i])
#   beelists.append(beelist)
#   plantlists.append(plantlist)
#
# # totalnoofmonthsx4
# upperbound = 12
#
# e = 0
# beedots = [[-10] for i in range(upperbound)]
# for i in range(0, upperbound, 4):
#   beedots[i] = beelists[e]
#   e += 1
#
# ideallen = longest(beedots)
#
# for beedot in beedots:
#   while len(beedot) < ideallen:
#     beedot.append(-10)
#
# e = 0
# plantdots = [[-10] for i in range(upperbound)]
# for i in range(2, upperbound, 4):
#   plantdots[i] = plantlists[e]
#   e += 1
#
# print plantdots
# print beedots
#
# # beeplants = [[0,0] for i in range(upperbound)]
# # for i in range(upperbound):
# #   beeplants[i][0] = beedots[i]
# #   beeplants[i][1] = plantdots[i]
# # separate the list out and then combine again......
#
# ideallen = longest(plantdots)
#
# for plantdot in plantdots:
#   while len(plantdot) < ideallen:
#     plantdot.append(-10)
#
# pl.axis([-1, 24, 0, 200])
#
#
# print beeplants
# print startofmonths
#
#
# pl.plot(beedots, 'mo')
# pl.plot(plantdots, 'go')
# plotpath = '../results/' + 'networkdraft' + '.pdf'
# pl.savefig(plotpath)
#
# pl.show()


