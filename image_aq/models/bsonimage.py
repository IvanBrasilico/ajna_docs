import os
import gzip
from collections import OrderedDict
from pathlib import Path

import bson
from bson.codec_options import CodecOptions


class BsonImage():
    def __init__(self, filename=None, **kwargs):
        self._filename = None
        self._metadata = None
        self._content = None
        if filename is not None:
            file = Path(filename)
            if file.exists():
                with open(filename, 'rb') as f:
                    content = f.read()
                print('File found')
                self._filename = os.path.basename(filename)
                self._content = content
                self._metadata = kwargs
                # self.set_campos(filename, content, kwargs)
            else:
                raise FileNotFoundError(
                    'Arquivo ' + filename + ' não encontrado.')

    def set_campos(self, filename, content, **kwargs):
        self._filename = filename
        self._content = content
        self._metadata = kwargs

    @property
    def todict(self):
        return dict(metadata=self._metadata,
                    filename=self._filename,
                    content=self._content)

    @property
    def tobson(self):
        return bson.BSON.encode(self.todict)

    def tofile(self, newfilename, zipped=False):
        with open(newfilename, 'wb') as f:
            payload = self.tobson
            if zipped:
                payload = gzip.compress(payload)
            f.write(payload)

    @classmethod
    def fromfile(cls, fromfilename, zipped=False):
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
        file_id = fs.put(self._content, filename=self._filename,
                         metadata=self._metadata)
        return file_id

    @classmethod
    def frommongo(cls, file_id, fs):
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
    def __init__(self):
        self._bsonimagelist = []

    @property
    def tolist(self):
        return self._bsonimagelist

    def addImage(self, filename, **kwargs):
        self._bsonimagelist.append(BsonImage(filename, **kwargs))

    def addBsonImage(self, bsonimage):
        self._bsonimagelist.append(bsonimage)

    def tofile(self, newfilename, zipped=False):
        dict_bson = OrderedDict()
        for index, bsonimage in enumerate(self._bsonimagelist):
            dict_bson[str(index)] = bsonimage.todict
        abson = bson.BSON.encode(dict_bson)
        with open(newfilename, 'wb') as f:
            if zipped:
                abson = gzip.compress(abson)
            f.write(abson)

    @classmethod
    def fromfile(cls, filename, zipped=False):
        options = CodecOptions(document_class=OrderedDict)
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
        files_ids = []
        for bsonimage in self._bsonimagelist:
            file_id = bsonimage.tomongo(fs)
            files_ids.append(file_id)
        return files_ids

    @classmethod
    def frommongo(cls, files_ids, fs):
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
