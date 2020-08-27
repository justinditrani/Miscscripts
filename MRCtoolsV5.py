#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 10:57:56 2020
@author: justin
modified on 18th Jun 2020 by Hui
"""

import mrcfile
import numpy as np
import os as os
import argparse

def open_mrc(filename):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file = dir_path + '/' + filename
    
    mrc = mrcfile.open(file, mode='r+')
    out = mrc.data
    mrc.close()

    return out

def get_density(map1,map2,thresh):
    binxyza = np.where(map2>thresh)
    #print (np.shape(binxyza),binxyza[0],binxyza[1],binxyza[2] )
    
    return sum(map1[binxyza[0],binxyza[1],binxyza[2]])/len(binxyza[0])

def get_noise(map1,radius):
    boxsize = np.shape(map1)[0]
    binxyza = np.zeros([boxsize,boxsize,boxsize])
    x,y,z = np.ogrid[0:boxsize,0:boxsize,0:boxsize]
    binxyza[np.sqrt((x-(boxsize-1)/2)**2+(y-(boxsize-1)/2)**2+(z-(boxsize-1)/2)**2)>radius]=1. #set voxels > radius to 1
    binxyza[np.sqrt((x-(boxsize-1)/2)**2+(y-(boxsize-1)/2)**2+(z-(boxsize-1)/2)**2)>(boxsize/2.)]=0 #set voxels > boxsize to 0
    pix_included = np.where(binxyza==1) #all voxels included in calculation
    pix_number=len(np.where(binxyza==1)[0]) # number of voxels
    noise = sum(map1[pix_included[0],pix_included[1],pix_included[2]])/pix_number
    #print (np.shape(binxyza),binxyza[0],binxyza[1],binxyza[2] )
    return noise
    
def get_voxels(map1,thresh):
    binxyza = np.where(map1>thresh)
    return len(binxyza[1][:])


parser = argparse.ArgumentParser()
parser.add_argument('--densitycompare1', nargs = 3, help="compare density between 2 maps in a given mask")
parser.add_argument('--densitycompare2', nargs = 5, help="compare occupancy of 2 regions of a map defined by 2 masks; map, mask1, mask2, threshold, particle radius(# of pixels)")
parser.add_argument('--densitycompare3', nargs = 7, help="compare occupancy of 2 regions of a map defined by 2 masks; map, mask1, mask2, threshold, noise from mask in background")
parser.add_argument('--nvox', nargs = 2, help="total voxels of a mask at a certain threshold")
args = parser.parse_args()


if args.densitycompare1:
    a, b, t = args.densitycompare1
    xyza = open_mrc(a)
    xyzb = open_mrc(b)
    tt = float(t)
    Dena = get_density(xyza,xyzb,tt) 
    print('Total density for ' + a + ' in region of mask ' + b + ' at threshold ' + t + ' is ' + str(Dena))
    
elif args.densitycompare2:
    a, b, c, t, r = args.densitycompare2

    print('Comparing occupancies of 2 regions of a map ' + a + ' defined by mask ' + b + ' and mask ' + c)
    xyza = open_mrc(a)
    xyzb = open_mrc(b)
    xyzc = open_mrc(c)
    tt = float(t)
    r = float(r)
    print(get_noise(xyza,r))
    Denb = get_density(xyza,xyzb,tt) - get_noise(xyza,r)
    Denc = get_density(xyza,xyzc,tt) - get_noise(xyza,r)
    print('Total density for ' + a + ' in region of mask ' + b + ' at threshold ' + t + ' is ' + str(Denb))
    print('Total density for ' + a +' in region of mask ' + c + ' at threshold ' + t + ' is ' + str(Denc))
    print('The occupancy at this site is '+str(Denb/Denc))

elif args.densitycompare3:
    a, b, c, d, t, t2, t3 = args.densitycompare3
    
    # MAP_of_interest numerator_mask denominator_mask background_mask thresh_numerator_mask thresh_denominator_mask thresh_background_mask
    print('Comparing occupancies of 2 regions of a map ' + a + ' defined by mask ' + b + ' and mask ' + c + ' at thresholds ' + t + ' and '+ t2 + 'respectively with a mask in the noise at threshold ' + t3)
    xyza = open_mrc(a)
    xyzb = open_mrc(b)
    xyzc = open_mrc(c)
    xyzd = open_mrc(d)
    tt = float(t)
    tt2 = float(t2)
    tt3 = float(t2)
    print(get_density(xyza,xyzd,tt3))
    Denb = get_density(xyza,xyzb,tt) - get_density(xyza,xyzd,tt3)
    n = get_density(xyza,xyzd,tt3) 
    print('noise is ' + str(n)) 
    print('Total density for ' + a + ' in region of mask ' + b + ' at threshold ' + t + ' is ' + str(Denb))
    Denc = get_density(xyza,xyzc,tt2) - get_density(xyza,xyzd,tt3)
    print('Total density for ' + a +' in region of mask ' + c + ' at threshold ' + t2 + ' is ' + str(Denc))
    print('The occupancy at this site is '+str(Denb/Denc))

elif args.nvox:
    a, t = args.nvox
    print('Total number of voxels of map ' + a + ' at threshold ' + t)
    xyza = open_mrc(a)
    tt = float(t)
    vox = get_voxels(xyza,tt) 
    print(vox)


