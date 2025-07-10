# driver_setup.py
"""
Configuración y obtención del driver de Selenium para TEAMMATES.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def get_driver():
    CHROMEDRIVER_PATH = r'C:/chromedriver/chromedriver.exe'
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver
