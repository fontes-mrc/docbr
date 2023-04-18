from re import search
from typing import (
    Any,
    Callable,
)

from numpy import (
    array,
    char,
    frombuffer,
    ndarray,
    repeat,
)


class RegExr:
    """
    This class provides methods to parse and validate regular expressions in an array of documents.

    :param docs: A numpy.ndarray with the input data.
    :type docs: numpy.ndarray

    :ivar _documents: The processed version of the input data.
    :vartype _documents: numpy.ndarray

    :ivar _is_valid: A numpy.ndarray containing booleans indicating the validity of each document.
    :vartype _is_valid: numpy.ndarray

    :ivar _pattern: The pattern used to search for regular expressions in the input data.
    :vartype _pattern: str

    :ivar _remove_spec_char: Whether or not to remove special characters from the input data.
    :vartype _remove_spec_char: bool

    :ivar _format_mask: The formatting mask to be applied to each document.
    :vartype _format_mask: str

    :ivar _attributes: A dictionary containing functions to collect document attributes.
    :vartype _attributes: dict[str, Any]
    """

    def __init__(self, docs: ndarray) -> None:
        self._documents = docs
        self._is_valid = array([True] * len(docs))

        self._pattern = r""
        self._remove_spec_char = True
        self._format_mask = ""
        self._attributes: dict[str, Any] = {}

    def _search_documents(self, return_values: bool) -> None:
        """
        Searches for regular expressions in the input data.

        :param return_values: Whether or not to return the values found by the regular expression search.
        :type return_values: bool
        """
        self._documents = [search(self._pattern, d) for d in self._documents]
        if return_values:
            self._documents = [
                d[0] if d is not None else None for d in self._documents
            ]
            self._documents = ["" if d is None else d for d in self._documents]
        self._documents = array(self._documents, dtype=str)

    def _check_nulls(self, narray: ndarray, null_value: str = None) -> ndarray:
        """
        Checks for null values in the input data.

        :param narray: The array to be checked for null values.
        :type narray: numpy.ndarray

        :param null_value: The value considered as a null value.
        :type null_value: str

        :return: A numpy.ndarray containing booleans indicating the validity of each document.
        :rtype: numpy.ndarray
        """
        valid = narray != null_value
        return valid

    def _remove_separators(self, narray: ndarray) -> ndarray:
        """
        Removes special characters from the input data.

        :param narray: The array of characters to be processed.
        :type narray: numpy.ndarray

        :return: A numpy.ndarray containing the processed input data.
        :rtype: numpy.ndarray
        """
        narray = narray.view((str, 1)).reshape(len(narray), -1).view(int)

        mask = (narray >= 40) & (narray <= 47)
        mask |= (narray >= 58) & (narray <= 64)
        mask |= (narray >= 91) & (narray <= 96)
        mask |= (narray >= 123) & (narray <= 126)

        # | 40 = '(' | 41 = ')' | 44 = ',' | 45 = '-' |
        # | 46 = '.' | 47 = '/' | 58 = ':' | 59 = ';' |
        # | 60 = '<' | 61 = '=' | 62 = '>' | 63 = '?' |
        # | 64 = '@' | 91 = '[' | 92 = '\' | 93 = ']' |
        # | 94 = '^' | 95 = '_' | 96 = '`' | 123= '{' |
        # | 124= '|' | 125= '}' | 126= '~' |          |

        narray[mask] = 32
        narray = frombuffer(narray.tobytes(), dtype=(str, narray.shape[1]))
        return char.replace(narray, " ", "")

    def _apply_mask(self) -> None:
        """
        Applies the formatting mask to each document using a given format mask.
        """
        frmat = array([self._format_mask]).view(int)
        frmat = repeat([frmat], self._documents.shape[0], axis=0)
        self._documents = self._documents.view((str, 1)).view(int)

        mask = frmat == 35
        frmat[mask] = self._documents

        frmat = frombuffer(frmat.tobytes(), dtype=(str, frmat.shape[1]))
        self._documents = frmat.astype(object)

    def _apply_attribute_function(self, func: Callable) -> ndarray:
        """
        Applies a function to collect an attribute from each document.

        :param func: The function to be applied to each document.
        :type func: Callable[[Any], Any]

        :return: A numpy.ndarray containing the collected attribute for each document.
        :rtype: numpy.ndarray
        """
        if self._documents.dtype != str:
            self._documents = self._documents.astype(str)

        self._documents[self._documents == ""] = "000000000000000"
        return func(self._documents)

    def parse(self, mask: bool) -> ndarray:
        """
        Parses the input data and applies formatting if necessary.

        :param mask: Whether or not to apply the formatting mask to the input data.
        :type mask: bool

        :return: A numpy.ndarray containing the parsed and formatted input data.
        :rtype: numpy.ndarray
        """
        self._search_documents(True)
        self._is_valid &= self._check_nulls(self._documents, null_value="")

        if self._remove_spec_char:
            self._documents = self._remove_separators(self._documents)

        if mask:
            self._apply_mask()

        self._documents = array(self._documents, dtype=object)
        self._documents[~self._is_valid] = None
        return self._documents

    def validate(self, lazy: bool) -> ndarray:
        """
        Validates the input data.

        :param lazy: Whether or not to fit the input data before collecting the attribute.
        :type lazy: bool

        :return: A numpy.ndarray containing the parsed and formatted input data.
        :rtype: numpy.ndarray
        """
        self._search_documents(False)
        self._is_valid &= self._check_nulls(self._documents, null_value="None")

        return self._is_valid

    def get_attribute(self, attribute: str, lazy: bool) -> ndarray:
        """
        Collects a specified attribute from each document.

        :param attribute: The name of the attribute to be collected.
        :type attribute: str

        :param lazy: Whether or not to fit the input data before collecting the attribute.
        :type lazy: bool

        :return: A numpy.ndarray containing the collected attribute for each document.
        :rtype: numpy.ndarray
        """
        if attribute not in list(self._attributes.keys()):
            raise ValueError(f'Attribute "{attribute}" not found')

        self._search_documents(True)
        if self._remove_spec_char:
            self._documents = self._remove_separators(self._documents)

        self._is_valid &= self._check_nulls(self._documents, null_value="")
        self._collected_attr = self._apply_attribute_function(
            self._attributes[attribute]
        )
        self._collected_attr[~self._is_valid] = None
        return self._collected_attr
