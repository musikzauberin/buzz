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

h = open('../../data/rearranged/new/2017/AllTurnoverOldCerrado.csv','rb')
data = csv.reader(h)


########## Inputting data into lists ##########

# copy and paste all headers in data twice
[years, months, bints, beeturnovers, plantturnovers, specturnovers, osturnovers, stturnovers, \
avgprecips, avgtemps, avgmaxtemps, avgtempranges, avghumids, \
diffprecips, difftemps, diffmaxtemps, difftempranges, diffhumids, seasons] = ([] for i in range(len(next(data))))

headers2 = [years, months, bints, beeturnovers, plantturnovers, specturnovers, osturnovers, stturnovers, \
avgprecips, avgtemps, avgmaxtemps, avgtempranges, avghumids, \
diffprecips, difftemps, diffmaxtemps, difftempranges, diffhumids, seasons]

for column in data:
  for j, i in enumerate(headers2):
    i.append(column[j])

h.close()


########## Bivariates between turnover data ##########
# separate into seasons
# drymonths = ['4', '5', '6', '7', '8', '9']
# wetmonths = ['10', '11', '12', '1', '2', '3']
# [drybints, wetbints] = separateintoseasons(months, bints, drymonths, wetmonths)
# [dryosturnovers, wetosturnovers] = separateintoseasons(months, osturnovers, drymonths, wetmonths)
# [drystturnovers, wetstturnovers] = separateintoseasons(months, stturnovers, drymonths, wetmonths)
# [dryspecturnovers, wetspecturnovers] = separateintoseasons(months, specturnovers, drymonths, wetmonths)
# [drybeeturnovers, wetbeeturnovers] = separateintoseasons(months, beeturnovers, drymonths, wetmonths)
# [dryplantturnovers, wetplantturnovers] = separateintoseasons(months, plantturnovers, drymonths, wetmonths)

pl.figure(figsize=(8, 4))
pl.subplot(1, 2, 1)

pl.plot(beeturnovers, bints, 'ko', alpha = 0.7)
allr, allp = stats.spearmanr(beeturnovers, bints)

# plot dimensions
axes = pl.gca()
ymin, ymax = axes.get_ylim()
xmin, xmax = axes.get_xlim()
pl.axis([ xmin - 0.01, xmax + 0.01, ymin - 0.01, ymax + 0.01])

# labels
pl.xlabel(r'$\beta_{Bee}$', size=16)
pl.ylabel(r'$\beta_{int}$', size=16)
pl.title('BBG site', size=16)

# correlation text
rc('text', usetex=True)
pl.text(0.7,0.7,  r'$r_{s}$ = ' + str(round(allr, 3)) + '\n' + r'$p$ = 0.150', size = 12)

# r' \underline{Spearman`s correlation}'

# # legend
# legend = pl.legend(loc='best', frameon=True, numpoints=1)
# light_grey = np.array([float(248)/float(255)]*3)
# legend.get_frame().set_linewidth(0.0)
# legend.get_frame().set_color(light_grey)

# remove borders
pl.gca().spines['top'].set_visible(False)
pl.gca().spines['right'].set_visible(False)
pl.gca().xaxis.set_ticks_position('bottom')
pl.gca().yaxis.set_ticks_position('left')

# grid
pl.grid(True)

h = open('../../data/rearranged/new/AllTurnoverCorrectedNewCerrado2.csv','rb')
data = csv.reader(h)


########## Inputting data into lists ##########

# copy and paste all headers in data twice
[years, months, bints, beeturnovers, plantturnovers, specturnovers, osturnovers, stturnovers, \
avgprecips, avgtemps, avgmaxtemps, avgtempranges, avghumids, \
diffprecips, difftemps, diffmaxtemps, difftempranges, diffhumids, seasons] = ([] for i in range(len(next(data))))

headers2 = [years, months, bints, beeturnovers, plantturnovers, specturnovers, osturnovers, stturnovers, \
avgprecips, avgtemps, avgmaxtemps, avgtempranges, avghumids, \
diffprecips, difftemps, diffmaxtemps, difftempranges, diffhumids, seasons]

for column in data:
  for j, i in enumerate(headers2):
    i.append(column[j])

h.close()


########## Bivariates between turnover data ##########
# separate into seasons
# drymonths = ['4', '5', '6', '7', '8', '9']
# wetmonths = ['10', '11', '12', '1', '2', '3']
# [drybints, wetbints] = separateintoseasons(months, bints, drymonths, wetmonths)
# [dryosturnovers, wetosturnovers] = separateintoseasons(months, osturnovers, drymonths, wetmonths)
# [drystturnovers, wetstturnovers] = separateintoseasons(months, stturnovers, drymonths, wetmonths)
# [dryspecturnovers, wetspecturnovers] = separateintoseasons(months, specturnovers, drymonths, wetmonths)
# [drybeeturnovers, wetbeeturnovers] = separateintoseasons(months, beeturnovers, drymonths, wetmonths)
# [dryplantturnovers, wetplantturnovers] = separateintoseasons(months, plantturnovers, drymonths, wetmonths)



pl.subplot(1, 2, 2)

pl.plot(beeturnovers, bints, 'ko', alpha = 0.7)
allr, allp = stats.spearmanr(beeturnovers, bints)

# plot dimensions
axes = pl.gca()
ymin, ymax = axes.get_ylim()
xmin, xmax = axes.get_xlim()
pl.axis([ xmin - 0.01, 1.01, 0.69, 1.01])

# labels
pl.xlabel(r'$\beta_{Bee}$', size=16)
pl.ylabel(r'$\beta_{int}$', size=16)
pl.title('IBGE site', size=16)

# correlation text
rc('text', usetex=True)
pl.text(0.8, 0.7,  r'$r_{s}$ = ' + str(round(allr, 3)) + '\n' + r'$p$ = 0.63377', size = 12)

# r' \underline{Spearman`s correlation}'

# # legend
# legend = pl.legend(loc='best', frameon=True, numpoints=1)
# light_grey = np.array([float(248)/float(255)]*3)
# legend.get_frame().set_linewidth(0.0)
# legend.get_frame().set_color(light_grey)

# remove borders
pl.gca().spines['top'].set_visible(False)
pl.gca().spines['right'].set_visible(False)
pl.gca().xaxis.set_ticks_position('bottom')
pl.gca().yaxis.set_ticks_position('left')

# grid
pl.grid(True)


pl.tight_layout()


# save plot and show
plotpath = '../plantturnover(New).pdf'
pl.savefig(plotpath)
pl.show()