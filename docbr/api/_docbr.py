from numpy import ndarray
from typing import(
    Union,
    Literal,
    )

from docbr.api._data import DocData
from docbr.core import Doc
from docbr.core._io import (
    io_get, 
    io_input_narray, 
    io_output_narray,
    )

def _get_instance(doctype: str) -> Doc:
    """
    Initialize a new instance of a document based on doctype.
    """
    try:
        params = getattr(DocData(), doctype)
        return Doc(params)
    except:
        raise ValueError(f"Doctype '{doctype}' not recognized.")

def _get_attr_list(attrs: Union[str, list]) -> list:
    """
    Parse the value(s) passed by the user to be considered as document attributes.
    """
    if isinstance(attrs, str) and attrs == '*':
        return ['*']
    elif (isinstance(attrs, list) and '*' in attrs):
        return ['*']
    elif isinstance(attrs, list):
        return [str(a) for a in attrs]
    elif isinstance(attrs, str):
        return [attrs]
    elif isinstance(attrs, int):
        return [str(attrs)]
    else:
        raise TypeError(f"Invalid attribute type: {type(attrs)}, must be str, list or '*'.")

def _check_for_attributes(doctype: str) -> None:
    """
    Check if the document given by the user have attributes.

    Raises
    ------
    ValueError
        If the document given by the user have no attributes.
    """
    params = getattr(DocData(), doctype)
    if params.get('DocAttributes') == None:
        raise ValueError(f"This documents has no attributes to extract, please check 'list_attributes' function for more details.")

def list_attributes() -> dict: # pragma: no cover
    # Docstrings of public methods are written in brazilian portuguese to benefit the target user of this package.
    """
    Retorna um dicionário com a lista de todos os atributos possíveis para cada documento.
    """
    
    attrs = vars(DocData())
    output = {}

    for key, attr in attrs.items():
        attr = attr.get('DocAttributes')
        if attr != None:
            attr = list(attr.keys())
            output[key] = attr

    return output

def parse(
        doc,
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
        mask: bool = False
    ) -> Union[str, ndarray]:
    # Docstrings of public methods are written in brazilian portuguese to benefit the target user of this package.
    """
    Realiza a extração do documento e retorna seu valor corrigido, adicionar máscara no documento é uma opção.
    Este método aceita objetos do tipo str, int, float, list, numpy.ndarray e pandas.series.

    Parâmetros
    ----------
    doc
        Documento(s) a ser(em) extraído(s).
    doctype: str
        Tipo do documento a ser extraído, pode ser: cnpj, cpf, cnh, te, pis, cert, rnvam, placa, tfone, email.
    mask: bool
        Se True, adiciona máscara no documento.

    Retorno
    -------
    ndarray ou str
        Retorna o(s) documento(s) extraído(s) como numpy.ndarray ou str.

    Raises
    ------
    TypeError 
        Se o tipo do(s) documento(s) enviado(s) não for str, int, float, list, ndarray ou pandas series.
    ValueError
        Se o tipo do documento não for reconhecido.
    """

    i_func, o_type = io_get(doc)
    doc = io_input_narray(doc, i_func)
    instance = _get_instance(doctype)
    result = instance.parse(doc, mask)
    return io_output_narray(result, o_type)

def validate(
        doc,
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
        lazy: bool = False
    ) -> Union[str, ndarray]:
    # Docstrings of public methods are written in brazilian portuguese to benefit the target user of this package.
    """
    Realiza a validação do documento e retorna True se o documento é válido.
    Este método aceita objetos do tipo str, int, float, list, numpy.ndarray e pandas.series.

    Parâmetros
    ----------
    doc
        Documento(s) a ser(em) extraído(s).
    doctype: str
        Tipo do documento a ser extraído, pode ser: cnpj, cpf, cnh, te, pis, cert, rnvam, placa, tfone, email.
    lazy: bool
        Se True, não realiza a extração do documento, apenas retorna True ou False diretamente sobre o valor concebido.

    Retorno
    -------
    ndarray ou str
        Retorna True se o documento é válido ou False se o documento é inválido.

    Raises
    ------
    TypeError
        Se o tipo do(s) documento(s) enviado(s) não for str, int, float, list, ndarray ou pandas series.
    ValueError
        Se o tipo do documento não for reconhecido.
    """

    i_func, o_type = io_get(doc)
    doc = io_input_narray(doc, i_func)
    instance = _get_instance(doctype)
    result = instance.validate(doc, lazy)
    return io_output_narray(result, o_type)

def attributes(
        doc,
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
        attrs: Union[Literal['*'], list[str], str] = '*'
    ) -> Union[str, ndarray]:
    # Docstrings of public methods are written in brazilian portuguese to benefit the target user of this package.
    """
    Coleta atributos do documento se for possível e retorna um dicionário com estes atributos, também é possível escolher estes atributos de acordo com cada documento.

    Parâmetros
    ----------
    doc
        Documento(s) a ser(em) extraído(s).
    doctype: str
        Tipo do documento a ser extraído, pode ser: cnpj, cpf, cnh, te, pis, cert, rnvam, placa, tfone, email.
    attr: list
        Lista de atributos do documento, pode ser demarcado como * para extrair todos.

    Retorno
    -------
        Retorna o(s) atributo(s) extraído(s) como numpy.ndarray ou dict.

    Raises
    ------
    TypeError
        Se o tipo do(s) documento(s) enviado(s) não for int, float, list, ndarray ou pandas series.
    ValueError
        Se o tipo do documento não for reconhecido.
    """

    attrs = _get_attr_list(attrs)
    i_func, o_type = io_get(doc)
    doc = io_input_narray(doc, i_func)
    instance = _get_instance(doctype)
    _check_for_attributes(doctype)
    result = instance.attributes(doc, attrs)
    return io_output_narray(result, o_type)
