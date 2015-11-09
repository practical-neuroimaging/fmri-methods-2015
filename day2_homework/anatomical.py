from _future_ import division
%matplotlib
import numpy as np
import matplotlib.pyplot as plt

#image shape = (I,J,32)

#Read the lines into an array of floats

image_array = np.loadtxt('anatomical.txt')

#Find total number of pixels

text_file = open('anatomical.txt')
lines = text_file.readlines()
total_pixels = len(lines)

#Define pixels in the third dimension (given)

pixels_3d = 32

#Find the size of a slice over the third dimension
#P == I * J

P = total_pixels // pixels_3d

#Make a list of candidates for I (between 120 and 200)
possible_Ifactors = []

for possible_I in range(120,201):
	remainder = P % I
	if remainder==0:
		possible_Ifactors.apend(possible_I)

#Make a list of pairs of I, J such that I * J == P

possible_I = np.array(possible_Ifactors)

possible_J = P // possible_I

#Make the pixel values list into an array
#Try reshaping the array with candidate tripes of (I,J,32)

index = 0

for I_option in possible_I:
	J_option = possible_J[index]
	possible_image = image_array.reshape(I_option,J_option,32)
	plt.imshow(possible_image[:,:,15], cmap='gray')
	plt.show()






#Make a list of candidates for I

