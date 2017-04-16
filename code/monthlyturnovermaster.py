#!/usr/bin/env python


"""Calculating monthly turnover in Cerrado"""

__author__ = 'Jia Le Lim'
__version__ = '0.0.4'

import csv
import operator
import decimal
import numpy as np
import matplotlib.pyplot as pl
import calendar


# to run, type:
# python test.py filename.txt
# or you can also do:
# python test.py "my file name has a space.txt"
# but you have to use " and not '
import sys
import os.path

if len(sys.argv) < 2:
  print 'You need to enter a file name!'
elif os.path.isfile(sys.argv[1]):
  print 'Valid file!'
else:
  print 'Invalid file!'

print sys.argv

