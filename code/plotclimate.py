import csv
import operator
import decimal
import numpy as np
import matplotlib.pyplot as pl
import calendar
import sys
import os.path
from math import log

h = open('../data/rearranged/new/AvgVisitsClimaData.csv','rb')
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
logavgvisits = [log(float(avgvisit),10) for avgvisit in avgvisits]

# pl.plot(x, y)
pl.plot(avgtemps, avghumids, 'bo')


pl.xlabel('Average temperature per Month', size=16)
pl.ylabel('Average Humidity per Month / %', size=16)

# Average Humidity per Month / %
# Monthly Precipitation Sum / mm
# Average daily visits per month
pl.grid(True)

pl.title('Climate data', size = 18)

plotpath = '../results/' + 'AvgTemp-AvgHumid' + '.pdf'
pl.savefig(plotpath)

pl.show()