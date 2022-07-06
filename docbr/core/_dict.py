from types import NoneType
from typing import Callable, Union
from numpy import (
    ndarray,
    array,
    repeat,
    vstack, 
    )

def dict_key_selector(
        key_list: list,
        key_pairs: dict
    ) -> dict:
    """
    Select key pair from dictionary based on keys in list and return a new dictiorary.
    Note: key_list = ['*'] selects all keys from key_pairs dictionary.
    
    Parameters
    ----------
    key_list : list of str
        List of keys to select from key_pairs dictionary.
    key_pairs : dict
        Dictionary of key pairs.

    Returns
    -------
    dict
        Dictionary of selected key pairs.

    Raises
    ------
    KeyError
        If key_list contains only keys that isn't in key_pairs dictionary.
    
    Examples
    --------
    >>> key_list = ['a', 'b']
    >>> key_pairs = {'a': 1, 'b': 2, 'c': 3}
    >>> dict_key_selector(key_list, key_pairs)
    {'a': 1, 'b': 2}

    key_list = ['*'] selects all keys from key_pairs dictionary.

    >>> key_list = ['*']
    >>> key_pairs = {'a': 1, 'b': 2, 'c': 3}
    >>> dict_key_selector(key_list, key_pairs)
    {'a': 1, 'b': 2, 'c': 3}

    """
    key_list = [*dict.fromkeys(key_list)]
    
    if len(key_list) == 1 and key_list[0] == '*':
        return key_pairs
    
    else:
        key_list = [k for k in key_list if k in key_pairs.keys()]
        if len(key_list) > 0:
            return {k: key_pairs[k] for k in key_list}
        else:
            raise KeyError('All the keys in given list are not in the key_pairs dictionary.')

def bulk_function_applier(
        narray: ndarray,
        funcs: Union[dict, NoneType],
        is_unique: bool
    ) -> ndarray:

    """
    Applies a series of functions over a numpy array and returns a new numpy array with the results, each element of the array will be a dictionary of the result of each function applied.
    If just one function is given and is_unique is True, the new numpy array will return the result of the function instead of a dictionary of named results.

    Parameters
    ----------
    narray : ndarray
        Numpy array of strings.
    funcs : dict of functions or None
        Dictionary of functions to apply over narray.
    is_unique : bool
        If True, the new numpy array will return the result of the single function instead of a dictionary of named results.

    Returns
    -------
    ndarray
        Numpy array of dictionaries of results.
    
    Raises
    ------
    ValueError
        If funcs is not a dictionary of functions.
    """

    if narray.dtype != str:
        narray = narray.astype(str)
    
    narray[narray=='']='000000000000000'

    keys, values = [], []
    for name, func in funcs.items():
        if not isinstance(func, Callable):
            raise ValueError('funcs must be a dictionary of functions.')
        
        keys.append(name)
        values.append(func(narray))

    if is_unique:
        return array(values[0], dtype=object)

    else:
        values = vstack(values).T
        keys = repeat([keys], values.shape[0], axis=0)
        
        narray = array([dict(zip(k, v)) for k, v in zip(keys, values)], dtype=object)
        return narray