from framework.api_libs.user_client import AutoCheckUserClient


class HistoryCore(AutoCheckUserClient):
    """"""
    history_prefix = 'handler'

    def get_entity_history(self, entity_type, entity_id, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.history_prefix + '/{}'.format(entity_type) + '/{}'.format(entity_id)
        with self.session():
            data = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()