import csv
import operator
import decimal
import numpy as np
import matplotlib.pyplot as pl
import matplotlib.lines as mlines
import calendar
import sys
import os.path

h1 = open('../data/rearranged/new/TurnoverOldCerrado.csv','rb')
data1 = csv.reader(h1)

h2 = open('../data/rearranged/new/OldCerradoAvgVisitsClimaData.csv','rb')
data2 = csv.reader(h2)


########## Inputting data into lists ##########

# copy and paste all headers in data twice
[years1, months1, bints1] = ([] for i in range(len(next(data1))))
headers1 = [years1, months1, bints1]

for column in data1:
  for j, i in enumerate(headers1):
    i.append(column[j])
h1.close()

# copy and paste all headers in data twice
[seasons, years, months, nodays, avgvisits, \
sumprecips, avghumids, avgmaxtemps, avgtemps, avgtempranges] = ([] for i in range(len(next(data2))))
headers2 = [seasons, years, months, nodays, avgvisits, \
sumprecips, avghumids, avgmaxtemps, avgtemps, avgtempranges]

for column in data2:
  for j, i in enumerate(headers2):
    i.append(column[j])
h2.close()

minavgv = min(float(t) for t in avgtempranges)
maxavgv = max(float(t) for t in avgtempranges)

# shifting data downwards into the same range
avgtempranges[:] = [float(t) - (minavgv - 1) for t in avgtempranges]
avgtempranges_set = set(avgtempranges)
avgtemprange_dict = dict(zip(avgtempranges_set, np.linspace(0.5, 0.7, len(avgtempranges_set), endpoint = True)))
avgtempranges = [avgtemprange_dict[t] for t in avgtempranges]


########## Plotting data ##########

import brewer2mpl

pl.figure(figsize=(20,5))
pl.axis([0.55, 15.5, 0.49, 1.1])

dotcolours = brewer2mpl.get_map('RdYlGn', 'diverging', 11).mpl_colors

xvalues1 = range(1, 13) 

pl.plot(xvalues1, bints1[0:12], 'bo', markersize=8, label = '1995-1996')
pl.plot(xvalues1, bints1[0:12], 'b', label = None)

pl.plot(xvalues1, bints1[12:24], 'go', markersize=8, label = '1996-1997')
pl.plot(xvalues1, bints1[12:24], 'g', label = None)

xvalues2 = np.arange(0.5, 12, 1)
pl.plot(xvalues2, avgtempranges[0:12], 'ko', markersize=8, label = '95-96 avg temp range')
pl.plot(xvalues2, avgtempranges[0:12], 'k', label = None)

pl.plot(xvalues2, avgtempranges[12:24], 'mo', markersize=8, label = '96-97 avg temp range')
pl.plot(xvalues2, avgtempranges[12:24], 'm', label = None)
#
# pl.plot(xvalues1, bints1[12:24], 'go', markersize=8, label = '1996-1997')
# pl.plot(xvalues1, bints1[12:24], 'g', label = None)

# pl.plot(bints1, 'o', color = dotcolours[2], label = '1995-1996', markersize=8)
# pl.plot(bints1, color = dotcolours[2], label = None)

# pbintsline[0] = None
# pl.plot(pbintsdisplay, 'o', color = dotcolours[10], label = 'Plant', markersize=8)
# pl.plot(pbintsline, color = dotcolours[10], label = None)
#
# pl.xticks(range(len(monthsdisplay)), monthsdisplay, size = 18)
#
# # bintsline[30] = None
# # pl.plot(bintsdisplay[30:48], 'ro', label = '1996-1997')
# # pl.plot(bintsline[30:48], 'k', label = None)
#

pl.grid(True)
#
pl.axvspan(0.5, 4.5, facecolor='r', alpha=0.1)
pl.axvspan(4.5, 10.5, facecolor='c', alpha=0.1)
pl.axvspan(10.5, 15.5, facecolor='r', alpha=0.1)
pl.text(2, 1.04, 'Dry Season', size = 16)
pl.text(7, 1.04, 'Wet Season', size = 16)
pl.text(12, 1.04, 'Dry Season', size = 16)
#
legend = pl.legend(loc='upper right', frameon=True, numpoints=1)
light_grey = np.array([float(248)/float(255)]*3)
legend.get_frame().set_linewidth(0.0)
legend.get_frame().set_color(light_grey)
#
# remove borders
pl.gca().spines['top'].set_visible(False)
pl.gca().spines['right'].set_visible(False)
pl.gca().xaxis.set_ticks_position('bottom')
pl.gca().yaxis.set_ticks_position('left')


monthlabels = 'Jun, Jul, Aug, Sep, Oct, Nov, Dec, Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep'
monthlabels = monthlabels.split(', ')

minor_ticks = np.arange(0.5, 16, 1)
print minor_ticks
major_ticks = np.arange(1, 16, 1)
pl.tick_params(axis = 'x', which = 'major', length = 0 )
pl.tick_params(axis = 'x', which = 'minor', length = 10, direction = 'inout')
pl.gca().set_xticks(minor_ticks, minor=True)
pl.gca().grid(True, axis = 'x', which='minor', linestyle='-', alpha=0.3)
pl.gca().grid(False, which='major', axis = 'x')
pl.xticks(minor_ticks, monthlabels)
#
# ymajor_ticks = np.arange(0, 1.1, 0.1)
# yminor_ticks = np.arange(0, 1.1, 0.02)
# pl.gca().set_yticks(ymajor_ticks)
#
# pl.gca().set_yticks(yminor_ticks, minor = True)
# pl.yticks(size = 16)
# pl.tick_params(axis = 'y', length = 10, direction = 'inout')
# pl.gca().grid(True, axis = 'y', which='major', linestyle='-', alpha=0.3)
# pl.gca().grid(True, axis = 'y', which='minor', linestyle='-', alpha=0.1)

# titles and axis labels
pl.title('Monthly Turnover in Cerrado', size = 20)

pl.ylabel('Turnover', size=22) # , fontweight='bold'


plotpath = '../results/' + 'avgtemprange&turnover(old)' + '.pdf'
pl.savefig(plotpath)

pl.show()