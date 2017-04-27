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
sumprecips = []
avghumid = []
avgvisits = []

for column in data:
  months.append(column[0])
  bints.append(column[1])
  seasons.append(column[2])
  boundarys.append(column[3])
  sumprecips.append(column[4])
  avghumid.append(column[5])
  avgvisits.append(column[5])

h.close()

#remove header
for i in [months, bints, seasons, boundarys, sumprecips, avghumid, avgvisits]:
  del i[0]


pl.plot(sumprecips, avgvisits, 'ro')

pl.grid(True)

pl.title('sumprecip-Avgvisits')

plotpath = '../results/' + 'sumprecip-Avgvisits' + '.pdf'
pl.savefig(plotpath)

pl.show()