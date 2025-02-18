""" Test stimuli module

Run tests with::

    nosetests test_stimuli.py
"""

import os

import numpy as np
import numpy.testing as npt

import stimuli

MY_DIRECTORY = os.path.dirname(__file__)


def test_events2neural():
    # test events2neural function
    cond_fname = os.path.join(MY_DIRECTORY, 'cond_test1.txt')
    neural = stimuli.events2neural(cond_fname, 2, 16)
    # cond_test1.txt file is:
    """
    10    5.0    1
    20    4.0    2
    24    3.0    0.1
    """
    # Expected values for tr=2, n_trs=16
    expected = np.zeros(16)
    expected[5:7] = 1
    expected[10:12] = 2
    expected[12] = 0.1
    npt.assert_array_equal(neural, expected)
    neural = stimuli.events2neural(cond_fname, 1, 30)
    # Expected values for tr=1, n_trs=30
    expected = np.zeros(30)
    expected[10:15] = 1
    expected[20:24] = 2
    expected[24:27] = 0.1
    npt.assert_array_equal(neural, expected)
