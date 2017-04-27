#!/usr/bin/env python

"""Analysing data and plotting general graphs"""

__author__ = 'Jia Le Lim'
__version__ = '0.0.1'

import csv
import operator
import decimal
import numpy as np
import matplotlib.pyplot as pl
import calendar
import sys
import os.path

# file has " "	System	Season	Month	Day	Year	Bee	Plant	Visits	Precip	Tmax	Tmin	Humid

h = open('../data/CerradoBoaVentura/rearrange/ClimNetDataLnx.csv','rb')
data = csv.reader(h)

indexes = []
seasons = []
months = []
days = []
years = []
bees = []
plants = []
visits = []
precip = []
tempmax = []
tempmin = []
humid = []

# import each column into lists
for column in data:
  indexes.append(column[0])
  seasons.append(column[2])
  months.append(column[3])
  days.append(column[4])
  years.append(column[5])
  bees.append(column[6])
  plants.append(column[7])
  visits.append(column[8])
  precip.append(column[9])
  tempmax.append(column[10])
  tempmin.append(column[11])
  humid.append(column[12])

h.close()

#remove header
for i in [indexes, seasons, months, days, years, bees, plants, visits, precip, tempmax, tempmin, humid]:
  del i[0]

# starting index of every month + the last index(len of months) -> stored as startofmonths
datalen = len(months)
startofmonths = [0]
for i in range(1, datalen):
  if months[i] != months[i-1]:
    startofmonths.append(i)
print "Total number of months is " + str(len(startofmonths)) + '.'
startofmonths.append(len(months))

# find sum for each month
sumvisit = 0
sumvisits = []
for x in range(len(startofmonths)-1):
  startindex = startofmonths[x]
  endindex = startofmonths[x + 1]
  sumvisit = 0
  for i in range(startindex, endindex):
    sumvisit += int(visits[i])
  sumvisits.append(sumvisit)

print sumvisits

# number of days observed in each month
nodays = []
for x in range(len(startofmonths)-1):
  startindex = startofmonths[x]
  endindex = startofmonths[x + 1]
  noday = 0
  for i in range(startindex, endindex):
    if days[i] != days[i-1]:
      noday += 1
  nodays.append(noday)
print nodays

# find average daily whatever in each month
averagevisits = range(len(nodays))
for i in range(len(nodays)):
  averagevisits[i] = sumvisits[i]/nodays[i]
print "average daily visits in each month: " + str(averagevisits)

g = open('../data/rearranged/AvgVisit.csv','wb')
csvwrite = csv.writer(g)

tobewritten = zip(averagevisits)

for row in tobewritten:
  csvwrite.writerow(row)

g.close()
