'''Combine multiple csv files into one'''
import sys
sys.path.insert(0,'/usr/local/lib/python2.7/site-packages')
import pandas as pd 

a = pd.read_csv("/Users/lele/Documents/MacDocuments/github/buzz/results/CorrectedNewCerrado/Bivariateplots/turnovers/TurnoverCoefficients(CorrectedNew).csv")
b = pd.read_csv("/Users/lele/Documents/MacDocuments/github/buzz/results/CorrectedNewCerrado/Bivariateplots/monthlydiff/DiffClimateCoefficients(CorrectedNew).csv")

c = pd.read_csv("/Users/lele/Documents/MacDocuments/github/buzz/results/CorrectedNewCerrado/Bivariateplots/monthlyaverage/AvgClimateCoefficients(CorrectedNew).csv")
d = pd.read_csv("/Users/lele/Documents/MacDocuments/github/buzz/results/CorrectedNewCerrado/Bivariateplots/monthdiff&turnover/Turnover&ClimateDiff(CorrectedNew).csv")
e = pd.read_csv("/Users/lele/Documents/MacDocuments/github/buzz/results/CorrectedNewCerrado/Bivariateplots/monthavg&turnover/Turnover&ClimateAvg(CorrectedNew).csv")

df_list = []
df_list.append(a)
df_list.append(b)
df_list.append(c)
df_list.append(d)
df_list.append(e)

full_df = pd.concat(df_list)

full_df.to_csv('/Users/lele/Documents/MacDocuments/github/buzz/results/CorrectedNewCerrado/Bivariateplots/AllCoefficients(CorrectedNew).csv')
# index = False removes first column of numbering