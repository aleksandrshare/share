#!/usr/bin/env python
# -*- coding: utf-8 -*-
from framework.platform.api_auto.pl_services.int_api_services import ApiServices
from framework.api_libs.user_client import ApiException
import allure
from json import dumps


class RelationsActions(ApiServices):

    def ra_create_relation(self, source_type, source_id, target_type, target_id, relation):
        """"""
        reference = {
            "sourceType": source_type,
            "sourceId": source_id,
            "targetType": target_type,
            "targetId": target_id,
            "relation": relation
        }
        resp = self.create_relation(reference)
        return resp['id']

    def ra_check_relation_exists(self, source_type, source_id, target_type, target_id, relation):
        """"""
        try:
            resp = self.get_relations_details(source_id=source_id, source_type=source_type, target_id=target_id,
                                              target_type=target_type, relation=relation)
            allure.attach(dumps(resp, indent=2, ensure_ascii=False), 'Ответ на get-запрос наличия связи',
                          allure.attachment_type.JSON)
            relation_id = resp['id']
        except ApiException:
            relation_id = None
        assert relation_id, f'Связь с типом {relation} между {source_type} {source_id} и {target_type} {target_id} ' \
                            f'не найдена'

    def ra_check_relation_detailed_contains_needed_relation(self, source_type, source_id, target_type, target_id,
                                                            relation):
        """"""
        resp = self.get_relations_detailed(source_type, source_id)
        allure.attach(dumps(resp, indent=2, ensure_ascii=False),
                      f'Ответ на get-запрос связей для {source_type} {source_id}', allure.attachment_type.JSON)
        is_found = False
        for item in resp['items']:
            if item['relationType'] == relation and item['objectType'] == target_type and item['object']['id'] == target_id:
                is_found = True
                self.log.info(f'Найдена сущность {target_type} {target_id} с типом связи {relation} в списке связей '
                              f'сущности {source_type} {source_id}')
                break
        assert is_found, f'Не найдена сущность {target_type} {target_id} с типом связи {relation} в списке связей ' \
                         f'сущности {source_type} {source_id}'
