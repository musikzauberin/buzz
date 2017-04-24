"""Analysing data and plotting general graphs"""

__author__ = 'Jia Le Lim'
__version__ = '0.0.9'

import csv
import operator
import decimal
import numpy as np
import matplotlib.pyplot as pl
import calendar
import sys
import os.path

with open('../data/CerradoBoaVentura/rearrange/ClimNetDataLnx.csv') as csvfile:
   reader = csv.DictReader(csvfile, delimiter=',')
   rows = list(reader)
   data = []
   for row in rows:
      i = []
      i.append(row['Plant']) # Your data columns
      i.append(row['Bee'])
      data.append(map(float, i)) # convert to float
      
print data[0]
print data[0][1]