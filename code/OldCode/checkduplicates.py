# check for duplicates script
# to run :
# python checkduplicates.py file.csv numberofmonths

import csv
import operator
import decimal
import numpy as np
import matplotlib.pyplot as pl
import calendar
import sys
import os.path

filename = sys.argv[1]
noofmonths = int(sys.argv[2])

pathname = os.path.join("../data/rearranged/", filename)

if os.path.isfile(pathname):
  print 'Valid file!'
else:
  print 'Invalid file!'
  sys.exit()

t = open(pathname,'rb')
data = csv.reader(t)

months = []
days = []
years = []
bees = []
plants = []

for column in data:
  months.append(column[0])
  days.append(column[1])
  years.append(column[2])
  bees.append(column[3])
  plants.append(column[4])

t.close()

months = months[1:]
days = days[1:]
years = years[1:]
bees = bees[1:]
plants = plants[1:]

datalen = len(months)

startofmonths = [0]
for i in range(1, datalen):
  if months[i] != months[i-1]:
    startofmonths.append(i)
startofmonths.append(len(months))

noofinteractions = []
for i in range(len(startofmonths)-1):
  noofinteraction = startofmonths[i+1]-startofmonths[i]
  noofinteractions.append(noofinteraction)

print "Number of interactions in each month: " + str(noofinteractions)

rangeofmonths = range(0, len(startofmonths) - noofmonths, noofmonths)

# finding and deleting duplicates

duplicateno = 0
duplicates = []

for x in rangeofmonths:
  startindex = startofmonths[x]
  nextindex = startofmonths[x + noofmonths]
  for i in range(startindex, nextindex):
    e = i + 1
    while e < nextindex:
      if bees[i] == bees[e]:
        if plants[i] == plants[e]:
          duplicateno += 1
          print str(i) + ' matches with ' + str(e) + ' really?'
          e += 1
        else:
          e += 1
      else:
        e += 1
        
if duplicateno == 0:
  print "No duplicates found in this file."
else:
  print "BEDO BEDO! DUPLICATES FOUND!"