#!/usr/bin/env python
'''Plot across time for all turnovers (1995-1997)'''

import csv
import operator
import decimal
import numpy as np
import matplotlib.pyplot as pl
import matplotlib.lines as mlines
import calendar
import sys
import os.path
import mpl_toolkits.axisartist as AA
from mpl_toolkits.axes_grid1 import host_subplot

h = open('../../data/rearranged/new/AllTurnoverCorrectedNewCerrado2.csv','rb')
data = csv.reader(h)


########## Inputting data into lists ##########

# copy and paste all headers in data twice
[years, months, bints, beeturnovers, plantturnovers, specturnovers, osturnovers, stturnovers, \
avgprecips, avgtemps, avgmaxtemps, avgtempranges, avghumids, \
diffprecips, difftemps, diffmaxtemps, difftempranges, diffhumids, season] = ([] for i in range(len(next(data))))

headers2 = [years, months, bints, beeturnovers, plantturnovers, specturnovers, osturnovers, stturnovers, \
avgprecips, avgtemps, avgmaxtemps, avgtempranges, avghumids, \
diffprecips, difftemps, diffmaxtemps, difftempranges, diffhumids, season]

for column in data:
  for j, i in enumerate(headers2):
    i.append(column[j])

h.close()


########## Manipulating data ##########

intervals = [0, 11]


########## Plotting data ##########

def makesubplotnice():
  'make every subplot the same, nice and simple'
  # subplot labels
  monthlabels = 'Nov, Dec, Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct'
  monthlabels = monthlabels.split(', ')
  minor_ticks = np.arange(0, 24, 2)
  #major_ticks = np.arange(1, 12, 1)
  pl.xticks(minor_ticks, monthlabels)
  
  # background color
  pl.axvspan(0, 9, facecolor='c', alpha=0.1)
  pl.axvspan(9, 21, facecolor='r', alpha=0.1)
  pl.axvspan(21, 23, facecolor='c', alpha=0.1)
  # pl.text(1.5, 1.04, 'Dry Season', size = 12)
  # pl.text(7, 1.04, 'Wet Season', size = 12)
  # pl.text(12, 1.04, 'Dry Season', size = 12)
  
  # legend
  legend = pl.legend(loc='lower right', frameon=True, numpoints=1, fontsize = 11.5, labelspacing=0.2)
  light_grey = np.array([float(248)/float(255)]*3)
  legend.get_frame().set_linewidth(0.0)
  legend.get_frame().set_color(light_grey)

# colors
import brewer2mpl
RdGy = brewer2mpl.get_map('RdGy', 'diverging', 11).mpl_colors
PRGn = brewer2mpl.get_map('PRGn', 'diverging', 11).mpl_colors
Spectral = brewer2mpl.get_map('Spectral', 'diverging', 11).mpl_colors
Blues = brewer2mpl.get_map('Blues', 'sequential', 9).mpl_colors
Dark2 = brewer2mpl.get_map('Dark2', 'qualitative', 8).mpl_colors
Paired = brewer2mpl.get_map('Paired', 'qualitative', 12).mpl_colors

colordict = {'Bint': RdGy[10], 'Bos': Paired[11], 'Bst': Dark2[5], 'Bs': Spectral[10], 'Bbee': PRGn[3], 'Bplant': PRGn[9], \
'Precip': Blues[8], 'Humid': Blues[8], 'Temp': RdGy[1], 'TempMax': Paired[4], 'TempRange': RdGy[0]}

light_grey = np.array([float(248)/float(255)]*3)
almost_black = '#262626'

# plot size
pl.figure(figsize=(12,5))

########## first plot avgprecips, avghumids ##########
host = host_subplot(211, axes_class=AA.Axes)
pl.subplots_adjust(right=0.75)
par1 = host.twinx()
offset = -50
new_fixed_axis = par1.get_grid_helper().new_fixed_axis
par1.axis["left"] = new_fixed_axis(loc="left", axes=par1, offset=(offset, 0))
par1.axis["left"].toggle(all=True)
par1.axis["right"].toggle(all=False)

# host.set_xlabel("Distance")
host.set_ylabel("Precipitation / mm")
par1.set_ylabel(r"Temperature / $^\circ$C")

p1, = host.plot(range(1, 23, 2), avgprecips[intervals[0]:intervals[1]], marker = 'o', color = colordict['Precip'], label = 'Precipitation', markeredgewidth=0.5, markeredgecolor=almost_black)
p2, = par1.plot(range(1, 23, 2), avgtemps[intervals[0]:intervals[1]], marker = 'o', color = colordict['Temp'], label = 'Temperature', markeredgewidth=0.5, markeredgecolor=almost_black)
host.set_xlim(-1, 24)
# axes = pl.gca()
# ymin, ymax = axes.get_ylim()
# xmin, xmax = axes.get_xlim()

# legend
host.legend()
host.axis["top"].set_visible(False)
host.axis["right"].set_visible(False)

# yaxes color
host.axis["left"].label.set_color('k')
par1.axis["left"].label.set_color(p2.get_color())
par1.axis["left"].line.set_color(p2.get_color())
par1.axis["left"].major_ticks.set_color(p2.get_color())
par1.axis["left"].major_ticklabels.set_color(p2.get_color())

pl.draw()
pl.title('Average climate-turnover model at IBGE site in Cerrado (2008-2009)')
makesubplotnice()

# grid lines
xs = np.arange(0, 24, 2)
ys = np.arange(0, 300, 50)
for x in xs:
    pl.plot([x, x], [ys[0], ys[-1]], color='black', alpha=0.3, linestyle='-')
for y in ys:
    pl.plot([-1, 24], [y, y], color='black', alpha=.33, linestyle=':')


########## third plot diffprecips, diffhumids ##########
host = host_subplot(212, axes_class=AA.Axes)
pl.subplots_adjust(right=0.75)
par1 = host.twinx()
offset = -65
new_fixed_axis = par1.get_grid_helper().new_fixed_axis
par1.axis["left"] = new_fixed_axis(loc="left", axes=par1, offset=(offset, 0))
par1.axis["left"].toggle(all=True)
par1.axis["right"].toggle(all=False)

# host.set_xlabel("Distance")
host.set_ylabel("Precipitation / mm")
par1.set_ylabel(r"Temperature / $^\circ$C")
p1, = host.plot(range(1, 23, 2), diffprecips[intervals[0]:intervals[1]], marker = 'o', color = colordict['Precip'], label = 'Precipitation', markeredgewidth=0.5, markeredgecolor=almost_black)
p2, = par1.plot(range(1, 23, 2), difftemps[intervals[0]:intervals[1]], marker = 'o', color = colordict['Temp'], label = 'Temperature', markeredgewidth=0.5, markeredgecolor=almost_black)
host.set_xlim(-1, 24)
# axes = pl.gca()
# ymin, ymax = axes.get_ylim()
# xmin, xmax = axes.get_xlim()

# legend
host.legend()
host.axis["top"].set_visible(False)
host.axis["right"].set_visible(False)

# yaxes color
host.axis["left"].label.set_color('k')
par1.axis["left"].label.set_color(p2.get_color())
par1.axis["left"].line.set_color(p2.get_color())
par1.axis["left"].major_ticks.set_color(p2.get_color())
par1.axis["left"].major_ticklabels.set_color(p2.get_color())
par1.set_ylim(-3.1, 3.15)

pl.draw()
pl.title('Difference climate-turnover model at IBGE site in Cerrado (2008-2009)')
makesubplotnice()

# grid lines
xs = np.arange(0, 24, 2)
ys = np.arange(-200, 250, 50)
for x in xs:
    pl.plot([x, x], [ys[0], ys[-1]], color='black', alpha=0.3, linestyle='-')
for y in ys:
    pl.plot([-1, 24], [y, y], color='black', alpha=.33, linestyle=':')


# ########## fourth plot difftemps, diffmaxtemps, difftempranges ##########
# host = host_subplot(414, axes_class=AA.Axes)
# pl.subplots_adjust(right=0.75)
# par1 = host.twinx()
# offset = -50
# new_fixed_axis = par1.get_grid_helper().new_fixed_axis
# par1.axis["left"] = new_fixed_axis(loc="left", axes=par1, offset=(offset, 0))
# par1.axis["left"].toggle(all=True)
# par1.axis["right"].toggle(all=False)
#
# # host.set_xlabel("Distance")
# host.set_ylabel(r"Temperature / $^\circ$C")
# par1.set_ylabel("Temperature Range")
# p1, = host.plot(difftemps[intervals[0]:intervals[1]], marker = 'o', color = colordict['Temp'], label = 'Temperature', markeredgewidth=0.5, markeredgecolor=almost_black)
# p1, = host.plot(diffmaxtemps[intervals[0]:intervals[1]], marker = 'o', color = colordict['TempMax'], label = 'Maximum Temperature', markeredgewidth=0.5, markeredgecolor=almost_black)
# p2, = par1.plot(difftempranges[intervals[0]:intervals[1]], marker = 'o', color = colordict['TempRange'], label = 'Temperature Range', markeredgewidth=0.5, markeredgecolor=almost_black)
# host.set_xlim(-1, 12)
# # axes = pl.gca()
# # ymin, ymax = axes.get_ylim()
# # xmin, xmax = axes.get_xlim()
#
# # legend
# host.legend()
# host.axis["top"].set_visible(False)
# host.axis["right"].set_visible(False)
#
# # yaxes color
# host.axis["left"].label.set_color('k')
# par1.axis["left"].label.set_color(p2.get_color())
# par1.axis["left"].line.set_color(p2.get_color())
# par1.axis["left"].major_ticks.set_color(p2.get_color())
# par1.axis["left"].major_ticklabels.set_color(p2.get_color())
#
# pl.draw()
# makesubplotnice()
# # grid lines
# xs = np.arange(-0.5, 11, 1)
# ys = np.arange(-4, 4, 1)
# for x in xs:
#     pl.plot([x, x], [-4, 4], color='black', alpha=0.3, linestyle='-')
# for y in ys:
#     pl.plot([-1, 13.5], [y, y], color='black', alpha=.33, linestyle=':')
legend = pl.legend(loc='lower right', frameon=True, numpoints=1, fontsize = 12, labelspacing=0.2)
light_grey = np.array([float(248)/float(255)]*3)
legend.get_frame().set_linewidth(0.0)
legend.get_frame().set_color(light_grey)


# overall
pl.tight_layout()

plotpath = '../../results/CorrectedNewCerrado/Timeplots/' + 'Climate(CorrectedNew)' + '.pdf'
pl.savefig(plotpath)

pl.show()