# docbr

DocBR é um pacote Python para extração e validação de documentos brasileiros em escala, projetado para APIs de alta performance e pipelines de engenharia de dados que necessitam processar grandes volumes de dados. Seu core é desenvolvido em Numpy e possui integração nativa com Pandas / Numpy para facilitar a sua utilização com outros frameworks.

## Instalação
_____________

Você pode instalar este pacote através do PyPI:

```
pip install docbr
```

## Análise de Documentos
________________________

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

## Métodos
___________

Existem 3 métodos que você pode utilizar em seus documentos dentro do DocBR: parse, validate e attributes.

### parse
___________

Recebe n documentos nos formatos int, str, list, numpy.array ou pandas.series. Estes objetos são então convertidos para um numpy.array de strings e os documentos são **extraídos** de acordo com o tipo do documento declarado.

Retorna um numpy.array de strings com os documentos extraídos.

Argumentos:
 - doc: n documentos nos formatos int, str, list, numpy.array ou pandas.series
 - doctype: tipo do documento, conforme lista acima
 - mask: boolean para definir se o documento deve ser mascarado ou não

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

docs = ['12 345 678 0001 58', '12345678000298..', '12345678000300']
dbr.parse(docs, doctype='cnpj', mask=False)
```

*Output:*
```text
array(['12345678000158', '12345678000298', '12345678000300'])
```

### validate
____________

Recebe n documentos nos formatos int, str, list, numpy.array ou pandas.series. Estes objetos são então convertidos para um numpy.array de strings e os documentos são **validados** de acordo com o tipo do documento declarado.

Retorna um numpy.array de booleans com os resultados das validações.

Argumentos:
 - doc: n documentos nos formatos int, str, list, numpy.array ou pandas.series
 - doctype: tipo do documento, conforme lista acima
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

### attributes
______________

Recebe um documento nos formatos int, str, list, numpy.array ou pandas.series. Estes objetos são então convertidos para um numpy.array de strings e o documento é então os atributos do documento são extraídos, se este tiver atributos para extração.

Retorna um numpy.array de dicts com os atributos extraídos, se for selecionado apenas um atributo, retorna um numpy.array de strings.

Argumentos:
 - doc: n documentos nos formatos int, str, list, numpy.array ou pandas.series
 - doctype: tipo do documento, conforme lista acima
 - attr: lista de atributos a serem extraídos, caso não seja especificado, todos os atributos são extraídos


*Input:*
```python
import docbr as dbr

docs = ['12345678000158', '12345678000298', '12345678000300']
dbr.attributes(docs, doctype='cnpj')
```

*Output:*
```text
array([{'raiz':'12345678','matriz/filial':'matriz'}, {'raiz':'12345678','matriz/filial':'filial'}, {'raiz':'12345678','matriz/filial':'filial'}])
```

*Input:*
```python
import docbr as dbr

docs = ['12345678000158', '12345678000298', '12345678000300']
dbr.attributes(docs, doctype='cnpj', attr='raiz')
```

*Output:*
```text
array(['12345678', '12345678', '12345678'])
```

Para você visualizar todos os atributos disponíveis de cada documento, use o método `list_attributes`.

```python
import docbr as dbr
dbr.list_attributes()
```

## Uso com Pandas
_________________

Para utilizar o DocBR com o Pandas, basta passar passar uma séries (coluna) para o método desejado e declarar o tipo de documento.

O retorno poderá ser inserido diretamente ao dataframe como uma nova coluna se desejado.

*Input:*
```python
import docbr as dbr
import pandas as pd

df = pd.DataFrame({'cnpj': ['12345678000158', '12345678000298', '12345678000300']})
df['cnpj_valido'] = dbr.validate(df['cnpj'], doctype='cnpj')
df['cnpj_raiz']   = dbr.attributes(df['cnpj'], doctype='cnpj', attr='raíz')
df.head()
```

*Output:*
```text
|   | cnpj           | cnpj_valido  |cnpj_raiz |
| 0 | 12345678000158 | False        |12345678  |
| 1 | 12345678000298 | False        |12345678  |
| 2 | 12345678000300 | False        |12345678  |
```