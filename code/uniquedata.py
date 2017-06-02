import csv
import operator
import decimal
import numpy as np
import matplotlib.pyplot as pl
import calendar
import sys
import os.path

#finding amt of data
h = open('../data/rearranged/OldCerradoData.csv','rb')
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
  if [bees[i], plants[i]] not in uniqueint:
    uniqueint.append([bees[i], plants[i]])

print len(uniqueint)
print uniqueint

noofdays = 0
for i in range(len(days)):
  if days[i] != days[i-1]:
    noofdays += 1

print noofdays
print len(bees)
print len(set(bees))
print len(set(plants))
