from typing import (
    Any,
    Literal,
    Union,
)

from numpy import ndarray

from docbr.attributes import AttributeStr
from docbr.core._io import (
    io_get,
    io_input_narray,
    io_output_narray,
)
from docbr.core.checkdigit._template import CheckDigit
from docbr.core.checkdigit.documents import (
    CNH,
    CNPJ,
    CPF,
    PIS,
    Certidao,
    Renavam,
    TituloEleitor,
)
from docbr.core.regexp._template import RegExr
from docbr.core.regexp.documents import (
    CarPlate,
    Email,
    Phone,
)


def _get_instance(doctype: str) -> CheckDigit | RegExr:
    """
    Return an instance of a class that validates documents based on the input `doctype`.

    :param doctype: A string representing the type of document to be validated.
    :type doctype: str

    :return: An instance of the appropriate validation class based on `doctype`.
    :rtype: CheckDigit or RegExr

    :raises ValueError: If `doctype` is not one of the supported document types.
    """
    classes = {
        "cpf": CPF,
        "cnpj": CNPJ,
        "cnh": CNH,
        "te": TituloEleitor,
        "pis": PIS,
        "cert": Certidao,
        "rnvam": Renavam,
        "placa": CarPlate,
        "tfone": Phone,
        "email": Email,
    }
    if doctype not in classes:
        raise ValueError(
            f"doctype must be one of the following: {list(classes.keys())}"
        )
    return classes[doctype]


def parse(
    doclist: Any,
    doctype: Literal[
        "cnpj",
        "cpf",
        "cnh",
        "te",
        "pis",
        "cert",
        "rnvam",
        "placa",
        "tfone",
        "email",
    ],
    mask: bool = False,
) -> Union[str, ndarray]:
    """
    Extracts the document and returns its corrected value.

    :param doclist: Document(s) to be extracted.
    :type doclist: Any

    :param doctype: Type of document to be extracted, can be: cnpj, cpf, cnh, te, pis, cert, rnvam, placa, tfone, email.
    :type doctype: Literal["cnpj", "cpf", "cnh", "te", "pis", "cert", "rnvam", "placa", "tfone", "email"]

    :param mask: If True, adds a mask on the document.
    :type mask: bool

    :return: Returns the extracted document(s) as numpy.ndarray or str.
    :rtype: Union[str, ndarray]

    :raises TypeError: If the type of the document(s) sent is not str, int, float, list, ndarray or pandas series.
    :raises ValueError: If the document type is not recognized.
    """

    i_func, o_type = io_get(doclist)
    doclist = io_input_narray(doclist, i_func)
    instance = _get_instance(doctype)
    result = instance(doclist).parse(mask)
    return io_output_narray(result, o_type)


def validate(
    doclist: Any,
    doctype: Literal[
        "cnpj",
        "cpf",
        "cnh",
        "te",
        "pis",
        "cert",
        "rnvam",
        "placa",
        "tfone",
        "email",
    ],
    lazy: bool = False,
) -> Union[str, ndarray]:
    """
    Validates the document and returns True if the document is valid.

    :param doclist: Document(s) to be extracted.
    :type doclist: Any

    :param doctype: Type of document to be extracted, can be: cnpj, cpf, cnh, te, pis, cert, rnvam, placa, tfone, email.
    :type doctype: Literal["cnpj", "cpf", "cnh", "te", "pis", "cert", "rnvam", "placa", "tfone", "email"]

    :param lazy: If True, does not perform the extraction of the document, just returns True or False directly on the conceived value.
    :type lazy: bool

    :return: Returns the extracted document(s) as numpy.ndarray or str.
    :rtype: Union[str, ndarray]

    :raises TypeError: If the type of the document(s) sent is not str, int, float, list, ndarray or pandas series.
    :raises ValueError: If the document type is not recognized.
    """

    i_func, o_type = io_get(doclist)
    doclist = io_input_narray(doclist, i_func)
    instance = _get_instance(doctype)
    result = instance(doclist).validate(lazy)
    return io_output_narray(result, o_type)


def get_attribute(
    doclist: Any,
    doctype: Literal[
        "cnpj",
        "cpf",
        "cnh",
        "te",
        "pis",
        "cert",
        "rnvam",
        "placa",
        "tfone",
        "email",
    ],
    attr: AttributeStr,
    lazy: bool = False,
) -> Union[str, ndarray]:
    """
    Collects an attribute from the document if it is valid.

    :param doclist: Document(s) to be extracted.
    :type doclist: Any

    :param doctype: Type of document to be extracted, can be: cnpj, cpf, cnh, te, pis, cert, rnvam, placa, tfone, email.
    :type doctype: Literal["cnpj", "cpf", "cnh", "te", "pis", "cert", "rnvam", "placa", "tfone", "email"]

    :param attr: Document attribute, must be one of the document class attributes.
    :type attr: AttributeStr

    :param lazy: If True, does not perform the extraction of the document, just returns True or False directly on the conceived value.
    :type lazy: bool

    :return: Returns the extracted document(s) as numpy.ndarray or str.
    :rtype: Union[str, ndarray]

    :raises TypeError: If the type of the document(s) sent is not str, int, float, list, ndarray or pandas series.
    :raises ValueError: If the document type is not recognized.
    """

    i_func, o_type = io_get(doclist)
    doclist = io_input_narray(doclist, i_func)
    instance = _get_instance(doctype)
    result = instance(doclist).get_attribute(attr, lazy)
    return io_output_narray(result, o_type)
