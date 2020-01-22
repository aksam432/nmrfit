# This program is for fitting rate equations provided by jonas



import numpy as np
import pandas as pd
import xlrd as xl

from pandas import ExcelWriter
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

#df= pd.read_excel("Titration data.xlsx")
#print (df.iloc[0,2])
#for x in df.columns():
#    print(x)

class Solver(object):
    def __init__(self,filename):
        self.filename = filename
        df = pd.read_excel(self.filename)
        self.xdata = df.iloc[:,2]  # delta
        self.ydata = df.iloc[:,1]  # O*tot
        self.Mtot  = df.iloc[0,0]  # Mtot
        self.delta_M = df.iloc[0,2] # delta M
        self.fit()

    def func(self,delta,K,delta_MO,x):
        lamda_d = (self.delta_M -delta)/(self.delta_M -delta_MO)
        tmp1= (1.0 -lamda_d)*K
        tmp2= (lamda_d/tmp1)
        tmp3= pow(tmp2,1.0/x)
        return tmp3 + x*self.Mtot*lamda_d

    def plot(self,popt):
        plt.plot(self.xdata,self.ydata,'bo',label='data')
        plt.plot(self.xdata,self.func(self.xdata,*popt),'r-',label='fit K=%3.6f Delta=%3.6f x=%3.6f'%tuple(popt))
        plt.xlabel('Chemical Shift')
        plt.ylabel('[O*]$_{tot}$')
        plt.legend()
        plt.savefig('plot.png',dpi=300)
        plt.show()
        

    def fit(self):
        popt,pcov = curve_fit(self.func,self.xdata,self.ydata)
        print(popt)
        self.plot(popt)
    

Solver("Titration data.xlsx")
