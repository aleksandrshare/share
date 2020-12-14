#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from configs.modify_data import participants_params_payer, participants_params_payee
from configs.settings import stands
import logging
from tools.utils import extract_domain_from_url, byte_to_Gb, to_fixed, remove_file
from framework.other_proj.api_auto.fc_api_workers import LKUapiPayee, LKUapiPayer
from framework.other_proj.ui_auto.fc_ui_workers import LKOOclass, LKUclass, LKOZclass
from ui_library.choose_driver import choose_and_cofig_driver
from configs.settings import url_to_selenoid
from time import time
from configs.dictionary_variables import prometheus_queries
import tools.monitoring as mon
import datetime
from tests.conftest import _configure_capabilities

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption('--dss_mode', default='no', help='Enter DssService mode value (emul, prod, no)')


@pytest.fixture(scope='session', autouse=True)
def shared_client_payer(stand, users_dss_pin):
    client = LKUapiPayer(stand, users_dss_pin)
    return client


@pytest.fixture(scope='session', autouse=True)
def shared_client_payee(stand, users_dss_pin):
    client = LKUapiPayee(stand, users_dss_pin)
    return client


@pytest.fixture(scope='session', autouse=True)
def prepare_data_for_obs(request, shared_client_payer, shared_client_payee):
    """подготовка данных для payer и payee, заполняет словари данными БИК, БИН"""
    shared_client_payer.get_antifraud_add_params_for_ui_tests()
    shared_client_payee.get_antifraud_add_params_for_ui_tests()
    shared_client_payer.log.info("Выполнен Запрос данных для участников")

    def clear_dicts():
        participants_params_payer.clear()
        participants_params_payee.clear()

    request.addfinalizer(clear_dicts)


@pytest.fixture(scope='session')
def dss_mode(request):
    return request.config.getoption("--dss_mode")


@pytest.fixture(scope='class')
def driver_do(request, stand):
    """фикстура запускает,настраивает драйвер, парсит парамтры из командной строки
    и передает в следующие фикстуры"""
    platform = request.config.getoption('--platform')
    browser = request.config.getoption("--browser")
    selenoid_server = request.config.getoption("--selenoid")
    capabilities = _configure_capabilities(platform, browser, request)
    driver = choose_and_cofig_driver(browser, platform, capabilities, url_to_selenoid.format(selenoid_server))

    # файналазер, завершает сессию драйвера и обнуляет собранные данные
    def driver_quit():
        global shared_obs_info, request_info_lko, request_info_lku
        shared_obs_info['counter'] = 0
        for i in request_info_lko.keys():
            request_info_lko[i] = None
        for i in request_info_lku.keys():
            request_info_lku[i] = None
        driver.quit()

    request.addfinalizer(driver_quit)

    return driver, stand.upper()


@pytest.fixture(scope='class')
def lkoo(driver_do):
    """инициализирует класс ЛКОо с selenium driver"""
    driver, stand = driver_do
    lkoo = LKOOclass(driver, stand)
    return lkoo


@pytest.fixture(scope='class')
def lku(driver_do, users_dss_pin):
    """инициализирует класс ЛКУ с selenium driver"""
    driver, stand = driver_do
    lku = LKUclass(driver, stand, users_dss_pin)
    return lku


@pytest.fixture(scope='class')
def lkoz(driver_do):
    """инициализирует класс ЛКОз с selenium driver"""
    driver, stand = driver_do
    lkoz = LKOZclass(driver, stand)
    return lkoz
