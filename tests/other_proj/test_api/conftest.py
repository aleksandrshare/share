#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from framework.other_proj.api_auto.fc_api_workers import (LKUapiPayee, LKUapiPayer, LKOOapiAdmin, LKOZapiAdmin,
                                                          LKOZapiOperator)
from configs.modify_data import test_modify_data
import logging

logger = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def lku_api_payer(stand, users_dss_pin):
    client = LKUapiPayer(stand, users_dss_pin)
    return client


@pytest.fixture(scope='session')
def lku_api_payee(stand, users_dss_pin):
    client = LKUapiPayee(stand, users_dss_pin)
    return client


@pytest.fixture(scope='session')
def lkoz_api(stand):
    client = LKOZapiAdmin(stand)
    return client


@pytest.fixture(scope='session')
def lkoo_api(stand):
    client = LKOOapiAdmin(stand)
    return client


@pytest.fixture(scope='session')
def lkoz_operator_api(stand):
    client = LKOZapiOperator(stand)
    return client


@pytest.fixture(scope='function', autouse=True)
def api_setup_and_teardown():
    """ Фикстура автоматически вызывается при запуске теста. Как setup, очищает данные в test_modify_data
    После окончания теста проверяет, есть ли записанные ошибки и фейлит тест при их наличи """
    logger.info('Clear test_modify_data')
    test_modify_data.clear()
    yield
    if test_modify_data.get('errors'):
        pytest.fail('\n'.join(test_modify_data['errors']))
