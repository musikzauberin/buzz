#!/usr/bin/env python

'''Plot bivariate graph and spearman coefficent (climateavg and turnover correlations)'''

__author__ = 'Jia Le Lim'
__version__ = '0.0.7'

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
  pl.title('Turnover in Cerrado (2008-2009)', size=16)

  # correlation text
  rc('text', usetex=True)
  pl.text(xmax - xmax/12, ymin, r' \underline{Spearman`s coefficient}' + '\n Dry Season: ' + str(round(dryr, 5)) + \
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
  plotpath = '../../results/CorrectedNewCerrado/Bivariateplots/monthavg&turnover/' + plotname + '.pdf'
  pl.savefig(plotpath)
  pl.close()
  
  # data to be printed
  return dryr, dryp, wetr, wetp, allr, allp

def writenewdata(filename_str, headers, values):
  'inputting new data into csv file'
  headers = headers.split(', ')
  pathname = '../../results/CorrectedNewCerrado/Bivariateplots/monthavg&turnover/' + filename_str + '.csv'
  g = open(pathname, 'wb')

  csvwrite = csv.writer(g)
  csvwrite.writerow(headers)
  tobewritten = zip(*values)
  for row in tobewritten:
    csvwrite.writerow(row)
  g.close()

# Plotting starts here
# bints, osturnovers, stturnovers, specturnovers, beeturnovers, plantturnovers
# avgprecips, avgtemps, avgmaxtemps, avgtempranges, avghumids

# separate into seasons
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

# removed Bst as no point comparing it to climate i think
# turnoverset for y, turnoverxset for x needed to be plotted against y
turnoverset = [bints, osturnovers, specturnovers, beeturnovers, plantturnovers]
xturnoverset = [avgprecips, avgtemps, avgmaxtemps, avgtempranges, avghumids]

wetturnoverset = [wetbints, wetosturnovers, wetspecturnovers, wetbeeturnovers, wetplantturnovers]
dryturnoverset = [drybints, dryosturnovers, dryspecturnovers, drybeeturnovers, dryplantturnovers]
xwetturnoverset = [wetavgprecips, wetavgtemps, wetavgmaxtemps, wetavgtempranges, wetavghumids]
xdryturnoverset = [dryavgprecips, dryavgtemps, dryavgmaxtemps, dryavgtempranges, dryavghumids]

turnoversetlabel = ['IntTurnover', 'Bos', 'SpeciesTurnovers', 'BeeTurnovers', 'PlantTurnovers']
xturnoversetlabel = ['AvgPrecips', 'AvgTemps', 'AvgMaxTemps', 'AvgTempRanges', 'AvgHumids']

# for each y value find the x values needed to be plotted against, find x index in dry and wet and label sets
# append the appropriate labels and values for exporting correlation values

[xlabels, ylabels, dryrs, dryps, wetrs, wetps, allrs, allps] = ([] for i in range(8))

for i in range(len(turnoverset)):
  for h in range(len(xturnoverset)):
    dryr, dryp, wetr, wetp, allr, allp = plotturnovers(xturnoverset[h], turnoverset[i], \
    xdryturnoverset[h], dryturnoverset[i], xwetturnoverset[h], wetturnoverset[i], xturnoversetlabel[h], turnoversetlabel[i])
    # a, b, drya, dryb, weta, wetb, xlabel_str, ylabel_str
    xlabels.append(xturnoversetlabel[h])
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
writenewdata('Turnover&ClimateAvg(Old)', newheaders, newvalues)
