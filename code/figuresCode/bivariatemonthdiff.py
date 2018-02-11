#!/usr/bin/env python

'''Plot bivariate graph and spearman coefficent (climate diff bet months)'''

__author__ = 'Jia Le Lim'
__version__ = '0.0.5'

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

h = open('../../data/rearranged/new/AllTurnoverCorrectedNewCerrado.csv','rb')
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

def plotturnovers(a, b, drya, dryb, weta, wetb, xlabel_str, ylabel_str):
  'Calculate correlation and plot bivariate plot'
  
  # Calculate Spearman Correlation Coefficient
  dryr, dryp = stats.spearmanr(drya, dryb)
  wetr, wetp = stats.spearmanr(weta, wetb)
  allr, allp = stats.spearmanr(a, b)
  
  # plot
  pl.plot(drya, dryb, 'ro', label = 'Dry Season')
  pl.plot(weta, wetb, 'bo', label = 'Wet Season')
  
  # plot dimensions
  axes = pl.gca()
  ymin, ymax = axes.get_ylim()
  xmin, xmax = axes.get_xlim()
  pl.axis([ xmin - 0.01, xmax + 0.01, ymin - 0.01, ymax + 0.01])

  # labels
  pl.xlabel(xlabel_str, size=16)
  pl.ylabel(ylabel_str, size=16)
  pl.title('Climate in Cerrado (2008-2009)', size=16)

  # correlation text
  rc('text', usetex=True)
  pl.text(xmax - xmax/4 - 1, ymin, r' \underline{Spearman`s coefficient}' + '\n Dry Season: ' + str(round(dryr, 5)) + \
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
  plotname = xlabel_str + '-' + ylabel_str
  plotpath = '../../results/CorrectedNewCerrado/Bivariateplots/monthlydiff/' + plotname + '.pdf'
  pl.savefig(plotpath)
  pl.close()
  
  # data to be printed
  return dryr, dryp, wetr, wetp, allr, allp

def writenewdata(filename_str, headers, values):
  'inputting new data into csv file'
  headers = headers.split(', ')
  pathname = '../../results/CorrectedNewCerrado/Bivariateplots/monthlydiff/' + filename_str + '.csv'
  g = open(pathname, 'wb')

  csvwrite = csv.writer(g)
  csvwrite.writerow(headers)
  tobewritten = zip(*values)
  for row in tobewritten:
    csvwrite.writerow(row)
  g.close()

# Plotting starts here
# diffprecips, difftemps, diffmaxtemps, difftempranges, diffhumids

# separate into seasons
drymonths = ['4', '5', '6', '7', '8', '9']
wetmonths = ['10', '11', '12', '1', '2', '3']
[drydiffprecips, wetdiffprecips] = separateintoseasons(months, diffprecips, drymonths, wetmonths)
[drydifftemps, wetdifftemps] = separateintoseasons(months, difftemps, drymonths, wetmonths)
[drydiffmaxtemps, wetdiffmaxtemps] = separateintoseasons(months, diffmaxtemps, drymonths, wetmonths)
[drydifftempranges, wetdifftempranges] = separateintoseasons(months, difftempranges, drymonths, wetmonths)
[drydiffhumids, wetdiffhumids] = separateintoseasons(months, diffhumids, drymonths, wetmonths)

# turnoverset for y, turnoverxset for x needed to be plotted against y
turnoverset = [diffprecips, difftemps, diffmaxtemps, difftempranges, diffhumids]
turnoverxset = [[difftemps, diffmaxtemps, difftempranges, diffhumids], \
[diffmaxtemps, difftempranges, diffhumids], \
[difftempranges, diffhumids], \
[], []]
wetturnoverset = [wetdiffprecips, wetdifftemps, wetdiffmaxtemps, wetdifftempranges, wetdiffhumids]
dryturnoverset = [drydiffprecips, drydifftemps, drydiffmaxtemps, drydifftempranges, drydiffhumids]
turnoversetlabel = ['PrecipsDiff', 'TempsDiff', 'MaxTempsDiff', 'TempRangesDiff', 'HumidsDiff']

# for each y value find the x values needed to be plotted against, find x index in dry and wet and label sets
# append the appropriate labels and values for exporting correlation values

[xlabels, ylabels, dryrs, dryps, wetrs, wetps, allrs, allps] = ([] for i in range(8))

for i in range(len(turnoverset)):
  for xturnover in turnoverxset[i]:
    for turnover in turnoverset:
      if xturnover == turnover:
        h = turnoverset.index(turnover)

    dryr, dryp, wetr, wetp, allr, allp = plotturnovers(xturnover, turnoverset[i], \
    dryturnoverset[h], dryturnoverset[i], wetturnoverset[h], wetturnoverset[i], turnoversetlabel[h], turnoversetlabel[i])

    xlabels.append(turnoversetlabel[h])
    ylabels.append(turnoversetlabel[i])
    dryrs.append(round(dryr, 5))
    dryps.append(round(dryp, 5))
    wetrs.append(round(wetr, 5))
    wetps.append(round(wetp, 5))
    allrs.append(round(allr, 5))
    allps.append(round(allp, 5))

# output data

newheaders = 'x-axis, y-axis, DryCoefficient, DryP-value, WetCoefficient, WetP-value, AllCoefficient, AllP-value'
newvalues = [xlabels, ylabels, dryrs, dryps, wetrs, wetps, allrs, allps]
writenewdata('DiffClimateCoefficients(New)', newheaders, newvalues)
