import unittest
from docbr.core._utils import array_slicer

from numpy import array, testing

class TestCoreUtils(unittest.TestCase):
    def test_array_slicer(self):
            cases = [
                ((array(['01234']), 0, 2, str), array(['012'])),
                ((array(['01234']), 2, None, str), array(['2'])),
                ((array(['01234']), 2, 4, int), array([234])),
            ]

            raises = [
                ((array(['01234']), 2, 4, float), ValueError),
                ((array(['01234']), 2, 4, bool), ValueError),
            ]

            for test, expected in cases:
                testing.assert_equal(array_slicer(*test), expected)

            for test, expected in raises:
                with self.assertRaises(expected):
                    array_slicer(*test)