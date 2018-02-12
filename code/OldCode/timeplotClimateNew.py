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

h = open('../data/rearranged/new/AllTurnoverNewCerrado.csv','rb')
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

intervals = [0, len(bints)]


########## Plotting data ##########

def makesubplotnice():
  'make every subplot the same, nice and simple'
  # subplot labels
  monthlabels = 'Oct, Nov, Dec, Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep '
  monthlabels = monthlabels.split(', ')
  minor_ticks = np.arange(-0.5, 12.5, 1)
  # major_ticks = np.arange(1, 12, 1)
  pl.xticks(minor_ticks, monthlabels)
  
  # background color
  pl.axvspan(-0.5, 4.5, facecolor='c', alpha=0.1)
  pl.axvspan(4.5, 10.5, facecolor='r', alpha=0.1)
  # pl.text(1.5, 1.04, 'Dry Season', size = 12)
  # pl.text(7, 1.04, 'Wet Season', size = 12)
  # pl.text(12, 1.04, 'Dry Season', size = 12)
  
  # legend
  legend = pl.legend(loc='upper right', frameon=True, numpoints=1, fontsize = 11.5, labelspacing=0.2)
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
'Precip': Blues[4], 'Humid': Blues[8], 'Temp': Paired[5], 'TempMax': Paired[4], 'TempRange': RdGy[0]}

light_grey = np.array([float(248)/float(255)]*3)
almost_black = '#262626'

# plot size
pl.figure(figsize=(12,9))

########## first plot avgprecips, avghumids ##########
host = host_subplot(411, axes_class=AA.Axes)
pl.subplots_adjust(right=0.75)
par1 = host.twinx()
offset = -50
new_fixed_axis = par1.get_grid_helper().new_fixed_axis
par1.axis["left"] = new_fixed_axis(loc="left", axes=par1, offset=(offset, 0))
par1.axis["left"].toggle(all=True)
par1.axis["right"].toggle(all=False)

# host.set_xlabel("Distance")
host.set_ylabel("Precipitation/ mm")
par1.set_ylabel("Humidity/ %")
p1, = host.plot(avgprecips[intervals[0]:intervals[1]], marker = 'o', color = colordict['Precip'], label = 'Precipitation', markeredgewidth=0.5, markeredgecolor=almost_black)
p2, = par1.plot(avghumids[intervals[0]:intervals[1]], marker = 'o', color = colordict['Humid'], label = 'Humidity', markeredgewidth=0.5, markeredgecolor=almost_black)
host.set_xlim(-1, 12)
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
pl.title('Climate (Average) in Cerrado (2008-2009)')
makesubplotnice()

# grid lines
xs = np.arange(-0.5, 11, 1)
ys = np.arange(0, 300, 50)
for x in xs:
    pl.plot([x, x], [ys[0], ys[-1]], color='black', alpha=0.3, linestyle='-')
for y in ys:
    pl.plot([-1, 13.5], [y, y], color='black', alpha=.33, linestyle=':')


########## second plot avgtemps, avgmaxtemps, avgtempranges ##########
host = host_subplot(412, axes_class=AA.Axes)
pl.subplots_adjust(right=0.75)
par1 = host.twinx()
offset = -50
new_fixed_axis = par1.get_grid_helper().new_fixed_axis
par1.axis["left"] = new_fixed_axis(loc="left", axes=par1, offset=(offset, 0))
par1.axis["left"].toggle(all=True)
par1.axis["right"].toggle(all=False)

# host.set_xlabel("Distance")
host.set_ylabel(r"Temperature / $^\circ$C")
par1.set_ylabel("Temperature Range")
p1, = host.plot(avgtemps[intervals[0]:intervals[1]], marker = 'o', color = colordict['Temp'], label = 'Temperature', markeredgewidth=0.5, markeredgecolor=almost_black)
p1, = host.plot(avgmaxtemps[intervals[0]:intervals[1]], marker = 'o', color = colordict['TempMax'], label = 'Maximum Temperature', markeredgewidth=0.5, markeredgecolor=almost_black)
p2, = par1.plot(avgtempranges[intervals[0]:intervals[1]], marker = 'o', color = colordict['TempRange'], label = 'Temperature Range', markeredgewidth=0.5, markeredgecolor=almost_black)
host.set_xlim(-1, 12)
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
makesubplotnice()
# grid lines
xs = np.arange(-0.5, 11, 1)
ys = np.arange(18, 30, 2)
for x in xs:
    pl.plot([x, x], [18, 30], color='black', alpha=0.3, linestyle='-')
for y in ys:
    pl.plot([-1, 13.5], [y, y], color='black', alpha=.33, linestyle=':')

########## third plot diffprecips, diffhumids ##########
host = host_subplot(413, axes_class=AA.Axes)
pl.subplots_adjust(right=0.75)
par1 = host.twinx()
offset = -65
new_fixed_axis = par1.get_grid_helper().new_fixed_axis
par1.axis["left"] = new_fixed_axis(loc="left", axes=par1, offset=(offset, 0))
par1.axis["left"].toggle(all=True)
par1.axis["right"].toggle(all=False)

# host.set_xlabel("Distance")
host.set_ylabel("Precipitation/ mm")
par1.set_ylabel("Humidity/ %")
p1, = host.plot(diffprecips[intervals[0]:intervals[1]], marker = 'o', color = colordict['Precip'], label = 'Precipitation', markeredgewidth=0.5, markeredgecolor=almost_black)
p2, = par1.plot(diffhumids[intervals[0]:intervals[1]], marker = 'o', color = colordict['Humid'], label = 'Humidity', markeredgewidth=0.5, markeredgecolor=almost_black)
host.set_xlim(-1, 12)
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
pl.title('Climate (Difference) in Cerrado (2008-2009)')
makesubplotnice()

# grid lines
xs = np.arange(-0.5, 11, 1)
ys = np.arange(-200, 200, 50)
for x in xs:
    pl.plot([x, x], [-200, 200], color='black', alpha=0.3, linestyle='-')
for y in ys:
    pl.plot([-1, 13.5], [y, y], color='black', alpha=.33, linestyle=':')


########## fourth plot difftemps, diffmaxtemps, difftempranges ##########
host = host_subplot(414, axes_class=AA.Axes)
pl.subplots_adjust(right=0.75)
par1 = host.twinx()
offset = -50
new_fixed_axis = par1.get_grid_helper().new_fixed_axis
par1.axis["left"] = new_fixed_axis(loc="left", axes=par1, offset=(offset, 0))
par1.axis["left"].toggle(all=True)
par1.axis["right"].toggle(all=False)

# host.set_xlabel("Distance")
host.set_ylabel(r"Temperature / $^\circ$C")
par1.set_ylabel("Temperature Range")
p1, = host.plot(difftemps[intervals[0]:intervals[1]], marker = 'o', color = colordict['Temp'], label = 'Temperature', markeredgewidth=0.5, markeredgecolor=almost_black)
p1, = host.plot(diffmaxtemps[intervals[0]:intervals[1]], marker = 'o', color = colordict['TempMax'], label = 'Maximum Temperature', markeredgewidth=0.5, markeredgecolor=almost_black)
p2, = par1.plot(difftempranges[intervals[0]:intervals[1]], marker = 'o', color = colordict['TempRange'], label = 'Temperature Range', markeredgewidth=0.5, markeredgecolor=almost_black)
host.set_xlim(-1, 12)
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
makesubplotnice()
# grid lines
xs = np.arange(-0.5, 11, 1)
ys = np.arange(-4, 4, 1)
for x in xs:
    pl.plot([x, x], [-4, 4], color='black', alpha=0.3, linestyle='-')
for y in ys:
    pl.plot([-1, 13.5], [y, y], color='black', alpha=.33, linestyle=':')
legend = pl.legend(loc='bes', frameon=True, numpoints=1, fontsize = 10, labelspacing=0.2)
light_grey = np.array([float(248)/float(255)]*3)
legend.get_frame().set_linewidth(0.0)
legend.get_frame().set_color(light_grey)


# overall
pl.tight_layout()

plotpath = '../results/' + 'ClimateAcrossTime(New)' + '.pdf'
pl.savefig(plotpath)

pl.show()