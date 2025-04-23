"""Transforma imagem(ns) e xml(s) em registro(s) BSON.

Os arquivos tem origem em dicionários do Python que são codificados,
através da biblioteca BSON do MongoDB, em arquivos BSON, que são
um JSON binário padrão no MongoDB. O BsonImage corresponde exatamente a
um registro do MongoDB GridFS. O BsonImageList é um dicionário, chave
index sequencial da lista e valor BsonImage.

Assim, deve ser possível abrir e também gerar os arquivos facilmente em outras
linguagens se necessário, ou até pelo MongoDB/Mongoose, como se fossem arquivos
JSON.

"""
import gzip
import os
from collections import OrderedDict
from hashlib import md5
from pathlib import Path

import bson
from bson.codec_options import CodecOptions

from ajna_commons.flask.log import logger


class BsonImage():
    """Classe para transporte de informações do AVATAR para VIRASANA.

    Esta classe usa o padrão BSON, largamente utilizado no MongoDB,
    uma derivação do JSON. Assim, será possível transportar arquivos
    e metadados (informações relativas ao arquivo) em pacotes únicos
    entre a origem (sistemas dos terminais) e destino (servidor central AJNA).

    Toda a informação é passada em forma de dicionários chave:valor,
    inclusive o conteúdo do arquivo original que vai numa chave especial
    de nome 'content'.

    """

    def __init__(self, filename=None, **kwargs):
        """Recebe o nome do arquivo e um dict kwargs.

        Args:
            filename: arquivo a ser transformado em BSON
            kwargs: dicionário de metadados do arquivo

        Lê o conteúdo do arquivo na chave content e o conteúdo do
        dicionário kwargs na chave metadata. Também cria uma chave
        filename com o nome do arquivo. Esta estrutura é o padrão
        utilizado no sistema GridFS do MongoDB.

        Caso arquivo não exista, levanta exceção.

        """
        self._filename = None
        self._metadata = None
        self._content = None
        if filename is not None:
            file = Path(filename)
            if file.exists():
                with open(filename, 'rb') as f:
                    content = f.read()
                # print('File found')
                self._filename = os.path.basename(filename)
                self._content = content
                self._metadata = kwargs
                # self.set_campos(filename, content, kwargs)
            else:
                raise FileNotFoundError(
                    'Arquivo ' + filename + ' não encontrado.')

    def set_campos(self, filename, content, **kwargs):
        """Opcional lazy init."""
        self._filename = filename
        self._content = content
        self._metadata = kwargs

    @property
    def todict(self):
        """Retorna representação da instância em dicionário."""
        return dict(metadata=self._metadata,
                    filename=self._filename,
                    content=self._content)

    @property
    def tobson(self):
        """Retorna dicionário da instância com codificação BSON."""
        return bson.BSON.encode(self.todict)

    def tofile(self, newfilename, zipped=False):
        """Salva instância em arquivo (padrão BSON)."""
        with open(newfilename, 'wb') as f:
            payload = self.tobson
            if zipped:
                payload = gzip.compress(payload)
            f.write(payload)

    @classmethod
    def fromfile(cls, fromfilename, zipped=False):
        """Recupera instância de arquivo (padrão BSON)."""
        with open(fromfilename, 'rb') as f:
            payload = f.read()
            if zipped:
                payload = gzip.decompress(payload)
            data = bson.BSON.decode(payload)
        result = BsonImage()
        result.set_campos(data['filename'],
                          data['content'],
                          **data['metadata'])
        return result

    def tomongo(self, fs):
        """Salva instância em GridFS MongoDB.

        Checa se arquivo existe antes de gravar.
        Se existir, retorna _id correspondente ao MD5 do conteúdo

        **IMPORTANTE**
        A checagem é realizada
        pelo nome do arquivo E pelo conteúdo, através de um digest MD5.
        Ou seja, serão aceitos dois arquivos no GridFS com mesmo nome e
        conteúdo diferente (o que pode indicar erro ou fraude na fonte das
        imagens e precisará ser tratado), só rejeitando no caso de o conteúdo
        ser o mesmo, que será interpretado como tentativa de carregar novamente
        o mesmo arquivo. O hash MD5 não é perfeito, podendo haver colisões, mas
        como é o padrão do MongoDB por ora será utilizado, mesmo porque a
        possibilidade de colisão no nome do arquivo E no hash é
        extremamente baixa.

        """
        m = md5()
        m.update(self._content)
        grid_out = fs.find_one({'md5': m.hexdigest()})
        if grid_out:
            if grid_out.filename == self._filename:
                logger.warning(
                    self._filename +
                    ' MD5(' + m.hexdigest() + ')' +
                    ' tentativa de inserir pela segunda vez!!')
                # File exists, abort inserting file, just return _id!
                return grid_out._id
        # Insert File
        return fs.put(self._content, filename=self._filename,
                      metadata=self._metadata)

    @classmethod
    def frommongo(cls, file_id, fs):
        """Recupera instância do MongoDB pelo id."""
        print(file_id)
        if fs.exists(file_id):
            grid_out = fs.get(file_id)
            data = dict()
            data['filename'] = grid_out.filename
            data['metadata'] = grid_out.metadata
            data['content'] = grid_out.read()
            result = BsonImage()
            result.set_campos(data['filename'],
                              data['content'],
                              **data['metadata'])
        else:
            raise FileNotFoundError('Arquivo não encontrado pelo MongoDB')
        return result


class BsonImageList():
    """Classe para transporte de informações do AVATAR para VIRASANA.

    Esta classe usa o padrão BSON, largamente utilizado no MongoDB,
    uma derivação do JSON.

    Ver classe :class:`BsonImage`

    Esta classe implementa uma lista da classe BsonImage.

    """

    def __init__(self):
        """Inicializa lista vazia."""
        self._bsonimagelist = []

    @property
    def tolist(self):
        """Retorna lista."""
        return self._bsonimagelist

    def addImage(self, filename, **kwargs):
        """Cria BsonImage e adiciona à lista.

        Args:
            filename: arquivo a ser transformado em BSON
            kwargs: dicionário de metadados do arquivo
        """
        self._bsonimagelist.append(BsonImage(filename, **kwargs))

    def addBsonImage(self, bsonimage):
        """Adiciona BsonImage à lista."""
        self._bsonimagelist.append(bsonimage)

    def tofile(self, newfilename, zipped=False):
        """Grava lista de BSON em um único arquivo padrão BSON."""
        dict_bson = OrderedDict()
        for index, bsonimage in enumerate(self._bsonimagelist):
            dict_bson[str(index)] = bsonimage.todict
        abson = bson.BSON.encode(dict_bson)
        with open(newfilename, 'wb') as f:
            if zipped:
                abson = gzip.compress(abson)
            f.write(abson)

    @classmethod
    def fromfile(cls, filename=None, abson=None, zipped=False):
        """Lê lista de BSON de um único arquivo padrão BSON."""
        options = CodecOptions(document_class=OrderedDict)
        if abson is None:
            with open(filename, 'rb') as f:
                abson = f.read()
        if zipped:
            abson = gzip.decompress(abson)
        dict_bson = bson.BSON.decode(abson, codec_options=options)
        bsonimagelist = BsonImageList()
        for _, data in dict_bson.items():  # key ignored
            bsonimage = BsonImage()
            bsonimage.set_campos(data['filename'],
                                 data['content'],
                                 **data['metadata'])
            bsonimagelist.addBsonImage(bsonimage)
        return bsonimagelist

    def tomongo(self, fs):
        """Grava lista de BSON no BD."""
        files_ids = []
        for bsonimage in self._bsonimagelist:
            file_id = bsonimage.tomongo(fs)
            files_ids.append(file_id)
        return files_ids

    @classmethod
    def frommongo(cls, files_ids, fs):
        """Gera BsonImageList de uma lista de _ids, a partir do BD."""
        result = BsonImageList()
        for file_id in files_ids:
            if fs.exists(file_id):
                grid_out = fs.get(file_id)
                data = dict()
                data['filename'] = grid_out.filename
                data['metadata'] = grid_out.metadata
                data['content'] = grid_out.read()
                bsonimage = BsonImage()
                bsonimage.set_campos(data['filename'],
                                     data['content'],
                                     **data['metadata'])
            else:
                raise FileNotFoundError('Arquivo não encontrado pelo MongoDB')
            result.addBsonImage(bsonimage)
        return result
