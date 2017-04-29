import csv
import operator
import decimal
import numpy as np
import matplotlib.pyplot as pl
import calendar
import sys
import os.path

h = open('../data/CerradoBoaVentura/Clima.csv','rb')
data = csv.reader(h)

years = []
months = []
days = []
precip = []
tempmax = []
tempmin = []
humid = []

for column in data:
  years.append(column[0])
  months.append(column[1])
  days.append(column[2])
  precip.append(column[3])
  tempmax.append(column[4])
  tempmin.append(column[5])
  humid.append(column[6])
h.close()

#remove header
for i in [years, months, days, precip, tempmax, tempmin, humid]:
  del i[0]

# starting index of every month + the last index(len of months) -> stored as startofmonths
datalen = len(months)
startofmonths = [0]
for i in range(1, datalen):
  if months[i] != months[i-1]:
    startofmonths.append(i)

print "Total number of months is " + str(len(startofmonths)) + '.'
startofmonths.append(len(months))

# sum of precip each month
sumprecips = []
for x in range(len(startofmonths)-1):
  startindex = startofmonths[x]
  endindex = startofmonths[x + 1]
  sumprecip = 0
  for i in range(startindex, endindex):
    sumprecip += float(precip[i])
    sumprecip = round(sumprecip, 1)
  sumprecips.append(sumprecip)

# mean temp each month

# mean humidity each month
sumhumids = []
for x in range(len(startofmonths)-1):
  startindex = startofmonths[x]
  endindex = startofmonths[x + 1]
  sumhumid = 0
  for i in range(startindex, endindex):
    if humid[i] == '':
      print "no humid values at " + str(i)
      i += 1
    sumhumid += int(humid[i])
  sumhumids.append(sumhumid)
  
print sumhumids
print len(startofmonths[1:])
print len(sumhumids)

avghumids = range(len(sumhumids))
print len(avghumids)
for i in range(len(sumhumids)):
  avghumids[i] = sumhumids[i]/int(days[startofmonths[i+1]-1])
print avghumids

monthlabels = []
yearlabels = []
for i in startofmonths[:-1]:
  monthlabels.append(months[i])
  yearlabels.append(years[i])

g = open('../data/rearranged/ClimaData2.csv','wb')
csvwrite = csv.writer(g)

tobewritten = zip(yearlabels,monthlabels, sumprecips, avghumids)

for row in tobewritten:
  csvwrite.writerow(row)

g.close()

