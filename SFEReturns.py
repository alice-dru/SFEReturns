# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import pandas as pd
import numpy as np
from scipy import stats

#pathfile specified by the user
#dax 30 
mypath = "/Users/alicedrube/Documents/Uni /Master/SFM_Python/sfm_dax.csv"
path   = open(mypath, "r")

#ftse100
#mypath = "/Users/alicedrube/Documents/Uni /Master/SFM_Python/sfm_ftse.csv"
#path   = open(mypath, "r")


data  = pd.read_csv(path,header=0) 
datax = data.iloc[:,1:]

del data


msg1 = "This program calculates the first order auto correlation of returns, squared returns and absolute returns and skewness, kurtosis and the Bera Jarque statistic for german blue chips, 1974 - 1996"
print(msg1)
del msg1

#dax 30 
stocks = ["all", "adidas", "allianz", "basf", "bmw", "bayer", "beiersdorf", "continental", "covestro",
          "daimler", "deutsche bank", "deutsche boerse", "deutsche post", "deutsche telekom", 
          "eon", "fresenius medical care", "fresenius", "heidelbergcement", "henkel", "infineon", "linde", 
          "lufthansa", "merck", "munich re", "rwe", "sap", "siemens", "thyssen", "volkswagen", 
          "vonovia", "wirecard"]

#ftse100
#stocks = ["all", "3i", "admiral", "anglo american", "antofagasta", "ashtead", "british foods", 
#         "astra zeneca", "aviva", "bae", "barclays", "baratt", "bat", "bhp", "bp", 
#         "british land", "bt", "bunzl", "burberry", "carnival", "centrica", "coca cola", 
#         "compass", "crh", "ds smith", "dcc", "diageo", "direct line", "easy jet", 
#          "evraz", "experian", "fresnillo", "glaxosmith", "glencore", "halma", "hargreaves", 
#          "hiscox", "hsbc", "imperial", "informa", "intercontinental", "int airlines", 
#          "intertex", "itv", "sainsbury", "johnson matthey", "just eat", "kingfisher", 
#          "landsecurities", "legal general", "lloyds", "lse", "marks spencer", "mondi", 
#          "national grid", "next", "nmc", "ocado", "paddy power", "pearson", "persimmon", 
#          "phoenix", "prudential", "rbs", "reckitt benckiser", "relx", "rentokil", "rio tinto", 
#          "rolls royce", "rsa", "sage", "schroders", "scottish mortgage", "segro", "severn trent", 
#          "shell a", "shell b", "smith nephew", "smiths", "smurfit kappa", "spirax sarco", "sse", 
#          "st james place", "standard chartered", "sla", "taylor wimpey", "tesco", "berkeley", 
 #         "tui", "unilever", "united utilities", "vodafone", "whitbread", "wm morrison", "wpp"]

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
    result = pd.DataFrame(data = np.zeros(shape = (shp_x+1, 7)),
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


