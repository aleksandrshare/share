from tools.api_client.user_client import AutoCheckUserClient


class ReferencesCore(AutoCheckUserClient):
    """"""
    references_prefix = '/api/relations'

    def get_relations(self, object_type, object_id, relation_type=None, limit=None, offset=None,
                      allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.references_prefix + f'?objectType={object_type}&objectId={object_id}'
        if relation_type:
            url += f'&relation={relation_type}'
        if limit:
            url += f'&limit={limit}'
        if offset:
            url += f'&offset={offset}'
        with self.session():
            response = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                                retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()

    def create_relation(self, reference, allowed_codes=[201], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.references_prefix
        with self.session():
            response = self.post(url=url, json=reference, verify=False, allowed_codes=allowed_codes,
                                 retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()

    def create_several_relations(self, references, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.references_prefix + '/bulk/create'

        with self.session():
            response = self.post(url=url, json=references, verify=False, allowed_codes=allowed_codes,
                                 retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()

    def delete_relation(self, relation_id, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.references_prefix + f'/{relation_id}'
        with self.session():
            response = self.delete(url=url, verify=False, allowed_codes=allowed_codes,
                                   retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response

    def get_relations_details(self, source_id, source_type, target_id, target_type, relation,
                              allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.references_prefix + f'/details?sourceType={source_type}&sourceId={source_id}' \
                                                       f'&targetType={target_type}&targetId={target_id}' \
                                                       f'&relation={relation}'
        with self.session():
            response = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                                retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()

    def get_relations_detailed(self, source_type, source_id,
                               allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.references_prefix + f'/detailed/{source_type}/{source_id}'
        with self.session():
            response = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                                retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()


class TagsCore(AutoCheckUserClient):
    """"""
    tags_prefix = '/api/tags'

    def get_tags(self, search_query=None, limit=None, offset=None,
                 allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.tags_prefix + '?'
        if search_query:
            url += f'&searchQuery={search_query}'
        if limit:
            url += f'&limit={limit}'
        if offset:
            url += f'&offset={offset}'
        with self.session():
            response = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                                retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()

    def post_new_tag(self, tag, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.tags_prefix
        with self.session():
            response = self.post(url=url, json=tag, verify=False, allowed_codes=allowed_codes,
                                retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()

    def delete_tag(self, tag, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.tags_prefix
        with self.session():
            response = self.delete(url=url, json=tag, verify=False, allowed_codes=allowed_codes,
                                retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()

    def get_entity_tags(self, entity_type, entity_id, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.tags_prefix + f'/list/{entity_type}/{entity_id}'
        with self.session():
            response = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                                retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()

    def post_entity_tag(self, entity_type, entity_id, tags, allowed_codes=[201], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.tags_prefix + f'/list/{entity_type}/{entity_id}'
        with self.session():
            response = self.post(url=url, json=tags, verify=False, allowed_codes=allowed_codes,
                                 retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()

    def search_tags(self, tag, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.tags_prefix + '/search'
        with self.session():
            response = self.post(url=url, json=tag, verify=False, allowed_codes=allowed_codes,
                                 retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()