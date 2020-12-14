#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import pytest
from framework.platform.api_auto.pl_api_workers import LKOApiAdmin, IntegrationApiUser
from configs.modify_data import test_modify_data, context_data
import os

logger = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def lko_admin(stand):
    """
    Инициализация клиента для работы с внутренним API

    :param stand: значение фикстуры "stand"
    :return: клиент для работы с внутренним API
    """
    client = LKOApiAdmin(stand)
    return client


@pytest.fixture(scope='session')
def ssh_admin(lko_admin):
    if not lko_admin.ssh_client.ssh_conn:
        pytest.skip("Test cannot be proceed because it needs ssh connection!"
                    "{}".format(lko_admin.ssh_client.connection_error))
    else:
        yield lko_admin
        lko_admin.ssh_client.close_ssh_connection()


@pytest.fixture(scope='class')
def sla_rules_file(ssh_admin):
    sla_file_name = os.path.basename(ssh_admin.sla_rule_path)
    ssh_admin.ssh_client.ftp.chdir(ssh_admin.sla_remote_directory)
    if sla_file_name not in ssh_admin.ssh_client.ftp.listdir():
        ssh_admin.sla_upload_custom_rule_file()
        yield ssh_admin
        ssh_admin.ssh_client.ftp_restore_files_after_backup_in_dir(ssh_admin.sla_remote_directory)
        ssh_admin.ssh_client.ssh_restart_win_service('PT.SP.SLA')
    else:
        yield


@pytest.fixture(scope='function', autouse=True)
def setup_and_teardown():
    """ Фикстура автоматически вызывается при запуске теста. Как setup, очищает данные в test_modify_data
    После окончания теста проверяет, есть ли записанные ошибки и фейлит тест при их наличи.
     Если были перезаписаны файлы на стендее, то востанавливает бекап и ребутает сервис"""
    test_modify_data.clear()
    test_modify_data['errors'] = []
    test_modify_data['need_restore'] = {}
    yield
    if test_modify_data.get('errors'):
        pytest.fail('\n'.join(test_modify_data['errors']))


@pytest.fixture(scope='session')
def integr_api_lko_admin(stand):
    """
    Инициализация клиента для работы с интеграционным API

    :param stand: значение фикстуры "stand"
    :return: клиент для работы с интеграционным API
    """
    client = IntegrationApiUser(stand)
    return client


@pytest.fixture(scope='class', autouse=True)
def clear_context():
    """
    Фикстура автоматически вызывается при запуске тестового класса. Очищает переменную-контекст
    """
    context_data.clear()
