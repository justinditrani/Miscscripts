#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 10:30:19 2019
@author: jdt
"""

import os as os
import numpy as np
import shutil
import glob

tt = os.path.dirname(os.path.abspath(__file__))
jn = os.path.join(tt + '/micrographs_accepted.cs')
jnf = jn.replace("\\", "/")
acc = np.load(jnf)

newdir = os.path.join(tt + '/rejected')
nd = newdir.replace("\\", "/")
ndd = os.mkdir(nd)

newdir2 = os.path.join(tt + '/accepted')
nd2 = newdir2.replace("\\", "/")
ndd2 = os.mkdir(nd2)

files = []
           
#files = [f for f in glob.glob(tt + "**/**/**/**/**/**/*Fractions.mrc", recursive=True)]
#         

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(tt):
    for file in f:
        if 'Fractions.mrc' in file:
            files.append(os.path.join(r, file))

   
ca = 0
cr = 0
sep = ','    
for kk in files:
    yy = 0
    for jj in acc:
        ppp = np.array2string(jj)
        n2 = ppp.rfind('Fractions')
        n1 = ppp.rfind('FoilHole') 
        m2 = kk.rfind('Fractions')
        m1 = kk.rfind('FoilHole')
        
        if ppp[n1:n2] == kk[m1:m2]:
            print(ppp[n1:n2])
            print(kk[m1:m2])
            shutil.move(kk,nd2)
            yy = 1
            ca = ca + 1
            
    if yy == 0:
        print('rejected')
        shutil.move(kk,nd)
        cr = cr + 1
   
          
print(ca, 'movies into accepted folder')
print(cr, 'movies into rejected folder')  
