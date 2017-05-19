#!/usr/bin/env python
"""Analysing climate data (histogram)"""

import csv
import operator
import decimal
import numpy as np
import matplotlib.pyplot as pl
import calendar
import sys
import os.path
from math import log

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

h = open('../data/CerradoBoaVentura/NewCerradoClima.csv','rb')
data = csv.reader(h)

########## Inputting data into lists ##########
# copy and paste all headers in data three times
headers = 'years, months, days, precips, tempmaxs, tempmins, humids'

[years, months, days, precips, tempmaxs, tempmins, humids] = ([] for i in range(len(next(data))))

headers2 = [years, months, days, precips, tempmaxs, tempmins, humids]

for column in data:
  for j, i in enumerate(headers2):
    i.append(column[j])

h.close()

# header was not deleted, somehow it is not read into file...


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
dailytemps = []

for x in range(len(startofmonths)-1):
  startindex = startofmonths[x]
  endindex = startofmonths[x + 1]
  sumtemp = 0
  noday = 0
  for i in range(startindex, endindex):
    if tempmaxs[i] != '' and tempmins[i] != '':
      dailytemp = (float(tempmaxs[i]) + float(tempmins[i]))/2
      sumtemp += dailytemp
      noday += 1
    dailytemps.append(round(dailytemp, 2))
  avgtemp = round(sumtemp/noday, 2)
  avgtemps.append(avgtemp)

# find average range of temperature
tempranges = []
dailytempranges = []
for x in range(len(startofmonths)-1):
  startindex = startofmonths[x]
  endindex = startofmonths[x + 1]
  sumtemprange = 0
  noday = 0
  for i in range(startindex, endindex):
    if tempmaxs[i] != '' and tempmins[i] != '':
      dailytemprange = float(tempmaxs[i]) - float(tempmins[i])
      sumtemprange += dailytemprange
      noday += 1
    dailytempranges.append(round(dailytemprange, 2))
  temprange = round(sumtemprange/noday, 2)
  tempranges.append(temprange)


########## Plotting data ##########

# newvalues = [yearlabels, monthlabels, sumprecips, avghumids, avgtempmaxs, avgtemps, tempranges]
# [years, months, days, precips, tempmaxs, tempmins, humids]
# bins = np.arange(0, 40, 0.1)

def makeHistall(values, startofmonths, valuetitle_str, plotname_str, color_str):
  values = filter(None, values)
  values = np.array(values).astype(np.float)
  for i in range(len(startofmonths)-1):
    startindex = startofmonths[i]
    endindex = startofmonths[i+1]
    plottitle = valuetitle_str + ' in Cerrado'
    pl.title(plottitle, size = 18)
    pl.hist(values[startindex:endindex], histtype='bar', color = color_str)
    # color = 'crimson', 'blue'
    plotpath = '../results/ClimateDistribution/NewCerrado/' + plotname_str + '.pdf'
    pl.savefig(plotpath)
  pl.close()

def makeHist(values, startofmonths, valuetitle_str, plotname_str, color_str):
  values = filter(None, values)
  values = np.array(values).astype(np.float)
  for i in range(len(startofmonths)-1):
    startindex = startofmonths[i]
    endindex = startofmonths[i+1]
    plottitle = valuetitle_str + months[startindex] + '/' + years[startindex] + 'in Cerrado'
    pl.title(plottitle, size = 18)
    pl.hist(values[startindex:endindex], histtype='bar', color = color_str)
    # color = 'crimson', 'blue'
    plotpath = '../results/ClimateDistribution/NewCerrado/' + plotname_str + years[startindex] + ',' + months[startindex] + '.pdf'
    pl.savefig(plotpath) 
    pl.close()

makeHistall(dailytempranges, startofmonths, 'Temperature Ranges', 'TempRange', 'burlywood')
makeHist(dailytempranges, startofmonths, 'Temperature Ranges', 'TempRange', 'burlywood')


#' + months[startindex] + '/' + years[startindex] + ' 
#' + years[startindex] + ',' + months[startindex] + '


# plottitle = 'Temperature range in Cerrado'
# pl.title(plottitle, size = 18)
# pl.hist(tempranges, normed=1, histtype='bar', color = 'burlywood')
# # color = 'crimson', 'blue'
# plotpath = '../results/TempDistributions/' + 'TempRangeDistributionAll' + '.pdf'
# pl.savefig(plotpath)

