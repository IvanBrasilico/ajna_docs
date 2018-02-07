import os
import pickle
import threading
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import sentinela.app as app

UPLOAD_ITEM = '/sentinela/tests/BTP.csv'

class SeleniumTestCase(unittest.TestCase):

    def setUp(self):
        """ 
        Obter o geckodriver no site
        https://github.com/mozilla/geckodriver/releases
        docs
        http://selenium-python.readthedocs.io/locating-elements.html
        escrever roteiro e artigo sobre o selenium
        """

        self.driver = webdriver.Firefox()

        # skip these tests if the browser could not be started
        if self.driver:
            self.app = app.app
            self.app_context = self.app.app_context()
            self.app_context.push()

            # start the Flask server in a thread
            self.server_thread = threading.Thread(target=self.app.run,
                                                  kwargs={'debug': False})
            self.server_thread.start()
            self._login()

    def _login(self):
        driver = self.driver
        driver.get('http://localhost:5000/')
        time.sleep(3)
        driver.find_element_by_name('username').send_keys('ajna')
        try:
            driver.find_element_by_name('senha').send_keys('ajna')
            driver.find_element_by_id('btnlogin').click()
            time.sleep(1)
        except Exception as e:
            print(e)
        driver.implicitly_wait(30)

    def tearDown(self):
        self.driver.close()

    def test_aplica_risco(self):
        driver = self.driver
        driver.get('http://localhost:5000/')
        time.sleep(15)
        driver.find_element_by_partial_link_text('Importar').click()
        time.sleep(3)
        # upload = driver.find_element_by_id('upload')
        # enviar = driver.find_element_by_name('btnenviar')
        driver.find_element_by_name('CPFCNPJConsignatario.csv').click()
        padrao = Select(driver.find_element_by_id('padrao'))
        padrao.select_by_value('1')
        visualizacao = Select(driver.find_element_by_id('visao'))
        visualizacao.select_by_value('1')
        driver.find_element_by_name('2017/0329').click()
        time.sleep(15)


if __name__ == '__main__':
    unittest.main()
