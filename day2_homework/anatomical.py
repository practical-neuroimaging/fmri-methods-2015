import numpy as np
import matplotlib.pyplot as plt

# read in an anatomical image in 1-dimensional form
image_1d = np.loadtxt('anatomical.txt')

# find the total length of the 1-dimensional form
n_elements = image_1d.size

# we are going to convert this to a 3-dimensional form (I,J,K)
# and we already know that the third dimension will be 32
K = 32

# we need to figure out values for I and J, so we will represent
# P = I*J, which is also:
P = n_elements/K

# We will now try to find possible factors of P between 120-200
possible_factors = range(120,201)

# once we find a number that is a factor of P we will add it to another array
actual_factors = []

# cycling through all possible factors between 120 and 200
for num in possible_factors:
	remainder = P % num
	if remainder==0:
		actual_factors.append(num)

# we will now say that those actual factors we found are possible values for I
possible_I = np.array(actual_factors)

# possible J values are those that make I*J=P
possible_J = P // possible_I

# now we will try printing a slice of the image with these values
index = 0

print 'You will have to close each image before continuing to the next one.'

for I in possible_I:
	J = possible_J[index]
	possible_image = image_1d.reshape(I,J,K)
	# going to the middle layer of the brain to get a good image, K=15
	plt.imshow(possible_image[:,:,15], cmap="gray")
	plt.show()
	# ask user if this image looks correct
	response = input('Did that image look correct? 0=no, 1=yes  ')
	# if it did look correct, save teh true values of I and J
	if response==1:
		true_I = I
		true_J = J
		break  # no need to try other values, so break out of loop
	index += 1

print " "  # just printing a blank line
# then printing out the correct dimensions that we found
print "Dimensions are (%d,%d,%d)" % (true_I, true_J, K)

#show the correct image again
image_3d = image_1d.reshape(true_I,true_J,K)
plt.imshow(image_3d[:,:,15], cmap="gray")
print "Close image to end process..."
plt.show()

