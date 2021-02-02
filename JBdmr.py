# Joseph Bradford
# CS 3580
# Assignment 3 Data Mapping and Reduction

import pandas as pd
import math
# import matplotlib.pyplot as plt

# Read in files
dft = pd.read_csv('acs2015_census_tract_data.csv', encoding='latin-1')
dfc = pd.read_csv('acs2015_county_data.csv', encoding='latin-1')

# Create dataframe that is just State and TotalPop with Puerto Rico and DC filtered out
PBS = dfc[(dfc.State != 'Puerto Rico') & (dfc.State != 'District of Columbia'
      '')].groupby('State').TotalPop.agg(['sum']).sort_index().rename(columns={'sum':'TotalPop'})

# Part 1: Which State Has the highest % of each race

#Change Race Columns from % to a hard number by county
dfc.Hispanic = dfc.TotalPop * (dfc.Hispanic /100)
dfc.White = dfc.TotalPop * (dfc.White /100)
dfc.Black = dfc.TotalPop * (dfc.Black /100)
dfc.Native = dfc.TotalPop * (dfc.Native /100)
dfc.Asian = dfc.TotalPop * (dfc.Asian /100)
dfc.Pacific = dfc.TotalPop * (dfc.Pacific /100)

# This section takes an aggregate sum of each race by state and merges with
# The total population by state
PBSDiversity = pd.merge(PBS, dfc.groupby('State').Black.agg(['sum']).
                rename(columns={'sum':'BlackPop'}), on='State')
PBSDiversity = pd.merge(PBSDiversity, dfc.groupby('State').Hispanic.agg(['sum']).
                rename(columns={'sum':'HispanicPop'}), on='State')
PBSDiversity = pd.merge(PBSDiversity, dfc.groupby('State').White.agg(['sum']).
                rename(columns={'sum':'WhitePop'}), on='State')
PBSDiversity = pd.merge(PBSDiversity, dfc.groupby('State').Native.agg(['sum']).
                rename(columns={'sum':'NativePop'}), on='State')
PBSDiversity = pd.merge(PBSDiversity, dfc.groupby('State').Asian.agg(['sum']).
                rename(columns={'sum':'AsianPop'}), on='State')
PBSDiversity = pd.merge(PBSDiversity, dfc.groupby('State').Pacific.agg(['sum']).
                rename(columns={'sum':'PacificPop'}), on='State')

# Transform Race Population back to percents
PBSDiversity['BlackPop'] = (PBSDiversity.BlackPop / PBSDiversity.TotalPop) * 100
PBSDiversity['HispanicPop'] = (PBSDiversity.HispanicPop / PBSDiversity.TotalPop) * 100
PBSDiversity['WhitePop'] = (PBSDiversity.WhitePop / PBSDiversity.TotalPop) * 100
PBSDiversity['NativePop'] = (PBSDiversity.NativePop / PBSDiversity.TotalPop) * 100
PBSDiversity['AsianPop'] = (PBSDiversity.AsianPop / PBSDiversity.TotalPop) * 100
PBSDiversity['PacificPop'] = (PBSDiversity.PacificPop / PBSDiversity.TotalPop) * 100

#
races = ['Black', 'Hispanic', 'White', 'Native', 'Asian', 'Pacific']

# Print Results
print('\n#1) State with highest percent of each of the 6 racial demographics\n')
print('Highest %-8s Population pct: %-11s : %.2f %%'%
        (races[0],str(PBSDiversity.BlackPop.idxmax()),(PBSDiversity.BlackPop.max())))
print('Highest %-8s Population pct: %-11s : %.2f %%'%
        (races[1],str(PBSDiversity.HispanicPop.idxmax()),(PBSDiversity.HispanicPop.max())))
print('Highest %-8s Population pct: %-11s : %.2f %%'%
        (races[2],str(PBSDiversity.WhitePop.idxmax()),(PBSDiversity.WhitePop.max())))
print('Highest %-8s Population pct: %-11s : %.2f %%'%
        (races[3],str(PBSDiversity.NativePop.idxmax()),(PBSDiversity.NativePop.max())))
print('Highest %-8s Population pct: %-11s : %.2f %%'%
        (races[4],str(PBSDiversity.AsianPop.idxmax()),(PBSDiversity.AsianPop.max())))
print('Highest %-8s Population pct: %-11s : %.2f %%'%
        (races[5],str(PBSDiversity.PacificPop.idxmax()),(PBSDiversity.PacificPop.max())))

# Part 2 Highest and Lowest Unemployment % by State

# reduce
myColumns = ['State', 'TotalPop', 'Unemployment']
dfU = dfc.loc[:, myColumns]

# Convert to a hard number of unemployed people by county
dfU['UnemployedPop'] = dfU.TotalPop * (dfU.Unemployment / 100)

# Unemployment By State - Merged with total population by state
UBS = pd.merge(PBS, dfU.groupby('State').UnemployedPop.agg(['sum']).rename(columns={'sum':'UnemployedPop'}),on='State')

# Now we can get an accurate percent Unemployment by state
UBS['UnemployedPct'] = UBS.UnemployedPop/UBS.TotalPop*100
print(UBS.UnemployedPct.sort_index())

print('\n#2 States with highest and lowest Unemployment as a percent\n')
print('State with Highest Percent Unemployment : %-12s: %.2f%%'%
        (UBS.UnemployedPct.idxmax(),UBS.UnemployedPct.max()))
print('State with Lowest  Percent Unemployment : %-12s: %.2f%%'%
        (UBS.UnemployedPct.idxmin(),UBS.UnemployedPct.min()))

# Part 3 Census Tracts with drastic income inequality

myColumns = ['CensusTract','State','County','Income','Poverty','Hispanic','White','Black','Native','Asian','Pacific']
df3 = dft.loc[:, myColumns]
df3 = df3[(df3.Income >= 50000) & (df3.Poverty > 50.0)]

print('\n#3 Census Tracts with average income >= $50,000 and Poverty > 50%\n')
print('%-15s%-12s%-12s %-30s'% (df3.columns[0], df3.columns[1], df3.columns[2], 'Races > 1%'))
for tract in df3.index:
    races = []
    for x in range(5,11):
        if df3.loc[tract][x] > 1:
            races.append(df3.columns[x])
    print("%-15s%-12s%-12s%-30s"% (df3.loc[tract][0],df3.loc[tract][1],df3.loc[tract][2],str(races)))

# Part 4 Census Tracts > 57% Female Pop >= 10000
# include Tract, County, State, Races > 1%

myColumns = ['CensusTract', 'State', 'County','Hispanic', 'White', 'Black', 'Native', 'Asian', 'Pacific', 'TotalPop', 'Women']
df4 = dft.loc[:, myColumns]

df4['FemalePct'] = df4.Women / df4.TotalPop * 100
df4 = df4[(df4.FemalePct > 57) & (df4.TotalPop >= 10000)]


print('\n#4 Census Tracts with TotalPop >= 10,000 and FemalePct > 57%\n')
print('%-15s%-17s%-12s %-30s'% (df4.columns[0], df4.columns[1], df4.columns[2], 'Races > 1%'))
for tract in df4.index:
    races = []
    for x in range(3,9):
        if df4.loc[tract][x] > 1:
            races.append(df4.columns[x])
    print("%-15s%-17s%-12s%-30s"% (df4.loc[tract][0],df4.loc[tract][1],df4.loc[tract][2],str(races)))

# Part 5 Racially Diverse Census Tracts - 4 or more races at least 15%
# Include Tract, State, County, Races > 1%
myColumns = ['CensusTract', 'State', 'County','Hispanic', 'White', 'Black', 'Native', 'Asian', 'Pacific']
df5 = dft.loc[:, myColumns]
df5['Diversity'] = df5.Hispanic.apply(lambda x: 0 if (math.isnan(x)) or x/15 < 1 else 1)
df5['Diversity'] += df5.White.apply(lambda x: 0 if (math.isnan(x)) or x/15 < 1 else 1)
df5['Diversity'] += df5.Black.apply(lambda x: 0 if (math.isnan(x)) or x/15 < 1 else 1)
df5['Diversity'] += df5.Native.apply(lambda x: 0 if (math.isnan(x)) or x/15 < 1 else 1)
df5['Diversity'] += df5.Asian.apply(lambda x: 0 if (math.isnan(x)) or x/15 < 1 else 1)
df5['Diversity'] += df5.Pacific.apply(lambda x: 0 if (math.isnan(x)) or (x/15) < 1 else 1)
df5 = df5[df5.Diversity >= 4]
print(df5['Diversity'].describe())


print('\n#5 Census Tracts that are very racially diverse(4+ Races >= 15%)\n')
print('%-15s%-17s%-15s %-30s'% (df5.columns[0], df5.columns[1], df5.columns[2], 'Races > 1%'))
for tract in df5.index:
    races = {}
    for x in range(3,9):
        if df5.loc[tract][x] > 1:
            races[df5.columns[x]] = df5.loc[tract][x]
    print("%-15s%-17s%-15s%-30s"% (df5.loc[tract][0],df5.loc[tract][1],df5.loc[tract][2],str(races)))
