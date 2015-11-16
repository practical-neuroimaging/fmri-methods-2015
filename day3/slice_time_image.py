""" Slice time image

This is a Python script.

You can run this script from the command line with::

    python slice_time_script.py an_image.nii

or from the IPython console with::

    run slice_time_script.py an_image.nii

You can check the individual functions with ``import`` in the IPython console,
something like this::

    import slice_time_script
    slice_time_script.slice_time_image(my_img, slice_times, TR)

If you use this import in IPython, and you edit ``slice_time_script.py``,
remember to do ``reload(slice_time_script)`` to get the new version.
"""

# Compatibility settings
from __future__ import print_function
from __future__ import division
from scipy.interpolate import InterpolatedUnivariateSpline

# Import modules
import os
import sys
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

# Parameter declaration
plt.rcParams['image.cmap'] = 'gray'
plt.rcParams['image.interpolation'] = 'nearest'

def slice_time_image(img, slice_times, TR):
    """Run slice-timing correction on nibabel image 'img'.

    You can assume the "slice" axis is axis 2, and the time axis is axis 3.

    Parameters
    ----------
    img: nibabel image
        Image to be slice-time corrected.
    slice_times: array_like
        The time in seconds at which each slice was acquired relative to the
        start of the TR, listed in spatial order.
    TR: double
        Repetition time in seconds.

    Returns
    -------
    st_img : Nifti1Image
        A new copy of the input image with slice-time interpolation applied
    """

    # Get the image data as an array;
    data = img.get_data()       # The current function structure leads to many loadings of the image file, making the process slower and increasing memory demands
    n_x_voxels = data.shape[0]    
    n_y_voxels = data.shape[1]    
    n_slices = data.shape[2] # number of slices on z dimension
    n_tr = data.shape[3]
    
    # Make a new empty array "interp_data" to hold the interpolated data;
    interp_data = np.zeros(data.shape)

    # Do the interpolation;
    tr_onsets = np.arange(n_tr) * TR  # define onset of each TR in sec

    # for each slice interpolate time series to the onset of the first slice acquired in the TR
    for iz in range(n_slices):
        all_iz_times = tr_onsets + slice_times[iz]
        # for each voxel in the slice do an interpolation; could possibly reshape matrix first, but more difficult to read and then have to inverse reshape
        for ix in range(n_x_voxels):
            for iy in range (n_y_voxels):
                voxel_timeseries = data[ix,iy,iz,:]
                interp = InterpolatedUnivariateSpline(all_iz_times, voxel_timeseries, k=1)
                interp_data[ix,iy,iz,:] = interp(tr_onsets)  #we could potentially also interpolate for all n_slices intervals and get n_tr * n_slices time points.

    # debug
    # plt.plot(tr_onsets[:10]+slice_times[10], data[0,0,10,:10], ':+')
    # plt.plot(tr_onsets[:10], interp_data[0,0,10,:10], ':kx')

    # This is how to make a new image with the interpolated data
    new_img = nib.Nifti1Image(interp_data, img.affine, img.header)
   
    return new_img


def slice_time_file(fname, slice_times, TR):
    """Perform slice-time correction on an image file.

    Write the corrected file as 'a' appended to the original file name.

    You can assume the "slice" axis is axis 2, and the time axis is axis 3.

    Parameters
    ----------
    fname: string
        Name of the image file (in any format nibabel.load accepts).
    slice_times: array_like
        The time in seconds at which each slice was acquired relative to the
        start of the TR, listed in spatial order.
    TR: double
        Repetition time in seconds.
    """

    img = nib.load(fname)
    interp_img = slice_time_image(img,slice_times,TR)
    
    # Hint: use os.path.split and os.path.join to make the new filename
    path, filename = os.path.split(fname)
    new_fname = 'a_' + filename
    new_fname = os.path.join(path,new_fname)
    
    nib.save(interp_img, new_fname)


def main():
    """ This function will be called when this file is run as a script
    """
    # Get the filename from the command line parameters
    fname = sys.argv[1]
    #fname = 'ds107_sub012_t1r2.nii'  # filename used 
    
    img = nib.load(fname)
    data = img.get_data()
    n_slices = data.shape[2] # number of slices on z dimension
    
    # Assume the TR
    TR = 2.0
    # Assume the slices were acquired even slices first, inferior to
    # superior, then odd slices, inferior to superior, where the most inferior
    # slice is index 0 and 0 is an even number.  What are the slice acquisition
    # times in seconds, where the first value is the acquisition time of slice
    # 0, the second is acquisition time of slice 1, etc?

    interval = TR / n_slices # acquisition time interval in seconds between each consecutive slice
    # Identify sequence of slices per TR
    even_slices = []  
    odd_slices = []
    for islice in range(n_slices):
        if islice % 2 == 0:
            even_slices = even_slices + [islice]
        else: 
            odd_slices = odd_slices + [islice]
    slice_seq = even_slices + odd_slices
    lag = 0    
    slice_lag = np.zeros(n_slices)
    for it in slice_seq:
        slice_lag[it] = lag
        lag = lag + interval
    
    slice_times = slice_lag
    slice_time_file(fname, slice_times, TR)

if __name__ == '__main__':
    # If this file is being run as a script, execute the "main" function
    # See: http://effbot.org/pyfaq/tutor-what-is-if-name-main-for.htm
    main()
