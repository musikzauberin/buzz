#!/usr/bin/env python

'''Correct the NewCerrado Dataset swap the days around '''

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
import itertools

def extract_data(pathname):
  'Extract data into corresponding columns + headers'
  # Data should have the following columns: months, days, years, bees, plants
  if os.path.isfile(pathname):
    print 'Valid file!'
  else:
    print 'Invalid file!'
    sys.exit()

  h = open(pathname,'rb')
  data = csv.reader(h)
  [months, days, years, bees, plants] = ([] for i in range(len(next(data))))
  headers = [months, days, years, bees, plants]
  for column in data:
    for j, i in enumerate(headers):
      i.append(column[j])
  h.close()

  return months, days, years, bees, plants

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
    
############# INPUT DATA AND MANIPULATE#############

# type in file to remove duplicates
print "Data file must have the following columns in the order: Month Day Year Bee Plant"
#filename = raw_input('Enter your data file name in rearranged folder: ')
filename = 'CorrectedNewCerradoData2.csv'
pathname = os.path.join("../data/rearranged/", filename)
months, days, years, bees, plants = extract_data(pathname)

startofdays = [0]
datalen = len(days)
for i in range(1, datalen):
  if days[i] != days[i-1]:
    startofdays.append(i)
print 'Total number of days is ' + str(len(startofdays)) + '.'
startofdays.append(len(days))

### OUTPUT
def writenewdata(filename_str, headers, values):
  'inputting new data into csv file'
  headers = headers.split(', ')
  pathname = '../data/rearranged/' + filename_str + '.csv'
  g = open(pathname, 'wb')

  csvwrite = csv.writer(g)
  csvwrite.writerow(headers)
  tobewritten = zip(*values)
  for row in tobewritten:
    csvwrite.writerow(row)
  g.close()

print startofdays
days2 = [0] * (len(days))
for i in range(len(startofdays)-1):
    for x in range(startofdays[i],startofdays[i+1]):
        days2[x] = i + 1

newheaders2 = 'Month, Collection Day, Year, Bee Nr, Plant Nr'
newvalues2 = [months, days2, years, bees, plants]

filename3 = 'test1'
writenewdata(filename3, newheaders2, newvalues2)
print 'Find edited data file in rearranged/new folder! \nFile saved as ' + filename3 + '.csv'
print 'Done!'
