# coding=utf-8
from tools.api_client.user_client import AutoCheckUserClient
import yaml

class ConfigurationCore(AutoCheckUserClient):
    """Класс набора функций для работы с сервисом PT SP ConfigurationService"""

    configuration_prefix = 'handler'

    def cc_download_config_file(self, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        url = self.auth_url + self.configuration_prefix + '/files'
        with self.session():
            data = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.content

    def remove_config_draft(self, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        url = self.auth_url + self.configuration_prefix + '/drafts/current/clear'
        with self.session():
            self.post(url=url, json={}, verify=False, allowed_codes=allowed_codes,
                      retry_attempts=retry_attempts, retry_delay=retry_delay)

    def cc_upload_config(self, attach_id, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        url = self.auth_url + self.configuration_prefix + '/drafts/current/attachments'
        body = [attach_id]
        with self.session():
            data = self.put(url=url, json=body, verify=False, allowed_codes=allowed_codes,
                                  retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def apply_config_draft(self, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        url = self.auth_url + self.configuration_prefix + '/drafts/current/apply'
        with self.session():
            self.post(url=url, json={}, verify=False, allowed_codes=allowed_codes,
                      retry_attempts=retry_attempts, retry_delay=retry_delay)

    def check_config_draft(self, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        url = self.auth_url + self.configuration_prefix + '/drafts/current'
        with self.session():
            data = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def get_single_config_file_data(self, asset_type, full_name, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """
        Метод отправки запроса на получение data файла из актуальной конфигурации

        :param asset_type: название файла до первой точки
        :param full_name: полное название файла
        :param allowed_codes: допустимые коды ответа
        :param retry_attempts: кол-во попыток отправки
        :param retry_delay: перерыв между отправкой в секундах
        :return: data файла в формате yaml
        """
        url = self.auth_url + self.configuration_prefix + '/{}/download/{}'.format(asset_type, full_name)
        with self.session():
            data = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay)
        return yaml.load(data.text)
