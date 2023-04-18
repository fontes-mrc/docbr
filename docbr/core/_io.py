from typing import (
    Any,
    Callable,
    Iterable,
    Optional,
    Tuple,
    Union,
)

from numpy import (
    array,
    integer,
    ndarray,
)


def io_get(obj: Any) -> Tuple[Optional[Callable[[Any], Any]], Optional[Any]]:
    """
    Determines the input conversion function and output type based on the type of an input object.

    :param obj: The input object.
    :type obj: Any

    :return: A tuple containing the input conversion function and the output type.
    :rtype: Tuple[Optional[Callable[[Any], Any]], Optional[Any]]

    :raises TypeError: If the type of the input object is not supported.
    :raises ValueError: If the input object contains types that are not supported.
    """
    _iotypes = {
        "<class 'int'>": (lambda x: array([str(x)]), str),
        "<class 'float'>": (lambda x: array([str(x)]), str),
        "<class 'str'>": (lambda x: array([x]), str),
        "<class 'numpy.ndarray'>": (lambda x: array(x, dtype=str), ndarray),
        "<class 'list'>": (lambda x: array(x, dtype=str), ndarray),
        "<class 'pandas.core.series.Series'>": (
            lambda x: x.to_numpy().astype(str),
            ndarray,
        ),
    }

    dtype = str(obj.__class__)
    i_func, o_type = _iotypes.get(dtype, (None, None))

    valid_type = i_func is not None
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


def io_input_narray(obj: Any, i_func: Callable) -> ndarray:
    """
    Converts an input object to a numpy.ndarray using the specified input conversion function.

    :param obj: The input object.
    :type obj: Any

    :param i_func: The input conversion function.
    :type i_func: Callable

    :return: The input object as a numpy.ndarray.
    :rtype: ndarray
    """
    return i_func(obj)


def io_output_narray(obj: ndarray, o_type: type) -> Union[str, ndarray]:
    """
    Converts a numpy.ndarray to either a string or numpy.ndarray depending on the specified output type.

    :param obj: The numpy.ndarray to be converted.
    :type obj: ndarray

    :param o_type: The desired output type.
    :type o_type: type

    :return: The numpy.ndarray as either a string or numpy.ndarray.
    :rtype: Union[str, ndarray]

    :raises TypeError: If the output type is not supported.
    """
    if o_type == str:
        return obj[0]
    elif o_type == ndarray:
        return obj
    else:
        raise TypeError(
            f"Type {o_type} not supported, please use str or numpy.ndarray"
        )
