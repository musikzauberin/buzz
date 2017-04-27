import csv
import operator
import decimal
import numpy as np
import matplotlib.pyplot as pl
import calendar
import sys
import os.path

#finding amt of data
h = open('../data/rearranged/OldCerradoData1-monthly.csv','rb')
data = csv.reader(h)

months = []
days = []
years = []
bees = []
plants = []

for column in data:
  months.append(column[0])
  days.append(column[1])
  years.append(column[2])
  bees.append(column[3])
  plants.append(column[4])

h.close()

#remove header
for i in [months, days, years, bees, plants]:
  del i[0]

datalen = len(months)
duplicateno = 0
duplicates = []

uniqueint = []
for i in range(datalen):
  e = i + 1
  while e < datalen:
    if bees[i] == bees[e]:
      if plants[i] == plants[e]:
        if str(i) + str(e) not in uniqueint:
          uniqueint.append(str(i) + str(e))
          print uniqueint
          print i 
          print e
          e += 1
      else:
        e += 1
    else:
      e += 1

print len(uniqueint)
