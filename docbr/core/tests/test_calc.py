import unittest
from numpy import testing, array, int8
from docbr.core._calc import calc_dig_generator, calc_dig_validator, calc_repeated_check, calc_federal_unit_validator

class TestCoreCalc(unittest.TestCase):
    def test_calc_dig_validator(self):
        cases = [
            ((array([[1,2,3,4,5],[0,1,2,3,4]]), [(array([4,4]), 3),(array([5,4]), 4)]),array([True, False])),
            ((array([[1,2,3,4,5],[0,1,2,3,4]]), [(array([5,4]), 4)]),array([True, True])),
            ((array([[1,2,3,4,5],[0,1,2,3,4]]), [(array([5,4]), 4)]),array([True, True])),
        ]

        for test, expected in cases:
            testing.assert_equal(calc_dig_validator(*test), expected)
    
    def test_calc_repeated_check(self):
        cases = [
            (array([[0,1,2],[0,1,0]]), array([True, True])),
            (array([[1,1,1],[0,1,0]]), array([False, True])),
            (array([[1,1,1],[0,0,0]]), array([False, False])),
        ]

        for test, expected in cases:
            testing.assert_equal(calc_repeated_check(test), expected)

    def test_calc_dig_generator(self):
        cases = [
            ((array([[1,2,3]]), [([1,1,0],2)], 11, lambda x: x*2, None)              , [(array([6], dtype=int8), 2)]),
            ((array([[1,2,3]]), [([1,1,0],2)], 11, lambda x: x, None)                , [(array([3], dtype=int8), 2)]),
            ((array([[1,2,3]]), [([1,1,0],2)], 11, lambda x: x, ['abc'])             , [(array([3], dtype=int8), 2)]),
            ((array([[1,2,0,0]]), [([1,1,0],2)], 11, lambda x: x, None)              , [(array([3], dtype=int8), 2)]),
            ((array([[1,2]]), [([1,1,0],2)], 11, lambda x: x, None)                  , [(array([3], dtype=int8), 1)]),
            ((array([[1]]), [([1,1,0],2)], 11, lambda x: x, None)                    , [(array([1], dtype=int8), 0)]),
            ((array([[5,0,0]]), [([2,0,0],1),([1,1,0],2)], 11, lambda x: x, ['cnh']) , [(array([10], dtype=int8), 1),(array([3], dtype=int8), 2)]),
        ]

        for test, expected in cases:
            self.assertEqual(
                calc_dig_generator(*test)[0],
                expected[0]
            )
    
    def test_calc_federal_unit_validator(self):
        cases = [
            ((array([[1,2,3,4,5]]), (0,1)),array([True])),
            ((array([[0,0,3,4,5]]), (0,1)),array([False])),
            ((array([[0,1,3,4,5]]), (0,1)),array([True])),
            ((array([[2,8,3,4,5]]), (0,1)),array([True])),
            ((array([[2,9,3,4,5]]), (0,1)),array([False])),
        ]

        for test, expected in cases:
            testing.assert_equal(calc_federal_unit_validator(*test), expected)
