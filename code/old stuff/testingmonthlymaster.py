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
# Month  Day  Year  Bee  Plant

h = open('../data/rearranged/CerradoData.csv','rb')
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

# starting index of every month + the last index(len of months) -> stored as startofmonths
startofmonths = [0]

for i in range(1, datalen):
  if months[i] != months[i-1]:
    startofmonths.append(i)
startofmonths.append(len(months))

# for every loop, startindex is where month 1 starts, nextindex is where month 2 starts, thereafter compare month 1 and month 2
# calculate a, similarity bet two consecutive months, and b & c, unique pairs in each month.

alist = []
blist = []
clist = []

noofmonths = 6

rangeofmonths = range(0, len(startofmonths) - noofmonths, noofmonths)

for x in rangeofmonths:
  startindex = startofmonths[x]
  nextindex = startofmonths[x + noofmonths]
  lastindex = x + noofmonths*2
  print lastindex
  print len(startofmonths)
  if lastindex >= len(startofmonths):
    break
  else:
    nextnextindex = startofmonths[x + noofmonths*2]
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
print "Total number of months is " + str(len(startofmonths) - 1) + '.'
print len(alist)
print len(alist) == len(blist) == len(clist)

bints = []

# calculate turnover rate
for i in range(len(alist)):
  bint = (alist[i] + blist[i] + clist[i]) / ((2*alist[i] + blist[i] + clist[i])/2.0) - 1.0
  bint = round(bint, 4)
  bints.append(bint)

print "Turnover rates are: " + str(bints)
print "Total number of comparisons made: "+ str(len(bints))

xlabel = []
xlabels = []

print rangeofmonths

for i in rangeofmonths[1:]:
  firstmonth = startofmonths[i]
  lastmonthindex = i + noofmonths -1
  print lastmonthindex
  if lastmonthindex >= len(startofmonths):
    print "ohnoes"
    break
  else:
    lastmonth = startofmonths[lastmonthindex]
    
  xlabel = calendar.month_abbr[int(months[firstmonth])] + ' ' + years[firstmonth][2:4] + \
  ' - ' + calendar.month_abbr[int(months[lastmonth])] + ' ' + years[lastmonth][2:4]
  xlabels.append(xlabel)

print xlabels
print len(xlabels) == len(bints)

pl.plot(bints, 'bo', bints, 'k')

if noofmonths == 1:
  pl.xticks( range(len(xlabels)), xlabels, rotation = '50', ha = 'right')
else:
  pl.xticks( range(len(xlabels)), xlabels, rotation = '30', ha = 'right')
pl.margins(0.2)
pl.subplots_adjust(bottom=0.30)

if noofmonths == 1:
  plottitle = "Monthly turnover rate in Cerrado" 
else:
  plottitle = str(noofmonths) + "-monthly turnover rate in Cerrado" 

pl.title(plottitle)

plotname = plottitle.title().strip().replace(" ", "")

plotpath = '../results/' + plotname + '.pdf'

pl.savefig(plotpath)

print 'Find figures in results folder! \nFigure saved as ' + plotname + '.pdf'
print 'Done!'

##########################
timeinterval = raw_input('Turnover rates in months or years?')
timeinterval = timeinterval.lower()

while timeinterval != 'months' and timeinterval != 'years':
  timeinterval = raw_input('Turnover rates in MONTHS or YEARS? If you want something else do the script yourself.')
  timeinterval = timeinterval.lower()
##########################
while True:
  timeinterval = raw_input('Turnover rates in MONTHS or YEARS? If you want something else do the script yourself.')
  timeinterval = timeinterval.lower()
  if timeinterval == 'months' or timeinterval == 'years':
    break
  else:
    print 'Eh what the heck last warning ah!'
##########################
while True:
  timeinterval = raw_input('Turnover rates in MONTHS or YEARS? If you want something else do the script yourself.')
  timeinterval = timeinterval.lower()
  if timeinterval == 'months' or timeinterval == 'years':
    break
##########################
