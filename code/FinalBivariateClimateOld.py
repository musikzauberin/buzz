#!/usr/bin/env python

'''Plot bivariate graph and spearman coefficent (turnover monthly values)'''

__author__ = 'Jia Le Lim'
__version__ = '0.0.4'

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

#separate into seasons
drymonths = ['4', '5', '6', '7', '8', '9']
wetmonths = ['10', '11', '12', '1', '2', '3']
[drybints, wetbints] = separateintoseasons(months, bints, drymonths, wetmonths)
[dryosturnovers, wetosturnovers] = separateintoseasons(months, osturnovers, drymonths, wetmonths)
[drystturnovers, wetstturnovers] = separateintoseasons(months, stturnovers, drymonths, wetmonths)
[dryspecturnovers, wetspecturnovers] = separateintoseasons(months, specturnovers, drymonths, wetmonths)
[drybeeturnovers, wetbeeturnovers] = separateintoseasons(months, beeturnovers, drymonths, wetmonths)
[dryplantturnovers, wetplantturnovers] = separateintoseasons(months, plantturnovers, drymonths, wetmonths)

[dryavgprecips, wetavgprecips] = separateintoseasons(months, avgprecips, drymonths, wetmonths)
[dryavgtemps, wetavgtemps] = separateintoseasons(months, avgtemps, drymonths, wetmonths)
[dryavgmaxtemps, wetavgmaxtemps] = separateintoseasons(months, avgmaxtemps, drymonths, wetmonths)
[dryavgtempranges, wetavgtempranges] = separateintoseasons(months, avgtempranges, drymonths, wetmonths)
[dryavghumids, wetavghumids] = separateintoseasons(months, avghumids, drymonths, wetmonths)

pl.figure(figsize=(8, 8))
pl.subplot(2, 2, 1)

dryr, dryp = stats.spearmanr(dryavgtemps, drybints)
wetr, wetp = stats.spearmanr(wetavgtemps, wetbints)
allr, allp = stats.spearmanr(avgtemps, bints)

# plot
pl.plot(dryavgtemps, drybints, 'ro', label = 'Dry Season')
pl.plot(wetavgtemps, wetbints, 'bo', label = 'Wet Season')

# plot dimensions
axes = pl.gca()
ymin, ymax = axes.get_ylim()
xmin, xmax = axes.get_xlim()
pl.axis([ xmin - 0.01, xmax + 0.01, ymin - 0.01, ymax + 0.01])

# labels
pl.xlabel(r'Temperature / \degree C', size=16)
pl.ylabel(r'$\beta_{int}$', size=16)
# pl.title('Turnover in Cerrado (1995-1997)', size=16)

# correlation text
rc('text', usetex=True)
pl.text(xmax - xmax/18, ymin, r' \underline{Spearman`s coefficient}' + '\n Dry Season: ' + str(round(dryr, 3)) + \
'\n Wet Season: ' + str(round(wetr, 3)) + '\n All: ' + str(round(allr, 3)) , size = 12)
# r' \underline{Spearman`s correlation}'

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

pl.subplot(2, 2, 2)

dryr, dryp = stats.spearmanr(dryavgprecips, drybints)
wetr, wetp = stats.spearmanr(wetavgprecips, wetbints)
allr, allp = stats.spearmanr(avgprecips, bints)

# plot
pl.plot(dryavgprecips, drybints, 'ro', label = 'Dry Season')
pl.plot(wetavgprecips, wetbints, 'bo', label = 'Wet Season')

# plot dimensions
axes = pl.gca()
ymin, ymax = axes.get_ylim()
xmin, xmax = axes.get_xlim()
pl.axis([ xmin - 0.01, xmax + 0.01, ymin - 0.01, ymax + 0.01])

# labels
pl.xlabel(r'Precipitation / mm', size=16)
pl.ylabel(r'$\beta_{int}$', size=16)
# pl.title('Turnover in Cerrado (1995-1997)', size=16)

# correlation text
rc('text', usetex=True)
pl.text(xmax - xmax/18, ymin, r' \underline{Spearman`s coefficient}' + '\n Dry Season: ' + str(round(dryr, 3)) + \
'\n Wet Season: ' + str(round(wetr, 3)) + '\n All: ' + str(round(allr, 3)) , size = 12)
# r' \underline{Spearman`s correlation}'

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

pl.subplot(2, 2, 3)

dryr, dryp = stats.spearmanr(dryavgtemps, dryplantturnovers)
wetr, wetp = stats.spearmanr(wetavgtemps, wetplantturnovers)
allr, allp = stats.spearmanr(avgtemps, plantturnovers)

# plot
pl.plot(dryavgtemps, dryplantturnovers, 'ro', label = 'Dry Season')
pl.plot(wetavgtemps, wetplantturnovers, 'bo', label = 'Wet Season')

# plot dimensions
axes = pl.gca()
ymin, ymax = axes.get_ylim()
xmin, xmax = axes.get_xlim()
pl.axis([ xmin - 0.01, xmax + 0.01, ymin - 0.01, ymax + 0.01])

# labels
pl.xlabel(r'Temperature / \degree C', size=14)
pl.ylabel(r'$\beta_{Plant}$', size=14)
# pl.title('Turnover in Cerrado (1995-1997)', size=16)

# correlation text
rc('text', usetex=True)
pl.text(xmax - xmax/18, ymin, r' \underline{Spearman`s coefficient}' + '\n Dry Season: ' + str(round(dryr, 3)) + \
'\n Wet Season: ' + str(round(wetr, 3)) + '\n All: ' + str(round(allr, 3)) , size = 10)
# r' \underline{Spearman`s correlation}'

# legend
legend = pl.legend(loc='best', frameon=True, numpoints=1, fontsize = 10)
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

pl.subplot(2, 2, 4)

dryr, dryp = stats.spearmanr(dryavgprecips, dryplantturnovers)
wetr, wetp = stats.spearmanr(wetavgprecips, wetplantturnovers)
allr, allp = stats.spearmanr(avgprecips, plantturnovers)

# plot
pl.plot(dryavgprecips, dryplantturnovers, 'ro', label = 'Dry Season')
pl.plot(wetavgprecips, wetplantturnovers, 'bo', label = 'Wet Season')

# plot dimensions
axes = pl.gca()
ymin, ymax = axes.get_ylim()
xmin, xmax = axes.get_xlim()
pl.axis([ xmin - 0.01, xmax + 0.01, ymin - 0.01, ymax + 0.01])

# labels
pl.xlabel(r'Precipitation / mm', size=13)
pl.ylabel(r'$\beta_{Plant}$', size=15)
# pl.title('Turnover in Cerrado (1995-1997)', size=16)

# correlation text
rc('text', usetex=True)
pl.text(xmax - xmax/18, ymin, r' \underline{Spearman`s coefficient}' + '\n Dry Season: ' + str(round(dryr, 3)) + \
'\n Wet Season: ' + str(round(wetr, 3)) + '\n All: ' + str(round(allr, 3)) , size = 10)
# r' \underline{Spearman`s correlation}'

# legend
legend = pl.legend(loc='best', frameon=True, numpoints=1, fontsize = 10)
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
pl.suptitle('Climatic Effect on turnovers (BBG site; Average Model)', size = 16)
pl.tight_layout()
pl.subplots_adjust(top=0.94)
# save plot and show
plotpath = '../climatebivariate(old).pdf'
pl.savefig(plotpath)
pl.show()