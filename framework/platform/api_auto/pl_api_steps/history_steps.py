#!/usr/bin/env python
# -*- coding: utf-8 -*-
from framework.platform.api_auto.pl_services.int_api_services import ApiServices
import allure
from json import dumps


class HistoryActions(ApiServices):

    def ha_check_history_contains_record(self, entity_type, entity_id, expected_record):
        """"""
        history = self.get_entity_history(entity_type, entity_id)
        allure.attach(dumps(history, indent=2, ensure_ascii=False),
                      f'Ответ на get-запрос истории для {entity_type} {entity_id}', allure.attachment_type.JSON)
        assert history.get('data'), f'Нет записей в истории для {entity_type} {entity_id}'
        is_found = False
        for event in history['data']:
            if expected_record in event['message']:
                is_found = True
                self.log.info(f'Найдена запись {event["message"]}, соответствующая ожидаемой {expected_record}')
                break
        assert is_found, f'Не найдена запись в истории {entity_type} {entity_id}, соответствующая ожидаемой ' \
                         f'{expected_record}'
