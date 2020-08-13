# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 16:34:03 2019

@author: MSI
"""

import tkinter as tk
from tkinter import filedialog
import csv
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model

file_path = filedialog.askopenfilename()

data = pd.read_csv(file_path,skiprows=27,skipfooter=3,usecols = ['Time', 'Oxygen 1'],engine='python')

Ti = data.index
Ox = data['Time']

plt.plot(Ti,Ox)
plt.title('Scatter plot pythonspot.com')
plt.xlabel('x')
plt.ylabel('y')
plt.show()
points= plt.ginput(n=4,timeout=60,show_clicks='true')

yy = list(range(0,4))

Xn=[]
for k in yy:
    GG = abs(Ti-points[k][0]) == min(abs(Ti-points[k][0]))
    PP = np.where(GG)[0]
    Xn.append(PP[0])

reg1 = linear_model.LinearRegression()
xx = pd.DataFrame(Ti[Xn[0]:Xn[1]])
yy1 = Ox.values
yy = yy1[Xn[0]:Xn[1]]
reg1.fit(xx,yy)
RS1 = reg1.coef_

reg2 = linear_model.LinearRegression()
xx2 = pd.DataFrame(Ti[Xn[2]:Xn[3]])
yy2 = Ox.values
yy = yy2[Xn[2]:Xn[3]]
reg1.fit(xx2,yy)
RS2 = reg1.coef_

print(RS2-RS1)