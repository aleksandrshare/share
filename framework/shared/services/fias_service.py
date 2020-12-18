#!/usr/bin/env python
# -*- coding: utf-8 -*-
from framework.api_libs.user_client import AutoCheckUserClient


class FiasCore(AutoCheckUserClient):
    """Класс набора функций для работы с сервисом PT SP Fias"""

    fias_prefix = 'handler'

    def get_address_data_by_oktmo(self, oktmo, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """
        Получение данных об адресе, соответсвующем заданному ОКТМО

        :param oktmo: код ОКТМО (строка)
        :param allowed_codes: список стаус-кодов, корректных для выполняемого http-запроса
        :param retry_attempts: кол-во попыток для выполнения http-запроса
        :param retry_delay: ожидание в секундах перед выполнением http-запроса
        :return: json ответа на http-запрос
        """
        url = self.auth_url + self.fias_prefix + f'/oktmo/{oktmo}'
        with self.session():
            data = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def get_fias_item_values_by_parent_id(self, parent_id, fias_item, allowed_codes=[200],
                                          retry_attempts=0, retry_delay=1):
        """
        Получение данных объектов ФИАС, соответсвующих заданному GUID родительского объекта ФИАС

        :param parent_id: GUID родительского объекта ФИАС
        :param fias_item: тип объекта адреса (districts, cities, cityDistricts, locatities, streets)
        :param allowed_codes: список стаус-кодов, корректных для выполняемого http-запроса
        :param retry_attempts: кол-во попыток для выполнения http-запроса
        :param retry_delay: ожидание в секундах перед выполнением http-запроса
        :return: json ответа на http-запрос
        """
        url = self.auth_url + self.fias_prefix + f'/{parent_id}/{fias_item}'
        with self.session():
            data = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def get_locations_values_by_subject_of_federation(self, subj_of_fed, allowed_codes=[200],
                                                      retry_attempts=0, retry_delay=1):
        """
        Полученик списка городов или населенных пунктов, соответсвующих субъекту федерации

        :param subj_of_fed: id субъекта федерации
        :param allowed_codes: список стаус-кодов, корректных для выполняемого http-запроса
        :param retry_attempts: кол-во попыток для выполнения http-запроса
        :param retry_delay: ожидание в секундах перед выполнением http-запроса
        :return: json ответа на http-запрос
        """
        url = self.auth_url + self.fias_prefix + f'/subjectsOfFederation/{subj_of_fed}/locations'
        with self.session():
            data = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()
