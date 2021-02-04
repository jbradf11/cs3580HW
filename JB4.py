import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('weatherAUS.csv', parse_dates=['Date'])

#P1
def date_difference(high, low):
    dys = high.day - low.day
    if dys >= 0:
        mth = high.month - low.month
    else:
        dys+=31 # need to replace this with something that works for all months
        mth = high.month - low.month -1
    if mth >= 0:
        yr = high.year - low.year
    else:
        mth+=12
        yr = high.year - low.year -1
    print("Date Range: " + str(dys) + "days " + str(mth) +
          "months " + str(yr) + "years")

print('\nPart 1: Basic Info\n')
print ('1.1: Date Range in Days, Months and Years')
print(df.Date.max())
print(df.Date.min())
date_difference(df.Date.max(),df.Date.min())

print('\n1.2 average MinTemp by month')
MTbymonth = df.groupby([df.Date.dt.month, df.Date.dt.strftime('%m')]).MinTemp.mean()
print(MTbymonth)
df.groupby(df.Date.dt.month).MinTemp.mean().plot.bar()
plt.show()

#1.4

print('\n1.4.1 - Unique Locations\nThere are %d unique locations'% df.groupby('Location').Location.count().count())
print('1.4.2 - Top 5 cities by average Rainfall')
print(df.groupby('Location').Rainfall.mean().sort_values(ascending=False).head())
