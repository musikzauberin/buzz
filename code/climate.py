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

h = open('../data/CerradoBoaVentura/Clima.csv','rb')
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

def nodaysinmonth(days, startofmonths):
  'find number of observed days in each month'
  nodays = []
  for x in range(len(startofmonths)-1):
    startindex = startofmonths[x]
    endindex = startofmonths[x + 1]
    noday = 1
    for i in range(startindex + 1, endindex):
      if days[i] != days[i-1]:
        noday += 1
    nodays.append(noday)
  return nodays

def dailyavgpermonth(divisor, values, decimalplaces):
  'Finding daily average of values for each month'
  values = [float(value) for value in values]
  avgvalues = map(div, values, divisor)
  avgvalues[:] = [round(avgvalue, decimalplaces) for avgvalue in avgvalues]
  print 'Average daily for each month: ' + str(avgvalues)
  return avgvalues

# find monthly sum of precipitation
sumprecips = monthlysum(precips, startofmonths, 2)

# find average daily humidity for each month
sumhumids = monthlysum(humids, startofmonths, 0)
nodays = nodaysinmonth(days, startofmonths)
avghumids = dailyavgpermonth(nodays, sumhumids, 2)

# find max temperature for each month
# find average temperature range for each month
# find average daily temperature for each month


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
  pathname = '../data/rearranged/' + filename_str + '.csv'
  g = open(pathname, 'wb')
  csvwrite = csv.writer(g)
  tobewritten = zip(*values)
  for row in tobewritten:
    csvwrite.writerow(row)
  g.close()

newheaders = 'Year, Month, SumPrecips, AvgHumidity'
newvalues = [yearlabels, monthlabels, sumprecips, avghumids]
writenewdata('ClimaData', newheaders, newvalues)