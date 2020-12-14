#!/usr/bin/env python
# -*- coding: utf-8 -*-
from framework.other_proj.api_auto.fc_api_workers import (LKUapiPayee, LKUapiPayer, LKOZapiAdmin, LKOOapiAdmin,
                                                          ExtApiPayer, ExtApiPayee, ExtApiPayer2, ExtApiPayee2,
                                                          ExtApiParticipantEdit, LKUapiParticipantEdit)
import pytest
from configs.modify_data import test_modify_data


def pytest_addoption(parser):
    parser.addoption("--platform_ext_api", action="store", default="", type=str,
                     help="запуск локально или через selenium hub")
    parser.addoption("--browser_ext_api", action="store", default="chrome", type=str, help="Выбор браузера")


@pytest.fixture(scope='function', autouse=True)
def setup_and_teardown():
    """ Фикстура автоматически вызывается при запуске теста. Как setup, очищает данные в test_modify_data
    После окончания теста проверяет, есть ли записанные ошибки и фейлит тест при их наличи """
    test_modify_data.clear()
    test_modify_data['errors'] = list()
    yield
    if test_modify_data.get('errors'):
        pytest.fail('\n'.join(test_modify_data['errors']))


@pytest.fixture(scope='session')
def api_payer(stand, users_dss_pin):
    client = LKUapiPayer(stand, users_dss_pin)
    return client


@pytest.fixture(scope='session')
def api_payee(stand, users_dss_pin):
    client = LKUapiPayee(stand, users_dss_pin)
    return client


@pytest.fixture(scope='session')
def api_participant_edit(stand, users_dss_pin=None):
    client = LKUapiParticipantEdit(stand, users_dss_pin=None)
    return client


@pytest.fixture(scope='session')
def api_admin_lkoz(stand):
    client = LKOZapiAdmin(stand)
    return client


@pytest.fixture(scope='session')
def api_admin_lkoo(stand):
    client = LKOOapiAdmin(stand)
    return client


@pytest.fixture(scope='session')
def ext_api_payer(stand, users_dss_pin):
    client = ExtApiPayer(stand, users_dss_pin)
    return client


@pytest.fixture(scope='session')
def ext_api_payer_2(stand):
    client = ExtApiPayer2(stand)
    return client


@pytest.fixture(scope='session')
def ext_api_payee(stand, users_dss_pin):
    client = ExtApiPayee(stand, users_dss_pin)
    return client


@pytest.fixture(scope='session')
def ext_api_payee_2(stand):
    client = ExtApiPayee2(stand)
    return client


@pytest.fixture(scope='session')
def ext_api_participant_edit(stand):
    client = ExtApiParticipantEdit(stand)
    return client


@pytest.fixture(scope='class')
def load_and_publish_feeds(api_admin_lkoz):
    api_admin_lkoz.upload_feeds()
    api_admin_lkoz.publish_feeds()
