import csv
import operator
import decimal
import numpy as np
import matplotlib.pyplot as pl
import calendar
import sys
import os.path

def simpleline(x1, y1, x2, y2):
  gradient = (y2-y1)/(x2-x1)
  intercept = y2 - gradient * x2
  x = np.arange(x1, x2)
  print x
  pl.plot(x, gradient*x + intercept)

x1 = 0
x2 = 2
y1 = 1
y2 = 4

simpleline(x1, y1, x2, y2)

pl.show()