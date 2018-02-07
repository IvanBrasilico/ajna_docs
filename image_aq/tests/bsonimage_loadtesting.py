import datetime
import os
import re
import subprocess
import time
import unittest

import gridfs
from pymongo import MongoClient

from image_aq.models.bsonimage import BsonImage, BsonImageList

CARGAS = [1000, 10000]
TEST_PATH = os.path.abspath(os.path.dirname(__file__))
IMG_FOLDER = os.path.join(TEST_PATH, '..', '..', 'padma/tests/')


class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """

    def __init__(self, methodName='runTest', param=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.param = param

    @staticmethod
    def parametrize(testcase_klass, param=None):
        """
         Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, param=param))
        return suite


class TestModel(ParametrizedTestCase):
    def setUp(self):
        self.s0 = time.time()
        self._bsonimage = BsonImage(
            filename=os.path.join(IMG_FOLDER, 'stamp1.jpg'),
            chave='MSKU123',
            origem=0,
            data=datetime.datetime.utcnow()
        )
        self._bsonimage2 = BsonImage(
            filename=os.path.join(IMG_FOLDER, 'stamp2.jpg'),
            chave='MSKU1234',
            origem=1,
            data=datetime.datetime.utcnow()
        )
        self._bsonimagelist = BsonImageList()
        for r in range(self.param // 2):
            self._bsonimagelist.addBsonImage(self._bsonimage)
            self._bsonimagelist.addBsonImage(self._bsonimage2)
        print('Testando carga com ', len(self._bsonimagelist.tolist),
              'imagens')
        self._db = MongoClient().test
        self._fs = gridfs.GridFS(self._db)
        self.stest = time.time()
        print('Tempo de inicio: ', self.stest - self.s0)

    def tearDown(self):
        send = time.time()
        print('Tempo do Teste: ', send - self.stest)
        print('Tempo Total: ', send - self.s0)

    def test_1savefilelist(self):
        self._bsonimagelist.tofile(os.path.join(TEST_PATH, 'testlist.bson'))

    def test_2loadfilelist(self):
        bsonimagelist = BsonImageList.fromfile(
            os.path.join(TEST_PATH, 'testlist.bson'))
        assert bsonimagelist is not None

    def test_3savefilelistzip(self):
        self._bsonimagelist.tofile(os.path.join(
            TEST_PATH, 'testlist.bson.zip'), zipped=True)

    def test_4loadfilelistzip(self):
        bsonimagelist = BsonImageList.fromfile(
            os.path.join(TEST_PATH, 'testlist.bson.zip'), zipped=True)
        assert bsonimagelist is not None

    def test_5savemongolist(self):
        global files_ids
        files_ids = self._bsonimagelist.tomongo(self._fs)
        assert files_ids is not None

    def test_6loadmongolist(self):
        bsonimagelist = BsonImageList.frommongo(files_ids, self._fs)
        assert bsonimagelist is not None


if __name__ == '__main__':
    print('##################################################')
    print('# Testes com uso de tabela RESUMO!!!')
    command = 'cat /proc/cpuinfo'
    all_info = subprocess.check_output(command, shell=True).strip()
    all_info = all_info.decode()
    for line in all_info.split('\n'):
        if 'model name' in line:
            print(re.sub('.*model name.*:', '', line, 1))
    print(os.uname())
    print(time.strftime('%Y-%m-%d %H:%M'))
    suite = unittest.TestSuite()
    for carga in CARGAS:
        suite.addTest(ParametrizedTestCase.parametrize(TestModel, param=carga))
    unittest.TextTestRunner(verbosity=2).run(suite)
