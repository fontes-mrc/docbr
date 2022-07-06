import unittest
from numpy import testing, array
from docbr.core._dict import bulk_function_applier, dict_key_selector
from docbr.core._unicode import un_slicer

class TestCoreDict(unittest.TestCase):
    def test_bulk_function_applier(self):
        cases = [
            ((array(['0123456','2345678']),{'n':lambda x: x},True),array(['0123456','2345678'])),
            ((array(['0123456','2345678']),{'n':lambda x: x},False),array([{'n':'0123456'},{'n':'2345678'}])),
            ((array(['0123456','2345678']),{'n':lambda x: un_slicer(x,0)},True),array(['0','2'])),
            ((array(['0123456','2345678']),{'n':lambda x: un_slicer(x,0)},False),array([{'n':'0'},{'n':'2'}])),
            ((array([1234567,2345678]),{'n':lambda x: un_slicer(x,0)},False),array([{'n':'1'},{'n':'2'}])),
            ((array(['','']),{'n':lambda x: un_slicer(x,0)},False),array([{'n':'0'},{'n':'0'}])),
        ]

        raises = [
            ((array(['']),{'n':0},True), ValueError),
        ]

        for test, expected in cases:
            testing.assert_equal(bulk_function_applier(*test), expected)

        for test, expected in raises:
            self.assertRaises(expected, bulk_function_applier, *test)

    def test_dict_key_selector(self):
        cases = [
            ((['*'],{'a':1,'b':2,'c':3}),{'a':1,'b':2,'c':3}),
            ((['a'],{'a':1,'b':2,'c':3}),{'a':1}),
            ((['a','a'],{'a':1,'b':2,'c':3}),{'a':1}),
            ((['a','c'],{'a':1,'b':2,'c':3}),{'a':1,'c':3}),
            ((['a','d'],{'a':1,'b':2,'c':3}),{'a':1}),
        ]

        raises = [
            ((['d','d'],{'a':1,'b':2,'c':3}),KeyError),
        ]

        for test, expected in cases:
            self.assertEqual(all(dict_key_selector(*test)), all(expected))


        for test, expected in raises:
            self.assertRaises(expected, dict_key_selector, *test)