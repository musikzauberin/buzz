#!/usr/bin/env python

"""Calculating monthly turnover in Cerrado"""

__author__ = 'Jia Le Lim'
__version__ = '0.0.9'

import csv
import operator
import decimal
import numpy as np
import matplotlib.pyplot as pl
import calendar
import sys
import os.path

def CheckInt(s):
  try: 
    int(s)
    return True
  except ValueError:
    return False

# type in file to be analysed
print "Data file must have the following columns in the order: Month Day Year Bee Plant"
filename = raw_input('Enter your data file name in rearranged folder: ')
pathname = os.path.join("../data/rearranged/", filename)

if os.path.isfile(pathname):
  print 'Valid file!'
else:
  print 'Invalid file!'
  sys.exit()

months = []
days = []
years = []
bees = []
plants = []

# Read a file containing:
# Month  Day  Year  Bee  Plant

h = open(pathname,'rb')
data = csv.reader(h)

for column in data:
  months.append(column[0])
  days.append(column[1])
  years.append(column[2])
  bees.append(column[3])
  plants.append(column[4])

h.close()

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
print "Total number of months is " + str(len(startofmonths)) + '.'
startofmonths.append(len(months))

# starting index of every year + the last index(len of years) -> stored as startofyears
startofyears = [0]
for i in range(1, datalen):
  if years[i] != years[i-1]:
    startofyears.append(i)
print "Total number of years is " + str(len(startofyears)) + '.'
startofyears.append(len(years))

#ask for interval of months
noofmonths = raw_input('What is the interval of months? Type an integer pls.')
while not CheckInt(noofmonths):
  print 'I asked for an integer! Last chance!'
  noofmonths = raw_input('What is the interval of months? Type an integer pls.')
noofmonths = int(noofmonths)

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
          duplicates.append(e)
          e += 1
        else:
          e += 1
      else:
        e += 1
       
tobedeleted = []
for y in duplicates:
  if y not in tobedeleted:
    tobedeleted.append(y)
tobedeleted = [x+1 for x in tobedeleted]

# write new file with deleted duplicates
f = open(pathname,'rb')
filename2 = filename.strip(".csv") + str(noofmonths) + "-monthly.csv"
pathname2 = os.path.join("../data/rearranged/", filename2)
g = open(pathname2,'wb')
csvread = csv.reader(f)
csvwrite = csv.writer(g)

rows = [row for row in csvread]
for i in range(len(rows)):
  if i not in tobedeleted:
    csvwrite.writerow(rows[i])

f.close()
g.close()

t = open(pathname2,'rb')
data = csv.reader(t)

print pathname2

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

rangeofmonths = range(0, len(startofmonths) - noofmonths, noofmonths)

noofinteractions = []
for i in range(len(startofmonths)-1):
  noofinteraction = startofmonths[i+1]-startofmonths[i]
  noofinteractions.append(noofinteraction)

print "Number of interactions in each month: " + str(noofinteractions)

# check for duplicates again

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
          duplicates.append(e)
          print str(i) + ' matches with ' + str(e) + ' really?'
          e += 1
        else:
          e += 1
      else:
        e += 1
if duplicateno == 0:
  print "No duplicates found in new file: " + filename2
else:
  print "BEDO BEDO! DUPLICATES FOUND!"

alist = []
blist = []
clist = []

rangeofmonths = range(0, len(startofmonths) - noofmonths, noofmonths)

# for every loop, startindex is where month 1 starts, nextindex is where month 2 starts, thereafter compare month 1 and month 2
# calculate a, similarity bet two consecutive months, and b & c, unique pairs in each month.

for x in rangeofmonths:
  startindex = startofmonths[x]
  nextindex = startofmonths[x + noofmonths]
  lastindex = x + noofmonths*2
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

if CheckInt(months[0]):
  if noofmonths == 1:
    for i in startofmonths[1:-1]:
      xlabel = calendar.month_abbr[int(months[i])] + ' ' + str(years[i][2:4])
      xlabels.append(xlabel)
  else:
    for i in rangeofmonths[1:]:
      firstmonth = startofmonths[i]
      lastmonthindex = i + noofmonths -1
      if lastmonthindex >= len(startofmonths):
        break
      else:
        lastmonth = startofmonths[lastmonthindex]
      xlabel = calendar.month_abbr[int(months[firstmonth])] + ' ' + years[firstmonth][2:4] + \
      ' - ' + calendar.month_abbr[int(months[lastmonth])] + ' ' + years[lastmonth][2:4]
      xlabels.append(xlabel)
elif len(months[0]) == 3:
  if noofmonths == 1:
    for i in startofmonths[1:-1]:
      xlabel = str(months[i]) + ' ' + str(years[i][2:4])
      xlabels.append(xlabel)
  else:
    for i in rangeofmonths[1:]:
      firstmonth = startofmonths[i]
      lastmonthindex = i + noofmonths -1
      if lastmonthindex >= len(startofmonths):
        break
      else:
        lastmonth = startofmonths[lastmonthindex]
      xlabel = str(months[firstmonth]) + ' ' + years[firstmonth][2:4] + \
      ' - ' + str(months[lastmonth]) + ' ' + years[lastmonth][2:4]
      xlabels.append(xlabel)
else:
  print 'The dumb computer does not understand the month column in dataset.'

if len(xlabels) == len(bints):
  print 'Correct number of x axis labels found.'
else:
  print 'ERROR! Incorrect number of x axis labels!'
  print 'Incorrect xlabels are: ' + str(xlabels)

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
