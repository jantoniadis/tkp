__author__ = 'Gijs Molenaar'

import unittest
if not  hasattr(unittest.TestCase, 'assertIsInstance'):
    import unittest2 as unittest
import os
import sys
from tkp.utility import accessors
from tkp.quality import statistics
from tkp.lofar import noise
import tkp.config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from decorators import requires_data
import numpy
from numpy.testing import assert_array_equal, assert_almost_equal

fits_file = '/home/gijs/Data/antonia_april/original/img1.fits'


@requires_data(fits_file)
#@unittest.skip
class test_maps(unittest.TestCase):
    def setUp(self):
        self.uncorr_map = accessors.FitsFile(fits_file)

    def testRms(self):
        #self.rms = rms.rms(self.uncorr_map.data)
        self.assertEquals(statistics.rms(numpy.ones([4,4])*4), 16)

    def testClip(self):
        a = numpy.ones([800, 800]) * 200
        a[400, 400] = 1000
        clipped = statistics.clip(a)
        check = numpy.ones([800, 800]) * 200
        check[400, 400] = 203
        assert_almost_equal(clipped,  check, decimal=5)

    def testTheoreticalMaxValue(self):
        bandwidth = self.uncorr_map.freqbw
        freq = self.uncorr_map.freqeff
        integration_time = self.uncorr_map.inttime

        # TODO: somehow these are 0 is some images sometimes?
        if bandwidth == 0.0: bandwidth = 1.0
        if integration_time == 0.0: integration_time = 1.0

        noise_level = noise.noise_level(freq, bandwidth, integration_time)
        self.assertGreater(noise_level, 0)


if __name__ == '__main__':
    unittest.main()