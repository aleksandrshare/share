#!/usr/bin/env python
# -*- coding: utf-8 -*-
from framework.platform.api_auto.pl_services.int_api_services import ApiServices
import pytest
from random import choice
import allure


class RequestsActions(ApiServices):
    """"""

    def req_get_random_request(self):
        """"""
        resp = self.get_requests()
        if not resp.get('items'):
            pytest.skip('Нет запросов в системе, пропускаем тест')
        else:
            req_id = choice(resp['items'])['id']
        self.log.info(f'Выбран запрос с id={req_id}')
        allure.attach(self.LKO_URL + f"/requests/view/{req_id}", 'Ссылка на запрос в UI',
                      allure.attachment_type.URI_LIST)
        return req_id
