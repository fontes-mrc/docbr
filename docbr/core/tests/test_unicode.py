import unittest
from numpy import int32, testing, array
from docbr.core._unicode import(
    un_align_chars, 
    un_assert_lenght, 
    un_digit_extractor, 
    un_formatter, 
    un_null_validator, 
    un_only_digits, 
    un_remove_separator, 
    un_slicer, 
    un_digit_retriever,
    )

class TestCoreUn(unittest.TestCase):
    def test_un_align_chars(self):
        cases = [
            ((array([[0,1,0,0],[2,3,4,0]]), 'right'),array([[0,0,0,1],[0,2,3,4]])),
            ((array([[0,1,0,0],[2,3,4,0]]), 'left'),array([[1,0,0,0],[2,3,4,0]])),
        ]

        raises = [
            ((array([[0,1,0,0],[2,3,4,0]]), 'center'), ValueError),
        ]

        for test, expected in cases:
            testing.assert_equal(un_align_chars(*test), expected)
        
        for test, expected in raises:
            with self.assertRaises(expected):
                un_align_chars(*test)
    
    def test_un_assert_lenght(self):
        cases = [
            ((array([[1,2,3]]), 2, 'left')  , array([[2,3]])),
            ((array([[1,2,3]]), 2, 'right') , array([[1,2]])),
            ((array([[1,2,3]]), 4, 'left')  , array([[0,1,2,3]])),
            ((array([[1,2,3]]), 4, 'right') , array([[1,2,3,0]])),
            ((array([[1,2,3]]), 3, 'left')  , array([[1,2,3]])),
            ((array([[1,2,3]]), 3, 'right') , array([[1,2,3]])),
        ]

        raises = [
            ((array([[1,2,3]]), 0, 'right') , ValueError),
            ((array([[1,2,3]]), 3, 'center') , ValueError),
        ]

        for test, expected in cases:
            testing.assert_equal(un_assert_lenght(*test), expected)

        for test, expected in raises:
            with self.assertRaises(expected):
                un_assert_lenght(*test)
    
    def test_un_digit_extractor(self):
        cases = [
            ((array(['abc12']), 3), array(['012'])),
            ((array(['abc12']), 4), array(['0012'])),
            ((array(['abc12.0']), 4), array(['0012'])),
            ((array(['abc12.3']), 4), array(['0123'])),
        ]

        for test, expected in cases:
            testing.assert_equal(un_digit_extractor(*test), expected)

    def test_un_formatter(self):
        cases = [
            ((array(['12345']), array(['##.###']).view(int)), array(['12.345'])),
            ((array(['12345']), array(['##A###']).view(int)), array(['12A345'])),
            ((array(['12345']), array(['## ###']).view(int)), array(['12 345'])),
            ((array(['12345'], dtype=object), array(['## ###']).view(int)), array(['12 345'])),
        ]

        for test, expected in cases:
            testing.assert_equal(un_formatter(*test), expected)
    
    def test_un_null_validator(self):
        cases = [
            ((array(['', 'abc']), ''),array([False, True])),
            ((array(['', 'abc']), None),array([True, True])),
        ]

        for test, expected in cases:
            testing.assert_equal(un_null_validator(*test), expected)
    
    def test_un_only_digits(self):
        # digits are between 48 and 57, dot is 46, null is 0
        cases = [
            ((array([[49,52,48,46,48]], dtype=int32), True)  , array([[49,52,48, 0, 0]], dtype=int32)),
            ((array([[49,52,48,46,48]], dtype=int32), False) , array([[49,52,48, 0,48]], dtype=int32)),
            ((array([[49,52,66,71,48]], dtype=int32), True)  , array([[49,52, 0, 0,48]], dtype=int32)),
        ]

        for test, expected in cases:
            testing.assert_equal(un_only_digits(*test), expected)
    
    def test_un_remove_separator(self):
        cases = [
            (array([' abc']), array(['abc'])),
            (array(['abc(),-./:;<=>?@[\]^_`{|}~']), array(['abc'])),
        ]

        for test, expected in cases:
            testing.assert_equal(un_remove_separator(test), expected)
    
    def test_un_slicer(self):
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
            testing.assert_equal(un_slicer(*test), expected)

        for test, expected in raises:
            with self.assertRaises(expected):
                un_slicer(*test)
    
    def test_un_digit_retriever(self):
        cases = [
            (array(['01234']),array([[0,1,2,3,4]])),
            (array(['(11)4']),array([[0,1,1,0,4]])),
            (array(['0123]']),array([[0,1,2,3,0]])),
            (array(['012xx']),array([[0,1,2,0,0]])),
        ]

        for test, expected in cases:
            testing.assert_equal(un_digit_retriever(test), expected)