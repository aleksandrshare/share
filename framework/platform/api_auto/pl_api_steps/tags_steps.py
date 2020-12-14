#!/usr/bin/env python
# -*- coding: utf-8 -*-
from framework.platform.api_auto.pl_services.int_api_services import ApiServices
from tools.utils import now_timestamp


class TagsActions(ApiServices):
    """"""

    def tag_add_tags_to_entity(self, entity_type, entity_id, tags_list=None):
        """"""
        if not tags_list:
            tags_list = [f'Метка {now_timestamp()}']
        self.post_entity_tag(entity_type, entity_id, tags_list)
        return tags_list

    def tag_check_entity_contains_tag(self, entity_type, entity_id, tags_list):
        """"""
        entity_tags = self.get_entity_tags(entity_type, entity_id)
        not_found_tags = list()
        for tag in tags_list:
            if tag not in entity_tags:
                not_found_tags.append(tag)
        assert not not_found_tags, f'Список отсутствующих меток: {not_found_tags}'

    def tag_create_search_payload(self, tags, entity_type="", limit=100, offset=0):
        """"""
        payload = {
            'tags': tags,
            'objectType': entity_type,
            'limit': limit,
            'offset': offset
        }
        return payload

    def tag_check_search_tag_method(self, entity_id, tags, entity_type="", limit=100, offset=0):
        """"""
        body = self.tag_create_search_payload(tags, entity_type, limit, offset)
        resp = self.search_tags(body)
        is_found = False
        for item in resp.get('items'):
            if item['objectId'] == entity_id:
                is_found = True
                break
        assert is_found, f'Не найдена сущность с id {entity_id} при поиске по меткам {tags}'

