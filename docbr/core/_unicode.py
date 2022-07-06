from typing import Literal
from numpy import(
    ndarray,
    char,
    newaxis,
    int8,
    array,
    frombuffer,
    hstack,
    indices,
    repeat,
    roll,
    sort,
    zeros_like,
    zeros,
    )

def un_only_digits(
        narray: ndarray,
        remove_dot_zero: bool = True
    ) -> ndarray:
    """
    Remove all characters except numbers from a given numpy array of unicode strings.
    By default, it removes '.0' from the end of the string.

    Parameters
    ----------
    narray: ndarray
        A numpy array of unicode strings.
    remove_dot_zero: bool
        If True, it removes '.0' from the end of the string.

    Returns
    -------
    ndarray
        A numpy array of unicode strings with only numbers.
    
    Examples
    --------
    >>> un_arr = array(['abc123', '14.0'])
    >>> un_only_digits(un_arr)
    array(['123', '14'])
    """
    mask = (narray > 57) | (narray < 48)
    
    if remove_dot_zero:
        last_id = narray.shape[1] - 1
        ids = indices(narray.shape)[1]
        mask |= (narray + roll(narray,1) == 94) & ((narray + roll(narray,-1) == 48) | (ids == last_id))
    
    narray[mask] = 0
    return narray

def un_align_chars(
        narray: ndarray,
        side: Literal['left','right'] = 'right'
    ) -> ndarray:
    """
    Aligns the characters of a given numpy array of decoded unicode strings.
    By default, it aligns the characters to the right.
    
    Parameters
    ----------
    narray: ndarray
        A numpy array of decoded unicode strings.
    side: Literal['left','right']
        If 'left', it aligns the characters to the left, otherwise to the right.
    
    Returns
    -------
    ndarray
        A numpy array of decoded unicode strings with aligned characters.
    
    Raises
    ------
    ValueError
        If side is not 'left' or 'right'.
    
    Examples
    --------
    >>> un_arr = array([[41,0,45],[0,54,0]])
    >>> un_align_chars(un_arr, 'left')
    array([[41,45,0],[54,0,0]])
        
    >>> un_arr = array([[41,0,45],[0,54,0]])
    >>> un_align_chars(un_arr, 'right')
    array([[0,41,45],[0,0,54]])
    """
    if side not in ['left','right']:
        raise ValueError('side must be "left" or "right"')

    mask = narray>0
    justified_mask = sort(mask,1)
    if side=='left':
        justified_mask = justified_mask[:,::-1]
    out = zeros_like(narray) 
    out[justified_mask] = narray[mask]
    return out

def un_assert_lenght(
        narray: ndarray,
        lenght: int,
        change_side: Literal['left','right'] = 'right'
    ) -> ndarray:
    """
    Asserts the lenght of a given numpy array of decoded unicode strings.
    By default, it moves the characters from the right side.

    Parameters
    ----------
    narray: ndarray
        A numpy array of decoded unicode strings.
    lenght: int
        The desired lenght of the string.
    change_side: Literal['left','right']
        If 'left', it moves the characters from the left side, otherwise from the right.
    
    Returns
    -------
    ndarray
        A numpy array of decoded unicode strings with the desired lenght.
    
    Raises
    ------
    ValueError
        If change_side is not 'left' or 'right'.
    
    Examples
    --------
    >>> un_arr = array([[41,0,45],[0,54,0]])
    >>> un_assert_lenght(un_arr, 5, 'left')
    array([[0,0,41,0,45],[0,0,0,54,0]])

    >>> un_arr = array([[41,0,45],[0,54,0]])
    >>> un_assert_lenght(un_arr, 5, 'right')
    array([[41,0,45,0,0],[0,54,0,0,0]])

    >>> un_arr = array([[41,0,45],[0,54,0]])
    >>> un_assert_lenght(un_arr, 3, 'left')
    array([[0,45],[54,0]])

    >>> un_arr = array([[41,0,45],[0,54,0]])
    >>> un_assert_lenght(un_arr, 3, 'right')
    array([[41,0],[0,54]])
    """
    if lenght < 1:
        raise ValueError('lenght must be greater than 0')
    if change_side not in ['left','right']:
        raise ValueError('side must be "left" or "right"')

    last_id = narray.shape[1] - 1
    n_cols = lenght - last_id - 1
    
    if n_cols > 0:
        zero = zeros((narray.shape[0], n_cols), dtype=int)
        if change_side == 'left':
            return hstack((zero, narray))
        else:
            return hstack((narray, zero))

    elif n_cols < 0:
        if change_side == 'left':
            return narray[:,-lenght:]
        else:
            return narray[:,:lenght]
    
    else:
        return narray

def un_slicer(
        narray: ndarray,
        start:int,
        end:int = None,
        dtype: type = str
    ) -> ndarray:
    """
    Slice a given numpy array of unicode strings based on the start and end position of the string.

    Parameters
    ----------
    narray: ndarray
        A numpy array of unicode strings.
    start: int
        The start position of the string slicing.
    end: int optional
        The end position of the string slicing, if None, the character on the start position will be returned.
    dtype: type optional
        The desired type of the output numpy array. It can be str or int.
    
    Returns
    -------
    ndarray
        A numpy array of unicode strings with the desired slicing.

    Raises
    ------
    ValueError
        If dtype is not str or int.

    Examples
    --------
    >>> un_arr = array(['abcdef'])
    >>> un_slicer(un_arr, 1, 3)
    array(['bcd'])

    >>> un_arr = array(['abcdef'])
    >>> un_slicer(un_arr, 1)
    array(['b'])

    >>> un_arr = array(['1'])
    >>> un_slicer(un_arr, 1, dtype=int)
    array([1])
    """
    if dtype not in [str, int]:
        raise ValueError('dtype must be str or int')

    narray = narray.view((str,1)).reshape(len(narray),-1)
    if end != None:
        end += 1
        narray = narray[:,start:end]
        _inner_dtype = (str,end-start)
    else:
        narray = narray[:,start]
        _inner_dtype = (str,1)
    narray = frombuffer(narray.tobytes(),dtype=_inner_dtype)
    return narray.astype(dtype)

def un_digit_retriever(
        narray: ndarray
    ) -> ndarray:
    """
    Retrieves the digits of a given numpy array of unicode strings and return a numpy array of integers (2D).

    Parameters
    ----------
    narray: ndarray
        A numpy array of unicode strings.
    
    Returns
    -------
    ndarray
        A numpy array of integers (2D).
    
    Examples
    --------
    >>> un_arr = array(['123x'])
    >>> un_digit_retriever(un_arr)
    array([[1,2,3]])
    """
    chars = narray[newaxis].T
    chars = chars.view('U1')
    chars = chars.view(int) - 48
    chars[(chars < 0) | (chars > 9)] = 0
    return array(chars, dtype=int8)

def un_digit_extractor(
        narray: ndarray,
        char_len: int
    ) -> ndarray:
    """
    Extract the digits of a given numpy array of unicode strings and return a new string of a given lenght.

    Parameters
    ----------
    narray: ndarray
        A numpy array of unicode strings.
    char_len: int
        The desired lenght of the string.

    Returns
    -------
    ndarray
        A numpy array of unicode strings with only digits with the desired lenght.

    
    Examples
    --------
    >>> un_arr = array(['123x'])
    >>> un_digit_extractor(un_arr, 3)
    array(['123'])

    >>> un_arr = array(['123x'])
    >>> un_digit_extractor(un_arr, 5)
    array(['00123'])
    """
    narray = narray.view((str,1)).reshape(len(narray), -1).view(int)
    narray = un_only_digits(narray, remove_dot_zero=True)
    narray = un_align_chars(narray, 'right')
    narray = un_assert_lenght(narray, char_len, 'left')
    narray[narray==0] = 48
    narray = frombuffer(narray.tobytes(),dtype=(str,narray.shape[1]))
    return narray.astype(str)

def un_formatter(
        narray: ndarray,
        frmat: ndarray
    ) -> ndarray:
    """
    Format a given numpy array of unicode strings based on a given format mask.

    Parameters
    ----------
    narray: ndarray
        A numpy array of unicode strings.
    frmat: ndarray
        A numpy array of decoded unicode strings with the format mask.
        
        "#" represents a character that will be replaced by the corresponding character in the numpy array.
    
    Returns
    -------
    ndarray
        A numpy array of unicode strings with the desired format.
    
    Examples
    --------
    >>> un_arr = array(['12345'])
    >>> frmat = array(['##.###']).view(int)
    >>> un_formatter(un_arr, frmat)
    array(['12.345'])
    """
    if narray.dtype == object:
        narray = narray.astype(str)
    
    frmat = repeat([frmat], narray.shape[0], axis=0)
    narray = narray.view((str,1)).view(int)

    mask = frmat == 35
    frmat[mask] = narray

    frmat = frombuffer(frmat.tobytes(),dtype=(str,frmat.shape[1]))
    return frmat.astype(str)

def un_null_validator(
        narray: ndarray,
        na: str = None
    ) -> ndarray:
    """
    Check if an element of an numpy array is null based on a given value to be considered null.

    Parameters
    ----------
    narray: ndarray
        A numpy array of unicode strings.
    na: str optional
        The value to be considered null.
    
    Returns
    -------
    ndarray
        A numpy array of booleans.
    
    Examples
    --------
    >>> un_arr = array(['12345', ''])
    >>> un_null_validator(un_arr, na='')
    array([ True,  False])
    """
    valid = narray != na
    return valid

def un_remove_separator(
        narray: ndarray,
    ) -> ndarray:
    """
    Remove the separator characters of a given numpy array of unicode strings.

    Parameters
    ----------
    narray: ndarray
        A numpy array of unicode strings.
    
    Returns
    -------
    ndarray
        A numpy array of unicode strings without separators.
    
    Examples
    --------
    >>> un_arr = array(['12.345', '12-345'])
    >>> un_remove_separator(un_arr)
    array(['12345', '12345'])
    """
    narray = narray.view((str,1)).reshape(len(narray), -1).view(int)

    mask  = (narray >=  40) & (narray <=  47) 
    mask |= (narray >=  58) & (narray <=  64) 
    mask |= (narray >=  91) & (narray <=  96) 
    mask |= (narray >= 123) & (narray <= 126)

    # | 40 = '(' | 41 = ')' | 44 = ',' | 45 = '-' |
    # | 46 = '.' | 47 = '/' | 58 = ':' | 59 = ';' |
    # | 60 = '<' | 61 = '=' | 62 = '>' | 63 = '?' |
    # | 64 = '@' | 91 = '[' | 92 = '\' | 93 = ']' |
    # | 94 = '^' | 95 = '_' | 96 = '`' | 123= '{' |
    # | 124= '|' | 125= '}' | 126= '~' |          |

    narray[mask] = 32
    narray = frombuffer(narray.tobytes(),dtype=(str,narray.shape[1]))
    return char.replace(narray, ' ', '')