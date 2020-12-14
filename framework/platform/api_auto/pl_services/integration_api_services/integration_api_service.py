#!/usr/bin/env python
# -*- coding: utf-8 -*-
from framework.api_libs.user_client import ExternalApiUserClient


class IntegrationApiCore(ExternalApiUserClient):
    """"""

    def __init__(self, **kwargs):
        self.integr_api_prefix = '/api/v1'
        super().__init__(**kwargs)

    def integr_api_check_async_id(self, async_id, allowed_codes=[200], retry_attempts=0, retry_delay=1,
                                  need_auto_auth=True, need_response=True):
        """"""
        url = self.auth_url + self.integr_api_prefix + f'/apiRequests/{async_id}'
        response = self.get(url=url, allowed_codes=allowed_codes, retry_attempts=retry_attempts,
                            retry_delay=retry_delay, need_auto_auth=need_auto_auth)
        if need_response:
            return response.json()

    def post_inbox_integr_api(self, data, allowed_codes=[200], retry_attempts=0, retry_delay=1, need_auto_auth=True,
                              need_response=True):
        """"""
        url = self.auth_url + self.integr_api_prefix + '/inbox'
        response = self.post(url=url, json=data, allowed_codes=allowed_codes, retry_attempts=retry_attempts,
                             retry_delay=retry_delay, need_auto_auth=need_auto_auth)
        if need_response:
            return response.json()
