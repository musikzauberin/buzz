#!/usr/bin/env python
"""Plotting Climate Data"""

import csv
import operator
import decimal
import numpy as np
import matplotlib.pyplot as pl
import calendar
import sys
import os.path
from math import log

h = open('../data/rearranged/new/NewCerradoAvgVisitsClimaData.csv','rb')
data = csv.reader(h)

########## Inputting data into lists ##########

# copy and paste all headers in data twice
[seasons, years, months, nodays, avgvisits, \
sumprecips, avghumids, avgmaxtemps, avgtemps, avgtempranges] = ([] for i in range(len(next(data))))

headers = [seasons, years, months, nodays, avgvisits, \
sumprecips, avghumids, avgmaxtemps, avgtemps, avgtempranges]

for column in data:
  for j, i in enumerate(headers):
    i.append(column[j])

h.close()

########## Plotting data ##########
# logavgvisits = [log(float(avgvisit),10) for avgvisit in avgvisits]

# # pl.plot(x, y)
# pl.plot(sumprecips, avghumids, 'bo')
#
#
# pl.xlabel('Monthly Precipitation Sum / mm', size=16)
# pl.ylabel('Average Humidity per Month / %', size=16)
#
# # Average temperature per Month
# # Average Humidity per Month / %
# # Monthly Precipitation Sum / mm
# # Average daily visits per month
# pl.grid(True)
# bins = np.arange(0, 40, 0.1)
print avgtemps
avgtemps = np.array(avgtemps).astype(np.float)
print avgtemps
pl.hist(avgtemps)

pl.title('Climate data in Cerrado (2008-2009)', size = 18)

plotpath = '../results/' + 'AvgTemp(New)' + '.pdf'
pl.savefig(plotpath)

pl.show()