#!/usr/bin/env python

'''Plot correlation coefficients for easy visualisation(five turnovers with temperature and precipitation)'''

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

h = open('../results/BivariatePlots/NewCerrado/monthavg&turnover/Turnover&ClimateAvg(New).csv','rb')
data = csv.reader(h)

h1 = open('../results/BivariatePlots/NewCerrado/monthdiff&turnover/Turnover&ClimateDiff(New).csv','rb')
data1 = csv.reader(h1)

########## Inputting data into lists ##########

# copy and paste all headers in data twice
[xmeasures, ymeasures, dryrs, dryps, wetrs, wetps, allrs, allps] = ([] for i in range(len(next(data))))

headers = [xmeasures, ymeasures, dryrs, dryps, wetrs, wetps, allrs, allps]

for column in data:
  for j, i in enumerate(headers):
    i.append(column[j])

h.close()

# copy and paste all headers in data twice, extra d infront stands for diff
[dxmeasures, dymeasures, ddryrs, ddryps, dwetrs, dwetps, dallrs, dallps] = ([] for i in range(len(next(data1))))

headers1 = [dxmeasures, dymeasures, ddryrs, ddryps, dwetrs, dwetps, dallrs, dallps]

for column in data1:
  for j, i in enumerate(headers1):
    i.append(column[j])

h.close()


########## Separate into appropriate lists for plotting ##########

def findstartindex(values):
  'Finds start index of each ymeasure'
  ystarts = [0]
  for i in range(1, len(values)):
    if values[i] != values[i-1]:
      ystarts.append(i)
  print 'Total number of y measures is ' + str(len(ystarts)) + '.'
  ystarts.append(len(ymeasures))
  return ystarts

ystarts = findstartindex(ymeasures)
print ystarts


########## Plot data ##########

def makesubplotnice():
  'make every subplot the same, nice and simple'
  # plot dimensions
  axes = pl.gca()
  ymin, ymax = axes.get_ylim()
  xmin, xmax = axes.get_xlim()
  pl.axis([-0.5, xmax + 0.5, - 1.01, 1.01])

  # subplot labels
  # pl.ylabel('Correlation coefficient', size=16)

  # # correlation text
  # rc('text', usetex=True)
  # pl.text(xmax - (xmax + abs(xmin))/6, ymin, r' \underline{Spearman`s coefficient}' + '\n Dry Season: ' + str(round(dryr, 5)) + \
  # '\n Wet Season: ' + str(round(wetr, 5)) + '\n All: ' + str(round(allr, 5)) , size = 12)

  # remove borders
  pl.gca().spines['top'].set_visible(False)
  pl.gca().spines['right'].set_visible(False)
  pl.gca().xaxis.set_ticks_position('bottom')
  pl.gca().yaxis.set_ticks_position('left')

  # grid
  pl.grid(True)


# plot subplots
# label each dot as the x measure compared to the y measure on the xaxis

pl.figure(figsize=(12, 8))
pl.subplot(1, 2, 1)
for i in range(len(ystarts)-1):
  print i
  for j in range(ystarts[i],ystarts[i+1]):
    if xmeasures[j] == 'AvgPrecips':
      pl.plot(i, allrs[j], 'bo')
      pl.text(i+0.1, allrs[j], 'AvgPrecips', size = 12)
    if xmeasures[j] == 'AvgTemps':
      pl.plot(i, allrs[j], 'ko')
      pl.text(i+0.1, allrs[j], 'AvgTemps', size = 12)

# finishing touches on subplots
# bints, osturnovers, stturnovers, specturnovers, beeturnovers, plantturnovers
xlabels = 'bints, Brw, Bs, Bbee, Bplant'
xlabels = xlabels.split(', ')
ylabels = 'Correlation Coefficient'

makesubplotnice()

# x labels
major_ticks = np.arange(0, len(ystarts)-1)
pl.xticks(major_ticks, xlabels)
# y labels
pl.ylabel(ylabels, size=16)


pl.subplot(1, 2, 2)
for i in range(len(ystarts)-1):
  print i
  for j in range(ystarts[i],ystarts[i+1]):
    if dxmeasures[j] == 'PrecipsDiff':
      pl.plot(i, dallrs[j], 'bo')
      pl.text(i+0.1, dallrs[j], 'PrecipsDiff', size = 12)
    if dxmeasures[j] == 'TempsDiff':
      pl.plot(i, dallrs[j], 'ko')
      pl.text(i+0.1, dallrs[j], 'TempsDiff', size = 12)

# finishing touches on subplots
# bints, osturnovers, stturnovers, specturnovers, beeturnovers, plantturnovers
xlabels = 'bints, Brw, Bs, Bbee, Bplant'
xlabels = xlabels.split(', ')
ylabels = 'Correlation Coefficient'

makesubplotnice()

# x labels
major_ticks = np.arange(0, len(ystarts)-1)
pl.xticks(major_ticks, xlabels)
# y labels
pl.ylabel(ylabels, size=16)

# # title
# pl.title(titles, size = 18)

# # legends
# light_grey = np.array([float(248)/float(255)]*3)
# almost_black = '#262626'
# drydotrep = mlines.Line2D([], [], linestyle="none", marker = 'o', color = 'r', markeredgewidth=0.5, markeredgecolor=almost_black, markersize=8)
# wetdotrep = mlines.Line2D([], [], linestyle="none", marker = 'o', color = 'b', markeredgewidth=0.5, markeredgecolor=almost_black, markersize=8)
# alldotrep = mlines.Line2D([], [], linestyle="none", marker = 'o', color = 'k', markeredgewidth=0.5, markeredgecolor=almost_black, markersize=8)
#
# pl.subplot(1, 3, 1)
# legend = pl.legend([drydotrep], ['Dry Season'], loc='best', frameon=True, numpoints=1)
# legend.get_frame().set_linewidth(0.0)
# legend.get_frame().set_color(light_grey)
# pl.gca().add_artist(legend)
#
# pl.subplot(1, 3, 2)
# legend = pl.legend([wetdotrep], ['Wet Season'], loc='best', frameon=True, numpoints=1)
# legend.get_frame().set_linewidth(0.0)
# legend.get_frame().set_color(light_grey)
# pl.gca().add_artist(legend)
#
# pl.subplot(1, 3, 3)
# legend = pl.legend([alldotrep], ['All'], loc='best', frameon=True, numpoints=1)
# legend.get_frame().set_linewidth(0.0)
# legend.get_frame().set_color(light_grey)
# pl.gca().add_artist(legend)

# save plot and show
plotname = 'Climate&Turnover(New)'
plotpath = '../results/BivariatePlots/thesisplots/' + plotname + '.pdf'
pl.savefig(plotpath)

pl.show()
