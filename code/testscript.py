timeinterval = raw_input('Turnover rates in months or years?')

while timeinterval.lower() != 'months' and timeinterval.lower() != 'years':
  timeinterval = raw_input('Turnover rates in MONTHS or YEARS? If you want something else do the script yourself.')

timeinterval = timeinterval.lower()