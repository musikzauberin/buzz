#!/usr/bin/env python

'''Plot correlation coefficients for easy visualisation'''

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

h = open('../results/BivariatePlots/OldCerrado/monthdiff&turnover/Turnover&ClimateDiff(Old).csv','rb')
data = csv.reader(h)


########## Inputting data into lists ##########

# copy and paste all headers in data twice
[xmeasures, ymeasures, dryrs, dryps, wetrs, wetps, allrs, allps] = ([] for i in range(len(next(data))))

headers = [xmeasures, ymeasures, dryrs, dryps, wetrs, wetps, allrs, allps]

for column in data:
  for j, i in enumerate(headers):
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
dotmeasures = ['PrecipsDiff', 'TempsDiff', 'MaxTempsDiff', 'TempRangesDiff', 'HumidsDiff']
dotlabels = ['Precips', 'Temps', 'MaxTemps', 'TRanges', 'Humids']

pl.figure(figsize=(20, 8))
for i in range(len(ystarts)-1):
  x = [i] * (ystarts[i+1] - ystarts[i])
  pl.subplot(1, 3, 1)
  pl.plot(x, dryrs[ystarts[i]:ystarts[i+1]], 'ro')
  for j in range(ystarts[i],ystarts[i+1]):
    for dotmeasure in dotmeasures:
      if xmeasures[j] == dotmeasure:
        h = dotmeasures.index(dotmeasure)
        pl.text(i+0.1, dryrs[j], dotlabels[h], size = 10)

  pl.subplot(1, 3, 2)
  pl.plot(x, wetrs[ystarts[i]:ystarts[i+1]], 'bo')
  for j in range(ystarts[i],ystarts[i+1]):
    for dotmeasure in dotmeasures:
      if xmeasures[j] == dotmeasure:
        h = dotmeasures.index(dotmeasure)
        pl.text(i+0.1, wetrs[j], dotlabels[h], size = 10)
  
  pl.subplot(1, 3, 3)
  pl.plot(x, allrs[ystarts[i]:ystarts[i+1]], 'ko')
  for j in range(ystarts[i],ystarts[i+1]):
    for dotmeasure in dotmeasures:
      if xmeasures[j] == dotmeasure:
        h = dotmeasures.index(dotmeasure)
        pl.text(i+0.1, allrs[j], dotlabels[h], size = 10)

# finishing touches on subplots
plotdimensions = [ (1, 3, 1), (1, 3, 2), (1, 3, 3)]
# bints, osturnovers, stturnovers, specturnovers, beeturnovers, plantturnovers
xlabels = 'Bint, Bos, Bs, Bbee, Bplant'
xlabels = xlabels.split(', ')
ylabels = 'Correlation Coefficient, Correlation Coefficient, Correlation Coefficient'
ylabels = ylabels.split(', ')
titles = 'Dry Season, Wet Season, All'
titles = titles.split(', ')

for nrows, ncols, plot_number in plotdimensions:
  pl.subplot(nrows, ncols, plot_number)
  makesubplotnice()

  # x labels
  major_ticks = np.arange(0, len(ystarts)-1)
  pl.xticks(major_ticks, xlabels)
  # y labels
  pl.ylabel(ylabels[plot_number - 1], size=16)
  # title
  pl.title(titles[plot_number - 1], size = 18)

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
plotname = 'Turnover&ClimateDiff(Old)'
plotpath = '../results/BivariatePlots/' + plotname + '.pdf'
pl.savefig(plotpath)

pl.show()
