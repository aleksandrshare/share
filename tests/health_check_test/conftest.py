#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from framework.platform.api_auto.pl_api_workers import LKOApiAdmin


@pytest.fixture(scope='session', autouse=True)
def system_monitoring(stand, mon_freq, request):
    pass


@pytest.fixture(scope='session')
def stand(request):
    """
    Фикстура для получения инфы о выбранном стенде из командной строки
    передавать как и сотальные фикстуры через параметры функций/методов для доступа

    :return str: имя стенда
    """
    stand = request.config.getoption("--stand").upper()
    return stand


@pytest.fixture(scope='session')
def lko_admin(stand):
    client = LKOApiAdmin(stand)
    return client
