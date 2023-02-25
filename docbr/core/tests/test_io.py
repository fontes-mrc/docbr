import unittest
from docbr.core._io import io_get, io_input_narray, io_output_narray

from typing import Iterable
#from pandas import Series, DataFrame
from numpy import array, ndarray, nan

class TestCoreIO(unittest.TestCase):
    def test_io_input_narray(self):
        cases = [
            (0                           ,array(['0'])),
            (nan                         ,array(['nan'])),
            (123.5                       ,array(['123.5'])),
            ('abc'                       ,array(['abc'])),
            (array([0])                  ,array(['0'])),
            (['abc',123]                 ,array(['abc','123'])),
            #(Series([0,0,'abc'])         ,array(['0','0','abc'])),
        ]

        raises = [
            ([[],[]]     , ValueError),
            (None        , TypeError),
            ([None,None] , ValueError),
            (True        , TypeError),
            ([{1:1},0]   , ValueError),
            #(Series({'col':[0,0,'abc']}) , ValueError),
            #([Series([0,0,'abc']),Series([0,0,'abc'])], ValueError),
            #(DataFrame([0,0,'abc']), TypeError),
        ]

        for test, expected in cases:
            self.assertEqual(all(io_input_narray(test, io_get(test)[0])), all(expected))
        
        for test, expected in raises:
            self.assertRaises(expected, io_get, test)
    
    def test_io_output_narray(self):
        cases = [
            ((array([''])     , str)    , ''),
            ((array(['None']) , str)    , 'None'),
            ((array([None])   , str)    , None),
            ((array([True])   , str)    , True),
            ((array(['0','0']) , int)   , None),
            ((array(['0','0']), ndarray), array(['0','0'])),
        ]

        for test, expected in cases:
            if isinstance(expected, Iterable):
                self.assertEqual(all(io_output_narray(*test)), all(expected))
            else:
                self.assertEqual(io_output_narray(*test), expected)