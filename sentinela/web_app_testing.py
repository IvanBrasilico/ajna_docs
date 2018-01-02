"""Configuration for functional WebTest
https://docs.pylonsproject.org/projects/webtest/en/latest/testapp.html
Usage: python sentinela/web_app_testing.py
Needs a running server to test
"""
import os
import unittest

from sentinela.tests.app_test import FlaskTestCase

os.environ['HTTP_SERVER'] = 'http://localhost:5000'

if __name__ == '__main__':
    test = FlaskTestCase
    unittest.main()
