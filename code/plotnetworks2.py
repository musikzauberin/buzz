import csv
import operator
import decimal
import numpy as np
import matplotlib.pyplot as pl
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import calendar
import sys
import os.path
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

minbee = min(int(bee) for bee in bees)
maxbee = max(int(bee) for bee in bees)
minplant = min(int(plant) for plant in plants)
maxplant = max(int(plant) for plant in plants)

# shifting data downwards into the same range
bees[:] = [int(bee) - (minbee - 1) for bee in bees]
plants[:] = [int(plant) - (minplant - 1) for plant in plants]
bee_set = set(bees)
bee_dict = dict(zip(bee_set, np.linspace(0, 200, len(bee_set), endpoint = True)))
bees = [bee_dict[bee] for bee in bees]
plant_set = set(plants)
plant_dict = dict(zip(plant_set, np.linspace(0, 200, len(plant_set), endpoint = True)))
plants = [plant_dict[plant] for plant in plants]

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

## list for dots of plants
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
## list for dots of plants
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

## create x axis labels
monthlabels = 'Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec, Jan, Feb, Mar'
monthlabels = monthlabels.split(', ')
monthsdisplay = [ '' for i in range(upperbound)]
e = 0
for i in range(1, upperbound, 4):
  monthsdisplay[i] = monthlabels[e]
  e += 1


########## Plotting data ##########

## figure size
# figure(num=None, figsize=(8, 6) #ininches, dpi=80 #noofpixels, facecolor='w', edgecolor='k')
pl.figure(figsize=(12,4))

## All needed colours
almost_black = '#262626'
## Get "Set2" colors from ColorBrewer (all colorbrewer scales: http://bl.ocks.org/mbostock/5577023)
dotcolours = brewer2mpl.get_map('RdYlGn', 'diverging', 11).mpl_colors
colours = brewer2mpl.get_map('Dark2', 'qualitative', 8).mpl_colors
# colourmap = pl.cm.brg #nipy_spectral, Set1,Paired
# noofcolours = 12
# colours = [colourmap(i) for i in np.linspace(0, 1, noofcolours)]

## plot dots
pl.plot(beedots, 'o', color = dotcolours[2], markeredgewidth=0.5, markeredgecolor=almost_black, markersize=4.5, alpha = 0.8)
pl.plot(plantdots, 'o', color = dotcolours[10], markeredgewidth=0.5, markeredgecolor=almost_black, markersize=4.5, alpha = 0.8)

## plot lines
# find unique interactions in the whole data set
uniqueints = []
for i in range(len(bees)):
  if (bees[i], plants[i]) not in uniqueints:
    uniqueints.append((bees[i], plants[i]))

# find max number of times an interaction appears in beeplants
beeplants = []
for i in range(len(bees)):
  beeplants.append((bees[i], plants[i]))

appearmax = 0
for i in range(len(uniqueints)):
  appearno = beeplants.count(uniqueints[i])
  if appearno > appearmax:
    appearmax = appearno
print 'Max number of appearances: ' + str(appearmax)

# define colours, alpha and widths for lines dependent on number of int appearances
colours2 = [colours[i] for i in [7, 7, 2, 2, 3, 3]]
alphanos = [0.1, 0.1, 0.7, 0.7, 1.0, 1.0]
widths = [0.8, 0.8, 1.0, 1.0, 1.1, 1.1]
  
# Assign colour , alpha and width to each interaction
colourdict = {}
alphadict = {}
widthdict = {}
for i in range(len(uniqueints)):
  appearno = beeplants.count(uniqueints[i])
  colourdict[uniqueints[i]] = colours2[appearno - 1]
  alphadict[uniqueints[i]] = alphanos[appearno - 1]
  widthdict[uniqueints[i]] = widths[appearno - 1]

# plot lines/interactions within months
def simpleline(x1, x2, y1, y2, colour, alphano, width):
  'draw a line between two points in plot'
  gradient = (y2-y1)/(x2-x1)
  intercept = y2 - gradient * x2
  x = np.arange(x1, x2 + 1)
  pl.setp(pl.plot(x, gradient*x + intercept), color=colour, alpha = alphano, linewidth=width)

for i in range(0, upperbound, 4):
  x1 = i # x value of bee in bees
  x2 = i + 2 # x value of plant in plants
  e = i / 4
  startindex = startofmonths[e]
  nextindex = startofmonths[e + noofmonths]
  p = startindex
  while p < nextindex:
    simpleline(x1, x2, bees[p], plants[p], colourdict[(bees[p], plants[p])], alphadict[(bees[p], plants[p])], widthdict[(bees[p], plants[p])])
    p += 1

## plotting lines between months
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
    simpleline(x1, x2, plants[cint], bees[cint], colourdict[(bees[cint], plants[cint])], alphadict[(bees[cint], plants[cint])], widthdict[(bees[cint], plants[cint])])


########## Making plot pretty ##########

##Axis
# axis limits
maxbee2 = max(int(bee) for bee in bees)
maxplant2 = max(int(plant) for plant in plants)
upperylimit = maxbee2
if maxbee2 < maxplant2:
  upperylimit = maxplant2
pl.axis([-1, 47, 0, upperylimit + 40])

## axis ticks
# major ticks at where labels are, minor ticks at where dots are plotted                                   
minor_ticks = np.arange(0, upperbound, 2)
major_ticks = np.arange(1, upperbound, 4)

# plot x ticks
pl.gca().set_xticks(minor_ticks, minor=True)
pl.gca().xaxis.set_ticks_position('bottom')
# pl.xticks(major_ticks)
# pl.xticks(minor_ticks)

# set x tick length
pl.tick_params(axis = 'both', which = 'major', length = 0 )
pl.tick_params(axis = 'both', which = 'minor', length = 5 )
#direction = 'inout'
#pl.setp(pl.gca().get_xmajorticklabels(), visible=False)
#pl.setp(pl.gca().get_xminorticklabels(), visible=True)

# x axis labels
pl.xticks(range(len(monthsdisplay)), monthsdisplay, size = 16)

# set y ticks
pl.gca().set_yticks(())

## set grid
# common grid
# xaxis.grid(linestyle='-', linewidth='0.5', color='black', alpha=0.5)
# pl.grid(True, which = 'both')
# different settings for the grids:
pl.gca().grid(True, which='minor', linestyle='--', alpha=0.3) 

## titles and axis labels
title = pl.title('Pollinator Networks in Cerrado, a Tropical Savanna (1996 - 1997)', size = 18)
title.set_position([.37, 1.05])
# pl.xlabel("this is X", size=10)

## colour background according to season
pl.axvspan(-1, 23, facecolor='r', alpha=0.05)
pl.axvspan(23, 48, facecolor='c', alpha=0.05)
pl.text(9, 215, 'Dry Season', size = 16)
pl.text(30, 215, 'Wet Season', size = 16)

# remove borders
pl.gca().spines['top'].set_visible(False)
pl.gca().spines['right'].set_visible(False)
pl.gca().spines['left'].set_visible(False)


########## Creating proxy artists for legends ##########

## Legend colours
light_grey = np.array([float(248)/float(255)]*3)

## legend for lines
# colours2 = [colours[i] for i in [7, 7, 2, 2, 3, 3]]
coloursused = [colours2[0], colours2[2], colours2[4]]
handles1 = []
for i in coloursused:
  handle1 = mlines.Line2D([], [], color= i , linewidth=2, markersize = 0.2)
  handles1.append(handle1)
labelsstr1 = '1 - 2 months, 3 - 4 months, 5 - 6 months'
labels1 = labelsstr1.split(', ')

first_legend = pl.legend(handles1, labels1, frameon=True, title='Interaction present in:', ncol=2, 
bbox_to_anchor=(1.02, 1.08), loc=1, borderaxespad=0., prop={'size':10}, handletextpad=0.2,
borderpad=0.5, labelspacing=0.2, columnspacing=0.5)
first_legend.get_title().set_fontsize('11') 
first_legend.get_frame().set_linewidth(0.0)
first_legend.get_frame().set_color(light_grey)
first_legend.get_title().set_position((-30, 0)) 
pl.gca().add_artist(first_legend)

## legend for dots
beedotrep = mlines.Line2D([], [], linestyle="none", marker='o', color=dotcolours[2], markeredgewidth=0.5, markeredgecolor=almost_black, markersize=8, alpha=0.7)
plantdotrep = mlines.Line2D([], [], linestyle="none", marker='o', color=dotcolours[10], markeredgewidth=0.5, markeredgecolor=almost_black, markersize=8, alpha=0.7)
handles2 = [beedotrep, plantdotrep]
labels2 = ['Bee node', 'Plant node']

second_legend = pl.legend(handles2, labels2, frameon=True, ncol=2, 
bbox_to_anchor=(1.02, 1.06), loc=4, borderaxespad=0., prop={'size':10}, handletextpad=0.5, numpoints=1, 
borderpad=0.8, labelspacing=1, columnspacing=1.9)
second_legend.get_frame().set_linewidth(0.0)
second_legend.get_frame().set_color(light_grey)
pl.gca().add_artist(second_legend)


########## Save plot ##########

pl.tight_layout()
plotname = 'perfectnetwork1'
plotpath = '../results/' + plotname + '.pdf'
pl.savefig(plotpath)

pl.show()