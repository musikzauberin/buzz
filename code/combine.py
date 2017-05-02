#!/usr/bin/env python

'''Deleting duplicated files'''

__author__ = 'Jia Le Lim'
__version__ = '0.0.314159'

import csv
import operator
import decimal
import numpy as np
import matplotlib.pyplot as pl
import calendar
import sys
import os.path

# returns header, months, days, years, bees, plants
def extract_data(pathname):
  if os.path.isfile(pathname):
    print 'Valid file!'
  else:
    print 'Invalid file!'
    sys.exit()

  h = open(pathname,'rb')
  data = csv.reader(h)

  header = []
  months = []
  days = []
  years = []
  bees = []
  plants = []

  for row in data:
    months.append(row[0])
    days.append(row[1])
    years.append(row[2])
    bees.append(row[3])
    plants.append(row[4])
  
  h.close()

  header.append(months.pop(0))
  header.append(days.pop(0))
  header.append(years.pop(0))
  header.append(bees.pop(0))
  header.append(plants.pop(0))
  
  return header, months, days, years, bees, plants

def CheckInt(s):
  try: 
    int(s)
    return True
  except ValueError:
    return False

def delete_duplicates(months, days, years, bees, plants, noofmonths):
  datalen = len(months)
  print datalen

  startofmonths = [0]
  for i in range(1, datalen):
    if months[i] != months[i - 1]:
      startofmonths.append(i)
  startofmonths.append(len(months))
  print len(startofmonths), startofmonths

  monthsindices = startofmonths[0::noofmonths] # pick the appropriate numbers from startofmonths to get the list of startindex and nextindex
  print monthsindices
  for m in reversed(range(len(monthsindices) - 1)): # doing it in reverse allows me to delete directly from the list without any maddening indexing issues!
    startindex = monthsindices[m]
    nextindex = monthsindices[m + 1]
    #print (startindex, nextindex)
    for i in reversed(range(startindex, nextindex)):
      for j in reversed(range(startindex, i - 1)):
        if bees[i] == bees[j] and plants[i] == plants[j]:
          # print (i, months[i], days[i], years[i], bees[i], plants[i]), \
                # 'matches with', (j, months[j], days[j], years[j], bees[j], plants[j])
          months.pop(i) # remove duplicate element
          days.pop(i)
          years.pop(i)
          bees.pop(i)
          plants.pop(i)
          break

def write_data(pathname, header):
  g = open(pathname,'wb')
  csvwrite = csv.writer(g)

  csvwrite.writerow(header)
  for i in range(len(months)):
      csvwrite.writerow([months[i], days[i], years[i], bees[i], plants[i]])

  g.close()

def calc_turnover(months, days, years, bees, plants, noofmonths):
  
  datalen = len(months)
  print datalen

  startofmonths = [0]
  for i in range(1, datalen):
    if months[i] != months[i - 1]:
      startofmonths.append(i)
  startofmonths.append(len(months))
  print len(startofmonths), startofmonths

  monthsindices = startofmonths[0::noofmonths] # pick the appropriate numbers from startofmonths to get the list of startindex and nextindex
  print monthsindices
  
  alist = [0] * (len(monthsindices) - 2)
  blist = [0] * (len(monthsindices) - 2)
  clist = [0] * (len(monthsindices) - 2)
  bints = [0] * (len(monthsindices) - 2)
  for m in range(len(monthsindices) - 2):
    startindex = monthsindices[m]
    nextindex = monthsindices[m + 1]
    nextnextindex = monthsindices[m + 2]
    #print (startindex, nextindex, nextnextindex)

    for i in range(startindex, nextindex):
      for j in range(nextindex, nextnextindex):
        if bees[i] == bees[j] and plants[i] == plants[j]:
          alist[m] += 1
          break
    blist[m] = nextindex - startindex - alist[m]
    clist[m] = nextnextindex - nextindex - alist[m]
    # calculate turnover rate
    bints[m] = round((alist[m] + blist[m] + clist[m]) / ((2*alist[m] + blist[m] + clist[m])/2.0) - 1.0, 4)

  print "Turnover rates are: " + str(bints)
  print "Total number of comparisons made: "+ str(len(bints))
  return bints
  
############# START HERE #############
          
# type in file to remove duplicates
print "Data file must have the following columns in the order: Month Day Year Bee Plant"
#filename = raw_input('Enter your data file name in rearranged folder: ')
filename = 'OldCerradoData.csv'
pathname = os.path.join("../data/rearranged/", filename)


header, months, days, years, bees, plants = extract_data(pathname)

while True:
  noofmonths = raw_input('What is the interval of months? Type an integer pls.')
  if CheckInt(noofmonths):
    noofmonths = int(noofmonths)
    break
  else:
    print 'I asked for an integer! Last chance!'

delete_duplicates(months, days, years, bees, plants, noofmonths)

filename2 = filename.strip(".csv") + str(noofmonths) + "-monthly (jg).csv"
#pathname2 = os.path.join("../data/rearranged/", filename2)
pathname2 = filename2
write_data(pathname2, header)
print 'Find edited data file in rearranged folder! \nFile saved as ' + filename2
print 'Done!'

bints = calc_turnover(months, days, years, bees, plants, noofmonths)
print bints