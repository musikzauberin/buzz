#!/usr/bin/env python

'''Plot bivariate graph and spearman coefficent (monthly values)'''

__author__ = 'Jia Le Lim'
__version__ = '0.0.2'

import csv
import operator
import decimal
import numpy as np
import scipy as sp
import matplotlib.pyplot as pl
import matplotlib.lines as mlines
import calendar
import sys
import os.path
from math import log
from scipy import stats
from matplotlib import rc

h = open('../data/rearranged/new/AllTurnoverOldCerrado.csv','rb')
data = csv.reader(h)


########## Inputting data into lists ##########

# copy and paste all headers in data twice
[years, months, bints, beeturnovers, plantturnovers, specturnovers, osturnovers, stturnovers, \
avgprecips, avgtemps, avgmaxtemps, avgtempranges, avghumids, \
diffprecips, difftemps, diffmaxtemps, difftempranges, diffhumids] = ([] for i in range(len(next(data))))

headers2 = [years, months, bints, beeturnovers, plantturnovers, specturnovers, osturnovers, stturnovers, \
avgprecips, avgtemps, avgmaxtemps, avgtempranges, avghumids, \
diffprecips, difftemps, diffmaxtemps, difftempranges, diffhumids]

for column in data:
  for j, i in enumerate(headers2):
    i.append(column[j])

h.close()


########## Bivariates between turnover data ##########

def separateintoseasons(months, values, drymonths, wetmonths):
  'Separate data into dry and wet seasons'
  dryvalues = []
  wetvalues = []
  for i in range(len(values)):
    if months[i] in drymonths:
      dryvalues.append(values[i])
    if months[i] in wetmonths:
      wetvalues.append(values[i])
  return dryvalues, wetvalues

drymonths = ['4', '5', '6', '7', '8', '9']
wetmonths = ['10', '11', '12', '1', '2', '3']

# avghumids vs sumprecips
# bints, beeturnovers, plantturnovers, specturnovers, osturnovers, stturnovers

[drybints, wetbints] = separateintoseasons(months, bints, drymonths, wetmonths)
[dryosturnovers, wetosturnovers] = separateintoseasons(months, osturnovers, drymonths, wetmonths)

# Calculate Spearman Correlation Coefficient

dryr, dryp = stats.spearmanr(drybints, dryosturnovers)
wetr, wetp = stats.spearmanr(wetbints, wetosturnovers)
allr, allp = stats.spearmanr(bints, osturnovers)


########## Plotting data ##########

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

# plot dimensions
pl.axis([-0.01, 1.01, 0.7, 1.01])

# plot
pl.plot(wetosturnovers, wetbints, 'bo', label = 'Wet Season')
pl.plot(dryosturnovers, drybints, 'ro', label = 'Dry Season')

# labels
pl.xlabel('osturnovers', size=16)
pl.ylabel('bints', size=16)
pl.title('Turnover in Cerrado (1995-1998)', size=16)

# correlation text
rc('text', usetex=True)
pl.text(0.8, 0.71, r' \underline{Spearman`s coefficient}' + '\n Dry Season: ' + str(round(dryr, 5)) + \
'\n Wet Season: ' + str(round(wetr, 5)) + '\n All: ' + str(round(allr, 5)) , size = 12)

# legend
legend = pl.legend(loc='best', frameon=True, numpoints=1)
light_grey = np.array([float(248)/float(255)]*3)
legend.get_frame().set_linewidth(0.0)
legend.get_frame().set_color(light_grey)

# remove borders
pl.gca().spines['top'].set_visible(False)
pl.gca().spines['right'].set_visible(False)
pl.gca().xaxis.set_ticks_position('bottom')
pl.gca().yaxis.set_ticks_position('left')

# grid
pl.grid(True)

# save plot and show
plotpath = '../results/ClimaPlots/OldCerradoClima/turnovers/osturnovers-bints.pdf'
pl.savefig(plotpath)
pl.show()