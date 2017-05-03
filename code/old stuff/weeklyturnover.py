#!/usr/bin/env python


"""Calculating weekly turnover"""

__author__ = 'Jia Le Lim'
__version__ = '0.0.1'

import csv
import numpy
import operator

month = []
day = []
year = []
bee = []
plant = []
dayindex = []
startofweeks = []

# Read a file containing:
# '' System	Season	Month	Day	Year	Bee	Plant	Visits	Precip	Tmax	Tmin	Humid

f = open('../data/CerradoBoaVentura/rearranged/ClimNetDataLnx.csv','rb')
g = open('../data/CerradoBoaVentura/rearranged/ReqData.csv','wb')
csvread = csv.reader(f)
csvwrite = csv.writer(g)

for row in csvread:
  csvwrite.writerow(row[3:8])

f.close()
g.close()

h = open('../data/CerradoBoaVentura/rearranged/ReqData.csv','rb')
data = csv.reader(h)

for column in data:
  month.append(column[0])
  day.append(column[1])
  year.append(column[2])
  bee.append(column[3])
  plant.append(column[4])

month = month[1:]
day = day[1:]
year = year[1:]
bee = bee[1:]
plant = plant[1:]

# create day index -> check out conversion function and make it more exact
for i in range(len(month)):
  dayindex.append(int(month[i])*30 + int(day[i]) + int(year[i])*365)

# Calculate total number of weeks
totaldays = int(dayindex[-1]) - int(dayindex[0])
totalweeks = (totaldays)/ 7

if totaldays % 7 > 3:
  totalweeks += 1
  
print 'Total number of weeks is ' + str(totalweeks)

# Find dayindex of start of weeks
startday = int(dayindex[0])
print 'startday' + str(startday)

for i in range(len(dayindex)):
  print dayindex[i]
  while int(dayindex[i]) < (startday + 7):
    print 'True'
    i += 1
  else:
    print 'False'
    
  
# i = dayindex[0]
# print i
#
# while i < (startday + 7):
#   print 'True'
#   i += 1
# else:
#   print 'False'
#   startofweeks.append(i)
#   startday = 
  
# for i in range(totalweeks):
#   startofweeks.append(startday)
#   startday += 7
#
# print startofweeks 


# for i in range(10):
#   print dayindex[i]
#   if int(dayindex[i]) < (startday + 7):
#     print 'True'
#     print 'startday'+ str(startday)
#     i += 1
#   else:
#     startofweeks.append(dayindex[i])
#     print 'False'
#     startday += 7
#     print 'new' + str(startday)
#     i += 1


# for i in range(len(dayindex)):
#   startday = int(dayindex[0])
#   for week in listofweeks:
#     if int(dayindex[i]) < startday + 7:
#       week.append(bee[i])


# sortedlist = sorted(data, key=operator.itemgetter(2), reverse=True)
# print sortedlist

# headings = ('month', 'day', 'year', 'bee', 'plant')
#
# # Remove the headings
# for i in headings:
#   i = i[1:]





