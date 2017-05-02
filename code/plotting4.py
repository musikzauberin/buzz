import csv
import operator
import decimal
import numpy as np
import matplotlib.pyplot as pl
import calendar
import sys
import os.path

h = open('../results/MonthlyTurnoverPlotData.csv','rb')
data = csv.reader(h)


months = []
bints = []

for column in data:
  months.append(column[0])
  bints.append(column[1])

h.close()

#remove header
for i in [months, bints]:
  del i[0]

print bints

upperbound = 31*2 + 6
bintsdisplay = [None for i in range(0, upperbound)]

e = 0
for i in range(5, upperbound, 2):
    bintsdisplay[i] = bints[e]
    e += 1

monthsdisplay = range(0,24)
e = 9
for i in range(0, 24, 2):
  monthsdisplay[i] = months[e]
  print e
  e += 1
for i in range(1, 24, 2):
  monthsdisplay[i] = ''

bintsline = [0 for i in range(0, upperbound)]
e = 1
for i in range(6, upperbound, 2):
  bintsline[i] = (float(bints[e]) + float(bints[e-1])) / 2
  e += 1
e = 0
for i in range(5, upperbound, 2):
  bintsline[i] = bints[e]
  e += 1

print bintsline
print monthsdisplay
print bints
print bintsdisplay

# plotting plotting plotting
pl.figure(figsize=(20,5))

bintsline[4] = None
pl.plot(bintsdisplay[0:24], 'bo', label = '1995-1996')
pl.plot(bintsline[0:24], 'k', label = None)
pl.xticks( range(len(monthsdisplay)), monthsdisplay)

# bintsline[30] = None
# pl.plot(bintsdisplay[30:48], 'ro', label = '1996-1997')
# pl.plot(bintsline[30:48], 'k', label = None)

pl.axis([-1, 24, 0.7, 1.05])
pl.grid(True)

pl.axvspan(0, 11, facecolor='r', alpha=0.05)
pl.axvspan(11, 22, facecolor='c', alpha=0.05)

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
pl.tick_params(axis = 'both', which = 'minor', length = 5 )
pl.gca().set_xticks(minor_ticks, minor=True)
pl.gca().grid(True, axis = 'x', which='minor', linestyle='-', alpha=0.3) 
pl.gca().grid(False, which='major', axis = 'x') 

y_ticks = np.arange(0.7, 1, 0.1)
pl.gca().set_yticks(y_ticks)
pl.gca().grid(True, axis = 'y', which='both', linestyle='-', alpha=0.3) 
# titles and axis labels
pl.title('Monthly Turnover in a Tropical Savanna', size = 20)

pl.ylabel(r"$ \beta_{int} $", size=20)

plotpath = '../results/' + 'turnoverfiguretest' + '.pdf'
pl.savefig(plotpath)

pl.show()