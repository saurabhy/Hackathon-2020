import warnings
import itertools
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import xlrd

from predictor import solver
plt.style.use('fivethirtyeight')

#data = pd.read_csv(r'C:\Users\saura\OneDrive\Desktop\data-1.csv', usecols=['date','storage'])

#print(data)

#data.set_index(['date'])

#data['storage'].plot(figsize=(15, 6))
#plt.show()

#retval = solver.solve(data['storage'])

#print('current predicted value is : {}'.format(retval))

def getkey(prefix, val):
    return prefix + str(val)

def readdata():
    data = pd.read_csv(r'data-1.csv')
    storage_data = list(data['storage'])
    date_data = list(data['date'])
    cid_data  = list(data['cid'])
    uid_data = list(data['uid'])
    #print(type(data))

    lookupuser = {}
    lookupcust = {}

    for i in range(0,len(date_data)):
        userkey = getkey('user_',uid_data[i])
        custkey = getkey('cust_',cid_data[i])
        if not lookupuser.get(userkey):
            lookupuser[userkey] = []
            lookupuser.get(userkey).append(storage_data[i])
        else:
            lookupuser.get(userkey).append(storage_data[i])

        if not lookupcust.get(custkey):
            lookupcust[custkey] = []
            lookupcust.get(custkey).append(storage_data[i])
        else:
            if len(lookupcust.get(custkey))<=date_data[i]:
                lookupcust.get(custkey).append(storage_data[i])
            else:
                lookupcust.get(custkey)[date_data[i]]+=storage_data[i]

    return lookupuser , lookupcust





if __name__ == "__main__":
     users ,customers = readdata()

     userdict = {}
     for key in users:
         val = solver.solve(users[key])
         userdict[key] = val

     custdict = {}

     for key in customers:
         val = solver.solve(customers[key])
         custdict[key] = val

     print(userdict)

     print(custdict)
