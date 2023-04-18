class AttributeStr(str):
    """
    A subclass of str that represents an attribute string.

    :param value: The initial value of the attribute string.
    :type value: str

    :return: A new instance of AttributeStr with the specified value.
    :rtype: AttributeStr

    :Example:

    >>> a = AttributeStr("foo")
    >>> isinstance(a, str)
    True
    >>> isinstance(a, AttributeStr)
    True
    >>> a.upper()
    'FOO'
    """

    def __new__(cls, value: str) -> "AttributeStr":
        return super().__new__(cls, value)


CPF_REGIAO = AttributeStr("regiao")
CNPJ_RAIZ = AttributeStr("raiz")
CNPJ_MATRIZ = AttributeStr("matriz_filial")
T_ELEITOR_UF = AttributeStr("estado")
CERTIDAO_CARTORIO = AttributeStr("cartorio")
CERTIDAO_ACERVO = AttributeStr("acervo")
CERTIDAO_NSRC = AttributeStr("nsrc")
CERTIDAO_ANO = AttributeStr("ano")
CERTIDAO_TIPO = AttributeStr("tipo")
CERTIDAO_TIPO_LIVRO = AttributeStr("tipo_livro")
CERTIDAO_LIVRO = AttributeStr("livro")
CERTIDAO_FOLHA = AttributeStr("folha")
CERTIDAO_TERMO = AttributeStr("termo")
PLACA_PADRAO = AttributeStr("padrao")
EMAIL_LOCAL = AttributeStr("local")
EMAIL_DOMINIO = AttributeStr("dominio")
TELEFONE_DDD = AttributeStr("ddd")
TELEFONE_UF = AttributeStr("estado")
TELEFONE_TIPO = AttributeStr("tipo")
