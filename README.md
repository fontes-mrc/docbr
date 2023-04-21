# docbr

DocBR é um pacote Python para extração e validação de documentos brasileiros em escala, projetado para APIs de alta performance e pipelines de engenharia de dados que necessitam processar grandes volumes de dados. Seu core é desenvolvido em Numpy e possui integração nativa com Pandas / Numpy para facilitar a sua utilização com outros frameworks.

## Instalação

Você pode instalar este pacote através do PyPI:

```
pip install docbr
```

## Análise de Documentos

Com DocBr, você pode tratar com os seguintes documentos:

| Grupo de Documentos | Nome do Documento                         | Chave   | Método de Validação |
|---------------------|-------------------------------------------|---------|---------------------|
| Pessoa Jurídica     | Carteira Nacional de Pessoas Jurídicas    | cnpj    | Digito Validador    |
| Pessoa Física       | Cadastro de Pessoa Física                 | cpf     | Digito Validador    |
| Pessoa Física       | Carteira Nacional de Habilitação          | cnh     | Digito Validador    |
| Pessoa Física       | Título de Eleitor                         | te      | Digito Validador    |
| Pessoa Física       | Programa de Integração Social             | pis     | Digito Validador    |
| Pessoa Física       | Certidão (Nascimento/Casamento/Óbito)     | cert    | Digito Validador    |
| Veículos            | Registro Nacional de Veículos Automotores | rnvam   | Digito Validador    |
| Veículos            | Placa de Veículo                          | placa   | RegExr              |
| Contato             | Telefone Celular / Fixo                   | tfone   | RegExr              |
| Contato             | E-mail                                    | email   | RegExr              |

## Benchmark

Uma vez que é uma biblioteca de processamento de dados em escala, DocBR foi projetado para ser rápido dentro do escopo de extração e validação de documentos. Abaixo temos um comparativo de performance entre DocBR e a biblioteca mais conhecida para validação de documentos brasileiros, o [validate-docbr](https://github.com/alvarofpp/validate-docbr).

O teste realizado consiste em comparar os métodos de validação de documentos, não levando em consideração os outros métodos específicos de cada biblioteca, visto que cada um possui propósitos de aplicação diferentes.

A tabela abaixo mostra o tempo de execução de cada método de validação de documentos, em segundos, para cada biblioteca. Os testes foram realizados em um dataset com 2 milhões de documentos de cada tipo, sendo 1 milhão de documentos com máscara e 1 milhão de documentos sem máscara.

Visto que a propriedade lazy para o método validate desta biblioteca não comporta documentos mascarados, o tempo de execução para este formato foi ignorado.

|  Document Type   | validate_docbr              | docbr      | docbr_lazy   | diff  | diff lazy |
|------------------|-----------------------------|------------|--------------|-------|-----------|
|  CPF - unmasked  |             5.07 s          |  443.75 ms |   333.11 ms  | -91%  |     -93%  |
|   CPF - masked   |             5.35 s          |  560.34 ms |      -       | -90%  |     -     |
| CNPJ - unmasked  |             8.06 s          |  499.33 ms |   371.79 ms  | -94%  |     -95%  |
|   CNPJ - masked  |             8.42 s          |  665.88 ms |      -       | -92%  |     -     |
|  CNH - unmasked  |             4.97 s          |  449.49 ms |   342.56 ms  | -91%  |     -93%  |
|   CNH - masked   |             5.22 s          |  582.03 ms |      -       | -89%  |     -     |
|  PIS - unmasked  |             3.66 s          |  400.62 ms |   291.46 ms  | -89%  |     -92%  |
|   PIS - masked   |             3.90 s          |  527.77 ms |      -       | -86%  |     -     |
|   TE - unmasked  |             4.45 s          |  474.77 ms |   359.42 ms  | -89%  |     -92%  |
|   TE - masked    |             4.62 s          |  575.36 ms |      -       | -88%  |     -     |
|RENAVAM - unmasked|             3.74 s          |  405.56 ms |   296.08 ms  | -89%  |     -92%  |
| RENAVAM - masked |             3.80 s          |  415.92 ms |      -       | -89%  |     -     |

A metodologia de avaliação de performance pode ser visualizada em detalhes neste repositório em `benchmark/performance.py`.

## Métodos
Existem 3 métodos que você pode utilizar em seus documentos dentro do DocBR: parse, validate e attributes.

### parse

Recebe n documentos nos formatos int, str, list, numpy.array ou pandas.series. Estes objetos são então convertidos para um numpy.array de strings e os documentos são **extraídos** de acordo com o tipo do documento declarado.

Retorna um numpy.array de strings com os documentos extraídos.

Argumentos:
 - doclist: n documentos nos formatos int, str, list, numpy.array ou pandas.series.
 - doctype: tipo do documento, conforme lista acima.
 - mask: boolean para definir se o documento deve ser mascarado ou não.

*Input:*
```python
import docbr as dbr

docs = ['12345678000158', '12345678000298', '12345678000300']
dbr.parse(docs, doctype='cnpj', mask=True)
```
*Output:*
```text
array(['12.345.678/0001-00', '12.345.678/0002-00', '12.345.678/0003-00'])
```

*Input:*
```python
import docbr as dbr
from docbr import doctypes as d

docs = ['12 345 678 0001 58', '12345678000298..', '12345678000300']
dbr.parse(docs, doctype=d.CNPJ, mask=False)
```

*Output:*
```text
array(['12345678000158', '12345678000298', '12345678000300'])
```

### validate

Recebe n documentos nos formatos int, str, list, numpy.array ou pandas.series. Estes objetos são então convertidos para um numpy.array de strings e os documentos são **validados** de acordo com o tipo do documento declarado.

Retorna um numpy.array de booleans com os resultados das validações.

Argumentos:
 - doclist: n documentos nos formatos int, str, list, numpy.array ou pandas.series.
 - doctype: tipo do documento, conforme lista acima.
 - lazy: boolean para definir se o documento deve ser extraído (parse) antes de validar ou não. É recomendado que esteja ligado caso precise validar um grande volume de documentos e estes já estejam padronizados e sem máscara.

*Input:*
```python
import docbr as dbr

docs = ['12345678000158', '12345678000298', '12345678000300']
dbr.validate(docs, doctype='cnpj', lazy=False)
```
*Output:*
```text
array([False, False, False])
```

### get_attribute

Recebe n documentos nos formatos int, str, list, numpy.array ou pandas.series e um atributo. Estes objetos são então convertidos para um numpy.array de strings e o atributo é **extraído** se este existir no documento.

Retorna um numpy.array de str com os atributos extraídos.

Argumentos:
 - doclist: n documentos nos formatos int, str, list, numpy.array ou pandas.series.
 - doctype: tipo do documento, conforme lista acima.
 - attr: atributo a ser extraído.
 - lazy: boolean para definir se o documento deve ser extraído (parse) antes de extrair o atributo ou não. É recomendado que esteja ligado caso precise extrair um grande volume de documentos e estes já estejam padronizados e sem máscara.


*Input:*
```python
import docbr as dbr
from docbr import doctypes as d
from docbr import attributes as attr

docs = ['12345678000158', '12345678000298', '12345678000300']
dbr.attributes(docs, doctype=d.CNPJ, attr=attr.CNPJ_RAIZ, lazy=True)
```

*Output:*
```text
array(['12345678', '12345678', '12345678'])
```

## Uso com Pandas

Para utilizar o DocBR com o Pandas, basta passar passar um objeto pandas.Series (coluna) para o método desejado e declarar o tipo de documento.

O retorno poderá ser inserido diretamente ao dataframe como uma nova coluna.

*Input:*
```python
import pandas as pd
import docbr as dbr
from docbr import doctypes as d
from docbr import attributes as attr

df = pd.DataFrame({'cnpj': ['12345678000158', '12345678000298', '12345678000300']})
df['cnpj_valido'] = dbr.validate(df['cnpj'], doctype=d.CNPJ)
df['cnpj_raiz']   = dbr.attributes(df['cnpj'], doctype=d.CNPJ, attr=attr.CNPJ_RAIZ)
df.head()
```

*Output:*
```text
|   | cnpj           | cnpj_valido  |cnpj_raiz |
| 0 | 12345678000158 | False        |12345678  |
| 1 | 12345678000298 | False        |12345678  |
| 2 | 12345678000300 | False        |12345678  |
```