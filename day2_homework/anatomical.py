import numpy as np
import matplotlib.pyplot as plt

# Read the lines into an array of floats
pixel_values = np.loadtxt('anatomical.txt')

# Find the size of a slice over the third dimension
P = pixel_values.shape[0]/32.0
# Make a list of candidates for I
I = np.arange(120,200)
mod = P%I
inds = mod==0
I = I[inds]
J = P/I
for i in I:
    print i
    pixel_values = pixel_values.reshape((i,-1,32))
    plt.figure()
    plt.imshow(pixel_values[:,:,16])
    plt.show()

I = 170
J = P/I