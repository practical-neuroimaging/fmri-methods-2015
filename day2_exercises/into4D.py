#%% Into four dimensions
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 13:46:24 2015
Exercise for Fall 2015
@author: Elissaios
"""
# Compatibility with Python 3
from __future__ import print_function, division

# Standard imports of libraries
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

# Declarations
TR = 2.5
std_vol = []
ave_task = []
ave_rest = []
outlier_task = []
outlier_rest = []

# Input data
folder = r"C:\Users\Elissaios\Box Sync\Projects\fMRI\analysis1";
filePath = folder + r"\ds114_sub009_t2r1.nii";
condPath = folder + r"\ds114_sub009_t2r1_cond.txt";
img = nib.load(filePath)
data = img.get_data()
#print(img.shape)
task = np.loadtxt(condPath)
task[:,0:2] = task[:,0:2]/TR  # change sec to TR for first two columns (2 is for 1+1)
dur = list(img.shape)[3]
nTR = dur
time_course = np.zeros(nTR)
nBlock = task.shape[0]

for itr in range(0,nBlock):
    durBlock = task[itr,1]
    blockS = int(task[itr,0])                # block start
    blockE = int(blockS+durBlock)     # block end
    time_course[blockS:blockE] = 1

plt.figure(0)
plt.ylim(-0.5,1.5)
plt.plot(time_course)

# Create two matrices, one for each condition; it includes first 10 s of rest
is_task_tr = [time_course==1]
is_rest_tr = [time_course==0]
taskInd = np.squeeze(np.array([is_task_tr]))
restInd = np.squeeze(np.array([is_rest_tr]))
data_task = data[...,taskInd]
data_rest = data[...,restInd]

# Identify outlier volumes in each; use 2.5 x interquartile range as cutoff
# You could do it with variance too rather than average signal (take np.std instead of np.average)
# however, for a proper analysis of outliers you probably need both (e.g. either signal
# is high in entire slice but with little variance, or signal is high is certain voxels only
# with low average value but high std)
nBlock_task = int(data_task.shape[3])
for t in range(0,nBlock_task):
    ave_task = ave_task + [np.average(data_task[...,t])]
ave_task_vol = np.average(ave_task)
iqRange_task = np.percentile(ave_task,75) - np.percentile(ave_task,25)
for t in range(0,nBlock_task):
    if ave_task[t] > (ave_task_vol + (iqRange_task*2.5)):
        outlier_task = outlier_task + [t]

nBlock_rest = int(data_rest.shape[3])
for t in range(0,nBlock_rest):
    ave_rest = ave_rest + [np.average(data_rest[...,t])]
ave_rest_vol = np.average(ave_rest)
iqRange_rest = np.percentile(ave_rest,75) - np.percentile(ave_rest,25)
for t in range(0,nBlock_task):
    if ave_rest[t] > (ave_rest_vol + (iqRange_rest*2.5)):
        outlier_rest = outlier_rest + [t]

cleanInd_task = np.arange(0,nBlock_task)
cleanInd_task = np.setdiff1d(np.array(cleanInd_task),np.array(outlier_task))

cleanInd_rest = np.arange(0,nBlock_rest)
cleanInd_rest = np.setdiff1d(np.array(cleanInd_rest),np.array(outlier_rest))

clean_task = data_task[...,cleanInd_task]      
clean_rest = data_rest[...,cleanInd_rest]

mean_task = np.average(clean_task,axis=3) # Average voxel volumes per task
mean_rest = np.average(clean_rest,axis=3) # Average voxel volumes per task
dTask_Rest = mean_task - mean_rest
plt.figure(1)
plt.imshow(dTask_Rest[...,10],'gray')

mean_task = np.average(data_task,axis=3) # Average voxel volumes per task
mean_rest = np.average(data_rest,axis=3) # Average voxel volumes per task
dTask_Rest = mean_task - mean_rest
plt.figure(2)
plt.imshow(dTask_Rest[...,10],'gray')

# Find std of volumes
dur = list(img.shape)[3]

for t in range(0,dur):
    vol = data[...,t]
    #print(vol1.shape)
    voxels = list(vol.shape)    # find how many voxels in each dimension
    slic = int(voxels[2]/2)-1   # define the middle slice
    #plt.figure(t)
    #plt.imshow(vol[...,slic],'gray')
    std_vol = std_vol + [np.std(vol)]

plt.figure(3)
plt.hist(std_vol)  # outline in the 800s
