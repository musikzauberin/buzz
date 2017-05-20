#!/usr/bin/env python

'''Analysing climate data and outputting monthly values'''

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
from operator import sub

def CheckInt(s):
  try: 
    int(s)
    return True
  except ValueError:
    return False


########## Inputting data into lists ##########

h = open('../data/CerradoBoaVentura/Clima.csv','rb')
data = csv.reader(h)

# copy and paste all headers in data three times
headers = 'years, months, days, precips, tempmaxs, tempmins, humids'

[years, months, days, precips, tempmaxs, tempmins, humids] = ([] for i in range(len(next(data))))

headers2 = [years, months, days, precips, tempmaxs, tempmins, humids]

for column in data:
  for j, i in enumerate(headers2):
    i.append(column[j])

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

def monthlysum(values, startofmonths, decimalplaces):
  'find sum of value per month'
  measures = []
  for x in range(len(startofmonths)-1):
    startindex = startofmonths[x]
    endindex = startofmonths[x + 1]
    measure = 0
    for i in range(startindex, endindex):
      # print CheckInt(values[i])
      # if CheckInt(values[i]):
      #   measure += int(values[i])
      if values[i] == '':
        print "no values at " + str(i)
      else:
        measure += float(values[i])
    measure = round(measure, decimalplaces)
    measures.append(measure)
  return measures

def dailyavgpermonth(values, startofmonths, decimalplaces):
  'find sum of value per month'
  avgmeasures = []
  for x in range(len(startofmonths)-1):
    startindex = startofmonths[x]
    endindex = startofmonths[x + 1]
    measure = 0
    noday = 0
    for i in range(startindex, endindex):
      if values[i] != '':
        measure += float(values[i])
        noday += 1
    avgmeasure = round(measure/noday, decimalplaces)
    avgmeasures.append(avgmeasure)
  return avgmeasures

# find monthly sum of precipitation
sumprecips = monthlysum(precips, startofmonths, 2)

# find average daily humidity for each month
avghumids = dailyavgpermonth(humids, startofmonths, 2)

# find average max temperature for each month
avgtempmaxs = dailyavgpermonth(tempmaxs, startofmonths, 2)

# find average daily temperature for each month
avgtemps = []
for x in range(len(startofmonths)-1):
  startindex = startofmonths[x]
  endindex = startofmonths[x + 1]
  dailytemp = 0
  noday = 0
  for i in range(startindex, endindex):
    if tempmaxs[i] != '' and tempmins[i] != '':
      dailytemp += (float(tempmaxs[i]) + float(tempmins[i]))/2
      noday += 1
  avgtemp = round(dailytemp/noday, 2)
  avgtemps.append(avgtemp)

# find average range of temperature
tempranges = []
for x in range(len(startofmonths)-1):
  startindex = startofmonths[x]
  endindex = startofmonths[x + 1]
  dailytemprange = 0
  noday = 0
  for i in range(startindex, endindex):
    if tempmaxs[i] != '' and tempmins[i] != '':
      dailytemprange += float(tempmaxs[i]) - float(tempmins[i])
      noday += 1
  temprange = round(dailytemprange/noday, 2)
  tempranges.append(temprange)

# find median temperature
tempmedians = []
for x in range(len(startofmonths)-1):
  startindex = startofmonths[x]
  endindex = startofmonths[x + 1]
  dailytemps = []
  for i in range(startindex, endindex):
    if tempmaxs[i] != '' and tempmins[i] != '':
      dailytemp = (float(tempmaxs[i]) + float(tempmins[i]))/2
    dailytemps.append(dailytemp)
  tempmedians.append(round(np.median(dailytemps), 5))


########## Writing Data ##########
def timelabels(timeinterval, startofmonths):
  'creating new timeinterval list that corresponds to new data'
  timelabels = []
  for i in startofmonths[:-1]:
    timelabels.append(timeinterval[i])
  return timelabels

yearlabels = timelabels(years, startofmonths)
monthlabels = timelabels(months, startofmonths)

def writenewdata(filename_str, headers, values):
  'inputting new data into csv file'
  headers = headers.split(', ')
  for i in range(len(headers)):
    values[i].insert(0, headers[i])
  pathname = '../data/rearranged/new/' + filename_str + '.csv'
  g = open(pathname, 'wb')
  csvwrite = csv.writer(g)
  tobewritten = zip(*values)
  for row in tobewritten:
    csvwrite.writerow(row)
  g.close()

newheaders = 'Year, Month, SumPrecips, AvgHumidity, AvgMaxTemp, AvgTemp, AvgTempRange, TempMedian'
newvalues = [yearlabels, monthlabels, sumprecips, avghumids, avgtempmaxs, avgtemps, tempranges, tempmedians]
writenewdata('ClimaData', newheaders, newvalues)