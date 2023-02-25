from numpy import (
    ndarray,
    integer,
    array,
    )
from typing import (
    Iterable,
    Tuple,
    Callable,
    Union,
    )

def io_get(obj) -> Tuple[Callable, type]:
    _iotypes={
        "<class 'int'>":                        (lambda x: array([str(x)])          , str    ),
        "<class 'float'>":                      (lambda x: array([str(x)])          , str    ),
        "<class 'str'>":                        (lambda x: array([x])               , str    ),
        "<class 'numpy.ndarray'>":              (lambda x: array(x, dtype=str)      , ndarray),
        "<class 'list'>":                       (lambda x: array(x, dtype=str)      , ndarray),
        "<class 'pandas.core.series.Series'>":  (lambda x: x.to_numpy().astype(str) , ndarray)
    }

    dtype = str(obj.__class__)
    i_func, o_type = _iotypes.get(dtype, (None,None))

    valid_type = i_func != None
    invalid_iterable = isinstance(obj, Iterable)
    if invalid_iterable:
            invalid_iterable &= dtype != "<class 'pandas.core.series.Series'>"
            invalid_iterable &= not isinstance(obj[0], (float, int, str, integer))

    if valid_type:
        if not invalid_iterable:
            return i_func, o_type
        else:
            raise ValueError(
                "Cannot convert {} to numpy array because it contains types not supported: {}".format(
                    dtype, type(obj[0])
                )
            )
    else:
        raise TypeError(
            "Type {} not supported, please use one of the following: int, float, str, numpy.ndarray, list, pandas.series".format(
                dtype
            )
        )

def io_input_narray(obj, i_func: Callable) -> ndarray:
    return i_func(obj)

def io_output_narray(obj: ndarray, o_type: type) -> Union[str, ndarray]:
    if o_type == str:
        return obj[0]
    if o_type == ndarray:
        return obj