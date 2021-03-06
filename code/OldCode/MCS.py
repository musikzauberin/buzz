'''Monte Carlo within months'''
import random
import csv
import operator
import decimal
import numpy as np
import scipy
import matplotlib.pyplot as pl
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import calendar
import sys
import os.path
import brewer2mpl
import matplotlib.cm as cm
from scipy import stats


filename = 'OldCerradoData1-monthly(New).csv'
pathname = '../data/rearranged/new/' + filename
h = open(pathname,'rb')
data = csv.reader(h)


########## Inputting data into lists ##########

# copy and paste all headers in data three times
headers = 'months, days, years, bees, plants'

[months, days, years, bees, plants] = ([] for i in range(len(next(data))))

headers2 = [months, days, years, bees, plants]

for column in data:
  for j, i in enumerate(headers2):
    i.append(column[j])

h.close()


############# Calculate turnovers #############

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

def monthlyunique(startofmonths2, noofmonths, bees, plants):
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
  return monthlybees, monthlyplants

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

  return bints


def calc_singlespecturnover(monthlyplants):
  # bee and plant turnover, create commonlist: bees common in first two months in 0 index...
  aplantlist = [0] * (len(monthlyplants) - 1)
  bplantlist = [0] * (len(monthlyplants) - 1)
  cplantlist = [0] * (len(monthlyplants) - 1)
  plantturnovers = [0] * (len(monthlyplants) - 1)
  commonplants = []

  for i in range(len(monthlyplants) - 1):
    commonplant = []
  
    for plant in monthlyplants[i]:
      if plant in monthlyplants[i+1]:
        aplantlist[i] += 1
        commonplant.append(plant)
    bplantlist[i] = len(monthlyplants[i]) - aplantlist[i]
    cplantlist[i] = len(monthlyplants[i+1]) - aplantlist[i]
    plantturnovers[i] = round((aplantlist[i] + bplantlist[i] + cplantlist[i]) / ((2*aplantlist[i] + bplantlist[i] + cplantlist[i])/2.0) - 1.0, 5)
    commonplants.append(commonplant)
  return commonplants, plantturnovers, aplantlist, bplantlist, cplantlist

def calc_specturnover(startofmonths2, aplantlist, bplantlist, cplantlist, abeelist, bbeelist, cbeelist):
  # species turnover
  alist = [0] * (len(startofmonths2) - 1)
  blist = [0] * (len(startofmonths2) - 1)
  clist = [0] * (len(startofmonths2) - 1)
  specturnovers = [0] * (len(startofmonths2) - 2)
  for i in range(len(monthlyplants) - 1):
    alist[i] = aplantlist[i] + abeelist[i]
    blist[i] = bplantlist[i] + bbeelist[i]
    clist[i] = cplantlist[i] + cbeelist[i]
    specturnovers[i] = round((alist[i] + blist[i] + clist[i]) / ((2*alist[i] + blist[i] + clist[i])/2.0) - 1.0, 5)
  return specturnovers

def calc_osstturnover(startofmonths2, noofmonths, bees, commonbees, plants, commonplants):
  monthsindices = startofmonths2[0::noofmonths] # pick the appropriate numbers from startofmonths to get the list of startindex and nextindex
  # Bos 
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
  # Bst
  stturnovers = [0] * (len(monthsindices) - 2)
  for m in range(len(monthsindices) - 2):
    stturnovers[m] = round(bints[m] - osturnovers[m], 5)
  return osturnovers, stturnovers

def gen_perm_dict(elems):
  elems_unique = list(set(elems))
  elems_perm = elems_unique[:]
  random.shuffle(elems_perm)
  return dict(zip(elems_unique, elems_perm))

# bees = replaced_bees
# plants = replaced_plants
noofmonths = 1
startofmonths = findstartindex(months, 'months')

allrs = []
for i in range(10000):
  replaced_bees = [0]* len(bees)
  for i in range(len(startofmonths)-1):
    startindex = startofmonths[i]
    endindex = startofmonths[i+1]
    beedict = gen_perm_dict(bees[startindex:endindex])
    replaced_bees[startindex:endindex] = map(lambda bee: beedict[bee], bees[startindex:endindex])

  replaced_plants = [0]* len(plants)
  for i in range(len(startofmonths)-1):
    startindex = startofmonths[i]
    endindex = startofmonths[i+1]
    plantdict = gen_perm_dict(plants[startindex:endindex])
    replaced_plants[startindex:endindex] = map(lambda plant: plantdict[plant], plants[startindex:endindex])

  bints = calc_turnover(months, days, years, replaced_bees, replaced_plants, noofmonths, startofmonths)

  [monthlybees, monthlyplants] = monthlyunique(startofmonths, noofmonths, replaced_bees, replaced_plants)
  [commonplants, plantturnovers, aplantlist, bplantlist, cplantlist] = calc_singlespecturnover(monthlyplants)
  [commonbees, beeturnovers, abeelist, bbeelist, cbeelist] = calc_singlespecturnover(monthlybees)

  specturnovers = calc_specturnover(startofmonths, aplantlist, bplantlist, cplantlist, abeelist, bbeelist, cbeelist)
  [osturnovers, stturnovers] = calc_osstturnover(startofmonths, noofmonths, replaced_bees, commonbees, replaced_plants, commonplants)

  # Bint with Bst
  r0, p0 = stats.spearmanr(bints, stturnovers)

  # Bint with Bos
  r1, p1 = stats.spearmanr(bints, osturnovers)

  # BInt with Bs
  r2, p2 = stats.spearmanr(bints, specturnovers)

  # BInt with Bbee
  r3, p3 = stats.spearmanr(bints, beeturnovers)

  # BInt with Bplant
  r4, p4 = stats.spearmanr(bints, plantturnovers)
  
  # Bos with Bst
  r5, p5 = stats.spearmanr(osturnovers, stturnovers)

  # bst with Bs
  r6, p6 = stats.spearmanr(stturnovers, specturnovers)
  
  # bst with Bbee
  r7, p7 = stats.spearmanr(stturnovers, beeturnovers)
  
  # bst with Bplant
  r8, p8 = stats.spearmanr(stturnovers, plantturnovers)

  # Bs with Bos
  r9, p9 = stats.spearmanr(specturnovers, osturnovers)

  # Bs with Bbee
  r10, p10 = stats.spearmanr(specturnovers, beeturnovers)

  # Bs with Bplant
  r11, p11 = stats.spearmanr(specturnovers, plantturnovers)
  
  # Bbee with Bplant
  r12, p12 = stats.spearmanr(beeturnovers, plantturnovers)
  
  allrs.append([r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12])

print len(allrs)

# print allrs[-1][0]
#
# print allrs[-1]


def makeHist(allrs, x, valuetitle_str, plotname_str, color_str):
  values = []
  for i in range(len(allrs)):
    values.append(allrs[i][x])
  histvalues = np.array(values).astype(np.float)
  plottitle = valuetitle_str 
  pl.title(plottitle, size = 18)
  pl.hist(histvalues, histtype='step', normed = 1, color = color_str)
  # color = 'crimson', 'blue'
  plotpath = '../results/' + plotname_str + years[startindex] + ',' + months[startindex] + '.pdf'
  pl.savefig(plotpath) 
  pl.show()

makeHist(allrs, 3, 'Bint with Bst', 'testing', 'blue')



# ########## Writing Turnover Data into new file ##########
#
# def writenewdata(filename_str, headers, values):
#   'inputting new data into csv file'
#   headers = headers.split(', ')
#   pathname = '../data/rearranged/new/' + filename_str + '.csv'
#   g = open(pathname, 'wb')
#
#   csvwrite = csv.writer(g)
#   csvwrite.writerow(headers)
#   tobewritten = zip(*values)
#   for row in tobewritten:
#     csvwrite.writerow(row)
#   g.close()
#
# def timelabels(timeinterval, startofmonths):
#   'creating new timeinterval list that corresponds to new data'
#   timelabels = []
#   for i in startofmonths[:-1]:
#     timelabels.append(timeinterval[i])
#   return timelabels
#
# yearlabels = timelabels(years, startofmonths)
# monthlabels = timelabels(months, startofmonths)
#
# newheaders2 = 'Year, Month, InteractionTurnover, BeeTurnover, PlantTurnover, SpeciesTurnover, B_os, B_st'
# newvalues2 = [yearlabels, monthlabels, bints, beeturnovers, plantturnovers, specturnovers, osturnovers, stturnovers]
#
# filename3 = 'RandomTurnoverOldCerrado'
# writenewdata(filename3, newheaders2, newvalues2)
# print 'Find edited data file in rearranged/new folder! \nFile saved as ' + filename3 + '.csv'
# print 'Done!'

