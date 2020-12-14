#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tools.api_client.user_client import AutoCheckUserClient


class DictionariesCore(AutoCheckUserClient):
    """Класс набора функций для работы со словарями """

    dictionaries_prefix = '/api/dictionaries'

    def get_reference_values(self, reference_id, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """
        Скачивание данных справочника

        :param reference_id: наименование справочника
        :param allowed_codes: список стаус-кодов, корректных для выполняемого http-запроса
        :param retry_attempts: кол-во попыток для выполнения http-запроса
        :param retry_delay: ожидание в секундах перед выполнением http-запроса
        :return: json ответа на http-запрос
        """
        url = self.auth_url + self.dictionaries_prefix + f'?reference_id={reference_id}'
        with self.session():
            data = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def post_reference_values(self, reference_id, reference_data, allowed_codes=[200],
                              retry_attempts=0, retry_delay=1):
        """
        Добавление данных в справочник

        :param reference_id: наименование справочника
        :param reference_data: JSON добавляемого значения
        :param allowed_codes: список стаус-кодов, корректных для выполняемого http-запроса
        :param retry_attempts: кол-во попыток для выполнения http-запроса
        :param retry_delay: ожидание в секундах перед выполнением http-запроса
        :return: json ответа на http-запрос
        """
        url = self.auth_url + self.dictionaries_prefix + f'?reference_id={reference_id}'
        with self.session():
            data = self.post(url=url, json=reference_data, verify=False, allowed_codes=allowed_codes,
                             retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()
