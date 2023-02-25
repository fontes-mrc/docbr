from typing import Literal, Union
from numpy import ndarray

from docbr.attributes import AttributeStr
from docbr.core.checkdigit._template import _CheckDigitTemplate
from docbr.core.regexp._template import _RegExrTemplate
from docbr.core._io import io_get, io_input_narray, io_output_narray
from docbr.core.checkdigit.documents import (
    CPF,
    CNPJ,
    CNH,
    TituloEleitor,
    PIS,
    Certidao,
    Renavam,
)
from docbr.core.regexp.documents import (
    CarPlate,
    Email,
    Phone,
)

def _get_instance(doctype: str) -> _CheckDigitTemplate | _RegExrTemplate:
    classes = {
        'cpf': CPF,
        'cnpj': CNPJ,
        'cnh': CNH,
        'te': TituloEleitor,
        'pis': PIS,
        'cert': Certidao,
        'rnvam': Renavam,
        'placa': CarPlate,
        'tfone': Phone,
        'email': Email,
    }
    if doctype not in classes:
        raise ValueError(f'doctype must be one of the following: {list(classes.keys())}')
    return classes[doctype]

def parse(
        doclist,
        doctype: Literal[
            'cnpj',
            'cpf',
            'cnh',
            'te',
            'pis',
            'cert',
            'rnvam',
            'placa',
            'tfone',
            'email',
        ],
        mask: bool = False,
    ) -> Union[str, ndarray]:
    """
    Extracts the document and returns its corrected value, adding a mask on the document is an option.
    This method accepts objects of type str, int, float, list, numpy.ndarray and pandas.series.
    
    Parameters
    ----------
    doc
        Document(s) to be extracted.
    doctype: str
        Type of document to be extracted, can be: cnpj, cpf, cnh, te, pis, cert, rnvam, placa, tfone, email.
    mask: bool
        If True, adds a mask on the document.
    
    Return
    ------
    ndarray or str
        Returns the extracted document(s) as numpy.ndarray or str.
    Raises
    ------
    
    TypeError
        If the type of the document(s) sent is not str, int, float, list, ndarray or pandas series.
    ValueError
        If the document type is not recognized.
    """

    i_func, o_type = io_get(doclist)
    doclist = io_input_narray(doclist, i_func)
    instance = _get_instance(doctype)
    result = instance(doclist).parse(mask)
    return io_output_narray(result, o_type)

def validate(
        doclist,
        doctype: Literal[
            'cnpj',
            'cpf',
            'cnh',
            'te',
            'pis',
            'cert',
            'rnvam',
            'placa',
            'tfone',
            'email',
        ],
        lazy: bool = False,
    ) -> Union[str, ndarray]:
    """
    Validates the document and returns True if the document is valid.
    This method accepts objects of type str, int, float, list, numpy.ndarray and pandas.series.
    
    Parameters
    ----------
    doc
        Document(s) to be extracted.
    doctype: str
        Type of document to be extracted, can be: cnpj, cpf, cnh, te, pis, cert, rnvam, placa, tfone, email.
    lazy: bool
        If True, does not perform the extraction of the document, just returns True or False directly on the conceived value.
    
    Return
    ------
    ndarray or str
        Returns True if the document is valid or False if the document is invalid.
    
    Raises
    ------
    TypeError
        If the type of the document(s) sent is not str, int, float, list, ndarray or pandas series.
    ValueError
        If the document type is not recognized.
    """

    i_func, o_type = io_get(doclist)
    doclist = io_input_narray(doclist, i_func)
    instance = _get_instance(doctype)
    result = instance(doclist).validate(lazy)
    return io_output_narray(result, o_type)

def get_attribute(
        doclist,
        doctype: Literal[
            'cnpj',
            'cpf',
            'cnh',
            'te',
            'pis',
            'cert',
            'rnvam',
            'placa',
            'tfone',
            'email'
        ],
        attr: AttributeStr,
        lazy: bool = False,
    ) -> Union[str, ndarray]:
    """
    Collects an attribute from the document if it is valid.

    Parameters
    ----------
    doclist
        Document(s) to be extracted.
    doctype: str
        Type of document to be extracted, can be: cnpj, cpf, cnh, te, pis, cert, rnvam, placa, tfone, email.
    attr: AttributeStr
        Document attribute, must be one of the document class attributes.
    lazy: bool
        If True, does not perform the extraction of the document, just returns the attribute directly on the conceived value.
    
    Returns
    -------
        Returns the extracted attribute(s) as numpy.ndarray or dict.
    
    Raises
    ------
    TypeError
        If the type of the document(s) sent is not int, float, list, ndarray or pandas series.
    ValueError
        If the document type is not recognized.
        If the attribute is not recognized.
    """

    i_func, o_type = io_get(doclist)
    doclist = io_input_narray(doclist, i_func)
    instance = _get_instance(doctype)
    result = instance(doclist).get_attribute(attr, lazy)
    return io_output_narray(result, o_type)