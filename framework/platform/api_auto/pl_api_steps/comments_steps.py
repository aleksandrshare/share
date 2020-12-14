#!/usr/bin/env python
# -*- coding: utf-8 -*-
from framework.platform.api_auto.pl_services.int_api_services import ApiServices
import allure
from json import dumps
from tools.concept_wws_iwc import universal_comparison_function_for_post_keys
import backoff


class CommentsActions(ApiServices):
    """"""

    def ca_add_comment_to_entity(self, entity_type, entity_id):
        """"""
        comment_data = self.generator.give_json('/api/comments/{entityType}/{entityId}')
        resp = self.add_new_comment(entity_type=entity_type, entity_id=entity_id, comment_body=comment_data)
        return resp, comment_data

    @backoff.on_exception(backoff.constant, AssertionError, max_time=10, interval=2)
    def ca_find_comment_data_by_id(self, entity_type, entity_id, comment_id):
        """"""
        resp = self.get_all_comments_for_entity(entity_type, entity_id)
        allure.attach(dumps(resp, indent=2, ensure_ascii=False),
                      f'Ответ на get-запрос комментариев {entity_type} {entity_id}', allure.attachment_type.JSON)
        assert resp.get('comments'), f'У {entity_type} {entity_id} нет комментариев'
        comment_data = None
        for item in resp['comments']:
            if item['id'] == comment_id:
                comment_data = item
                break
        assert comment_data, f'Не найден комментарий с id={comment_id} в комментариях {entity_type} {entity_id}'
        return comment_data

    def ca_check_comment_data(self, entity_type, entity_id, comment_id, send_data, operator_id):
        """"""
        comment_data = self.ca_find_comment_data_by_id(entity_type, entity_id, comment_id)
        asserts = universal_comparison_function_for_post_keys(send_data, comment_data)
        if operator_id != comment_data['creator']['id']:
            asserts.update({'creator.id': {'expected': operator_id, 'actual': comment_data['creator']['id']}})
        assert not asserts, "Не совпадают полученные данные с ожидаемыми: {}".format(str(asserts))
