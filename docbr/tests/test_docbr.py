import unittest
from docbr import parse, validate, get_attribute
from docbr import doctypes as d
from docbr import attributes as attr

class TestDocbr(unittest.TestCase):
    def test_parse(self):
        cases = [
            (('155-59.A539000152','cnpj', True),'15.559.539/0001-52'),
            (('155-59.A539000152','cnpj', False),'15559539000152'),
            (('826-83.A688377','cpf', True),'826.836.883-77'),
            (('826-83.A688377','cpf', False),'82683688377'),
            (('751-45.A500065','pis', True),'751.45500.06-5'),
            (('751-45.A500065','pis', False),'75145500065'),
            (('389-44.A1060167','te', True),'3894 4106 0167'),
            (('389-44.A1060167','te', False),'389441060167'),
            (('842-23.A533040','cnh', True),'842 235 330 40'),
            (('842-23.A533040','cnh', False),'84223533040'),
            (('242-98.A401552012167386797522780794','cert', True),'242984.01.55.2012.1.67386.797.5227807-94'),
            (('242-98.A401552012167386797522780794','cert', False),'24298401552012167386797522780794'),
            (('311-86.A126948','rnvam', True),'3118612694-8'),
            (('31186126948','rnvam', False),'31186126948'),
            (('ABC1234','placa', True),'ABC-1234'),
            (('ABC-1234','placa', True),'ABC-1234'),
            (('ABC 1234','placa', False),'ABC1234'),
            (('11987659876','tfone', True),'(11)98765-9876'),
            (('11987659876','tfone', False),'11987659876'),
            (('987659876','tfone', True),'98765-9876'),
            (('98765-9876','tfone', False),'987659876'),
            (('98765 9876','tfone', True),'98765-9876'),
            (('98765.9876','tfone', False),'987659876'),
            (('abc@abc.com.br','email', True),'abc@abc.com.br'),
            (('abc@abc.com.br','email', False),'abc@abc.com.br'),
        ]

        raises = [
            (('any','ccard', True), ValueError),
        ]

        for test, expected in cases:
            self.assertEqual(parse(*test), expected)

        for test, expected in raises:
            with self.assertRaises(expected):
                get_attribute(*test)

    
    def test_validate(self):
        cases = [
            (('155-59.A539000152','cnpj'                  , False),True),
            (('826-83.A688377','cpf'                      , False),True),
            (('751-45.A500065','pis'                      , False),True),
            (('389-44.A1060167','te'                      , False),True),
            (('842-23.A533040','cnh'                      , False),True),
            (('242-98.A401552012167386797522780794','cert', False),True),
            (('311-86.A126948','rnvam'                    , False),True),
            (('ABC-1234','placa'                          , False),True),
            (('98765-9876','tfone'                        , False),True),
            (('abc@abc.com.br','email'                    , False),True),
            (('15559539000152','cnpj'                     , True ),True),
            (('82683688377','cpf'                         , True ),True),
            (('75145500065','pis'                         , True ),True),
            (('389441060167','te'                         , True ),True),
            (('84223533040','cnh'                         , True ),True),
            (('24298401552012167386797522780794','cert'   , True ),True),
            (('31186126948','rnvam'                       , True ),True),
            (('ABC1234','placa'                           , True ),True),
            (('11987659876','tfone'                       , True ),True),
            (('abc@abc.com.br','email'                    , True ),True),
        ]

        for test, expected in cases:
            self.assertEqual(validate(*test), expected)

    def test_attributes(self):
        cases = [
            (('15559539000152', d.CNPJ, attr.CNPJ_RAIZ, True), '15559539'),
            (('82683688377', d.CPF, attr.CPF_REGIAO), 'CE/MA/PI'),
            (('389441060167',d.T_ELEITOR, attr.T_ELEITOR_UF), 'SP'),
            (('24298401552012167386797522780794',d.CERTIDAO, attr.CERTIDAO_ANO), '2012'),
            (('abc@abc.com.br', d.EMAIL, attr.EMAIL_DOMINIO), 'abc.com.br'),
            (('11987654321', d.TELEFONE, attr.TELEFONE_UF), 'SP'),
        ]

        raises = [
            (('15559539000152',d.CNPJ, 'estado'),  ValueError),
            (('84223533040',d.PLACA, '*'), ValueError),
        ]

        for test, expected in cases:
            self.assertEqual(get_attribute(*test), expected)
        
        for test, expected in raises:
            with self.assertRaises(expected):
                get_attribute(*test)
