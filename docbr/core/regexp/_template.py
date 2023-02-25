from re import search
from typing import Callable
from numpy import(
    ndarray,
    char,
    array,
    frombuffer,
    repeat,
    )

class _RegExrTemplate():
    def __init__(self, docs: ndarray) -> None:
        self._documents = docs
        self._is_valid = array([True] * len(docs))

        self._pattern = r''
        self._remove_spec_char = True
        self._format_mask = ''
        self._attributes = {}

    def _search_documents(self, return_values: bool) -> None:
        self._documents = [search(self._pattern, d) for d in self._documents]
        if return_values:
            self._documents = [d[0] if d != None else None for d in self._documents]
            self._documents = ['' if d == None else d for d in self._documents]
        self._documents = array(self._documents, dtype=str)

    def _check_nulls(self, narray: ndarray, null_value: str = None) -> ndarray:
        valid = narray != null_value
        return valid
    
    def _remove_separators(self, narray: ndarray) -> ndarray:
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

    def _apply_mask(self) -> None:
        frmat = array([self._format_mask]).view(int)
        frmat = repeat([frmat], self._documents.shape[0], axis=0)
        self._documents = self._documents.view((str,1)).view(int)

        mask = frmat == 35
        frmat[mask] = self._documents

        frmat = frombuffer(frmat.tobytes(),dtype=(str,frmat.shape[1]))
        self._documents = frmat.astype(object)

    def _apply_attribute_function(self, func: Callable) -> ndarray:
        if self._documents.dtype != str:
            self._documents = self._documents.astype(str)
        
        self._documents[self._documents==''] = '000000000000000'
        return func(self._documents)

    def parse(self, mask: bool) -> ndarray:
        """
        Parse documents and apply mask if mask is True.
        """
        self._search_documents(True)
        self._is_valid &= self._check_nulls(self._documents, null_value='')

        if self._remove_spec_char:
            self._documents = self._remove_separators(self._documents)
        
        if mask:
            self._apply_mask()

        self._documents = array(self._documents, dtype=object)
        self._documents[~self._is_valid] = None
        return self._documents

    def validate(self, lazy: bool) -> ndarray:
        """
        Validate documents and return a boolean array with the results.
        Lazy is not used in this class, it is only for interface compatibility with other classes.
        """
        self._search_documents(False)
        self._is_valid &= self._check_nulls(self._documents, null_value='None')
        
        return self._is_valid
    
    def get_attribute(self, attribute: str, lazy: bool) -> ndarray:
        """
        Get attribute from documents and return a numpy array.
        Lazy is not used in this class, it is only for interface compatibility with other classes. 
        """
        if attribute not in list(self._attributes.keys()):
            raise ValueError(f'Attribute "{attribute}" not found')

        self._search_documents(True)
        if self._remove_spec_char:
            self._documents = self._remove_separators(self._documents)
        
        self._is_valid &= self._check_nulls(self._documents, null_value='')
        self._collected_attr = self._apply_attribute_function(self._attributes[attribute])
        self._collected_attr[~self._is_valid] = None
        return self._collected_attr