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
import matplotlib.cm as cm
import matplotlib.image as image

def longest(listoflists):
  'find length of longest list in list of lists'
  if(not isinstance(listoflists, list)): 
    return(0)
  else:
    return(max([len(onelist) for onelist in listoflists]))

filename = 'CorrectedNewCerradoData1-monthly(New).csv'
pathname = '../../data/rearranged/new/' + filename
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

# insert dummy values to let every beedot be the same length
ideallen = longest(beelists)
for beelist in beelists:
  while len(beelist) < ideallen:
    beelist.append(-10)

# insert dummy values to let every plantdot be the same length
ideallen2 = longest(plantlists)
for plantlist in plantlists:
  while len(plantlist) < ideallen2:
    plantlist.append(-10)

## create x axis labels
monthlabels = 'Nov, Dec, Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct'
monthlabels = monthlabels.split(', ')
monthdisplay = monthlabels*2
monthdisplay.append('Jun')

######### Plotting data ##########

## figure size
# figure(num=None, figsize=(8, 6) #ininches, dpi=80 #noofpixels, facecolor='w', edgecolor='k')
pl.figure(figsize=(20,4))

## All needed colours
RdGy = brewer2mpl.get_map('RdGy', 'diverging', 11).mpl_colors
PRGn = brewer2mpl.get_map('PRGn', 'diverging', 11).mpl_colors
Spectral = brewer2mpl.get_map('Spectral', 'diverging', 11).mpl_colors
Blues = brewer2mpl.get_map('Blues', 'sequential', 9).mpl_colors
Dark2 = brewer2mpl.get_map('Dark2', 'qualitative', 8).mpl_colors
Paired = brewer2mpl.get_map('Paired', 'qualitative', 12).mpl_colors

colordict1 = {'Bint': RdGy[10], 'Bos': Paired[11], 'Bst': Dark2[5], 'Bs': Spectral[10], 'Bbee': PRGn[3], 'Bplant': PRGn[9], \
'Precip': Blues[4], 'Humid': Blues[8], 'Temp': Paired[5], 'TempMax': Paired[4], 'TempRange': RdGy[0]}


light_grey = np.array([float(248)/float(255)]*3)
almost_black = '#262626'


## Get "Set2" colors from ColorBrewer (all colorbrewer scales: http://bl.ocks.org/mbostock/5577023)
# color_palette("cubehelix", 10)
beecolour = colordict1['Bbee']
plantcolour = colordict1['Bplant']
colours = [RdGy[9], Paired[11], Paired[1], Paired[5]]
# brewer2mpl.get_map('Dark2', 'qualitative', 8).mpl_colors
# colourmap = pl.cm.brg #nipy_spectral, Set1,Paired
# noofcolours = 12
# colours = [colourmap(i) for i in np.linspace(0, 1, noofcolours)]

## plot dots
beexcoord = np.arange(0, len(beelists)*2, 2)
plantxcoord = np.arange(1, len(plantlists)*2, 2)

pl.plot(beexcoord, beelists, 'o', color = beecolour, markeredgewidth=0.5, markeredgecolor=almost_black, markersize=4.5, alpha = 1)
pl.plot(plantxcoord, plantlists, 'o', color = plantcolour, markeredgewidth=0.5, markeredgecolor=almost_black, markersize=4.5, alpha = 0.8)

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

appearnos = []
appearmax = 0
for i in range(len(uniqueints)):
  appearno = beeplants.count(uniqueints[i])
  appearnos.append(appearno)
  if appearno > appearmax:
    appearmax = appearno
print 'Max number of appearances: ' + str(appearmax)

for i in range(appearmax+1):
  print i, appearnos.count(i)
print len(appearnos)

# define colours, alpha and widths for lines dependent on number of int appearances
colours2 = [colours[i] for i in [0, 0, 2, 3]]
alphanos = [0.4, 0.4, 1.0, 1.0]
widths = [0.5, 0.5, 1.4, 1.4]

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

for i in range(0, (len(startofmonths)-1)*2, 2):
  x1 = i # x value of bee in bees
  x2 = i + 1 # x value of plant in plants
  e = i / 2
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
  x1 = 2 * i + 1
  x2 = x1 + 1
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
pl.axis([-1, len(startofmonths)*2-2, 0, upperylimit + 50])

## axis ticks
# major ticks at where labels are, minor ticks at where dots are plotted
minor_ticks = np.arange(0, len(startofmonths)*2-2)
major_ticks = np.arange(0.5, len(startofmonths)*2-2, 2)

# plot x ticks
pl.gca().set_xticks(minor_ticks, minor=True)
pl.gca().xaxis.set_ticks_position('bottom')

# set x tick length
pl.tick_params(axis = 'x', which = 'major', length = 0 )
pl.tick_params(axis = 'x', which = 'minor', length = 5 )
pl.tick_params( axis='y', which='both', left='off', right='off', labelleft='off')

# x axis labels
pl.xticks(major_ticks, monthdisplay, size = 14)

## set grid
pl.gca().grid(True, which='minor', linestyle='-', alpha=0.5)

## titles and axis labels
title = pl.title('Pollinator Networks at the IBGE site in Cerrado (2008-2009)', size = 18)
title.set_position([.37, 1.05])

# colour background according to season
for i in np.arange(-1, 9.0, 2):
  pl.axvspan(i, i+1, facecolor='c', alpha=0.1)
for i in np.arange(0, 9.5, 2):
  pl.axvspan(i, i+1, facecolor='c', alpha=0.05)
pl.axvspan(9, 9.5, facecolor='c', alpha=0.1)

pl.axvspan(9.5, 10, facecolor='r', alpha=0.1)
for i in np.arange(10, len(startofmonths)*2-5, 2):
  pl.axvspan(i, i+1, facecolor='r', alpha=0.05)
for i in np.arange(11, len(startofmonths)*2-5, 2):
  pl.axvspan(i, i+1, facecolor='r', alpha=0.1)
  
pl.axvspan(len(startofmonths)*2-5, len(startofmonths)*2-4.5, facecolor='r', alpha=0.1)
pl.axvspan(len(startofmonths)*2-4.5, len(startofmonths)*2-4, facecolor='c', alpha=0.1)
pl.axvspan(len(startofmonths)*2-4, len(startofmonths)*2-3, facecolor='c', alpha=0.05)
pl.axvspan(len(startofmonths)*2-3, len(startofmonths)*2-2, facecolor='c', alpha=0.1)

# pl.axvspan(11.5, len(startofmonths)*2-2, facecolor='r', alpha=0.08)
pl.text(3.5, 230, 'Wet Season', size = 14)
pl.text(15.5, 230, 'Dry Season', size = 14)

# # colour background according to season
# for i in np.arange(-1, 11.0, 2):
#   pl.axvspan(i, i+1, facecolor='c', alpha=0.2)
# for i in np.arange(0, 11.5, 2):
#   pl.axvspan(i, i+1, facecolor='c', alpha=0.08)
# pl.axvspan(11, 11.5, facecolor='c', alpha=0.2)
#
# pl.axvspan(11.5, 12, facecolor='r', alpha=0.2)
# for i in np.arange(12, len(startofmonths)*2-2, 2):
#   pl.axvspan(i, i+1, facecolor='r', alpha=0.08)
# for i in np.arange(13, len(startofmonths)*2-2, 2):
#   pl.axvspan(i, i+1, facecolor='r', alpha=0.2)
#
#
# # pl.axvspan(11.5, len(startofmonths)*2-2, facecolor='r', alpha=0.08)
# pl.text(4.5, 230, 'Wet Season', size = 14)
# pl.text(16.5, 230, 'Dry Season', size = 14)

# remove borders
pl.gca().spines['top'].set_visible(False)
pl.gca().spines['right'].set_visible(False)
pl.gca().spines['left'].set_visible(False)


########## Creating proxy artists for legends ##########

## Legend colours
light_grey = np.array([float(248)/float(255)]*3)

## legend for lines
# colours2 = [7, 7, 7, 0, 0, 0, 1, 1, 1, 3, 3, 3, 3]
coloursused = [colours2[0], colours2[2], colours2[3]]
handles1 = []
for i in coloursused:
  handle1 = mlines.Line2D([], [], color= i , linewidth=2, markersize = 0.2)
  handles1.append(handle1)
labelsstr1 = '1 - 2 months, 3 months, 4 months'
labels1 = labelsstr1.split(', ')

first_legend = pl.legend(handles1, labels1, frameon=True, title='Interaction present in:', ncol=2,
bbox_to_anchor=(1.0, 1.08), loc=1, borderaxespad=0., prop={'size':10}, handletextpad=0.2,
borderpad=0.5, labelspacing=0.2, columnspacing=0.5)
first_legend.get_title().set_fontsize('11')
first_legend.get_frame().set_linewidth(0.0)
first_legend.get_frame().set_color(light_grey)
first_legend.get_title().set_position((-20, 0))
pl.gca().add_artist(first_legend)

## legend for dots
beedotrep = mlines.Line2D([], [], linestyle="none", marker='o', color=beecolour, markeredgewidth=0.5, markeredgecolor=almost_black, markersize=8, alpha=1)
plantdotrep = mlines.Line2D([], [], linestyle="none", marker='o', color=plantcolour, markeredgewidth=0.5, markeredgecolor=almost_black, markersize=8, alpha=0.7)
handles2 = [beedotrep, plantdotrep]
labels2 = ['Bee node', 'Plant node']

second_legend = pl.legend(handles2, labels2, frameon=True, ncol=2,
bbox_to_anchor=(1.01, 1.06), loc=4, borderaxespad=0., prop={'size':10}, handletextpad=0.5, numpoints=1,
borderpad=0.8, labelspacing=1, columnspacing=1.9)
second_legend.get_frame().set_linewidth(0.0)
second_legend.get_frame().set_color(light_grey)
pl.gca().add_artist(second_legend)

########## Save plot ##########

pl.tight_layout()
plotname = 'network(CorrectedNew)'
plotpath = '../../results/CorrectedNewCerrado/Timeplots/' + plotname + '.pdf'
pl.savefig(plotpath)

pl.show()