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

pl.figure(figsize=(12, 4))

pl.subplot(1, 3, 1)

pl.plot(specturnovers, bints, 'ko', alpha = 0.7)
allr, allp = stats.spearmanr(specturnovers, bints)

# plot dimensions
axes = pl.gca()
ymin, ymax = axes.get_ylim()
xmin, xmax = axes.get_xlim()
pl.axis([ xmin - 0.01, 1.01, ymin-0.01, 1.01])

# labels
pl.xlabel(r'$\beta_{S}$', size=16)
pl.ylabel(r'$\beta_{int}$', size=16)
# pl.title('Turnover in Cerrado (1995-1997)', size=16)

# correlation text
rc('text', usetex=True)
pl.text(0.85, ymin,  r'$r_{s}$ = ' + str(round(allr, 3)) + '\n' + r'$p$ = 0.012', size = 12)

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

pl.subplot(1, 3, 2)

pl.plot(specturnovers, osturnovers, 'ko', alpha = 0.7)
allr, allp = stats.spearmanr(specturnovers, osturnovers)

# plot dimensions
axes = pl.gca()
ymin, ymax = axes.get_ylim()
xmin, xmax = axes.get_xlim()
pl.axis([ xmin - 0.01, 1.01, -0.01, 1.01])

# labels
pl.xlabel(r'$\beta_{S}$', size=16)
pl.ylabel(r'$\beta_{rw}$', size=16)
pl.suptitle('Turnover measures of IBGE networks', size=16)

# correlation text
rc('text', usetex=True)
pl.text(xmin + 0.01 , ymin + 0.01,  r'$r_{s}$ = ' + str(round(allr, 3)) + '\n' + r'$p$ = 0.359', size = 12)

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

pl.subplot(1, 3, 3)

pl.plot(specturnovers, stturnovers, 'ko', alpha = 0.7)
allr, allp = stats.spearmanr(specturnovers, stturnovers)

# plot dimensions
axes = pl.gca()
ymin, ymax = axes.get_ylim()
xmin, xmax = axes.get_xlim()
pl.axis([ xmin - 0.01, 1.01, -0.01, 1.01])

# labels
pl.xlabel(r'$\beta_{S}$', size=16)
pl.ylabel(r'$\beta_{st}$', size=16)
# pl.title('Turnover in Cerrado (1995-1997)', size=16)

# correlation text
rc('text', usetex=True)
pl.text(0.85, 0.01,  r'$r_{s}$ = ' + str(round(allr, 3)) + '\n' + r'$p$ = 0.379', size = 12)

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
pl.subplots_adjust(top=0.88)


# save plot and show
plotpath = '../turnoversbivariate(New).pdf'
pl.savefig(plotpath)
pl.show()