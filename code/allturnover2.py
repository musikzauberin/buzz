#!/usr/bin/env python

'''Deleting duplicated files & calculating turnover'''

__author__ = 'Jia Le Lim'
__version__ = '0.0.5'

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

def extract_data2(pathname):
  'Extract data into corresponding columns + headers'
  # Data should have the following columns: cyears, cmonths, sumprecips, medtemps, medmaxtemps, medtempranges, medhumids
  if os.path.isfile(pathname):
    print 'Valid file!'
  else:
    print 'Invalid file!'
    sys.exit()

  h = open(pathname,'rb')
  data = csv.reader(h)
  [cyears, cmonths, sumprecips, medtemps, medmaxtemps, medtempranges, medhumids] = ([] for i in range(len(next(data))))
  headers = [cyears, cmonths, sumprecips, medtemps, medmaxtemps, medtempranges, medhumids]
  for column in data:
    for j, i in enumerate(headers):
      i.append(column[j])
  h.close()

  return cyears, cmonths, sumprecips, medtemps, medmaxtemps, medtempranges, medhumids

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
  for m in reversed(range(len(monthsindices) - 1)): # doing it in reverse allows me to delete directly from the list without any maddening indexing issues!
    startindex = monthsindices[m]
    nextindex = monthsindices[m + 1]
    # nextindex is bigger than startindex
    for i in reversed(range(startindex, nextindex)):
      for j in reversed(range(startindex, i)):
        if bees[i] == bees[j] and plants[i] == plants[j]:
          months.pop(i) # remove duplicate element
          days.pop(i)
          years.pop(i)
          bees.pop(i)
          plants.pop(i)
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
    bints[m] = round((alist[m] + blist[m] + clist[m]) / ((2*alist[m] + blist[m] + clist[m])/2.0) - 1.0, 5)

  print "Turnover rates are: " + str(bints)
  print "Total number of comparisons made: "+ str(len(bints))
  return bints


############# INPUT DATA AND REMOVE DUPLICATES #############

# type in file to remove duplicates
print "Data file must have the following columns in the order: Month Day Year Bee Plant"
#filename = raw_input('Enter your data file name in rearranged folder: ')
filename = 'NewCerradoData.csv'
pathname = os.path.join("../data/rearranged/", filename)
months, days, years, bees, plants = extract_data(pathname)

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


############# Calculate turnovers #############

startofmonths2 = findstartindex(months, 'months')
bints = calc_turnover(months, days, years, bees, plants, noofmonths, startofmonths2)

# create list of unique plants and bees in each month
monthlyplants = []
monthlybees = []
monthsindices = startofmonths2[0::noofmonths] # pick the appropriate numbers from startofmonths to get the list of startindex and nextindex
for m in range(len(monthsindices) - 1): 
  startindex = monthsindices[m]
  nextindex = monthsindices[m + 1]
  monthlyplant = []
  monthlybee = []
  for plant in plants[startindex:nextindex]:
    if plant not in monthlyplant:
      monthlyplant.append(plant)
  monthlyplants.append(monthlyplant)

  for bee in bees[startindex:nextindex]:
    if bee not in monthlybee:
      monthlybee.append(bee)
  monthlybees.append(monthlybee)

# bee and plant turnover, create commonlist: bees common in first two months in 0 index...
aplantlist = [0] * (len(monthlyplants) - 1)
bplantlist = [0] * (len(monthlyplants) - 1)
cplantlist = [0] * (len(monthlyplants) - 1)
plantturnovers = [0] * (len(monthlyplants) - 1)
commonplants = []

abeelist = [0] * (len(monthlyplants) - 1)
bbeelist = [0] * (len(monthlyplants) - 1)
cbeelist = [0] * (len(monthlyplants) - 1)
beeturnovers = [0] * (len(monthlyplants) - 1)
commonbees = []

for i in range(len(monthlyplants) - 1):
  commonplant = []
  commonbee = []
  
  for plant in monthlyplants[i]:
    if plant in monthlyplants[i+1]:
      aplantlist[i] += 1
      commonplant.append(plant)
  bplantlist[i] = len(monthlyplants[i]) - aplantlist[i]
  cplantlist[i] = len(monthlyplants[i+1]) - aplantlist[i]
  plantturnovers[i] = round((aplantlist[i] + bplantlist[i] + cplantlist[i]) / ((2*aplantlist[i] + bplantlist[i] + cplantlist[i])/2.0) - 1.0, 5)
  commonplants.append(commonplant)
  
  for bee in monthlybees[i]:
    if bee in monthlybees[i+1]:
      abeelist[i] += 1
      commonbee.append(bee)
  bbeelist[i] = len(monthlybees[i]) - abeelist[i]
  cbeelist[i] = len(monthlybees[i+1]) - abeelist[i]
  beeturnovers[i] = round((abeelist[i] + bbeelist[i] + cbeelist[i]) / ((2*abeelist[i] + bbeelist[i] + cbeelist[i])/2.0) - 1.0, 5)
  commonbees.append(commonbee)
  
# species turnover
alist = [0] * (len(monthlyplants) - 1)
blist = [0] * (len(monthlyplants) - 1)
clist = [0] * (len(monthlyplants) - 1)
specturnovers = [0] * (len(monthlyplants) - 1)
for i in range(len(monthlyplants) - 1):
  alist[i] = aplantlist[i] + abeelist[i]
  blist[i] = bplantlist[i] + bbeelist[i]
  clist[i] = cplantlist[i] + cbeelist[i]
  specturnovers[i] = round((alist[i] + blist[i] + clist[i]) / ((2*alist[i] + blist[i] + clist[i])/2.0) - 1.0, 5)

# Bos %%%%%%%%%%%%%%%CHECKHECKHECK
alist2 = [0] * (len(monthsindices) - 2)
blist2 = [0] * (len(monthsindices) - 2)
clist2 = [0] * (len(monthsindices) - 2)
osturnovers = [0] * (len(monthsindices) - 2)

for m in range(len(monthsindices) - 2):
  startindex = monthsindices[m]
  nextindex = monthsindices[m + 1]
  nextnextindex = monthsindices[m + 2]
  for i in range(startindex, nextindex):
    if bees[i] in commonbees[m] and plants[i] in commonplants[m]:
      blist2[m] += 1
    for j in range(nextindex, nextnextindex):
      if bees[i] == bees[j] and plants[i] == plants[j]:
        alist2[m] += 1
  for h in range(nextindex, nextnextindex):
    if bees[h] in commonbees[m] and plants[h] in commonplants[m]:
      clist2[m] += 1
  blist2[m] -= alist2[m]
  clist2[m] -= alist2[m]

for m in range(len(monthsindices) - 2):
  if alist2[m] + blist2[m] + clist2[m] == 0:
    osturnovers[m] = 0
  else:
    osturnovers[m] = round((alist2[m] + blist2[m] + clist2[m]) / ((2*alist2[m] + blist2[m] + clist2[m])/2.0) - 1.0, 5)
# check osturnover values

# Bst
stturnovers = [0] * (len(monthsindices) - 2)
for m in range(len(monthsindices) - 2):
  stturnovers[m] = round(bints[m] - osturnovers[m], 5)


########### Extract climate data and Manipulate ####################

cyears, cmonths, sumprecips, medtemps, medmaxtemps, medtempranges, medhumids = extract_data2('../data/rearranged/new/NewCerradoClimaData.csv')

# average between two months
[avgprecips, avgtemps, avgmaxtemps, avgtempranges, avghumids] = ([0]*(len(sumprecips)-1) for i in range(5))
averages = [avgprecips, avgtemps, avgmaxtemps, avgtempranges, avghumids]
measures = [sumprecips, medtemps, medmaxtemps, medtempranges, medhumids]
pairs = zip(measures, averages)

for pair in pairs:
  for x in range(len(sumprecips)-1):
    pair[1][x] = round((float(pair[0][x]) + float(pair[0][x+1]))/2, 2)

# difference between two months
[diffprecips, difftemps, diffmaxtemps, difftempranges, diffhumids] = ([0]*(len(sumprecips)-1) for i in range(5))
differences = [diffprecips, difftemps, diffmaxtemps, difftempranges, diffhumids]
pairs2 = zip(measures, differences)

for pair2 in pairs2:
  for x in range(len(sumprecips)-1):
    pair2[1][x] = round(float(pair2[0][x+1]) - float(pair2[0][x]), 2)


########## Writing Turnover Data into new file ##########

def timelabels(timeinterval, startofmonths):
  'creating new timeinterval list that corresponds to new data'
  timelabels = []
  for i in startofmonths[:-1]:
    timelabels.append(timeinterval[i])
  return timelabels

yearlabels = timelabels(years, startofmonths2)
monthlabels = timelabels(months, startofmonths2)

newheaders2 = 'Year, Month, InteractionTurnover, BeeTurnover, PlantTurnover, SpeciesTurnover, B_os, B_st, \
Avgprecips, Avgtemps, Avgmaxtemps, Avgtempranges, Avghumids, \
diffprecips, difftemps, diffmaxtemps, difftempranges, diffhumids'
newvalues2 = [yearlabels, monthlabels, bints, beeturnovers, plantturnovers, specturnovers, osturnovers, stturnovers, \
avgprecips, avgtemps, avgmaxtemps, avgtempranges, avghumids, \
diffprecips, difftemps, diffmaxtemps, difftempranges, diffhumids]

filename3 = 'AllTurnoverNewCerrado'
writenewdata(filename3, newheaders2, newvalues2)
print 'Find edited data file in rearranged/new folder! \nFile saved as ' + filename3 + '.csv'
print 'Done!'