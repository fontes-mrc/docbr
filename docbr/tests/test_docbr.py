import unittest
from docbr import parse, validate, attributes

class TestDocBR(unittest.TestCase):
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

        for test, expected in cases:
            self.assertEqual(parse(*test), expected)
    
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
            (('15559539000152','cnpj', '*'), {'raíz':'15559539','matriz/filial':'matriz'}),
            (('15559539000152','cnpj', 'raíz'), '15559539'),
            (('82683688377','cpf', '*'), {'região':'CE/MA/PI'}),
            (('82683688377','cpf', 'região'), 'CE/MA/PI'),
            (('389441060167','te', 'estado'), 'SP'),
            (('24298401552012167386797522780794','cert', 'ano'), '2012'),
            (('ABC1234','placa', '*'), {'padrão':'brasil'}),
            (('11987659876','tfone', '*'), {'ddd':'11','estado':'SP','tipo':'celular'}),
            (('abc@abc.com.br','email', 'domínio'), 'abc.com.br'),
        ]

        raises = [
            (('15559539000152','cnpj', 'estado'),  KeyError),
            (('84223533040','cnh'    , '*')     ,ValueError),
            (('75145500065','pis'    , '*')     ,ValueError),
            (('31186126948','rnvam'  , '*')     ,ValueError),
            (('31186126948','abc'    , '*')     ,ValueError),
        ]

        for test, expected in cases:
            self.assertEqual(attributes(*test), expected)
        
        for test, expected in raises:
            with self.assertRaises(expected):
                attributes(*test)