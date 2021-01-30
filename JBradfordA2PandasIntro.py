# Joseph Bradford
# CS3580 Data Science Algorithms
# Assignment 2 : Introduction to Pandas Library

import pandas as pd
import math
import matplotlib.pyplot as plt

# played with display options
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.expand_frame_repr', False)

# 1
df = pd.read_csv('weatherHistory.csv')
df['Formatted Date'] = pd.to_datetime(df['Formatted Date'], utc=True)
print('#1: Read in Data Successful\n')

# 2
print('#2 First 5 Temperature Values(From Temperature (C)): ')
print(df['Temperature (C)'].head())
print()

# 3
print('#3 Last 5 Temperature Values(From Temperature (C)): ')
print(df['Temperature (C)'].tail())
print()

# 4
print('#4 Min, Max, Standard Deviation of Temperatures(From Temperature (C))')
print('Min Temperature: ' + str(df['Temperature (C)'].min()))
print('Max Temperature: ' + str(df['Temperature (C)'].max()))
print('Temperature Standard Deviation: ' + str(df['Temperature (C)'].std()))
print()


# 5
# First Create List of desired weather to get aggregate data for
# Then filter, groupby, aggregate
print('#5: Min, Max, Standard Deviation (From Temperature (C)) for Summary = Clear, Partly Cloudy, Foggy')
weather = ['Clear', 'Partly Cloudy', 'Foggy']
print(df[df.Summary.isin(weather)].groupby('Summary')['Temperature (C)'].agg(['min', 'max', 'std']))
print()

# 6
# I use the apply function, to apply a function to all values and assign
# to a new column named Radians
print('#6: Convert Wind Bearing (degrees) to radians and apply to new column')
df['Radians'] = df['Wind Bearing (degrees)'].apply(math.radians)
print('6.1 Describe "Radians" column:')
print(df['Radians'].describe())
print()

#7
# Filter and save as a new dataframe
# use pandas function to export html data file
print('#7: Create new dataframe with only Rows with 0.6 <= Humidity <= 0.7')
df2 = df[(df.Humidity >= .6) & (df.Humidity <= .7)]
print('7.1 Describe "Wind_Speed (km/h)" column:')
print(df2['Wind Speed (km/h)'].describe())
print('Export this new dataframe to Bradford_Joseph.html')
df2.to_html('Bradford_Joseph.html')
print('File Bradford_Joseph.html created\n')

# #8

# Just for fun, practice with functions
# Prints a date difference in Years, Months, and Days
def date_difference(high, low):
    if(high.hour - low.hour) >= 0:
        dys = high.day - low.day
    else:
        dys = high.day - low.day - 1
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
    print("Date Range: " + str(yr) + "years " + str(mth) +
          "months " + str(dys) + "days")

# I use this function to convert to Farenheight so that I can create
# a visual that displays temperatures in a unit I am more familiar with
def cToF(x):
    return ((x * 9/5) + 32)

# 8.1
print('#8:\n8.1(Date Range of entire dataset):')
date_difference(df['Formatted Date'].max(), df['Formatted Date'].min())
print('Part 2(Data Characterization): ')

#create Farenheight Column for American Audience(me)
df['Temp(F)'] = df['Temperature (C)'].apply(cToF)

# 8.2
print('8.2.1')
print('This chart shows the average temperatures in Farenheight for each hour of each month,')
print('I need to learn how labeling and such works, but I found this graph')
print('very useful, the 12 peaks indicate the average "high" for each month')
print('and the valleys indicate the average "low" for each month')
print('This is a place that is hot during the summer, and cold during the winter')
print('Judging by temperatures alone, this place is not much different from the Salt Lake City area.')
print('Source: https://www.rssweather.com/climate/Utah/Salt%20Lake%20City/')
print()

# This graph characterizes the average highs and lows for each month,
# As a visual tool for understanding the data I found it useful
# With a bit more practice with this tool, I will understand how to format it for
# an audience
print(df.groupby([df['Formatted Date'].dt.month, df['Formatted Date'].dt.hour])['Temp(F)'].mean())
df.groupby([df['Formatted Date'].dt.month, df['Formatted Date'].dt.hour])['Temp(F)'].mean().plot()
plt.show()
print('Temp(F) Statistics:')
print(df['Temp(F)'].describe())
print()

# Humidity Characterization
print('8.2.2')
print('This place is quite humid, with an average Humidity of 73%')
print('This probably indicates that it is a coastal city')
print('Source: https://www.currentresults.com/Weather/US/humidity-city-annual.php')
print('\nHumidity Statistics:')
print(df.Humidity.describe())
print('\nAverage by month:')
print(df.groupby([df['Formatted Date'].dt.month])['Humidity'].mean())
print()

#Wind Characterization
print('8.2.3')
print('With an average wind speed of almost 11 km/h it is not a super windy city')
print('So ordinary it is hard to make a guess of where it might be')
print('Source: https://www.currentresults.com/Weather/US/wind-speed-city-annual.php')
print('\nWind Statistics')
print(df['Wind Speed (km/h)'].describe())
print()

#Would I like to live here?
print('8.2.4')
print('This place seems to be a fairly pleasant place to live')
print('It is quite humid, and cloudy most of the time,')
print('but it is not a brutally hot or cold climate.')
print('Maybe not a perfect place to live, but I would not complain too much')
print('Weather Summary value counts:')
print(df.Summary.value_counts())
