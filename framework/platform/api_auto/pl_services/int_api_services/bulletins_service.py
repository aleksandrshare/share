# coding=utf-8
from framework.api_libs.user_client import AutoCheckUserClient


class BulletinsCore(AutoCheckUserClient):
    """"""

    bulletins_prefix = '/api/bulletins'

    def create_publication(self, pub_data, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.bulletins_prefix
        with self.session():
            data = self.post(url=url, json=pub_data, verify=False, allowed_codes=allowed_codes,
                             retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def get_all_bulletins(self, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.bulletins_prefix
        with self.session():
            result = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                              retry_attempts=retry_attempts, retry_delay=retry_delay)
        return result.json()

    def get_bulletin_by_id(self, bulletin_id, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.bulletins_prefix + f'/{bulletin_id}'
        with self.session():
            result = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                              retry_attempts=retry_attempts, retry_delay=retry_delay)
        return result.json()
