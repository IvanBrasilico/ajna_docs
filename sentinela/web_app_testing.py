"""Configuration for functional WebTest
https://docs.pylonsproject.org/projects/webtest/en/latest/testapp.html
Usage: python sentinela/web_app_testing.py
Needs a running server to test
"""
import unittest
import os

os.environ['HTTP_SERVER'] = 'http://localhost:5000'

from sentinela.tests.app_test import FlaskTestCase

if __name__ == '__main__':
    test = FlaskTestCase
    unittest.main()
