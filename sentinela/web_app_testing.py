import unittest
import os

os.environ['HTTP_SERVER'] = 'http://localhost:5000'

from sentinela.tests.app_test import FlaskTestCase

if __name__ == '__main__':
    test = FlaskTestCase
    unittest.main()
