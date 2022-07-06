from numpy import ndarray, array
from re import search

def re_searcher(
        narray: ndarray,
        pattern: str,
        return_values: bool
    ) -> ndarray:
    """
    Apply regex search over a numpy array and return a new numpy array with the results.

    Parameters
    ----------
    narray : ndarray
        Numpy array of strings.
    
    pattern : str
        Regex pattern to be used as search.
    
    return_values : bool
        If True, the new numpy array will return the result of the search instead of regex search objects.

    Returns
    -------
    ndarray
        Numpy array of regex search objects or regex search results.
    
    Examples
    --------
    >>> narray = array(['a', 'b', 'c'])
    >>> re_searcher(narray, 'a', True)
    array([True, False, False])
    """
    narray = [search(pattern, d) for d in narray]
    if return_values:
        narray = [d[0] if d != None else None for d in narray]
        narray = ['' if d == None else d for d in narray]
    return array(narray, dtype=str)