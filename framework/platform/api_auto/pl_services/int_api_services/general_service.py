from framework.api_libs.user_client import AutoCheckUserClient
from configs.service_ports import ports
from tools.utils import extract_domain_from_url


class ConfigurationFilesCore(AutoCheckUserClient):
    """"""
    prefix = 'handler'

    def upload_configuration_files(self, file_data, entity_type, allowed_codes=[200], retry_attempts=5, retry_delay=1):
        """"""
        domain = extract_domain_from_url(self.auth_url)
        if entity_type == 'incident':
            port = ports.get('Incidents')
        elif entity_type == 'ticket':
            port = ports.get('Tickets')
        else:
            assert False, 'Unsupported entity type "{}" for uploading configuration files!'
        url = 'http://' + domain + f':{port}' + self.prefix
        headers = {
            'Authorization': "access_default_token"
        }
        self.post(url=url, files=file_data, verify=False, allowed_codes=allowed_codes,
                  retry_attempts=retry_attempts, retry_delay=retry_delay, headers=headers)