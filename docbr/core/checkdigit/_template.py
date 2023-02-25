from typing import Literal, Callable
from numpy import(
    ndarray,
    newaxis,
    int8,
    invert,
    all,
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

class _CheckDigitTemplate():
    def __init__(self, docs: ndarray) -> None:
        self._documents = docs
        self._is_valid = array([True] * len(docs))
        
        self._doc_len = 0
        self._modulo = 0
        self._format_mask = ''
        self._operation = lambda x: x
        self._sequence = []
        self._attributes = {}

    def _fit_documents(self, remove_dot_zero: bool = False) -> None:

        def keep_only_digits(narray: ndarray) -> None:
            mask = (narray > 57) | (narray < 48)
            if remove_dot_zero: #pragma: no cover
                last_id = narray.shape[1] - 1
                ids = indices(narray.shape)[1]
                mask |= (narray + roll(narray,1) == 94) & ((narray + roll(narray,-1) == 48) | (ids == last_id))
            narray[mask] = 0
            return narray

        def align_chars(narray: ndarray, align: Literal['left', 'right']) -> None:
            if align not in ['left','right']: #pragma: no cover
                raise ValueError('align side must be "left" or "right"')

            mask = narray > 0
            justified_mask = sort(mask,1)
            if align=='left': #pragma: no cover
                justified_mask = justified_mask[:,::-1]
            out = zeros_like(narray) 
            out[justified_mask] = narray[mask]
            return out

        def fit_length(narray: ndarray, char_len: int, align: Literal['left', 'right']) -> None:
            if char_len < 1: #pragma: no cover
                raise ValueError('char_len must be greater than 0')
            if align not in ['left','right']: #pragma: no cover
                raise ValueError('align side must be "left" or "right"')

            last_id = narray.shape[1] - 1
            n_cols = char_len - last_id - 1
            
            if n_cols > 0:
                zero = zeros((narray.shape[0], n_cols), dtype=int)
                if align == 'left':
                    return hstack((zero, narray))
                else:
                    return hstack((narray, zero))

            elif n_cols < 0:
                if align == 'left':
                    return narray[:,-char_len:]
                else:
                    return narray[:,:char_len]
    
            else:
                return narray

        self._documents = self._documents.view((str,1)).reshape(len(self._documents), -1).view(int)
        self._documents = keep_only_digits(self._documents)
        self._documents = align_chars(self._documents, 'right')
        self._documents = fit_length(self._documents, self._doc_len, 'left')
        self._documents[self._documents==0] = 48
        self._documents = frombuffer(self._documents.tobytes(),dtype=(str,self._documents.shape[1]))
        self._documents = self._documents.astype(str)

    def _get_digits(self) -> ndarray:
        chars = self._documents[newaxis].T
        chars = chars.view('U1')
        chars = chars.view(int) - 48
        chars[(chars < 0) | (chars > 9)] = 0
        return array(chars, dtype=int8)

    def _apply_mask(self) -> None:
        frmat = array([self._format_mask]).view(int)
        frmat = repeat([frmat], self._documents.shape[0], axis=0)
        self._documents = self._documents.view((str,1)).view(int)

        mask = frmat == 35
        frmat[mask] = self._documents

        frmat = frombuffer(frmat.tobytes(),dtype=(str,frmat.shape[1]))
        self._documents = frmat.astype(object)

    def _check_repeated_digits(self, digits: ndarray) -> ndarray:
        check = all(digits == digits[:,0][newaxis].T, axis=1)
        check = invert(check)
        return check

    def _validation_process(self, digits: ndarray) -> ndarray:
        check_digits = self._generate_check_digit(digits)
        return self._validate_check_digit(digits, check_digits)

    def _generate_check_digit(self, digits: ndarray) -> ndarray:
        doc_qty = digits.shape[0]
        digits = digits.copy()
        cache = []
        out = []

        for sequence, position in self._sequence:
            doc_length = min(len(sequence), digits.shape[1])
            sequence_arr = repeat([sequence], doc_qty, axis=0)

            digit = (digits[:,:doc_length] * sequence_arr[:,:doc_length]).sum(axis=1)
            digit = digit % self._modulo

            cache.append(digit)
            digit = self._operation(digit)
            digit = array(digit, dtype=int8)

            position = min(position, digits.shape[1] -1)
            digits[:, position] = digit
            out.append((digit,position))

        return out

    def _validate_check_digit(self, digits: ndarray, check_digits: ndarray) -> ndarray:
        checks = []

        for cv_digit_and_position in check_digits:
            cv_digit, position = cv_digit_and_position
            check = digits[:,position] == cv_digit
            checks.append(check)
        
        return array(checks).all(axis=0)

    def _apply_attribute_function(self, func: Callable) -> ndarray:
        if self._documents.dtype != str:
            self._documents = self._documents.astype(str)
        
        self._documents[self._documents==''] = '000000000000000'
        return func(self._documents)

    def parse(self, mask: bool) -> ndarray:
        """
        Parse documents and apply mask if mask is True.
        """
        self._fit_documents()
        self._digits = self._get_digits()
        
        if mask:
            self._apply_mask()

        self._is_valid &= self._check_repeated_digits(self._digits)
        self._documents[~self._is_valid] = None
        
        return self._documents

    def validate(self, lazy: bool) -> ndarray:
        """
        Validate documents and return a boolean array with the results.
        If lazy is True, documents will not be parsed.
        """
        if not lazy:
            self._fit_documents()
        self._digits = self._get_digits()

        self._is_valid &= self._validation_process(self._digits)
        self._is_valid &= self._check_repeated_digits(self._digits)

        return self._is_valid
    
    def get_attribute(self, attribute: str, lazy: bool) -> ndarray:
        """
        Get attribute from documents and return a numpy array.
        If lazy is True, documents will not be parsed.
        """
        if attribute not in list(self._attributes.keys()):
            raise ValueError(f'Attribute "{attribute}" not found')

        if not lazy:
            self._fit_documents()
        self._digits = self._get_digits()
        self._collected_attr = self._apply_attribute_function(self._attributes[attribute])
        
        self._is_valid &= self._check_repeated_digits(self._digits)
        self._collected_attr[~self._is_valid] = None

        return self._collected_attr
