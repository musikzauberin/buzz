import csv
import operator
import decimal
import numpy as np
import matplotlib.pyplot as pl
import matplotlib.lines as mlines
import calendar
import sys
import os.path

h = open('../results/MonthlyTurnoverPlotData2.csv','rb')
data = csv.reader(h)

months = []
bints = []
bbints = []
pbints = []

for column in data:
  months.append(column[0])
  bints.append(column[1])
  bbints.append(column[2])
  pbints.append(column[3])

h.close()

#remove header
for i in [months, bints, bbints, pbints]:
  del i[0]

print bints

upperbound = len(months)*2 -2
bintsdisplay = [None for i in range(0, upperbound)]
e = 0
for i in range(1, upperbound, 2):
    bintsdisplay[i] = bints[e]
    e += 1

bbintsdisplay = [None for i in range(0, upperbound)]
e = 0
for i in range(1, upperbound, 2):
    bbintsdisplay[i] = bbints[e]
    e += 1

pbintsdisplay = [None for i in range(0, upperbound)]
e = 0
for i in range(1, upperbound, 2):
    pbintsdisplay[i] = pbints[e]
    e += 1

monthsdisplay = range(0,24)
e = 0
for i in range(0, 24, 2):
  monthsdisplay[i] = months[e]
  e += 1
for i in range(1, 24, 2):
  monthsdisplay[i] = ''

bintsline = [0 for i in range(0, upperbound)]
e = 01
for i in range(2, upperbound, 2):
  bintsline[i] = (float(bints[e]) + float(bints[e-1])) / 2
  e += 1
e = 0
for i in range(1, upperbound, 2):
  bintsline[i] = bints[e]
  e += 1

bbintsline = [0 for i in range(0, upperbound)]
e = 01
for i in range(2, upperbound, 2):
  bbintsline[i] = (float(bbints[e]) + float(bbints[e-1])) / 2
  e += 1
e = 0
for i in range(1, upperbound, 2):
  bbintsline[i] = bbints[e]
  e += 1

pbintsline = [0 for i in range(0, upperbound)]
e = 01
for i in range(2, upperbound, 2):
  pbintsline[i] = (float(pbints[e]) + float(pbints[e-1])) / 2
  e += 1
e = 0
for i in range(1, upperbound, 2):
  pbintsline[i] = pbints[e]
  e += 1

print bintsline
print monthsdisplay
print bints
print bintsdisplay
import brewer2mpl

# plotting plotting plotting
pl.figure(figsize=(20,5))

dotcolours = brewer2mpl.get_map('RdYlGn', 'diverging', 11).mpl_colors

bintsline[0] = None
pl.plot(bintsdisplay, 'bo', label = 'Interaction', markersize=8)
pl.plot(bintsline, 'b', label = None)

bbintsline[0] = None
pl.plot(bbintsdisplay, 'o', color = dotcolours[2], label = 'Bee', markersize=8)
pl.plot(bbintsline, color = dotcolours[2], label = None)

pbintsline[0] = None
pl.plot(pbintsdisplay, 'o', color = dotcolours[10], label = 'Plant', markersize=8)
pl.plot(pbintsline, color = dotcolours[10], label = None)

pl.xticks(range(len(monthsdisplay)), monthsdisplay, size = 18)

# bintsline[30] = None
# pl.plot(bintsdisplay[30:48], 'ro', label = '1996-1997')
# pl.plot(bintsline[30:48], 'k', label = None)

pl.axis([-1, 23, 0, 1.1])
pl.grid(True)

pl.axvspan(-1, 11, facecolor='r', alpha=0.1)
pl.axvspan(11, 23, facecolor='c', alpha=0.1)
pl.text(4, 1.04, 'Dry Season', size = 16)
pl.text(16, 1.04, 'Wet Season', size = 16)

legend = pl.legend(loc='lower right', frameon=True, numpoints=1)

light_grey = np.array([float(248)/float(255)]*3)

legend.get_frame().set_linewidth(0.0)
legend.get_frame().set_color(light_grey)

# remove borders
pl.gca().spines['top'].set_visible(False)
pl.gca().spines['right'].set_visible(False)
pl.gca().xaxis.set_ticks_position('bottom')
pl.gca().yaxis.set_ticks_position('left')

minor_ticks = np.arange(0, 24, 2)
major_ticks = np.arange(1, 24, 2)
pl.tick_params(axis = 'x', which = 'major', length = 0 )
pl.tick_params(axis = 'x', which = 'minor', length = 10, direction = 'inout')
pl.gca().set_xticks(minor_ticks, minor=True)
pl.gca().grid(True, axis = 'x', which='minor', linestyle='-', alpha=0.3) 
pl.gca().grid(False, which='major', axis = 'x') 


ymajor_ticks = np.arange(0, 1.1, 0.1)
yminor_ticks = np.arange(0, 1.1, 0.02)
pl.gca().set_yticks(ymajor_ticks)

pl.gca().set_yticks(yminor_ticks, minor = True)
pl.yticks(size = 16)
pl.tick_params(axis = 'y', length = 10, direction = 'inout')
pl.gca().grid(True, axis = 'y', which='major', linestyle='-', alpha=0.3) 
pl.gca().grid(True, axis = 'y', which='minor', linestyle='-', alpha=0.1) 
# titles and axis labels
# pl.title('Monthly Turnover in a Tropical Savanna', size = 20)

pl.ylabel('Turnover', size=22) # , fontweight='bold'

pl.text(1, .87 , r'$\beta_{int} = 0.859$', size = 18)


plotpath = '../results/' + 'turnover2' + '.pdf'
pl.savefig(plotpath)

pl.show()