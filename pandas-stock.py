#!/usr/bin/env python

import pandas as pd
import glob
import re
import matplotlib.pyplot as plt

print "### Auto Stock Prices with Python and Panda ###"

stockSymbol = '*'  # Example: fm
batchGroup = "20000101-20161231"
filePath = "/Users/jmcmaster/projects/python-pandas/stock-price"

fields = ['Symbol', 'Company']
file = filePath + "/" + "reference-symbol-list.csv.gz"
symbolDict = pd.read_table(file, compression='infer',
                           header=1).to_dict()

print "--- Symbol Dictionary ---"
print symbolDict

fileList = glob.glob(filePath + "/" +
                     "stock-price." +
                     stockSymbol + "." +
                     batchGroup + ".csv.gz")
df = pd.DataFrame()
dfFileList = []
for file in fileList:
    dfFile = pd.read_csv(file, compression='infer',
                         index_col=None, header=0)
    try:
        symbol = re.search(".*/stock-price\.(.+?)\." +
                           batchGroup + ".csv",
                           file).group(1)
        dfFile['Symbol'] = symbol.upper()
        dfFile['Company'] = symbolDict.get(symbol.lower(), "Unknown")
    except AttributeError:
        dfFile['Symbol'] = ''
        dfFile['Company'] = ''
    dfFileList.append(dfFile)
df = pd.concat(dfFileList)

print "--- Review Dataframe Types ---"
print df.columns
print df.dtypes
df['Date'] = df['Date'].astype('datetime64[ns]')
print df.dtypes

print "--- DataFrame Summary ---"
print "Records: " + "{:,.0f}".format(len(df.index))
print df.head(3)
print "..."
print df.tail(3)

print "--- Plot ---"

plt.figure()
df.pivot(index='Date',
         columns='Symbol',
         values='Close').plot()
plt.legend(loc='best')

recent = df['Date'] >= '2010-01-01'
plt.figure()
df[recent].pivot(index='Date',
                 columns='Symbol',
                 values='Close').plot()
plt.legend(loc='best')

lower = df['Date'] >= '2007-01-01'
upper = df['Date'] <= '2010-12-31'
plt.figure()
df[lower & upper].pivot(index='Date',
                        columns='Symbol',
                        values='Close').plot()
plt.legend(loc='best')


recent = df['Date'] >= '2010-01-01'
select = (df['Symbol'] == 'TSLA') | (df['Symbol'] == 'F')
# select = df['Symbol'].isin(['TSLA', 'F'])
plt.figure()
df[recent & select].pivot(index='Date',
                          columns='Symbol',
                          values='Close').plot()
plt.legend(loc='best')
