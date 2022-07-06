import unittest
from numpy import testing, array
from docbr.core._regex import re_searcher
from re import search

class TestCoreRe(unittest.TestCase):
    def test_re_searcher(self):
        pattern_placa = r'[a-zA-Z]{3}\s?\-?[0-9][A-Za-z0-9][0-9]{2}'
        cases = [
            ((array(['abc-1234']), pattern_placa, False), array([search(pattern_placa,'abc-1234')], dtype='<U48')),
            ((array(['abc-1234']), pattern_placa, True), array(['abc-1234'], dtype='<U8')),
            ((array(['abc12']), pattern_placa, True), array([''], dtype='<U1')),
        ]

        for test, expected in cases:
            testing.assert_equal(re_searcher(*test), expected)