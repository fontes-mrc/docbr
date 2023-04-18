from numpy import (
    frombuffer,
    ndarray,
)


def array_slicer(
    narray: ndarray, start: int, end: int = None, dtype: type = str
) -> ndarray:
    """
    Slices a numpy.ndarray along its second axis based on a start and (optionally) an end index.

    :param narray: The numpy.ndarray to be sliced.
    :type narray: ndarray

    :param start: The index at which to begin slicing the numpy.ndarray.
    :type start: int

    :param end: The index at which to stop slicing the numpy.ndarray. If not provided, only the element at `start` will be extracted.
    :type end: int, optional

    :param dtype: The desired output data type (str or int).
    :type dtype: type

    :return: A new numpy.ndarray containing the sliced elements.
    :rtype: ndarray

    :raises ValueError: If the specified data type is not supported.
    """
    if dtype not in [str, int]:
        raise ValueError("dtype must be str or int")

    narray = narray.view((str, 1)).reshape(len(narray), -1)
    if end is not None:
        end += 1
        narray = narray[:, start:end]
        _inner_dtype = (str, end - start)
    else:
        narray = narray[:, start]
        _inner_dtype = (str, 1)
    narray = frombuffer(narray.tobytes(), dtype=_inner_dtype)
    return narray.astype(dtype)
