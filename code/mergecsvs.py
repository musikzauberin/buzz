'''Combine multiple csv files into one'''

import pandas as pd

a = pd.read_csv("../results/BivariatePlots/NewCerrado/turnovers/TurnoverCoefficients(New).csv")
b = pd.read_csv("../results/BivariatePlots/NewCerrado/monthlydiff/DiffClimateCoefficients(New).csv")

c = pd.read_csv("../results/BivariatePlots/NewCerrado/monthlyaverage/AvgClimateCoefficients(New).csv")
d = pd.read_csv("../results/BivariatePlots/NewCerrado/monthdiff&turnover/Turnover&ClimateDiff(New).csv")
e = pd.read_csv("../results/BivariatePlots/NewCerrado/monthavg&turnover/Turnover&ClimateAvg(New).csv")

df_list = []
df_list.append(a)
df_list.append(b)
df_list.append(c)
df_list.append(d)
df_list.append(e)

full_df = pd.concat(df_list)

full_df.to_csv('../results/BivariatePlots/AllCoefficients(New).csv')
# index = False removes first column of numbering