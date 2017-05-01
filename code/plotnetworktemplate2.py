import csv
import operator
import decimal
import numpy as np
import matplotlib.pyplot as pl
import calendar
import sys
import os.path
import networkx as nx
import brewer2mpl


def longest(listoflists):
  'find length of longest list in list of lists'
  if(not isinstance(listoflists, list)): 
    return(0)
  else:
    return(max([len(onelist) for onelist in listoflists]))

filename = 'Apr1996-1997.csv'
pathname = '../data/rearranged/' + filename
h = open(pathname,'rb')
data = csv.reader(h)

########## Inputting data into lists ##########

# copy and paste all headers in data three times
headers = 'months, days, years, bees, plants'

[months, days, years, bees, plants] = ([] for i in range(len(next(data))))

headers2 = [months, days, years, bees, plants]

for column in data:
  for j, i in enumerate(headers2):
    i.append(column[j])

h.close()

########## Adjusting data for plotting ##########

def findstartindex(values, timescale_str):
  'Finds starting index of timescale + last index(len(timescale)), returns startoftimescale'
  'require years and months list'
  startofmonths = [0]
  startofyears = [0]
  datalen = len(values)
  if timescale_str == 'months':
    for i in range(1, datalen):
      if values[i] != values[i-1]:
        startofmonths.append(i)
    print 'Total number of months is ' + str(len(startofmonths)) + '.'
    startofmonths.append(len(months))
    return startofmonths
  if timescale_str == 'years':
    for i in range(1, datalen):
      if values[i] != values[i-1]:
        startofyears.append(i)
    print 'Total number of years is ' + str(len(startofyears)) + '.'
    startofyears.append(len(years))
    return startofyears

startofmonths = findstartindex(months, 'months')

# shifting data downwards

minbee = min(int(bee) for bee in bees)
maxbee = max(int(bee) for bee in bees)
minplant = min(int(plant) for plant in plants)
maxplant = max(int(plant) for plant in plants)

# shifting data downwards into the same range
bees[:] = [int(bee) - (minbee - 1) for bee in bees]
plants[:] = [int(plant) - (minplant - 1) for plant in plants]

# create list of lists of bees and plants in each month, each entry is unique
beelists = []
plantlists = []
noofmonths = 1
rangeofmonths = range(0, len(startofmonths) - noofmonths, noofmonths)

for x in rangeofmonths:
  startindex = startofmonths[x]
  nextindex = startofmonths[x + noofmonths]
  beelist = []
  plantlist = []
  for i in range(startindex, nextindex):
    if bees[i] not in beelist:
      beelist.append(bees[i])
    if plants[i] not in plantlist:
      plantlist.append(plants[i])
  beelists.append(beelist)
  plantlists.append(plantlist)

## create lists for dots in graph for bees and plants
# upperbound = total#ofmonths x 4
upperbound = (len(startofmonths) - 1) * 4

# bees occupy 0, 4, 8, 12... array index
e = 0
beedots = [[-10] for i in range(upperbound)]
for i in range(0, upperbound, 4):
  beedots[i] = beelists[e]
  e += 1

# insert dummy values to let every beedot be the same length 
ideallen = longest(beedots)
for beedot in beedots:
  while len(beedot) < ideallen:
    beedot.append(-10)

# plants occupy 2, 6, 10, 14... array index
e = 0
plantdots = [[-10] for i in range(upperbound)]
for i in range(2, upperbound, 4):
  plantdots[i] = plantlists[e]
  e += 1

# insert dummy values to let every plantdot be the same length
ideallen = longest(plantdots)

for plantdot in plantdots:
  while len(plantdot) < ideallen:
    plantdot.append(-10)

## create lists to draw plant-bee interactions within months.

# create beeplants, list for interactions.
beeplants = [[0,0] for i in range(upperbound)]
for i in range(upperbound):
  beeplants[i][0] = beedots[i]
  beeplants[i][1] = plantdots[i]

# create x axis labels
monthlabels = 'Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec, Jan, Feb, Mar'
monthlabels = monthlabels.split(', ')
monthsdisplay = [ '' for i in range(upperbound)]
e = 0
for i in range(1, upperbound, 4):
  monthsdisplay[i] = monthlabels[e]
  e += 1

########## Plotting data ##########
# twelve months

maxbee2 = max(int(bee) for bee in bees)
maxplant2 = max(int(plant) for plant in plants)

upperylimit = maxbee2
if maxbee2 < maxplant2:
  upperylimit = maxplant2
pl.axis([-1, 24, 0, upperylimit + 10])

# plot dots
pl.plot(beedots, 'mo')
pl.plot(plantdots, 'go')

beeplants = []
for i in range(len(bees)):
  beeplants.append([bees[i], plants[i]])

# find unique interactions in the whole data set
uniqueints = []
for i in range(len(bees)):
  if (bees[i], plants[i]) not in uniqueints:
    uniqueints.append((bees[i], plants[i]))


# Get "Set2" colors from ColorBrewer (all colorbrewer scales: http://bl.ocks.org/mbostock/5577023)
colours = brewer2mpl.get_map('Paired', 'qualitative', 12).mpl_colors

# colourmap = pl.cm.brg #nipy_spectral, Set1,Paired
# noofcolours = 12
# colours = [colourmap(i) for i in np.linspace(0, 1, noofcolours)]

# find max number of times an interaction appears in beeplants
appearmax = 0
for i in range(len(uniqueints)):
  appearno = beeplants.count([bees[i], plants[i]])
  if appearno > appearmax:
    appearmax = appearno
print 'max number of appearances: ' + str(appearmax)

#create better range of colours for interaction lines
colours2 = []
for i in range(1, 12, 12/appearmax):
  colours2.append(colours[i])
  
# Assign a colour to interactions based on how many months they appear in 
colourdict = {}
for i in range(len(uniqueints)):
  appearno = beeplants.count([bees[i], plants[i]])
  colourdict[uniqueints[i]] = colours2[appearno - 1]

# plot lines/interactions within months
def simpleline(x1, x2, y1, y2, colour):
  'draw a line between two points in plot'
  gradient = (y2-y1)/(x2-x1)
  intercept = y2 - gradient * x2
  x = np.arange(x1, x2 + 1)
  line = pl.plot(x, gradient*x + intercept)
  pl.setp(line, color=colour, linewidth=1.0, alpha = 0.8)

for i in range(0, upperbound, 4):
  x1 = i # x value of bee in bees
  x2 = i + 2 # x value of plant in plants
  e = i / 4
  startindex = startofmonths[e]
  nextindex = startofmonths[e + noofmonths]
  p = startindex
  while p < nextindex:
    simpleline(x1, x2, bees[p], plants[p], colourdict[(bees[p], plants[p])])
    p += 1

## create list for drawing lines/common points between months
# find indexes of common interactions between months and save as list of lists
# first list: comparison between first and second timeinterval
commonints = []
for x in rangeofmonths:
  startindex = startofmonths[x]
  nextindex = startofmonths[x + noofmonths]
  lastindex = x + noofmonths*2
  if lastindex >= len(startofmonths):
    break
  else:
    nextnextindex = startofmonths[x + noofmonths*2]
    commonint = []
  for i in range(startindex, nextindex):
    e = nextindex
    while e < nextnextindex:
      if bees[i] == bees[e]:
        if plants[i] == plants[e]:
          commonint.append(i)
          break # breaks the while loop
        else:
          e += 1
      else:
        e += 1
  commonints.append(commonint)

for i in range(len(commonints)):
  x1 = 4 * i + 2
  x2 = x1 + 2
  for cint in commonints[i]:
    simpleline(x1, x2, plants[cint], bees[cint], colourdict[(bees[cint], plants[cint])])

## aesthetics
# axis 
pl.xticks(range(len(monthsdisplay)), monthsdisplay)
pl.grid(True)

pl.axvspan(-1, 23, facecolor='r', alpha=0.1)
pl.axvspan(23, 48, facecolor='c', alpha=0.1)

# pl.legend(loc='upper right', frameon=True, numpoints=1)
# pl.title('Monthly Turnover in Cerrado')

# save plot
plotname = 'Apr1996-1997'
plotpath = '../results/' + plotname + '.pdf'
pl.savefig(plotpath)

pl.show()


