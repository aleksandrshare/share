import pandas
import requests
import logging
import json
from configs.settings import prometheus_api_url

logger = logging.getLogger(__name__)


def file_headers(file_name, header):
    """
    Функция открывает и дозаписывает в файл заголовки

    :param file_name: месторасположение и название файла
    :param header: заголовок для дозаписи
    """
    with open(file_name, 'a') as file:
        file.write(header + '\n')
        file.close()


def write_csv_table_in_file(matrix, file_name):
    """
    Функция формирует таблицу из матрицы и дозаписывает её в файл

    :param matrix: квадратичная матрица
    :param file_name: месторасположение и название файла
    """
    df = pandas.DataFrame(matrix)
    df.to_csv(file_name, sep=',', index=False, mode='a')


def prometheus_api_path(type='query_range'):
    """
    Функция формирует полный api path для запроса к prometheus

    :param type: тип prometheus запроса
    :return: полный api path
    """
    full_url = prometheus_api_url + type
    return full_url


def get_prometheus_apirequest(params):
    """
    Функция отправляет GET api запрос в prometheus с параметрами

    :param params: параметры запроса
    :return: api response на запрос к prometheus
    """
    try:
        result = requests.get(prometheus_api_path(), params=params)
        logger.debug('Response: {}'.format(result.text))
    except requests.exceptions.ConnectionError:
        error = '{} is not callable!'.format(prometheus_api_url)
        logger.error(error)
        return False
    result_json = json.loads(result.text)
    if result.status_code != 200:
        error = 'Status code {} is not expected! Error: {}'.format(result.status_code, result_json['error'])
        logger.error(error)
        return False
    else:
        if result_json['data']['result']:
            return result_json
        else:
            error = 'No data to analyze, please, correct the request!'
            logger.error(error)
            return False
