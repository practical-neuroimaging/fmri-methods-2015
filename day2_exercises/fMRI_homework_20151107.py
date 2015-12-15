# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 09:02:19 2015

@author: Elissaios
"""

#%% Load nii image (after it was unzipped)
import nibabel as nib

folder = r"c:\Anaconda3\Lib\site-packages\nibabel\tests\data";
#filePath = path + 'ds107_sub001_highres.nii';
filePath = folder + r"\example_nifti2.nii";

img = nib.load(filePath);
data = img.get_data();

#%% Anatomical image
import numpy as np
#import math;
import matplotlib.pyplot as plt

folder = r"c:\Users\Elissaios\Box Sync\Projects\fMRI\analysis1";
filePath = folder +r"\anatomical.txt";
anat = np.loadtxt(filePath);

zdim=32;
anat_slice = int(len(anat)/zdim)
for ix in range(120,200+1):
    anat_mod = anat_slice % ix;
    if anat_mod == 0:
        ij = anat_slice/ix;
        #if ij.is_integer():
        #if np.floor(ij)-ij == 0:
        #if int(ij)-ij == 0:
        if ij % 1 == 0:
            print(ix, int(ij))
            anat3d = anat.reshape(ix,int(ij),zdim)
            plt.imshow(anat3d[:,:,16],'gray')
            #answer 170 by 156
            
            
#%% Working with four dimensional images
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

folder = r"C:\Users\Elissaios\Box Sync\Projects\fMRI\analysis1";
filePath = folder + r"\ds114_sub009_t2r1.nii";
img = nib.load(filePath)
data = img.get_data()
volume = data[...,0]
#plt.imshow(volume[...,15])
var_vol = np.var(data,3)
plt.figure(1)
plt.imshow(var_vol[...,14],'gray')
low_vol = volume[volume<10]
plt.figure(2)
plt.hist(low_vol)
uniq = np.unique(low_vol)

#%% Into four dimensions
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
folder = r"C:\Users\Elissaios\Box Sync\Projects\fMRI\analysis1";
filePath = folder + r"\ds114_sub009_t2r1.nii";
img = nib.load(filePath)
data = img.get_data()



















