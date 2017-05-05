import csv
import operator
import decimal
import numpy as np
import matplotlib.pyplot as pl
import calendar
import sys
import os.path

h = open('../results/MonthlyTurnoverOldCerrado.csv','rb')
data = csv.reader(h)


months = []
bints = []
seasons = []
boundarys = []

for column in data:
  months.append(column[0])
  bints.append(column[1])
  seasons.append(column[2])
  boundarys.append(column[3])

h.close()

#remove header
for i in [months, bints, seasons, boundarys]:
  del i[0]

bintsdisplay = range(0, 48)
for i in range(0, 48, 2):
  bintsdisplay[i] = None
e = 0
for i in range(1, 48, 2):
    bintsdisplay[i] = bints[e]
    e += 1

monthsdisplay = range(0,48)
e = 0
for i in range(0, 48, 2):
  monthsdisplay[i] = months[e]
  e += 1
for i in range(1, 48, 2):
  monthsdisplay[i] = ''

bintsline = range(0,48)
e = 0
for i in range(0, 48, 2):
  bintsline[i] = (float(bints[e]) + float(bints[e-1])) / 2
  e += 1
e = 0
for i in range(1, 48, 2):
  bintsline[i] = bints[e]
  e += 1

print bintsline
print monthsdisplay
print bintsdisplay[7:30:2]
print len(bintsdisplay[6:30])

# plotting plotting plotting
bintsline[6] = None
pl.plot(bintsdisplay[6:30], 'bo', label = '1995-1996')
pl.plot(bintsline[6:30], 'k', label = None)
pl.xticks( range(len(monthsdisplay[6:30])), monthsdisplay[6:30])

bintsline[30] = None
pl.plot(bintsdisplay[30:48], 'ro', label = '1996-1997')
pl.plot(bintsline[30:48], 'k', label = None)

pl.axis([-1, 24, 0.7, 1.05])
pl.grid(True)

pl.axvspan(0, 11, facecolor='c', alpha=0.2)
pl.axvspan(11, 23, facecolor='r', alpha=0.2)

pl.legend(loc='upper right', frameon=True, numpoints=1)
pl.title('Monthly Turnover in Cerrado')

plotpath = '../results/' + 'MonthlyTurnoverOldCerrado2' + '.pdf'
pl.savefig(plotpath)

pl.show()