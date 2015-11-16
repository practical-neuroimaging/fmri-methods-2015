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
import sys, os
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import InterpolatedUnivariateSpline

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
    interp_data = np.array(data.shape)

    # Do the interpolation;

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
    fdir, fn = os.path.split(fname)
    fslug, ext = os.path.splitext(fn)
    new_fname = os.path.join(fdir, fslug+'_st'+ext)
    # Hint: use os.path.split and os.path.join to make the new filename
    data = img.get_data()
    # discard first tp (???)
    fixed_data = data[..., 1:]
    new_data = fixed_data.copy()
    n_tps = fixed_data.shape[3]
    s0_times = TR * np.asarray(range(n_tps))
    for x in range(fixed_data.shape[0]):
        for y in range(fixed_data.shape[1]):
            for z in range(fixed_data.shape[2]):
                ts = fixed_data[x, y, z, :]
                xs = (TR * np.asarray(range(n_tps))) + slice_times[z]
                interp = InterpolatedUnivariateSpline(xs, ts, k=1)
                new_series = interp(s0_times)
                new_data[x,y,z,:] = new_series
                
    new_img = nib.Nifti1Image(new_data, img.affine, img.header)
    nib.save(new_img, new_fname)

def main():
    """ This function will be called when this file is run as a script
    """
    # Get the filename from the command line parameters
    fname = sys.argv[1]
    img = nib.load(fname)
    n_slices = img.shape[2]
    # Assume the TR
    TR = 2.0
    slice_duration = TR/n_slices

    e_slices = range(0, n_slices, 2) # 0 2 4
    o_slices = range(1, n_slices, 2) # 1 3 5
    ind_order = []
    ind_order.extend(e_slices)
    ind_order.extend(o_slices)

    offsets = slice_duration * np.asarray(range(n_slices))
    print offsets
    slice_times = np.zeros(n_slices)
    slice_times[ind_order] = offsets
    print(slice_times)

    # Assume the slices were acquired even slices first, inferior to
    # superior, then odd slices, inferior to superior, where the most inferior
    # slice is index 0 and 0 is an even number.  What are the slice acquisition
    # times in seconds, where the first value is the acquisition time of slice
    # 0, the second is acquisition time of slice 1, etc?
    slice_time_file(fname, slice_times, TR)


if __name__ == '__main__':
    # If this file is being run as a script, execute the "main" function
    # See: http://effbot.org/pyfaq/tutor-what-is-if-name-main-for.htm
    main()
