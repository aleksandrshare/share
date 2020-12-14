#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tools.api_client.user_client import AutoCheckUserClient


class CustomDictionariesCore(AutoCheckUserClient):
    """Класс набора функций для работы с кастомными словарями """

    custom_dictionaries_prefix = '/api/dictionaries/v2/enums'

    def get_custom_reference_values(self, reference_id):
        url = self.auth_url + self.custom_dictionaries_prefix + '/{}'.format(reference_id)
        with self.session():
            data = self.get(url=url, verify=False)
        return data.json()
