'''Plot across time for all turnovers (1995-1997)'''

import csv
import operator
import decimal
import numpy as np
import matplotlib.pyplot as pl
import matplotlib.lines as mlines
import calendar
import sys
import os.path

h = open('../data/rearranged/new/AllTurnoverOldCerrado.csv','rb')
data = csv.reader(h)


########## Inputting data into lists ##########

# copy and paste all headers in data twice
[years, months, bints, beeturnovers, plantturnovers, specturnovers, osturnovers, stturnovers, \
avgprecips, avgtemps, avgmaxtemps, avgtempranges, avghumids, \
diffprecips, difftemps, diffmaxtemps, difftempranges, diffhumids] = ([] for i in range(len(next(data))))

headers2 = [years, months, bints, beeturnovers, plantturnovers, specturnovers, osturnovers, stturnovers, \
avgprecips, avgtemps, avgmaxtemps, avgtempranges, avghumids, \
diffprecips, difftemps, diffmaxtemps, difftempranges, diffhumids]

for column in data:
  for j, i in enumerate(headers2):
    i.append(column[j])

h.close()


########## Manipulating data ##########

intervals = [0, 12, len(bints)]


########## Plotting data ##########

def makesubplotnice():
  'make every subplot the same, nice and simple'

  # subplot labels
  pl.ylabel('Dissimilarity', size=12)
  
  monthlabels = 'Jun, Jul, Aug, Sep, Oct, Nov, Dec, Jan, Feb, Mar, Apr, May, Jun'
  monthlabels = monthlabels.split(', ')

  minor_ticks = np.arange(-0.5, 12.5, 1)
  major_ticks = np.arange(1, 12, 1)
  pl.tick_params(axis = 'x', which = 'major', length = 0 )
  pl.tick_params(axis = 'x', which = 'minor', length = 10, direction = 'inout')
  pl.gca().set_xticks(minor_ticks, minor=True)
  pl.gca().grid(True, axis = 'x', which='minor', linestyle='-', alpha=0.3)
  pl.gca().grid(False, which='major', axis = 'x')
  pl.xticks(minor_ticks, monthlabels)
  pl.gca().grid(True, axis = 'y', alpha = 0.5)

  # remove borders
  pl.gca().spines['top'].set_visible(False)
  pl.gca().spines['right'].set_visible(False)
  pl.gca().xaxis.set_ticks_position('bottom')
  pl.gca().yaxis.set_ticks_position('left')
  
  # background color
  pl.axvspan(-1, 3.5, facecolor='r', alpha=0.1)
  pl.axvspan(3.5, 9.5, facecolor='c', alpha=0.1)
  pl.axvspan(9.5, 13.5, facecolor='r', alpha=0.1)

  
  # legend
  legend = pl.legend(loc='upper right', frameon=True, numpoints=1)
  light_grey = np.array([float(248)/float(255)]*3)
  legend.get_frame().set_linewidth(0.0)
  legend.get_frame().set_color(light_grey)


# colors
import brewer2mpl
RdGy = brewer2mpl.get_map('RdGy', 'diverging', 11).mpl_colors
PRGn = brewer2mpl.get_map('PRGn', 'diverging', 11).mpl_colors
Spectral = brewer2mpl.get_map('Spectral', 'diverging', 11).mpl_colors
Blues = brewer2mpl.get_map('Blues', 'sequential', 9).mpl_colors
Dark2 = brewer2mpl.get_map('Dark2', 'qualitative', 8).mpl_colors
Paired = brewer2mpl.get_map('Paired', 'qualitative', 12).mpl_colors

colordict = {'Bint': RdGy[10], 'Bos': Paired[11], 'Bst': Dark2[5], 'Bs': Spectral[10], 'Bbee': PRGn[3], 'Bplant': PRGn[9], \
'Precip': Blues[4], 'Humid': Blues[8], 'Temp': RdGy[0], 'TempMax': Paired[4], 'TempRange': Paired[5]}

light_grey = np.array([float(248)/float(255)]*3)
almost_black = '#262626'

# plot size
pl.figure(figsize=(12,9))

# first plot (1995-1996), Bint, Bos, Bst
pl.subplot(4, 1, 1)
pl.axis([-1, 13, -0.05, 1.05])
pl.plot(bints[intervals[0]:intervals[1]], marker = 'o', color = colordict['Bint'], label = r'$\beta_{int}$', markeredgewidth=0.5, markeredgecolor=almost_black)
pl.plot(osturnovers[intervals[0]:intervals[1]], marker = 'o', color = colordict['Bos'], label = r'$\beta_{rw}$', markeredgewidth=0.5, markeredgecolor=almost_black)
pl.plot(stturnovers[intervals[0]:intervals[1]], marker = 'o', color = colordict['Bst'], label = r'$\beta_{st}$', markeredgewidth=0.5, markeredgecolor=almost_black)
pl.title('BBG site in Cerrado (1995-1996)', size = 16)
makesubplotnice()

# second plot (1995-1996), Bs, Bplant, Bbee
pl.subplot(4, 1, 2)
pl.axis([-1, 13, 0.4, 1.05])
pl.plot(specturnovers[intervals[0]:intervals[1]], marker = 'o', color = colordict['Bs'], label = r'$\beta_{S}$', markeredgewidth=0.5, markeredgecolor=almost_black)
pl.plot(beeturnovers[intervals[0]:intervals[1]], marker = 'o', color = colordict['Bbee'], label = r'$\beta_{Bee}$', markeredgewidth=0.5, markeredgecolor=almost_black)
pl.plot(plantturnovers[intervals[0]:intervals[1]], marker = 'o', color = colordict['Bplant'], label = r'$\beta_{Plant}$', markeredgewidth=0.5, markeredgecolor=almost_black)
makesubplotnice()

# third plot (1996-1997), Bint, Bos, Bst
pl.subplot(4, 1, 3)
pl.axis([-1, 13, -0.05, 1.05])
pl.plot(bints[intervals[1]:intervals[2]], marker = 'o', color = colordict['Bint'], label = r'$\beta_{int}$', markeredgewidth=0.5, markeredgecolor=almost_black)
pl.plot(osturnovers[intervals[1]:intervals[2]], marker = 'o', color = colordict['Bos'], label = r'$\beta_{rw}$', markeredgewidth=0.5, markeredgecolor=almost_black)
pl.plot(stturnovers[intervals[1]:intervals[2]], marker = 'o', color = colordict['Bst'], label = r'$\beta_{st}$', markeredgewidth=0.5, markeredgecolor=almost_black)
pl.title('BBG site in Cerrado (1996-1997)', size = 16)
makesubplotnice()

# fourth plot (1996-1997), Bs, Bplant, Bbee
pl.subplot(4, 1, 4)
pl.axis([-1, 13, 0.4, 1.05])
pl.plot(specturnovers[intervals[1]:intervals[2]], marker = 'o', color = colordict['Bs'], label = r'$\beta_{S}$', markeredgewidth=0.5, markeredgecolor=almost_black)
pl.plot(beeturnovers[intervals[1]:intervals[2]], marker = 'o', color = colordict['Bbee'], label = r'$\beta_{Bee}$', markeredgewidth=0.5, markeredgecolor=almost_black)
pl.plot(plantturnovers[intervals[1]:intervals[2]], marker = 'o', color = colordict['Bplant'], label = r'$\beta_{Plant}$', markeredgewidth=0.5, markeredgecolor=almost_black)
makesubplotnice()

print bints[12], osturnovers[12], stturnovers[12], specturnovers[12], beeturnovers[12], plantturnovers[12]


# overall
pl.tight_layout()

plotpath = '../' + 'TimeplotTurnovers(old)' + '.pdf'
pl.savefig(plotpath)

pl.show()