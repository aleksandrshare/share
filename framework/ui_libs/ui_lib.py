#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import allure
from allure_commons.types import AttachmentType
import logging


def decorator_for_wait(_wait_element):
    """ декоратор для селениум waits расширяет функционал метода wait
    если передать str 'clickable' в метод _wait_element то элемент будет проверять на кликабельность, а
    не на видимость на странице"""
    def new_check(self, *locator):
        if locator[0] == 'clickable':
            locator = locator[1:]
            try:
                self.log.info("WAIT method 'clickable' for locator: %s" % str(locator))
                self.wait.until(EC.element_to_be_clickable(locator))
                sleep(1)
                return True
            except Exception as ex:
                self.log.error("EXCEPTION WAIT method 'clickable' for locator: %s" % str(ex))
                allure.attach(name='screen', body=self.driver.get_screenshot_as_png(), attachment_type=AttachmentType.PNG)
                raise Exception("locator %s dont found because it is very slow loading, or except:%s" % (str(locator),
                                                                                                         ex))
        else:
            return _wait_element(self, *locator)
    return new_check


class Page:
    """Основной класс для работы с селениумом"""
    log = logging.getLogger(__name__)
    video_counter = 0

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        # self.driver.implicitly_wait(30) # совместно с WebDriverWait лучше не использовать implicitly_wait
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 20)

    @classmethod
    def get_counter(cls):
        """class метод увеличивает счетчика для имени видео файла
        :return int
        """
        cls.video_counter += 1
        return cls.video_counter

    def open_page(self):
        self.log.info("Open page: %s" % self.url)
        self.driver.get(self.url)

    @decorator_for_wait
    def _wait_element(self, *locator):
        """ метод принимает локатор ищет элемент и ожидает когда элемент станет видим на странице"""
        try:
            self.log.info("WAIT method 'visible' for locator: %s" % str(locator))
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except Exception as ex:
            self.log.error("EXCEPTION WAIT method 'visible' for locator: %s" % str(ex))
            allure.attach(name='screen', body=self.driver.get_screenshot_as_png(), attachment_type=AttachmentType.PNG)
            raise Exception("locator %s dont found because it is very slow loading, or except: %s" % (str(locator), ex))

    def wait_for_invisibility_element(self, *locator):
        """ метод принимает локатор ищет элемент и ожидает когда элемент станет не видим на странице"""
        try:
            self.log.info("WAIT method 'invisibility' for locator: %s" % str(locator))
            element = self.wait.until(EC.invisibility_of_element_located(locator))
            if element:
                self.log.info("ELEMENT INVISIBILITY  go on: %s" % element)
                return True
        except Exception as ex:
            self.log.error("EXCEPTION WAIT method 'invisibility' for locator: %s" % str(ex))
            allure.attach(name='screen', body=self.driver.get_screenshot_as_png(), attachment_type=AttachmentType.PNG)
            raise Exception("locator %s don`t become invisible, or except: %s" % (str(locator), ex))

    def search_element(self, *locator):
        """Метод поиска одного элемента возвращает
        :return webelement"""
        element_wait = self._wait_element(*locator)
        if element_wait:
            element = self.driver.find_element(*locator)
            return element

    def search_elements(self, *locator):
        """Метод поиска нескольких элементов возвращает
        :return list"""
        element_wait = self._wait_element(*locator)
        if element_wait:
            elements = self.driver.find_elements(*locator)
            return elements

    def _click_element(self, element, *locator):
        """метод нахдит элемент проверяет его на кликабельность и кликает на него"""
        element_wait = self._wait_element('clickable', *locator)
        if element_wait:
            element.click()

    def find_and_clear_element(self, *locator):
        """метод находит и очищает формы"""
        element = self.search_element(*locator)
        if element.is_displayed():
            element.clear()

    def find_and_click(self, *locator):
        """метод находит элемент и кликает на него
        :return webelement"""
        element = self.search_element(*locator)
        self._click_element(element, *locator)
        return element

    def return_text_ele(self, *locator):
        """метод находит элемент и возвращает его текстовое значение"""
        element = self.search_element(*locator)
        sleep(1)
        return element.text

    def return_attrs_element(self, attr, *locator):
        """метод находит элемент и возвращает его атрибуты
        принимает str имя атрибута и локатор"""
        element = self.search_element(*locator)
        return element.get_attribute(attr)

    def find_and_fill_element(self, word, *locator):
        """метод находит и заполняет формы"""
        element = self.search_element(*locator)
        element.send_keys(word)

    def dropdown_list(self, name, *locator):
        """метод принимает имя для поиска внутри списка и локатор
        возвращает 2 элемента
        1. кликабельный элемент для открытия списка
        2. объэкт класса Select
        """
        main_element = self.search_element(*locator)
        select = Select(main_element.find_element_by_name(name))
        return main_element, select
