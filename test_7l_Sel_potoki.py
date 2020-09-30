import time
import pytest
import urllib

from selenium import webdriver
from selenium.webdriver import ActionChains  # скрол до элемента
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestRebelStar:
    def setup_class(self):
        # DRIVER_PATH_FIREFOX = "C:/Program Files (x86)/Mozilla Firefox/geckodriver.exe"
        # DRIVER_PATH_OPERA = "C:/Program Files (x86)/Opera/operadriver.exe"
        # self.firefox = webdriver.Firefox(executable_path=DRIVER_PATH_FIREFOX)
        # self.opera = webdriver.Opera(executable_path=DRIVER_PATH_OPERA)
        self.driver = webdriver.Chrome()
        self.domain = 'https://rebelstar.ru/'

    def teardown_class(self):
        self.driver.close()

    @pytest.mark.parametrize("raider, operative, fog", [
        (True, True, True), (True, True, False),
        (True, False, True), (True, False, False),
        (False, True, True), (False, True, False),
        (False, False, True), (False, False, False),
        #('opera', True, True, True), ('opera', True, True, False),
        #('opera', True, False, True), ('opera', True, False, False),
        #('opera', False, True, True), ('opera', False, True, False),
        #('opera', False, False, True), ('opera', False, False, False)
    ])
    def test_domain(self, raider, operative, fog):
        # driver = webdriver.Chrome()
        self.driver.get(self.domain)
        try:
            assert "Rebel Star" in self.driver.title
            if raider:
                self.driver.execute_script("document.getElementById('rs1-ai1').checked = true")
                # self.driver.find_element_by_css_selector(
                #     '#two > div > div > article:nth-child(1) > div > ul > li:nth-child(1) > label').click()
            if operative:
                self.driver.execute_script("document.getElementById('rs1-ai2').checked = true")
                # self.driver.find_element_by_css_selector(
                #     '#two > div > div > article:nth-child(1) > div > ul > li:nth-child(2) > label').click()
            if fog:
                self.driver.execute_script("document.getElementById('rs1-fog').checked = true")
                # self.driver.find_element_by_css_selector(
                #     '#two > div > div > article:nth-child(1) > div > ul > li:nth-child(3) > label').click()

            # target = self.driver.find_element_by_id('imgRS1')     # скрол до элемента
            # actions = ActionChains(self.driver)
            # actions.move_to_element(target)
            # actions.perform()

            button = self.driver.find_element_by_id('imgRS1')
            button.click()

            urlParse = urllib.parse.urlparse(self.driver.current_url)
            assert urlParse.path == '/RS1/index.html'
            query = urllib.parse.urlencode(dict(raider=raider, operative=operative, fog=fog)).lower()
            assert urlParse.query == query
            gamecanvas = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'gamecanvas')))
            uicanvas = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'uicanvas')))
            assert gamecanvas.get_attribute('width') == uicanvas.get_attribute('width')
            print(urlParse)
            self.driver.back()
            self.driver.find_element_by_tag_name('body').send_keys(Keys.UP)    # скрол вверх
            butt = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'imgRS2')))
            assert butt
            # self.driver.close()
        except ValueError as err:
            # self.driver.quit()
            print(err)
            assert False

