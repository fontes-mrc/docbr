from typing import (
    Any,
    Callable,
    List,
    Literal,
    Tuple,
)

from numpy import (
    all,
    array,
    frombuffer,
    hstack,
    indices,
    int8,
    invert,
    ndarray,
    newaxis,
    repeat,
    roll,
    sort,
    zeros,
    zeros_like,
)


class CheckDigit:
    """
    This class provides methods to parse and validate check digits from an array of documents.

    :param docs: A numpy.ndarray with the input data.
    :type docs: numpy.ndarray

    :ivar _documents: The processed version of the input data.
    :vartype _documents: numpy.ndarray

    :ivar _is_valid: A numpy.ndarray containing booleans indicating the validity of each document.
    :vartype _is_valid: numpy.ndarray

    :ivar _doc_len: The desired length for each document.
    :vartype _doc_len: int

    :ivar _modulo: The modulus to be used in the check digit generation/validation process.
    :vartype _modulo: int

    :ivar _format_mask: The formatting mask to be applied to each document.
    :vartype _format_mask: str

    :ivar _operation: A function to be applied to each check digit before validation.
    :vartype _operation: Callable[[Any], Any]

    :ivar _sequence: A list of tuples containing the sequence of coefficients and positions for check digit generation.
    :vartype _sequence: List[Tuple[List[int], int]]

    :ivar _attributes: A dictionary containing functions to collect document attributes.
    :vartype _attributes: dict[str, Any]
    """

    def __init__(self, docs: ndarray) -> None:
        self._documents = docs
        self._is_valid = array([True] * len(docs))

        self._doc_len = 0
        self._modulo = 0
        self._format_mask = ""
        self._operation = lambda x: x
        self._sequence: List[Tuple[List[int], int]] = []
        self._attributes: dict[str, Any] = {}

    def _fit_documents(self, remove_dot_zero: bool = False) -> None:
        """
        Fits the input data to the defined document length and formats.

        :param remove_dot_zero: Whether or not to remove '.0' from the end of the documents.
        :type remove_dot_zero: bool
        """

        def keep_only_digits(narray: ndarray) -> ndarray:
            mask = (narray > 57) | (narray < 48)
            if remove_dot_zero:  # pragma: no cover
                last_id = narray.shape[1] - 1
                ids = indices(narray.shape)[1]
                mask |= (narray + roll(narray, 1) == 94) & (
                    (narray + roll(narray, -1) == 48) | (ids == last_id)
                )
            narray[mask] = 0
            return narray

        def align_chars(
            narray: ndarray, align: Literal["left", "right"]
        ) -> ndarray:
            if align not in ["left", "right"]:  # pragma: no cover
                raise ValueError('align side must be "left" or "right"')

            mask = narray > 0
            justified_mask = sort(mask, 1)
            if align == "left":  # pragma: no cover
                justified_mask = justified_mask[:, ::-1]
            out = zeros_like(narray)
            out[justified_mask] = narray[mask]
            return out

        def fit_length(
            narray: ndarray, char_len: int, align: Literal["left", "right"]
        ) -> ndarray:
            if char_len < 1:  # pragma: no cover
                raise ValueError("char_len must be greater than 0")
            if align not in ["left", "right"]:  # pragma: no cover
                raise ValueError('align side must be "left" or "right"')

            last_id = narray.shape[1] - 1
            n_cols = char_len - last_id - 1

            if n_cols > 0:
                zero = zeros((narray.shape[0], n_cols), dtype=int)
                if align == "left":
                    return hstack((zero, narray))
                else:
                    return hstack((narray, zero))

            elif n_cols < 0:
                if align == "left":
                    return narray[:, -char_len:]
                else:
                    return narray[:, :char_len]

            else:
                return narray

        self._documents = (
            self._documents.view((str, 1))
            .reshape(len(self._documents), -1)
            .view(int)
        )
        self._documents = keep_only_digits(self._documents)
        self._documents = align_chars(self._documents, "right")
        self._documents = fit_length(self._documents, self._doc_len, "left")
        self._documents[self._documents == 0] = 48
        self._documents = frombuffer(
            self._documents.tobytes(), dtype=(str, self._documents.shape[1])
        )
        self._documents = self._documents.astype(str)

    def _get_digits(self) -> ndarray:
        """
        Split the documents into digits.

        :return: A numpy.ndarray containing the digits of the input data.
        :rtype: numpy.ndarray
        """
        chars = self._documents[newaxis].T
        chars = chars.view("U1")
        chars = chars.view(int) - 48
        chars[(chars < 0) | (chars > 9)] = 0
        return array(chars, dtype=int8)

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

    def _check_repeated_digits(self, digits: ndarray) -> ndarray:
        """
        Checks for documents with repeated digits only and invalidates them.

        :param digits: The digits of the input data.
        :type digits: numpy.ndarray

        :return: A numpy.ndarray containing booleans indicating if the document is valid.
        :rtype: numpy.ndarray
        """
        check = all(digits == digits[:, 0][newaxis].T, axis=1)
        check = invert(check)
        return check

    def _validation_process(self, digits: ndarray) -> ndarray:
        """
        Checks the validity of the input data using one or more validation methods.

        :param digits: The digits of the input data.
        :type digits: numpy.ndarray

        :return: A numpy.ndarray containing booleans indicating the validity of each document.
        :rtype: numpy.ndarray
        """
        check_digits = self._generate_check_digit(digits)
        return self._validate_check_digit(digits, check_digits)

    def _generate_check_digit(self, digits: ndarray) -> ndarray:
        """
        Generates a check digit for each document in the input data.

        :param digits: The digits of the input data.
        :type digits: numpy.ndarray

        :return: A list of tuples containing the generated check digit and its position in each document.
        :rtype: List[Tuple[int, int]]
        """
        doc_qty = digits.shape[0]
        digits = digits.copy()
        cache = []
        out = []

        for sequence, position in self._sequence:
            doc_length = min(len(sequence), digits.shape[1])
            sequence_arr = repeat([sequence], doc_qty, axis=0)

            digit = (digits[:, :doc_length] * sequence_arr[:, :doc_length]).sum(
                axis=1
            )
            digit = digit % self._modulo

            cache.append(digit)
            digit = self._operation(digit)
            digit = array(digit, dtype=int8)

            position = min(position, digits.shape[1] - 1)
            digits[:, position] = digit
            out.append((digit, position))

        return out

    def _validate_check_digit(
        self, digits: ndarray, check_digits: ndarray
    ) -> ndarray:
        """
        Validates the check digits in the input data.

        :param digits: The digits of the input data.
        :type digits: numpy.ndarray

        :param check_digits: A list of tuples containing the generated check digit and its position in each document.
        :type check_digits: List[Tuple[int, int]]

        :return: A numpy.ndarray containing booleans indicating the validity of each document.
        :rtype: numpy.ndarray
        """
        checks = []

        for cv_digit_and_position in check_digits:
            cv_digit, position = cv_digit_and_position
            check = digits[:, position] == cv_digit
            checks.append(check)

        return array(checks).all(axis=0)

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
        self._fit_documents()
        self._digits = self._get_digits()

        if mask:
            self._apply_mask()

        self._is_valid &= self._check_repeated_digits(self._digits)
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
        if not lazy:
            self._fit_documents()
        self._digits = self._get_digits()

        self._is_valid &= self._validation_process(self._digits)
        self._is_valid &= self._check_repeated_digits(self._digits)

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

        if not lazy:
            self._fit_documents()
        self._digits = self._get_digits()
        self._collected_attr = self._apply_attribute_function(
            self._attributes[attribute]
        )

        self._is_valid &= self._check_repeated_digits(self._digits)
        self._collected_attr[~self._is_valid] = None

        return self._collected_attr
