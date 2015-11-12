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
import sys

import nibabel as nib


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
    # Make a new empty array "interp_data" to hold the interpolated data;
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
    # Hint: use os.path.split and os.path.join to make the new filename
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
    slice_times = ?
    slice_time_file(fname, slice_times, TR)


if __name__ == '__main__':
    # If this file is being run as a script, execute the "main" function
    # See: http://effbot.org/pyfaq/tutor-what-is-if-name-main-for.htm
    main()
