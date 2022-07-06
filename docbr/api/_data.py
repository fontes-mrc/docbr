from docbr.core._unicode import un_slicer
from numpy import (
    vectorize, 
    where, 
    take, 
    array, 
    char,
)

_ddd_estados = \
array([None,                                             # 00
    None,None,None,None,None,None,None,None,None,None,   # 01-10
    'SP','SP','SP','SP','SP','SP','SP','SP','SP',None,   # 11-20
    'RG','RG',None,'RG',None,None,'ES','ES',None,None,   # 21-30
    'MG','MG','MG','MG','MG',None,'MG','MG',None,None,   # 31-40
    'PR','PR','PR','PR','PR','PR','SC','SC','SC',None,   # 41-50
    'RS',None,'RS','RS','RS',None,None,None,None,None,   # 51-60
    'DF','GO','TO','GO','MT','MT','MS','AC','RO',None,   # 61-70
    'BA',None,'BA','BA','BA',None,'BA',None,'SE',None,   # 71-80
    'PB','AL','PA','RN','CE','PI','PB','CE','PI',None,   # 81-90
    'PA','AM','PA','PA','RR','AP','AM',None,None,        # 91-99
])

class DocData():
    def __init__(self) -> None:

        self.cnpj = {
            'DocCategory': 'CheckDigit',
            'DocLen': 14,
            'DigModulo': 11,
            'DigOperation': lambda x: where(x < 2, 0, 11 - x),
            'DigSequence': [
                            ([5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2, 0, 0], 12),
                            ([6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2, 0], 13)
                        ],
            "DocFormat": array(list("##.###.###/####-##")).view(int),
            'DocAttributes':{
                'raíz':lambda x: un_slicer(x,0,7,dtype=str),
                'matriz/filial':lambda x: where(
                                                un_slicer(x,8,11,dtype=int) == 1,
                                                'matriz',
                                                'filial'
                                            )
                }
            }

        self.cpf = {
            'DocCategory': 'CheckDigit',
            'DocLen': 11,
            'DigModulo': 11,
            'DigOperation': lambda x: where(x < 2, 0, 11 - x),
            'DigSequence': [
                            ([10, 9, 8, 7, 6, 5, 4, 3, 2, 0, 0] ,9),
                            ([11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 0], 10)
                        ],
            "DocFormat": array(list("###.###.###-##")).view(int),
            'DocAttributes':{
                'região':lambda x: take(
                                        array([
                                            'RS',
                                            'DF/GO/MS/MT/TO',
                                            'AC/AM/AP/PA/RO/RR',
                                            'CE/MA/PI',
                                            'AL/PB/PE/RN',
                                            'BA/SE',
                                            'MG',
                                            'ES/RJ',
                                            'SP',
                                            'PR/SC'
                                        ]),
                                        un_slicer(x,8,dtype=int)
                                    )
                }
        }

        self.cnh ={
            'DocCategory': 'CheckDigit',
            'DocLen': 11,
            'DigModulo': 11,
            'DigOperation': lambda x: where(x > 9, 0, x),
            'DigSpecialOperations': ['cnh'],
            'DigSequence': [
                            ([9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 0], 9),
                            ([1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0], 10)
                        ],
            "DocFormat": array(list("### ### ### ##")).view(int)
        }

        self.te = {
            'DocCategory': 'CheckDigit',
            'DocLen': 12,
            'DigFederalState': (8,9),
            'DigModulo': 11,
            'DigOperation': lambda x: where(x == 10, 0, x),
            'DigSequence': [
                            ([2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0], 10),
                            ([0, 0, 0, 0, 0, 0, 0, 0, 7, 8, 9, 0], 11)
                        ],
            "DocFormat": array(list("#### #### ####")).view(int),
            'DocAttributes':{
                'estado':lambda x: take(
                                        array([
                                            '',
                                            'SP','MG','RJ','RS',
                                            'BA','PR','CE','PE',
                                            'SC','GO','MA','PB',
                                            'PA','ES','PI','RN',
                                            'AL','MT','MS','DF',
                                            'SE','AM','RO','AC',
                                            'AP','RR','TO','ZZ'
                                        ]),
                                        un_slicer(x,8,9,dtype=int)
                                    )
                }
        }

        self.pis = {
            'DocCategory': 'CheckDigit',
            'DocLen': 11,
            'DigModulo': 11,
            'DigOperation': lambda x: where(x < 2, 0, 11 - x),
            'DigSequence': [([3, 2, 9, 8, 7, 6, 5, 4, 3, 2, 0], 10)],
            "DocFormat": array(list("###.#####.##-#")).view(int)
        }

        self.cert = {
            'DocCategory': 'CheckDigit',
            'DocLen': 32,
            'DigModulo': 11,
            'DigOperation': lambda x: where(x == 10, 1, x),
            'DigSequence': [
                            ([2,3,4,5,6,7,8,9,10,0,1,2,3,4,5,6,7,8,9,10,0,1,2,3,4,5,6,7,8,9,0,0], 30),
                            ([1,2,3,4,5,6,7,8,9,10,0,1,2,3,4,5,6,7,8,9,10,0,1,2,3,4,5,6,7,8,9,0], 31)
                        ],
            "DocFormat": array(list("######.##.##.####.#.#####.###.#######-##")).view(int),
            'DocAttributes':{
                'cartório':  lambda x: un_slicer(x,0,5,dtype=str),
                'acervo':    lambda x: un_slicer(x,6,7,dtype=str),
                'nsrc':      lambda x: un_slicer(x,8,9,dtype=str),
                'ano':       lambda x: un_slicer(x,10,13,dtype=str),
                'tipo':      lambda x: take(
                                            array([
                                                '',
                                                'nascimento',
                                                'casamento',
                                                'casamento religioso com efeito civil',
                                                'óbito',
                                                'natimorto',
                                                'registro de proclamas',
                                                'demais atos relativos ao registro civil',
                                                'emancipações',
                                                'interdições'
                                            ]),
                                            un_slicer(x,14,dtype=int)
                                        ),
                'tipo-livro':lambda x: take(
                                            array(['','A','B','B','C','C','D','E','E','E']),
                                            un_slicer(x,14,dtype=int)
                                        ),
                'livro':     lambda x: un_slicer(x,15,19,dtype=str),
                'folha':     lambda x: un_slicer(x,20,22,dtype=str),
                'termo':     lambda x: un_slicer(x,23,29,dtype=str)
                }
        }

        self.rnvam = {
            'DocCategory': 'CheckDigit',
            'DocLen': 11,
            'DigModulo': 11,
            'DigOperation': lambda x: where(x < 2, 0, 11-x),
            'DigSequence': [([3, 2, 9, 8, 7, 6, 5, 4, 3, 2, 0], 10)],
            "DocFormat": array(list("##########-#")).view(int)
        }

        self.placa = {
            'DocCategory': 'RegExr',
            'DocPattern': r'[a-zA-Z]{3}\s?\-?[0-9][A-Za-z0-9][0-9]{2}',
            'RemoveSpecial': True,
            "DocFormat": array(list("###-####")).view(int),
            'DocAttributes':{
                'padrão': lambda x: where(char.isnumeric(un_slicer(x,4,dtype=str)), 'brasil', 'mercosul')
            }
        }

        self.email = {
            'DocCategory': 'RegExr',
            'DocPattern': r'[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+\.[a-z]+(\.[a-z]+)?(\.[a-z]+)?',
            'RemoveSpecial': False,
            'DocAttributes':{
                'local': lambda x: array([xx[0] for xx in char.split(x, '@')], dtype=str),
                'domínio': lambda x: array([xx[1] for xx in char.split(x, '@')], dtype=str)
            }
        }

        self.tfone = {
            'DocCategory': 'RegExr',
            'DocPattern': r'(?:\(?(?:[14689][1-9]|2[12478]|3[1234578]|5[1345]|7[134579])\)?)?\s?(?:[2-8]|9[1-9])[0-9]{3}(?:\s|\-|\.)?[0-9]{4}',
            'RemoveSpecial': True,
            'DocFormatFunction': vectorize(lambda x: "({}){}-{}".format(x[:2], x[2:-4], x[-4:]) if len(x) > 9 else "{}-{}".format(x[:-4], x[-4:])),
            'DocAttributes':{
                'ddd': lambda x: where(char.str_len(x) > 9, un_slicer(x,0,1,dtype=str), None),
                'estado': lambda x: where(char.str_len(x) > 9, take(_ddd_estados, un_slicer(x,0,1,dtype=int)), None),
                'tipo': lambda x: where((char.str_len(x) == 10) | (char.str_len(x) == 8), 'fixo', 'celular')
            }
        }