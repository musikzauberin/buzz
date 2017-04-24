import csv
import operator
import decimal
import numpy as np
import matplotlib.pyplot as pl
import calendar
import sys
import os.path

months = []
days = []
years = []
bees = []
plants = []

h = open('../data/rearranged/OldCerradoData.csv','rb')

columns = [column for column in csv.reader(h)]

h = open('../data/rearranged/OldCerradoData.csv','rb')
rows = [row for row in csv.reader(h)]


print len(rows)
print len(columns)
