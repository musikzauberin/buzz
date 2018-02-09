#!/usr/bin/env python

'''Deleting duplicated files & calculating turnover'''

__author__ = 'Jia Le Lim'
__version__ = '0.0.4'

import csv
import operator
import decimal
import numpy as np
import matplotlib.pyplot as pl
import calendar
import sys
import os.path
import itertools

# Data should have the following columns: months, days, years, bees, plants
# otherwise edit extract_data function.

def extract_data(pathname):
  'Extract data into corresponding columns + headers'
  if os.path.isfile(pathname):
    print 'Valid file!'
  else:
    print 'Invalid file!'
    sys.exit()

  h = open(pathname,'rb')
  data1, data2 = itertools.tee(csv.reader(h))
  # check that data columns are correct
  [header, months, days, years, bees, plants] = ([] for i in range(len(next(data1)) + 1))
  datacolumns = [months, days, years, bees, plants]
  
  for column in data2:
    for j, i in enumerate(datacolumns):
      i.append(column[j])
  h.close()
  
  for i in datacolumns:
    header.append(i.pop(0))

  return header, months, days, years, bees, plants

def CheckInt(s):
  'Check if s is an integer'
  try: 
    int(s)
    return True
  except ValueError:
    return False

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

def delete_duplicates(months, days, years, bees, plants, noofmonths, startofmonths):
  'deletes duplicates within noofmonths intervals'
  monthsindices = startofmonths[0::noofmonths] # pick the appropriate numbers from startofmonths to get the list of startindex and nextindex
  print monthsindices
  for m in reversed(range(len(monthsindices) - 1)): # doing it in reverse allows me to delete directly from the list without any maddening indexing issues!
    startindex = monthsindices[m]
    nextindex = monthsindices[m + 1]
    # nextindex is bigger than startindex
    for i in reversed(range(startindex, nextindex)):
      for j in reversed(range(startindex, i)):
        if bees[i] == bees[j] and plants[i] == plants[j]:
          print (i, months[i], days[i], years[i], bees[i], plants[i]), \
                'matches with', (j, months[j], days[j], years[j], bees[j], plants[j])
          months.pop(i) # remove duplicate element
          days.pop(i)
          years.pop(i)
          bees.pop(i)
          plants.pop(i)
          print bees
          break

def writenewdata(filename_str, headers, values):
  'inputting new data into csv file'
  headers = headers.split(', ')

  pathname = '../data/rearranged/new/' + filename_str + '.csv'
  g = open(pathname, 'wb')

  csvwrite = csv.writer(g)
  csvwrite.writerow(headers)
  tobewritten = zip(*values)
  for row in tobewritten:
    csvwrite.writerow(row)
  g.close()

def calc_turnover(months, days, years, bees, plants, noofmonths, startofmonths):
  monthsindices = startofmonths[0::noofmonths] # pick the appropriate numbers from startofmonths to get the list of startindex and nextindex
  
  alist = [0] * (len(monthsindices) - 2)
  blist = [0] * (len(monthsindices) - 2)
  clist = [0] * (len(monthsindices) - 2)
  bints = [0] * (len(monthsindices) - 2)
  for m in range(len(monthsindices) - 2):
    startindex = monthsindices[m]
    nextindex = monthsindices[m + 1]
    nextnextindex = monthsindices[m + 2]
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
filename = 'CorrectedNewCerradoData.csv'
pathname = os.path.join("../data/rearranged/", filename)
header, months, days, years, bees, plants = extract_data(pathname)
print "Column headers: " + str(header)

startofmonths = findstartindex(months, 'months')

while True:
  noofmonths = raw_input('What is the interval of months? Type an integer pls.')
  if CheckInt(noofmonths):
    noofmonths = int(noofmonths)
    break
  else:
    print 'I asked for an integer! Last chance!'

delete_duplicates(months, days, years, bees, plants, noofmonths, startofmonths)

# write new file for data without duplicates
newheaders = 'Month, Day, Year, Bee, Plant'
newvalues = [months, days, years, bees, plants]
filename2 = filename.strip(".csv") + str(noofmonths) + "-monthly(New)"
writenewdata(filename2, newheaders, newvalues)
print 'Find edited data file in rearranged/new folder! \nFile saved as ' + filename2 + '.csv'
print 'Done!'

startofmonths2 = findstartindex(months, 'months')
bints = calc_turnover(months, days, years, bees, plants, noofmonths, startofmonths2)


########## Writing Turnover Data into new file ##########

def timelabels(timeinterval, startofmonths):
  'creating new timeinterval list that corresponds to new data'
  timelabels = []
  for i in startofmonths[:-1]:
    timelabels.append(timeinterval[i])
  return timelabels

yearlabels = timelabels(years, startofmonths2)
monthlabels = timelabels(months, startofmonths2)

newheaders2 = 'Year, Month, InteractionTurnover'
newvalues2 = [yearlabels, monthlabels, bints]

filename3 = 'TurnoverNewCerrado'
writenewdata(filename3, newheaders2, newvalues2)
print 'Find edited data file in rearranged/new folder! \nFile saved as ' + filename3 + '.csv'
print 'Done!'