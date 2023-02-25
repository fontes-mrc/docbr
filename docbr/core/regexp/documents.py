from docbr.core._utils import array_slicer
from docbr.core.regexp._template import _RegExrTemplate
from numpy import(
    ndarray,
    vectorize,
    char,
    array,
    where,
    take,
    )

class CarPlate(_RegExrTemplate):
    def __init__(self, docs: ndarray) -> None:
        super().__init__(docs)
        self._pattern = r'[a-zA-Z]{3}\s?\-?[0-9][A-Za-z0-9][0-9]{2}'
        self._remove_spec_char = True
        self._format_mask = '###-####'
        self._attributes = {
            'padrao': lambda x: where(char.isnumeric(array_slicer(x,4,dtype=str)), 'brasil', 'mercosul')
        }

class Email(_RegExrTemplate):
    def __init__(self, docs: ndarray) -> None:
        super().__init__(docs)
        self._pattern = r'[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+\.[a-z]+(\.[a-z]+)?(\.[a-z]+)?'
        self._remove_spec_char = False
        self._attributes = {
            'local': lambda x: array([xx[0] for xx in char.split(x, '@')], dtype=str),
            'dominio': lambda x: array([xx[1] for xx in char.split(x, '@')], dtype=str)
        }
    
    def _apply_mask(self) -> None:
        pass

class Phone(_RegExrTemplate):
    def __init__(self, docs: ndarray) -> None:
        super().__init__(docs)
        self._pattern = r'(?:\(?(?:[14689][1-9]|2[12478]|3[1234578]|5[1345]|7[134579])\)?)?\s?(?:[2-8]|9[1-9])[0-9]{3}(?:\s|\-|\.)?[0-9]{4}'
        self._remove_spec_char = True
        self._ddd_estados = \
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
        self._attributes = {
                'ddd': lambda x: where(char.str_len(x) > 9, array_slicer(x,0,1,dtype=str), None),
                'estado': lambda x: where(char.str_len(x) > 9, take(self._ddd_estados, array_slicer(x,0,1,dtype=int)), None),
                'tipo': lambda x: where((char.str_len(x) == 10) | (char.str_len(x) == 8), 'fixo', 'celular')
        }

    def _apply_mask(self) -> None:
        func = vectorize(lambda x: "({}){}-{}".format(x[:2], x[2:-4], x[-4:]) if len(x) > 9 else "{}-{}".format(x[:-4], x[-4:]))
        self._documents = func(self._documents)
        self._documents = self._documents.astype(object)