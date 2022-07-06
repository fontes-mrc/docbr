import unittest
from numpy import array
from docbr.api._docbr import _check_for_attributes, _get_attr_list, _get_instance
from docbr.api._data import DocData
from docbr.core import Doc

class TestAPIInner(unittest.TestCase):
    def test_check_for_attributes(self):
        cases = [
            ('cnpj',None),
            ('cpf',None),
            ('te',None),
            ('cert',None),
            ('placa',None),
            ('tfone',None),
            ('email',None),
        ]

        raises = [
            ('cnh',ValueError),
            ('pis',ValueError),
            ('rnvam',ValueError),
        ]

        for test, expected in cases:
            self.assertEqual(_check_for_attributes(test), expected)

        for test, expected in raises:
            with self.assertRaises(expected):
                _check_for_attributes(test)
    
    def test_get_attr_list(self):
        cases = [
            ('*',['*']),
            (['*','abc'],['*']),
            ([0,'abc'],['0','abc']),
            ('abc',['abc']),
            (0,['0']),
        ]

        raises = [
            ({0:0},TypeError),
            ((0,0),TypeError),
            (array([0]),TypeError),
        ]

        for test, expected in cases:
            self.assertEqual(_get_attr_list(test), expected)

        for test, expected in raises:
            with self.assertRaises(expected):
                _get_attr_list(test)