from framework.api_libs.user_client import AutoCheckUserClient


class CommentCore(AutoCheckUserClient):
    """"""
    comments_prefix = 'handler'

    def get_all_comments_for_entity(self, entity_type, entity_id, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.comments_prefix + f'/{entity_type}/{entity_id}'
        with self.session():
            response = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                                retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()

    def add_new_comment(self, entity_type, entity_id, comment_body,
                        allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.comments_prefix + f'/{entity_type}/{entity_id}'
        with self.session():
            response = self.post(url=url, json=comment_body, verify=False, allowed_codes=allowed_codes,
                                 retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()

    def get_unread_comments_count(self, entity_type, entity_id, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.comments_prefix + f'/{entity_type}/{entity_id}/unread'
        with self.session():
            response = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                                retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()

    def mark_comments_as_read(self, entity_type, entity_id, ids, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.comments_prefix + f'/{entity_type}/{entity_id}/markAsRead'
        with self.session():
            response = self.put(url=url, json=ids, verify=False, allowed_codes=allowed_codes,
                                retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response
