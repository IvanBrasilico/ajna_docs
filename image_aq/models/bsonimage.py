import pymongo
import os
from pathlib import Path
from bson import Binary
from bson.json_util import dumps


class BsonImage():
    def __init__(self, filename, **kwargs):
        self._metadata = kwargs
        self._filename = filename

    def todict(self):
        return dict(metadata=self._metadata,
                    filename=self._filename
                    )

    def tobson(self):
        file = Path(self._filename)
        data = None
        if file.exists():
            with open(self._filename, 'rb') as f:
                content = f.read()
            print('File found')
            mydict = self.todict()
            mydict['content'] = Binary(content)
            data = dumps(mydict)
        return data

    def tofile(self, newfilename):
        with open(newfilename, 'w') as f:
            f.write(self.tobson())

    def fromfile(self, filename):
        with open(filename, 'rb') as f:
            pass

    def tomongo(self, fs):
        with fs.new_file(**self.todict()) as fp:
            with open(self._filename, 'rb') as fo:
                fp.write(fo)

class BsonImageList():
    pass
