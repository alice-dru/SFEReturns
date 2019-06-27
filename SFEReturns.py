# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import pandas as pd
import numpy as np
from scipy import stats

#pathfile specified by the user
mypath = "/Users/alicedrube/Documents/Uni /Master/SFM_Python/sfm_pri.csv"
path   = open(mypath, "r")


data  = pd.read_csv(path,header=0) 
datax = data.iloc[:,1:]

del data


msg1 = "This program calculates the first order auto correlation of returns, squared returns and absolute returns and skewness, kurtosis and the Bera Jarque statistic for german blue chips, 1974 - 1996"
print(msg1)
del msg1

stocks = ["all", "allianz", "basf", "bayer", "bmw", "cobank", "daimler",
          "deutsche bank", "degussa", "dresdner bank", "hoechst", "karstadt", "linde", 
          "man", "mannesmann", "preussag", "rwe", "schering", "siemens", "thyssen", 
          "volkswagen"]

print ("Stocks : ") 
for i in range(len(stocks)): 
    print (i, end = " ") 
    print (stocks[i]) 
    
s  = stocks.index('all') #choose desired stock

n  = datax.shape[0] 
 
if s == 0:
    x      = datax.iloc[:,1:]
    st     = stocks[1:]
    shp_x  = x.shape[1]
    result = pd.DataFrame(data = np.zeros(shape = (shp_x, 7)),
                          index = st,
                          columns = ["rho(ret):", "rho n(ret^2):",
                                  "rho(|ret|):", "S:", "K:", "JB:",
                                  "JB p-value:"])
else:
    x      = pd.DataFrame(datax.iloc[:,(s-1)])
    shp_x  = x.shape[1]
    st     = stocks[s]
    result = pd.DataFrame(data = np.zeros(shape = (shp_x, 7)),
                          index = [st], #klappt nur für die eindimensionalen
                          columns = ["rho(ret):", "rho n(ret^2):",
                                  "rho(|ret|):", "S:", "K:", "JB:",
                                  "JB p-value:"]) #bis hier klappt alles
 


    
for i in range(shp_x):
    #calculate log returns from closing prices
    df1  = np.log(x.iloc[1:, i]).reset_index()
    df2  = pd.DataFrame(np.log(x.iloc[0:(n - 1), i]))
    ret1 = pd.DataFrame(df1.iloc[:,1] - df2.iloc[:,0])
   
    # start calculation
    skew = ret1.skew()
    kurt = ret1.kurt()
    ret2 = pd.DataFrame(ret1**2)
    ret3 = ret1.abs()
    n    = ret1.shape[0]
    df1  = ret1.iloc[1:].reset_index()
    df2  = ret1.iloc[0:(n-1)]
    rho1 = df1.iloc[:,1:].corrwith(df2)
    df1  = ret2.iloc[1:].reset_index()
    df2  = ret2.iloc[0:(n-1)]
    rho2 = df1.iloc[:,1:].corrwith(df2)
    df1  = ret3.iloc[1:].reset_index()
    df2  = ret3.iloc[0:(n-1)]
    rho3 = df1.iloc[:,1:].corrwith(df2)
    jb   = pd.DataFrame(stats.jarque_bera(ret1.iloc[:(n-1),])) #extra checken
   
    # end calculation
    result.iloc[i, 0] = rho1.iloc[0] #hier noch mal checken
    result.iloc[i, 1] = rho2.iloc[0]
    result.iloc[i, 2] = rho3.iloc[0]
    result.iloc[i, 3] = skew.iloc[0]
    result.iloc[i, 4] = kurt.iloc[0]
    result.iloc[i, 5] = jb.iloc[0,0]
    result.iloc[i, 6] = jb.iloc[1,0]
   

    
msg2 = "first order auto correlation of returns, squared returns and absolute returns and skewness, kurtosis and Bera Jarque statistic for german blue chips, 1974 - 1996"
print(msg2)
print("")
print(result) 


