timeinterval = raw_input('Turnover rates in months or years?')
timeinterval = timeinterval.lower()
print timeinterval

while timeinterval is 'months' or timeinterval is 'years':
  timeinterval = raw_input('Turnover rates in MONTHS or YEARS? If you want something else do the script yourself.')
  print timeinterval
  timeinterval = timeinterval.lower()