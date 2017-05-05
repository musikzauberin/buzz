#!/usr/bin/env python


"""Calculating weekly turnover in Cerrado"""

__author__ = 'Jia Le Lim'
__version__ = '0.0.2'

import csv
import numpy
import operator

months = []
days = []
years = []
bees = []
plants = []
startofmonths = [0]
alist = []
blist = []
clist = []

# Read a file containing:
# '' System	Season	Month	Day	Year	Bee	Plant	Visits	Precip	Tmax	Tmin	Humid

# f = open('../data/CerradoBoaVentura/rearranged/ClimNetDataLnx.csv','rb')
# g = open('../data/CerradoBoaVentura/rearranged/ReqData.csv','wb')
# csvread = csv.reader(f)
# csvwrite = csv.writer(g)
#
# for row in csvread:
#   csvwrite.writerow(row[3:8])
#
# f.close()
# g.close()

h = open('../data/trial1.csv','rU')
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

for i in range(1, datalen):
  if months[i] == months[i-1]:
    i += 1
  else:
    startofmonths.append(i)
    i += 1
startofmonths.append(len(months))
print 'startofmonths' + str(startofmonths)

for x in range(len(startofmonths)-2):
  startindex = startofmonths[x]
  nextindex = startofmonths[x + 1]
  nextnextindex = startofmonths[x + 2]
  a = 0
  b = 0
  c = 0
  e = nextindex
  print 'indexes ' + str(startindex) + ' ' + str(nextindex) + ' ' + str(nextnextindex)
  
  for i in range(startindex, nextindex):
    e = nextindex
    print 'start ' + str(i) + ' ' + str(e)
    
    while e < nextnextindex:
      print 'middle ' + str(i) + ' ' + str(e)
      if bees[i] == bees[e]:
        if plants[i] == plants[e]:
          a += 1
          break
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





