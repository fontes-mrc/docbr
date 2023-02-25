from docbr.core._utils import array_slicer
from docbr.core.checkdigit._template import _CheckDigitTemplate
from numpy import(
    ndarray,
    int8,
    array,
    repeat,
    where,
    take
    )

class CPF(_CheckDigitTemplate):
    def __init__(self, docs: ndarray) -> None:
        super().__init__(docs)
        self._doc_len = 11
        self._modulo = 11
        self._format_mask = '###.###.###-##'
        self._operation = lambda x: where(x < 2, 0, 11 - x)
        self._sequence = [
            ([10, 9, 8, 7, 6, 5, 4, 3, 2, 0, 0] ,9),
            ([11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 0], 10),
        ]
        self._attributes = {
            'regiao': lambda x: 
                take(
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
                    array_slicer(x,8,dtype=int)
                )
        }

class CNPJ(_CheckDigitTemplate):
    def __init__(self, docs: ndarray) -> None:
        super().__init__(docs)
        self._doc_len = 14
        self._modulo = 11
        self._format_mask = '##.###.###/####-##'
        self._operation = lambda x: where(x < 2, 0, 11 - x)
        self._sequence = [
            ([5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2, 0, 0], 12),
            ([6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2, 0], 13),
        ]
        self._attributes = {
            'raiz':lambda x: array_slicer(x,0,7,dtype=str),
            'matriz_filial':lambda x: where(
                array_slicer(x,8,11,dtype=int) == 1,
                'matriz',
                'filial'
            )
        }

class CNH(_CheckDigitTemplate):
    def __init__(self, docs: ndarray) -> None:
        super().__init__(docs)
        self._doc_len = 11
        self._modulo = 11
        self._format_mask = '### ### ### ##'
        self._operation = lambda x: where(x > 9, 0, x)
        self._sequence = [
            ([9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 0], 9),
            ([1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0], 10),
        ]

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

            if len(cache) > 0:
                digit = where(cache[0] < 10, digit, where(digit - 2 < 0, digit + 9, digit - 2))

            cache.append(digit)
            digit = self._operation(digit)
            digit = array(digit, dtype=int8)

            position = min(position, digits.shape[1] -1)
            digits[:, position] = digit
            out.append((digit,position))

        return out

class TituloEleitor(_CheckDigitTemplate):
    def __init__(self, docs: ndarray) -> None:
        super().__init__(docs)
        self._doc_len = 12
        self._modulo = 11
        self._federal = (8,9)
        self._format_mask = '#### #### ####'
        self._operation = lambda x: where(x == 10, 0, x)
        self._sequence = [
            ([2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0], 10),
            ([0, 0, 0, 0, 0, 0, 0, 0, 7, 8, 9, 0], 11),
        ]
        self._attributes = {
            'estado':lambda x:
                take(
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
                    array_slicer(x,8,9,dtype=int)
                )
        }

    def _federal_unit_validator(self, digs: ndarray, dig_fu: tuple[int, int]) -> ndarray:
        left_fu, right_fu = dig_fu
        check = (digs[:, left_fu] == 1)
        check |= (digs[:, left_fu] == 2) & (digs[:, right_fu] < 9)
        check |= (digs[:, left_fu] == 0) & (digs[:, right_fu] > 0)
        return check

    def _validation_process(self, digits: ndarray) -> ndarray:
        check_digits = self._generate_check_digit(digits)
        is_valid = self._validate_check_digit(digits, check_digits)
        is_valid &= self._federal_unit_validator(digits, self._federal)
        return is_valid

class PIS(_CheckDigitTemplate):
    def __init__(self, docs: ndarray) -> None:
        super().__init__(docs)
        self._doc_len = 11
        self._modulo = 11
        self._format_mask = '###.#####.##-#'
        self._operation = lambda x: where(x < 2, 0, 11 - x)
        self._sequence = [([3, 2, 9, 8, 7, 6, 5, 4, 3, 2, 0], 10)]

class Certidao(_CheckDigitTemplate):
    def __init__(self, docs: ndarray) -> None:
        super().__init__(docs)
        self._doc_len = 32
        self._modulo = 11
        self._format_mask = '######.##.##.####.#.#####.###.#######-##'
        self._operation = lambda x: where(x == 10, 1, x)
        self._sequence = [
            ([2,3,4,5,6,7,8,9,10,0,1,2,3,4,5,6,7,8,9,10,0,1,2,3,4,5,6,7,8,9,0,0], 30),
            ([1,2,3,4,5,6,7,8,9,10,0,1,2,3,4,5,6,7,8,9,10,0,1,2,3,4,5,6,7,8,9,0], 31),
        ]
        self._attributes = {
            'cartorio':  lambda x: array_slicer(x,0,5,dtype=str),
            'acervo':    lambda x: array_slicer(x,6,7,dtype=str),
            'nsrc':      lambda x: array_slicer(x,8,9,dtype=str),
            'ano':       lambda x: array_slicer(x,10,13,dtype=str),
            'tipo':      lambda x:
                take(
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
                    array_slicer(x,14,dtype=int)
                ),
            'tipo_livro':lambda x:
                take(
                    array(['','A','B','B','C','C','D','E','E','E']),
                    array_slicer(x,14,dtype=int)
                ),
            'livro':     lambda x: array_slicer(x,15,19,dtype=str),
            'folha':     lambda x: array_slicer(x,20,22,dtype=str),
            'termo':     lambda x: array_slicer(x,23,29,dtype=str)
        }

class Renavam(_CheckDigitTemplate):
    def __init__(self, docs: ndarray) -> None:
        super().__init__(docs)
        self._doc_len = 11
        self._modulo = 11
        self._format_mask = '##########-#'
        self._operation = lambda x: where(x < 2, 0, 11-x)
        self._sequence = [([3, 2, 9, 8, 7, 6, 5, 4, 3, 2, 0], 10)]