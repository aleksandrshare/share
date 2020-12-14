#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from configs.settings import stands
import logging
import os
import sys
import shutil
from tools.utils import TEST_ARTIFACTS_DIR, extract_domain_from_url, byte_to_Gb, to_fixed, remove_file
from configs.settings import selenoid_driver_capabilities
from time import time
from configs.dictionary_variables import prometheus_queries
import tools.monitoring as mon
import datetime


logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    # Переменная окружения указывающая на корневую папку тестов, использование os.environ.get("TESTS_ROOT_DIR")#######
    os.environ["TESTS_ROOT_DIR"] = str(str(parser.extra_info.get('rootdir').strpath))
    ##################################################################################################################
    parser.addoption("--stand", action="store", default="domen_name", type=str,
                     help="Выбор группы стендов")
    parser.addoption('--health_check', default='yes', help='Start health check: yes, no, full')
    parser.addoption("--platform", action="store", default="", type=str, help="remote or local browser")
    parser.addoption("--browser", action="store", default="chrome", type=str, help="choose browser")
    parser.addoption("--selenoid", action="store", default="test_serv_01", type=str,
                     help="choose grid/selenoid test_serv_01 or test_serv_02")
    parser.addoption("--mon", action="store", default="no", type=str, help="monitoring in test yes/no")
    parser.addoption("--mon_freq", action="store", default="1m", type=str, help="frequency of monitoring metrics"
                                                                                " sec/min (example: 1s, 1m)")
    parser.addoption("--mon_dir", action="store", default=os.environ["TESTS_ROOT_DIR"] + "//logs//", type=str,
                     help="dir for monitoring artifacts")


@pytest.fixture(scope='session', autouse=True)
def delete_artifacts():
    os.path.exists(TEST_ARTIFACTS_DIR)
    shutil.rmtree(TEST_ARTIFACTS_DIR)


@pytest.fixture(scope='session')
def stand(request):
    """
    Фикстура для получения инфы о выбранном стенде из командной строки

    :return str: stand name
    """
    stand = request.config.getoption("--stand").upper()
    return stand


def _configure_capabilities(platform, browser, req):
    """
    функция проверяет аргументы pytest на remote driver и настраивает capabilities

    :return: dict
    """
    capabilities = None
    video_name = "video_%s.mp4" % str(req.node.name)
    if platform == 'remote':
        if browser == 'chrome':
            capabilities = selenoid_driver_capabilities['chrome']
        elif browser == 'firefox':
            capabilities = selenoid_driver_capabilities['firefox']
        capabilities["videoName"] = video_name
    return capabilities


@pytest.fixture(scope='class')
def clear_dir_for_browser(request):
    """ очистка папки for_browser перед тестами и после тестов, работает на класс и только при запуске на удаленной
        машине selenoid"""
    def clear_files():
        if 'linux' in sys.platform:
            import glob
            files = glob.glob('/home/for_browser/*')
            for file in files:
                if os.path.isfile(file):
                    os.remove(file)
            logger.info("Clear dir for_browser before/after tests")
    clear_files()
    request.addfinalizer(clear_files)


@pytest.fixture(scope='session')
def mon_freq(request):
    """
    Фикстура определяет значение частоты мониторинга prometheus

    :param request: строка параметров
    :return: значение частоты мониторинга
    """
    return request.config.getoption("--mon_freq")


@pytest.fixture(scope='session', autouse=True)
def system_monitoring(stand, mon_freq, request):
    """
    Фикстура для получения метрик о производительности стендов из параметров, и записью их в csv и json файлы

    :param stand: название группы стендов
    :param mon_freq: значение частоты мониторинга
    :param request: строка параметров
    """
    on_off_mon = request.config.getoption("--mon")
    mon_dir = request.config.getoption("--mon_dir")
    if on_off_mon == 'no':
        logger.info('Мониторинг не включен')
        yield
    else:
        monitoring_file_path = mon_dir + '/' + 'monitoring_results.csv'
        stable_file_path = mon_dir + '/' + 'stable_monitoring_results.json'
        remove_file(monitoring_file_path)
        remove_file(stable_file_path)
        test_start_time = time()

        yield test_start_time

        test_end_time = time()
        domain_lko = extract_domain_from_url(stands[stand]['LKO_URL'])
        stand_domains = (domain_lko, )
        stable_file = open(stable_file_path, 'w')
        with open(monitoring_file_path, 'w') as monitoring_file:
            monitoring_file.write('Build details' + '\n')
            monitoring_file.close()
        for domain in stand_domains:
            mon.file_headers(monitoring_file_path, domain)
            stable_file.write(domain + '\n')
            date_array = []
            report_array = list()
            report_array.append([])
            for query in prometheus_queries:
                stable_file.write('\t' + query + '\n')
                stable_file.write('\t\tDate\t\tValue\n')
                value_array = []
                query_with_domain = prometheus_queries.get(query) % {'job_name': 'job="{}"'.format(domain)}
                params = dict(query=query_with_domain, start=test_start_time, end=test_end_time, step=mon_freq)
                logger.info('GET "{}" on {}...'.format(query, domain))
                result_json = mon.get_prometheus_apirequest(params)
                if result_json:
                    for response_block in result_json['data']['result'][0]['values']:
                        value = to_fixed(response_block[1], 2)
                        date = to_fixed(response_block[0])
                        date = datetime.datetime.fromtimestamp(date)
                        stable_file.write(str(date))
                        if query != 'cpu_usage':
                            value = to_fixed(byte_to_Gb(value), 2)
                            value_array.append(value)
                            stable_file.write('\t' + str(value) + ' Gb\n')
                        else:
                            date_array.append(date)
                            value_array.append(value)
                            stable_file.write('\t' + str(value) + ' %\n')
                    report_array.append(value_array)
                else:
                    logger.error('Monitoring results is empty! Force to stop reporting!!!')
                    return
            report_array[0] = date_array
            table = dict(Date=report_array[0], cpu_usage_percentage=report_array[1], memory_usage_gb=report_array[2],
                         disk_c_free_gb=report_array[3])
            mon.write_csv_table_in_file(table, monitoring_file_path)
            stable_file.write('\n\n')
        stable_file.close()
