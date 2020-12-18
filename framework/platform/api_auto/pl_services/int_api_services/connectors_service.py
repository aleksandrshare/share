#!/usr/bin/env python
# -*- coding: utf-8 -*-

from framework.api_libs.user_client import AutoCheckUserClient


class ConnectorsCore(AutoCheckUserClient):
    """"""

    connectors_prefix = 'handler'

    def get_connectors(self, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.connectors_prefix
        with self.session():
            response = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                                retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()

    def get_connector_by_namespace(self, namespace, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.connectors_prefix + f'/{namespace}'
        with self.session():
            response = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                                retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()

    def enable_all_connector_parts_by_namespace(self, namespace, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.connectors_prefix + f'/{namespace}/enable'
        with self.session():
            response = self.post(url=url, verify=False, allowed_codes=allowed_codes,
                                 retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.text

    def disable_all_connector_parts_by_namespace(self, namespace, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.connectors_prefix + f'/{namespace}/disable'
        with self.session():
            response = self.post(url=url, verify=False, allowed_codes=allowed_codes,
                                 retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.text

    def restart_all_connector_parts_by_namespace(self, namespace, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""

        url = self.auth_url + self.connectors_prefix + f'/{namespace}/restart'
        with self.session():
            response = self.post(url=url, verify=False, allowed_codes=allowed_codes,
                                 retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.text

    def get_connector_info_for_identifier_in_namespace(self, namespace, identifier, allowed_codes=[200],
                                                       retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.connectors_prefix + f'/{namespace}/{identifier}'
        with self.session():
            response = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                                retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()

    def disable_connector_identifier_in_namespace(self, namespace, identifier, allowed_codes=[200],
                                                  retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.connectors_prefix + f'/{namespace}/{identifier}/disable'
        with self.session():
            response = self.post(url=url, verify=False, allowed_codes=allowed_codes,
                                 retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.text

    def enable_connector_identifier_in_namespace(self, namespace, identifier, allowed_codes=[200],
                                                  retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.connectors_prefix + f'/{namespace}/{identifier}/enable'
        with self.session():
            response = self.post(url=url, verify=False, allowed_codes=allowed_codes,
                                 retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.text

    def reset_connector_identifier_in_namespace(self, namespace, identifier, allowed_codes=[200],
                                                  retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.connectors_prefix + f'/{namespace}/{identifier}/reset'
        with self.session():
            response = self.post(url=url, verify=False, allowed_codes=allowed_codes,
                                 retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.text

    def get_connector_status_for_identifier_in_namespace(self, namespace, identifier, allowed_codes=[200],
                                                         retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.connectors_prefix + f'/{namespace}/{identifier}/status'
        with self.session():
            response = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                                retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()

    def restart_connector_identifier_in_namespace(self, namespace, identifier, allowed_codes=[200],
                                                  retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.connectors_prefix + f'/{namespace}/{identifier}/restart'
        with self.session():
            response = self.post(url=url, verify=False, allowed_codes=allowed_codes,
                                 retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.text
