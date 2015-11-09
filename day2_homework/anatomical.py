# Import packages
# Compatibility with Python 3
from __future__ import print_function, division

# Standard imports of libraries
import numpy as np
import matplotlib.pyplot as plt

# Read the lines into an array of floats (load data)
image_array = np.loadtxt('anatomical.txt')

# Number of pixels in file
p = image_array.size # 848640

# Find the size of a slice over the third dimension
P = image_array.size/32

# The image is not square: I != J
# Find candidates for I by using the modulus operator (%) to find a few numbers between 120 and 200 that divide exactly into the slice size P. Hint: the first value will be 120.
P%120 # 0.0
P%170

# List of candidates for I: 120, 130, 136, 156, 170*, 195
P//120                    # 221, 204, 195, 170, 156*, 136
I = 170
J = P//I

# Reshape the pixel data with the (I, J, 32) candidates
image_array3D = image_array.reshape(I, J, 32)

# Plot a slice on the 3rd dimension to determine which (I, J, 32) is the right one
slice_on_third = image_array3D[:, :, 15] # or 20 or 25, as long as there is brain there
plt.imshow(slice_on_third)
plt.show()

# Show another slice!
slice_on_third2 = image_array3D[:, :, 20] 
plt.imshow(slice_on_third2)
plt.show()

# Show a third slice!
slice_on_third3 = image_array3D[:, :, 25] 
plt.imshow(slice_on_third3)
plt.show()

