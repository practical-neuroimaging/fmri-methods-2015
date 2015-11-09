import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
task = np.loadtxt('ds114_sub009_t2r1_cond.txt')
I = task.shape[0]
J = task.shape[1]
cond_array = np.array(range(I*J))
cond_array = cond_array.reshape(I,J)
TR_array = (task[:,0:2])/2.5
img = nib.load('ds114_sub009_t2r1.nii')
time_course = np.zeros(img.shape[3])
nConds = TR_array.shape[0]
for i in range(nConds):
	temp_index1 = int(TR_array[i,0])
	temp_index2 = int(TR_array[i,1])
	time_course[(temp_index1):(temp_index1+temp_index2)] = 1
is_task_tr = time_course==1
is_rest_tr = time_course==0
img_real = nib.load('ds114_sub009_t2r1.nii')
data = img_real.get_data()
data = np.asarray(data)
data_at_task = data[:,:,:,(np.where(is_task_tr))]
data_at_rest = data[:,:,:,(np.where(is_rest_tr))]
data_at_task = np.squeeze(data_at_task)
data_at_rest = np.squeeze(data_at_rest)
mean_task = np.mean(data_at_task, axis=3)
mean_rest = np.mean(data_at_rest, axis=3)
subt_mean = mean_task-mean_rest
plt.imshow(subt_mean[..., 15], cmap='gray')

#Find the Standard Deviation (variance in this case)
stdVals_rest = []
for i in range(0,data_at_rest.shape[3]):
	curr_vol = data_at_rest[...,i]
	curr_stdVal = np.var(curr_vol)
	stdVals_rest.append(curr_stdVal)
plt.plot(stdVals_rest)
plt.show()
# The data won't plot correctly. Maybe try it as a float value???

