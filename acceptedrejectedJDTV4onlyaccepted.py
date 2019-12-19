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

jtn = os.path.join(tt + '/micrographs_rejected.cs')
jnft = jtn.replace("\\", "/")
rej = np.load(jnft)

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
        if ppp[-133:-69] == kk[-68:-4]:
            print(ppp[-133:-69])
            print(kk[-68:-4])
            temp = os.path.join(tt + "/" + kk[-68:-4] + ".mrc")
            temp2 = temp.replace("\\", "/")
            shutil.move(kk,nd2)
            yy = 1
            ca = ca + 1
            
    if yy == 0:
        print('rejected')
        temp = os.path.join(tt + "/" + kk[-68:-4] + ".mrc")
        temp2 = temp.replace("\\", "/")
        shutil.move(kk,nd)
        cr = cr + 1
   
          
print(ca, 'movies into accepted folder')
print(cr, 'movies into rejected folder')   
           


   