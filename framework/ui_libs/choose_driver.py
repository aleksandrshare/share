#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from selenium import webdriver
import getpass

#########################################################
# paths до бинарников и remote url selenium drivers
# смотрим нужную ОС и закидываем бинарники в указанные пути или передаем ip к Grid серверу в remote_driver
driver_bins = {
    'firefox_unix': '/usr/bin/geckodriver',
    'chrome_unix': '/usr/bin/chromium.chromedriver',
    'firefox_win':  'C:\\Selenium_drivers\\geckodriver.exe',
    'chrome_win': 'C:\\Selenium_drivers\\chromedriver.exe',
    'chrome_mac': '/Users/%s/sele_drivers/chromedriver' % getpass.getuser(),
    'firefox_mac': '/Users/%s/sele_drivers/geckodriver' % getpass.getuser(),
    'safari_mac': '/usr/bin/safaridriver',
    'remote_driver': "http://%s:4444/wd/hub"  # сюда небходимо передать ip или доменное имя до Grid/selenoid
               }
#########################################################


def choose_and_cofig_driver(browser, platform="", capabilities=None, url_remote_driver=None):
    """функция помогает настроить дрйвер под разные ОС, принимает :param
    browser: str имя браузера варианты 'chrome', 'firefox', 'safari'

    параметры ниже передавать не нужно если дравер локальный
    platform: str 'remote' для настройки удаленного драйвера или пустая строка для локального драйвера
    capabilities: dict c настройками для remote driver
        пример {"browserName": "chrome", "version": "74.0", "videoName": None}
    url_remote_driver: str ip или доменное имя Grid/selenoid пример '127.0.0.1' используеться только для remote driver
    :return driver настроенный экземпляр класса selenium.webdriver
    """
    if platform == 'remote':
        return _config_remote_platform(capabilities, url_remote_driver)
    elif sys.platform == 'win32':
        return _config_win_platform(browser)
    elif sys.platform == 'linux':
        return _config_linux_platform(browser)
    elif sys.platform == 'darwin':
        return _config_mac_platform(browser)
    else:
        raise Exception("unknown OS see the choose_driver.py file for usage understanding")


def _config_remote_platform(capabilities, url_remote_driver):
    # платформа удаленная грид или селенойд
    driver_bin = driver_bins['remote_driver'] % url_remote_driver
    return webdriver.Remote(driver_bin, desired_capabilities=capabilities)


def _config_win_platform(browser):
    # виндовс машина
    driver = None
    if browser == 'firefox':
        driver = webdriver.Firefox(executable_path=driver_bins['firefox_win'])
    elif browser == 'chrome':
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(executable_path=driver_bins['chrome_win'], chrome_options=options)
    return driver


def _config_linux_platform(browser):
    # линукс машина
    driver = None
    if browser == 'firefox':
        driver = webdriver.Firefox(executable_path=driver_bins['firefox_unix'])
    elif browser == 'chrome':
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(executable_path=driver_bins['chrome_unix'], chrome_options=options)
    return driver


def _config_mac_platform(browser):
    # mac машина
    driver = None
    if browser == 'firefox':
        driver = webdriver.Firefox(executable_path=driver_bins['firefox_mac'])
    elif browser == 'chrome':
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(executable_path=driver_bins['chrome_mac'], chrome_options=options)
    elif browser == 'safari':
        driver = webdriver.Safari(executable_path=driver_bins['safari_mac'])
    return driver
