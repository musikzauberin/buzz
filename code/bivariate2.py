#!/usr/bin/env python

'''Plot bivariate graph '''

__author__ = 'Jia Le Lim'
__version__ = '0.0.2'

import csv
import operator
import decimal
import numpy as np
import matplotlib.pyplot as pl
import matplotlib.lines as mlines
import calendar
import sys
import os.path

h1 = open('../data/rearranged/new/OldCerradoClimaData.csv','rb')
data1 = csv.reader(h1)


########## Inputting data into lists ##########

# copy and paste all headers in data twice
[cyears, cmonths, sumprecips, avghumids, maxtemps, avgtemps, tempranges, tempmedians] = ([] for i in range(len(next(data1))))
headers1 = [cyears, cmonths, sumprecips, avghumids, maxtemps, avgtemps, tempranges, tempmedians]

for column in data1:
  for j, i in enumerate(headers1):
    i.append(column[j])
h1.close()


########## Separating into dry and wet seasons ##########

drymonths = ['4', '5', '6', '7', '8', '9' ]
wetmonths = ['10', '11', '12', '1', '2', '3' ]

sumprecips, avghumids, maxtemps, avgtemps, tempranges, tempmedians


# avghumids vs sumprecips
dryavghumids = []
wetavghumids = []
drysumprecips = []
wetsumprecips = []

def separateintoseasons(months, values, dryvalues, wetvalues, drymonths, wetmonths):
  for i in range(len(values)):
    if months[i] in drymonths:
      dryvalues.append(values[i])
    if months[i] in wetmonths:
      wetvalues.append(values[i])
  return dryvalues, wetvalues



[dryavghumids, wetavghumids] = separateintoseasons(cmonths, avghumids, dryavghumids, wetavghumids, drymonths, wetmonths)




# turnoverset = [bints1, beeturnovers, plantturnovers, specturnovers, osturnovers, stturnovers]
# climateset = [sumprecips, avghumids, maxtemps, avgtemps, tempranges, tempmedians]
#
# turnoversetlabel = [['Interaction Turnover'], ['beeturnovers'], ['plantturnovers'], ['species turnovers'], ['osturnovers'], ['stturnovers']]
# climatesetlabel = [['sumprecips'], ['avghumids'], ['maxtemps'], ['avgtemps'], ['tempranges'], ['tempmedians']]
#
# turnoverlist = [list(a) for a in zip(turnoverset, turnoversetlabel)]
# climatelist = [list(a) for a in zip(climateset, climatesetlabel)]
#
# remainderset1 = [bints1, osturnovers, stturnovers, specturnovers]
# remainderset2 = [osturnovers, stturnovers, beeturnovers, plantturnovers, specturnovers]

# for i in range(len(turnoverlist)):
#   for c in range(len(climatelist)):
#     print climatelist[c][1], turnoverlist[i][1]
#     pl.plot(climatelist[c][0], turnoverlist[i][0], 'bo')
#     pl.grid(True)
#     pl.title('Climate data in Cerrado (1995-1997)', size = 18)
#     pl.xlabel(climatelist[c][1], size=16)
#     pl.ylabel(turnoverlist[i][1], size=16)
#     plotpath = '../results/' + str(climatelist[c][1]) + '-' + str(turnoverlist[i][1]) + '.pdf'
#     pl.savefig(plotpath)
#     pl.close()
#
#
pl.plot(avghumids, sumprecips, 'bo')
pl.xlabel('Average Humidity per Month / %', size=16)
pl.ylabel('Monthly Precipitation Sum / mm', size=16)
plotpath = '../results/sumprecips-avgtemps.pdf'
pl.savefig(plotpath)
pl.show()

# pl.plot(tempmedians, sumprecips, 'bo')
# pl.xlabel('sumprecips', size=16)
# pl.ylabel('tempmedians', size=16)
# plotpath = '../results/sumprecips-tempmedians.pdf'
# pl.savefig(plotpath)
# pl.close()