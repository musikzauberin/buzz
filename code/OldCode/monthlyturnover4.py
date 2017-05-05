#!/usr/bin/env python


"""Calculating monthly turnover in Cerrado"""

__author__ = 'Jia Le Lim'
__version__ = '0.0.4'

import csv
import operator
import decimal
import numpy as np
import matplotlib.pyplot as pl
import calendar

months = []
days = []
years = []
bees = []
plants = []

# Read a file containing:
# '' System  Season  Month  Day  Year  Bee  Plant  Visits  Precip  Tmax  Tmin  Humid

f = open('../data/CerradoBoaVentura/rearranged/ClimNetDataLnx.csv','rb')
g = open('../data/CerradoBoaVentura/rearranged/ReqData.csv','wb')

csvread = csv.reader(f)
csvwrite = csv.writer(g)

for row in csvread:
  csvwrite.writerow(row[3:8])

f.close()
g.close()


# do a rearranging data script at the top

h = open('../data/CerradoBoaVentura/rearranged/ReqData.csv','rb')
data = csv.reader(h)

for column in data:
  months.append(column[0])
  days.append(column[1])
  years.append(column[2])
  bees.append(column[3])
  plants.append(column[4])

months = months[1:]
days = days[1:]
years = years[1:]
bees = bees[1:]
plants = plants[1:]

datalen = len(months)

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


# for every loop, startindex is where month 1 starts, nextindex is where month 2 starts, thereafter compare month 1 and month 2
# calculate a, similarity bet two consecutive months, and b & c, unique pairs in each month.

alist = []
blist = []
clist = []
bints = []

for x in range(len(startofmonths)-2):
  startindex = startofmonths[x]
  nextindex = startofmonths[x + 1]
  nextnextindex = startofmonths[x + 2]
  a = 0
  b = 0
  c = 0

  for i in range(startindex, nextindex):
    e = nextindex
    
    while e < nextnextindex:
      if bees[i] == bees[e]:
        if plants[i] == plants[e]:
          a += 1
          break # breaks the while loop
        else:
          e += 1
      else:
        e += 1
  b = nextindex - startindex - a
  c = nextnextindex - nextindex - a
  alist.append(a)
  blist.append(b)
  clist.append(c)

print alist
print blist
print clist
print len(startofmonths) - 1
print len(alist)
print len(alist) == len(blist) == len(clist)

# calculate turnover rate
for i in range(len(alist)):
  bint = (alist[i] + blist[i] + clist[i]) / ((2*alist[i] + blist[i] + clist[i])/2.0) - 1.0
  bint = round(bint, 4)
  bints.append(bint)

print bints
print len(bints)

xlabel = []
xlabels = []

for i in startofmonths[1:-1]:
  xlabel = calendar.month_abbr[int(months[i])] + ' ' + str(years[i])
  xlabels.append(xlabel)

print xlabels
print len(xlabels) == len(bints)

pl.plot(bints, 'bo', bints, 'k')

pl.xticks( range(len(xlabels)), xlabels, rotation = 'vertical')
pl.margins(0.2)
pl.subplots_adjust(bottom=0.15)

pl.title(' monthly turnover rate Cerrado')

pl.savefig('../results/monthlyCerrado.pdf')
# pl.plot(x, y, options)
# ro : scatterplots

# plot(x1, y1, r)

# pl.xlabel(' ')
# pl.ylabel(' ')
#


# pl.xlim('')
# pl.ylim('')

# python unique elements