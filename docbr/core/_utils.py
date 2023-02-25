from numpy import ndarray, frombuffer

def array_slicer(
        narray: ndarray,
        start:int,
        end:int = None,
        dtype: type = str
    ) -> ndarray:
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