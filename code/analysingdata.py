#!/usr/bin/env python

'''Analysing data and plotting general graphs'''

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
from operator import div

########## Script starts here ##########

filename = 'ClimNetDataLnx.csv'
pathname = '../data/CerradoBoaVentura/rearrange/' + filename
h = open(pathname,'rb')
data = csv.reader(h)


########## Inputting data into lists ##########

# copy and paste all headers in data three times
headers = 'indexes, systems, seasons, months, days, years, bees, plants, \
visits, precip, tempmax, tempmin, humid'

[indexes, systems, seasons, months, days, years, bees, plants, \
visits, precip, tempmax, tempmin, humid] = ([] for i in range(len(next(data))))

headers2 = [indexes, systems, seasons, months, days, years, bees, plants, \
visits, precip, tempmax, tempmin, humid]

enu = enumerate(headers2)
for i in enu:
  print i

for column in data:
  for j, i in enumerate(headers2):
    i.append(column[j])
    print j

h.close()

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

def monthlysum1(values, startofmonths):
  'find sum of value per month'
  measures = []
  for x in range(len(startofmonths)-1):
    startindex = startofmonths[x]
    endindex = startofmonths[x + 1]
    measure = 0
    for i in range(startindex, endindex):
      measure += int(values[i])
    measures.append(measure)
  return measures

def nodaysinmonth(days, startofmonths):
  'find number of observed days in each month'
  nodays = []
  for x in range(len(startofmonths)-1):
    startindex = startofmonths[x]
    endindex = startofmonths[x + 1]
    noday = 0
    for i in range(startindex, endindex):
      if days[i] != days[i-1]:
        noday += 1
    nodays.append(noday)
  print 'Number of observed days in each month: ' + str(nodays)
  return nodays

def dailyavgpermonth(divisor, values, decimalplaces):
  'Finding daily average of values for each month'
  values = [float(value) for value in values]
  avgvalues = map(div, values, divisor)
  avgvalues[:] = [round(avgvalue, decimalplaces) for avgvalue in avgvalues]
  print 'Average daily for each month: ' + str(avgvalues)
  return avgvalues

sumvisits = monthlysum1(visits, startofmonths)
nodays = nodaysinmonth(days, startofmonths)
avgvisits = dailyavgpermonth(nodays, sumvisits, 2)

########## Writing Data ##########
def timelabels(timeinterval, startofmonths):
  'creating new timeinterval list that corresponds to new data'
  timelabels = []
  for i in startofmonths[:-1]:
    timelabels.append(timeinterval[i])
  return timelabels

seasonlabels = timelabels(seasons, startofmonths)
yearlabels = timelabels(years, startofmonths)
monthlabels = timelabels(months, startofmonths)

def writenewdata(filename_str, headers, values):
  'inputting new data into csv file'
  headers = headers.split(', ')
  for i in range(len(headers)):
    values[i].insert(0, headers[i])
  pathname = '../data/rearranged/' + filename_str + '.csv'
  g = open(pathname, 'wb')
  csvwrite = csv.writer(g)
  tobewritten = zip(*values)
  for row in tobewritten:
    csvwrite.writerow(row)
  g.close()

newheaders = 'Season, Year, Month, NoDaysInMonth, AverageDailyVisits'
newvalues = [seasonlabels, yearlabels, monthlabels, nodays, avgvisits]
writenewdata('AvgVisits', newheaders, newvalues)