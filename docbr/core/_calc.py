from typing import Callable, Tuple
from numpy import (
    ndarray, 
    newaxis, 
    int8, 
    invert, 
    all, 
    array, 
    where,
    repeat, 
    )

def calc_federal_unit_validator(
        digs: ndarray,
        dig_fu: tuple[int, int]
    ) -> ndarray:
    """
    Check if the digits in a given range of a numpy array of digits are between 01 and 28 (they are representations of the federal states in Brazil).
    
    Parameters
    ----------
    digs : ndarray
        Numpy array of digits.
    dig_fu : tuple of int
        Tuple of the first and last digit of the federal unit.

    Returns
    -------
    ndarray
        Numpy array of boolean values.

    Examples
    --------
    >>> digs = array([[1,2,3],[4,2,2]])
    >>> calc_federal_unit_validator(digs, (0,1))
    array([[ True,  False]
    """

    left_fu, right_fu = dig_fu
    check = (digs[:, left_fu] == 1)
    check |= (digs[:, left_fu] == 2) & (digs[:, right_fu] < 9)
    check |= (digs[:, left_fu] == 0) & (digs[:, right_fu] > 0)
    return check

def calc_dig_validator(
        digs: ndarray,
        cv_digs: list[tuple[ndarray, int]]
    ) -> ndarray:
    """
    Check if an numpy array of digits is valid given a numpy array of valid digits and the position of digits to check.

    Parameters
    ----------
    digs : ndarray
        Numpy array of digits.
    cv_digs : list of tuple of array of digits and int
        List of tuples of numpy array of digits and the position of digits to check.
    
    Returns
    -------
    ndarray
        Numpy array of boolean values.

    Examples
    --------
    >>> digs = array([[1,2,3],[1,2,2]])
    >>> cv_digs = [(array([2,2]), 1),(array([3,2]), 2)]
    >>> calc_dig_validator(digs, cv_digs)
    array([[ True,  True]
    """

    checks = []
    for cv_dig_pos in cv_digs:
        cv_dig, pos = cv_dig_pos
        check = digs[:, pos] == cv_dig
        checks.append(check)

    checks = array(checks).all(axis=0)

    return checks

def calc_repeated_check(
        digs: ndarray
    ) -> ndarray:
    """
    Check if an element (row) of a numpy array of digits (2d array) contains repeated digits.

    Parameters
    ----------
    digs : ndarray
        Numpy array of digits.

    Returns
    -------
    ndarray
        Numpy array of boolean values.

    Examples
    --------
    >>> digs = array([[1,2,3],[1,1,1]])
    >>> calc_repeated_check(digs)
    array([[ False,  True]
    """
    
    check = all(digs == digs[:,0][newaxis].T, axis=1)
    return invert(check)

def calc_dig_generator(
        digs: ndarray,
        dig_seq: list[tuple[list,int]],
        dig_mod: int,
        dig_oper: Callable,
        special_oper: list = None
    ) -> list[Tuple[ndarray,int]]:
    """
    Generate a list of numpy arrays of check digits given specific parameters.
    It uses a digit sequence to generate a list of numpy arrays of check digits.
    
    Those numpy arrays of check digits are passed to a specific digit modulo and a specific digit operation in order to generate the results.

    Parameters
    ----------
    digs : ndarray
        Numpy array of digits.
    dig_seq : list of tuple of list of int and int
        List of tuples of list of digits and the position of digits to generate the new array.
    dig_mod : int
        Modulo to be aplied to the results of multiplication of digs and dig_seq.
    dig_oper : Callable
        Function to be applied over result of modulo.
    special_oper : list of str, optional
        List of special operations to be applied over the result of modulo. The default is None.

    Returns
    -------
    list of tuple of ndarray and int
        List of tuples of numpy array of digits and the position of array belongs in the original array.

    Examples
    --------
    >>> digs = array([[1,2,3],[1,2,5]])
    >>> dig_seq = [([1,1,0], 1),([2,2,0], 2)]
    >>> dig_mod = 10
    >>> dig_oper = lambda x: x
    >>> calc_dig_generator(digs, dig_seq, dig_mod, dig_oper)
    [(array([2,2]), 1), (array([3,5]), 2)]
    """
    doc_qt = digs.shape[0]
    digs = digs.copy()
    cache = []
    out = []

    for seq, pos in dig_seq:
        doc_len = min(len(seq), digs.shape[1])
        seq = repeat([seq], doc_qt, axis=0)
        
        dig = (digs[:,:doc_len] * seq[:,:doc_len]).sum(axis=1)
        dig = dig % dig_mod
        
        if special_oper != None and 'cnh' in special_oper:
            if len(cache) > 0:
                dig = where(cache[0] < 10, dig, where(dig - 2 < 0, dig + 9, dig - 2))

        cache.append(dig)
        dig = dig_oper(dig)
        dig = array(dig, dtype=int8)

        pos = min(pos, digs.shape[1] -1)
        digs[:, pos] = dig
        out.append((dig,pos))
    
    return out