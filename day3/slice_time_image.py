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

# Add any extra imports here
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
from scipy.interpolate import InterpolatedUnivariateSpline as IUS

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
    data = img.get_data()
    # Make a new empty array "interp_data" to hold the interpolated data;
    interp_data = np.zeros(data.shape)
    
    # Do the interpolation;
    time_offset = slice_times/slice_times.shape * TR
    print "Time Offsets: %s" % time_offset
    slice_0_times = TR * np.arange(data.shape[-1])
    
    # For each z coordinate (slice index):
    for z in range(data.shape[2]):
        print "Starting Slice %s of %s" % (z+1, data.shape[2])
        slice_z_times = slice_0_times + time_offset[z]
        # For each x coordinate:
        for x in range(data.shape[0]):
            # For each y coordinate:
            for y in range(data.shape[1]):
                # extract the time series at this x, y, z coordinate;
                current_timecourse = data[x,y,z,:]
                # make a linear interpolator object with the `slice_z_times` and the extracted time series;
                current_interp = IUS(slice_z_times, current_timecourse, k=1)
                # resample this interpolator at the slice 0 times;
                current_timecourse_estimate = current_interp(slice_0_times)
                # put this new resampled time series into the new data at the same position
                interp_data[x,y,z,:] = current_timecourse_estimate

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
    interp_img = slice_time_image(img, slice_times, TR)
    # Hint: use os.path.split and os.path.join to make the new filename
    path, tail = os.path.split(fname)
    new_tail = 'Interp_' + tail
    new_fname = os.path.join(path,new_tail)
    nib.save(interp_img, new_fname)


def main():
    """ This function will be called when this file is run as a script
    """
    # Get the filename from the command line parameters
    fname = sys.argv[1]
    # Assume the TR
    TR = 2.0
    # Assume the slices were acquired even slices first, inferior to
    # superior, then odd slices, inferior to superior, where the most inferior
    # slice is index 0 and 0 is an even number.  What are the slice acquisition
    # times in seconds, where the first value is the acquisition time of slice
    # 0, the second is acquisition time of slice 1, etc?
    img = nib.load(fname)
    # Get the data array from the image
    data = img.get_data()
    # Need to know how many slices there are in the image
    num_slices = data.shape[2]
    print "Number of slices: %s" % num_slices
    first_half = np.arange(0, np.ceil(num_slices/2.))
    second_half = np.arange(np.ceil(num_slices/2.), num_slices)
    slice_times = np.array([])
    for i in first_half:
        slice_times = np.append(slice_times,first_half[i])
        if i < len(second_half):
            slice_times = np.append(slice_times,second_half[i])
    print "Slice Ordering: %s" % slice_times
    slice_time_file(fname, slice_times, TR)


if __name__ == '__main__':
    # If this file is being run as a script, execute the "main" function
    # See: http://effbot.org/pyfaq/tutor-what-is-if-name-main-for.htm
    main()
