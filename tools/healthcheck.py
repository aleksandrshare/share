#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import requests
from time import sleep
from urllib.parse import urlparse
from pathlib import Path
from framework.other_proj_ui.queries.fc_pg_queries import PgSQLQueries
import os
from configs.service_ports import ports

ROOT_DIR = Path(__file__).parent.parent.absolute()
ARTIFACTS_DIR = str(ROOT_DIR / '_artifacts')
LOGGER = logging.getLogger(__name__)


def health_check_rabbit(rabbit_host):
    """ функция проверяет доступность хоста с rabbitMQ

    :param rabbit_host: url хоста с короликом, без http
    :type rabbit_host: str
    :return: True или False, в зависимости от доступности кролика
    :rtype: bool
    """
    result = True
    url = 'http://{}/'.format(rabbit_host)
    LOGGER.info('Check RabbitMQ availability on {}'.format(url))
    try:
        LOGGER.debug('Making request: GET {}'.format(url))
        resp = requests.get(url)
        if resp.status_code != 200:
            result = False
            error = 'Error! {} is unavailable'.format(url)
            LOGGER.error(error)
            return result
        else:
            LOGGER.debug('{} is available'.format(url))
    except requests.exceptions.ConnectionError:
        result = False
        error = '{} connection error'.format(url)
        LOGGER.error(error)
        return result
    return result


def health_check_db(db_host):
    """ функция проверяет наличие доступа к базе данных PosgreSQL

    :param db_host: имя хоста с портом
    :return: True, если удалось получить ответ на запрос к базе
    :rtype: bool
    """
    result = True
    url = 'http://{}/'.format(db_host)
    LOGGER.info('Check Database availability on {}'.format(url))
    # Запрос в базу на кол-во коннекшенов
    db_client = PgSQLQueries(db_host)
    response = db_client.pg_stat_activity_request()
    if response:
        LOGGER.debug('Database available on {}'.format(url))
    else:
        LOGGER.error('Cannot get any response from {}'.format(url))
        result = False
        return result
    return result


def health_check_db_rabbit(rabbit_host, db_host):
    """ объединяющий метод проверки доступа к базе данных PosgreSQL и к хосту с rabbitMQ"""
    result = False
    if health_check_rabbit(rabbit_host) and health_check_db(db_host):
        result = True
    return result


def health_check_services(stand_url, stand_type):
    """ функция проверки сервисов на стендах """
    stand_name = urlparse(stand_url).hostname
    LOGGER.info('Check services on {}'.format(stand_name))
    result = True
    for port in ports.keys():
        url = 'http://{}:{}/api/health'.format(stand_name, port)
        try:
            LOGGER.debug('Making request: GET {}'.format(url))
            resp = requests.get(url)
            if resp.status_code != 200:
                if resp.status_code == 418:
                    if stand_type == 'LKOO' and port == '7022':
                        LOGGER.info('{}: {} with port {} has status code: {}. It is OK on LKOo'
                                    .format(stand_name, ports[port], port, resp.status_code))
                        continue
                    for _ in range(30):
                        sleep(2)
                        LOGGER.debug('Making request: GET {}'.format(url))
                        resp = requests.get(url)
                        if resp.status_code == 200:
                            break
                    if resp.status_code != 200:
                        raise ValueError
                else:
                    raise ValueError
            if resp.json().get('status') != 'running':
                result = False
                error = '{}:{} {} has status: {}'.format(stand_name, port, ports[port],
                                                                    resp.json().get('status'))
                LOGGER.error(error)
                save_failed_services(error)
            else:
                LOGGER.debug(
                    '{}:{} {} has status: {}'.format(stand_name, port, ports[port],
                                                                    resp.json().get('status')))
        except requests.exceptions.ConnectionError:
            error = '{}: connection error for {} with port {}.'.format(stand_name, ports[port], port)
            LOGGER.error(error)
            result = False
            save_failed_services(error)
        except ValueError:
            error = '{}: service {} with port {} got unexpected response code: {}. Response body:{}' \
                .format(stand_name, ports[port], port, resp.status_code, resp.text)
            LOGGER.error(error)
            save_failed_services(error)
            result = False
    return result


def save_failed_services(error):
    """ Функция сохраняет текст ошибки в файл

    :param error: текст ошибки, который нужно сохранить
    """
    if not os.path.exists(ARTIFACTS_DIR):
        os.makedirs(ARTIFACTS_DIR)
    file_name = ARTIFACTS_DIR + '/health_check.txt'
    with open(file_name, 'a', encoding='utf-8') as test_result:
        test_result.write(error + '\n')
    return file_name


def get_services_from_system_info(client):
    try:
        services = client.sysInfo_get_for_health_check()
    except Exception as ex:
        LOGGER.error("Проблема при запросе списка сервисов у сервиса SystemInfo, текст ошибки ниже")
        LOGGER.error(str(ex))
        raise
    return services


def platform_health_check_services(stand_url, client):
    """ функция проверки сервисов на стендах """
    stand_name = urlparse(stand_url).hostname
    LOGGER.info('Check services on {}'.format(stand_name))
    result = True
    failed_services_name = list()
    services_from_system_info = get_services_from_system_info(client)
    for service in services_from_system_info:
        url = 'http://{}:{}/api/health'.format(stand_name, ports.get(service))
        try:
            LOGGER.debug('Making request: GET {}'.format(url))
            resp = requests.get(url)
            if resp.status_code != 200:
                if resp.status_code == 418:
                    for _ in range(30):
                        sleep(2)
                        LOGGER.debug('Making request: GET {}'.format(url))
                        resp = requests.get(url)
                        if resp.status_code == 200:
                            break
                    if resp.status_code != 200:
                        raise ValueError
                else:
                    raise ValueError
            if resp.json().get('status') != 'running':
                result = False
                error = '{}:{} {} has status: {}'.format(stand_name, ports.get(service), service,
                                                         resp.json().get('status'))
                LOGGER.error(error)
                save_failed_services(error)
                failed_services_name.append(service)
            else:
                LOGGER.debug(
                    '{}:{} {} has status: {}'.format(stand_name, ports.get(service), service,
                                                     resp.json().get('status')))
        except requests.exceptions.ConnectionError:
            error = '{}: connection error for {} with port {}.'.format(stand_name, service, ports.get(service))
            LOGGER.error(error)
            result = False
            failed_services_name.append(service)
            save_failed_services(error)
        except ValueError:
            error = '{}: service {} with port {} got unexpected response code: {}. Response body:{}' \
                .format(stand_name, service, ports.get(service), resp.status_code, resp.text)
            LOGGER.error(error)
            save_failed_services(error)
            result = False
    return result, failed_services_name
