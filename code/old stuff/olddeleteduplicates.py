#!/usr/bin/env python

"""Deleting duplicated files"""

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

def CheckInt(s):
  try: 
    int(s)
    return True
  except ValueError:
    return False

months = []
days = []
years = []
bees = []
plants = []

# type in file to remove duplicates
print "Data file must have the following columns in the order: Month Day Year Bee Plant"
filename = raw_input('Enter your data file name in rearranged folder: ')
pathname = os.path.join("../data/rearranged/", filename)

if os.path.isfile(pathname):
  print 'Valid file!'
else:
  print 'Invalid file!'
  sys.exit()

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

startofmonths = [0]

for i in range(1, datalen):
  if months[i] != months[i-1]:
    startofmonths.append(i)

startofmonths.append(len(months))

#ask for interval of months
noofmonths = raw_input('What is the interval of months? Type an integer pls.')
while not CheckInt(noofmonths):
  print 'I asked for an integer! Last chance!'
  noofmonths = raw_input('What is the interval of months? Type an integer pls.')
noofmonths = int(noofmonths)

rangeofmonths = range(0, len(startofmonths) - noofmonths, noofmonths)
print rangeofmonths

duplicateno = 0
duplicates = []

for x in rangeofmonths:
  startindex = startofmonths[x]
  nextindex = startofmonths[x + noofmonths]
  if (x + noofmonths) >= len(startofmonths):
    break
  for i in range(startindex, nextindex):
    e = i + 1
    
    while e < nextindex:
      if bees[i] == bees[e]:
        if plants[i] == plants[e]:
          duplicateno += 1
          duplicates.append(e)
          print str(i) + ' matches with ' + str(e)
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

print 'Find edited data file in rearranged folder! \nFile saved as ' + filename2 + '.csv'
print 'Done!'


