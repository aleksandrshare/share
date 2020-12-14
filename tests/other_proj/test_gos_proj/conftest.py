#!/usr/bin/env python
# -*- coding: utf-8 -*-

from framework.other_proj.api_auto.cp_api_workers import CpApiAdmin
from framework.other_proj.ui_auto.cp_ui_workers import CertPortalAdminClass
from framework.other_proj.api_auto.fc_api_workers import LKUapiPayee, LKUapiPayer, LKOZapiAdmin
from framework.other_proj.ui_auto.fc_ui_workers import LKOOclass, LKUclass, LKOZclass
from ui_library.choose_driver import choose_and_cofig_driver
from configs.settings import url_to_selenoid
from tests.conftest import _configure_capabilities
import pytest


def pytest_addoption(parser):
    parser.addoption("--cert_stand", action="store", default="CERTAUTOFT", type=str, help="Выбор стенда с gos_proj")


@pytest.fixture(scope='session')
def cert_stand(request):
    stand = request.config.getoption("--cert_stand").upper()
    return stand


@pytest.fixture(scope='session')
def lku_payer_api(stand, users_dss_pin):
    client = LKUapiPayer(stand, users_dss_pin)
    return client


@pytest.fixture(scope='session')
def lku_payee_api(stand, users_dss_pin):
    client = LKUapiPayee(stand, users_dss_pin)
    return client


@pytest.fixture(scope='session')
def lkoz_admin_api(stand):
    client = LKOZapiAdmin(stand)
    return client


@pytest.fixture(scope='session')
def cp_api_admin(cert_stand):
    client = CpApiAdmin(cert_stand)
    return client


@pytest.fixture(scope='function')
def do_driver(request, stand):
    """фикстура запускает,настраивает драйвер, парсит парамтры из командной строки
    и передает в следующие фикстуры"""
    platform = request.config.getoption('--platform')
    browser = request.config.getoption("--browser")
    selenoid_server = request.config.getoption("--selenoid")
    capabilities = _configure_capabilities(platform, browser, request)
    driver = choose_and_cofig_driver(browser, platform, capabilities, url_to_selenoid.format(selenoid_server))

    # файналазер, завершает сессию драйвера
    def driver_quit():
        try:
            driver.quit()
        except Exception:
            print('Session expired and already closed')

    request.addfinalizer(driver_quit)
    return driver, stand.upper()


@pytest.fixture(scope='function')
def lkoo_ui(do_driver):
    """инициализирует класс ЛКОо с selenium driver"""
    driver, stand = do_driver
    lkoo = LKOOclass(driver, stand)
    return lkoo


@pytest.fixture(scope='function')
def lku_ui(do_driver, users_dss_pin):
    """инициализирует класс ЛКУ с selenium driver"""
    driver, stand = do_driver
    lku = LKUclass(driver, stand, users_dss_pin)
    return lku


@pytest.fixture(scope='function')
def lkoz_ui(do_driver):
    """инициализирует класс ЛКОз с selenium driver"""
    driver, stand = do_driver
    lkoz = LKOZclass(driver, stand)
    return lkoz


@pytest.fixture(scope='function')
def cp_admin(do_driver, cert_stand):
    """инициализирует класс церт-портала с selenium driver"""
    driver, _ = do_driver
    cert = CertPortalAdminClass(driver, cert_stand)
    return cert





