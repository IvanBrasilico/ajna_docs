import bson
from PIL import Image


class BsonImage():
    def __init__(self, filename, **kwargs):
        self._metadata = kwargs
        self._filename = filename

    def tobson(self):
        image = Image.open(self._filename)
        data = bson.BSON.encode(
            dict(metadata = self._metadata,
            filename=self._filename,
            content=image)
        )
        return data

    def tofile(self, filename):
        with open(filename, 'wb') as f:
            pass


    def fromfile(self, filename):
        with open(filename, 'rb') as f:
            pass

    def tomongo(self, conn):
        pass


class BsonImageList():
    pass
