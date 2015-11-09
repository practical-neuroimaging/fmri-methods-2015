import nibabel as nib
import numpy as np
anatomical = np.loadtxt('anatomical.txt')
K = 32
P = anatomical.size/K
TrueVals = []
for i in range(120,200):
	if P % i == 0:
		TrueVals.append(i)
I = TrueVals
J = [P / x for x in TrueVals]
