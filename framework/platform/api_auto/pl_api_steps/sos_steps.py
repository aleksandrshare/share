#!/usr/bin/env python
# -*- coding: utf-8 -*-
import allure
from datetime import datetime
from framework.platform.api_auto.pl_services.int_api_services import ApiServices
from json import dumps, loads
from random import choice
from tools.utils import add_key_to_json
from jsondiff import diff


class SosActions(ApiServices):
    """"""

    def sa_get_operator(self, specific_operator=None):
        users_list = self.get_lko_active_users_list()
        if specific_operator:
            for user in users_list:
                if user['login'] == specific_operator:
                    return user
        else:
            user = choice(users_list)
            self.log.info(f'Выбран оператор {user}')
            return user

    def sa_get_root_group_info(self):
        """"""
        result = self.pl_get_groups_tree()
        if result:
            if result[0].get('children'):
                del result[0]['children']
            return result[0]
        else:
            raise Exception('Error! Not found root group info')

    # Словарь для корректного отображения данных в allure-отчете
    entity_rus = {
        'subject': 'Субъект',
        'object': 'Объект',
        'system': 'Система'
    }

    def sa_post_new_sos_entity(self, entity_type, entity_json):
        """"""
        result = self.pl_create_sos_entity(entity_type, entity_json)
        allure.attach(self.LKO_URL + f'/{entity_type}s/list?{entity_type}Id={result["id"]}',
                      f'{self.entity_rus[entity_type]}: ссылка в UI', allure.attachment_type.URI_LIST)
        return result['id']

    def sa_get_random_sos_entity_data(self, entity_type, need_active=False):
        """"""
        result = self.pl_get_sos_entities(entity_type)
        if result:
            if need_active:
                act_entity = [item for item in result if item.get('isActive')]
                if act_entity:
                    random_entity = choice(act_entity)
                else:
                    return False
            else:
                random_entity = choice(result)
            allure.attach(dumps(random_entity, indent=2, ensure_ascii=False),
                          f'{self.entity_rus[entity_type]}: данные случайно выбранной сущности',
                          allure.attachment_type.JSON)
            return random_entity
        else:
            return False

    def sa_get_sos_entity_data_by_id(self, entity_type, entity_id):
        """"""
        result = self.pl_get_sos_entity_info(entity_type, entity_id)
        allure.attach(dumps(result, indent=2, ensure_ascii=False),
                      f'{self.entity_rus[entity_type]}: данные выбранной сущности',
                      allure.attachment_type.JSON)
        return result

    def sa_put_edit_in_sos_entity(self, entity_type, entity_id, edit_json):
        """"""
        result = self.pl_put_edit_sos_entity(entity_type, entity_id, edit_json)
        allure.attach(self.LKO_URL + f'/{entity_type}s/list?{entity_type}Id={result["id"]}',
                      f'{self.entity_rus[entity_type]}: ссылка в UI для просмотра изменений',
                      allure.attachment_type.URI_LIST)
        return result['id']

    def sa_cmp_api_and_sent_subject_data(self, subj_id, sent_data, api_data=None):
        """"""
        if not api_data:
            api_data = self.sa_get_sos_entity_data_by_id(entity_type='subject', entity_id=subj_id)

        api_data = add_key_to_json(api_data, ['$.confidentialOfficeAddress.id', '$.legalAddress.id',
                                              '$.licenses..id', '$.licenses..updateInfo', '$.id'])
        sent_data = add_key_to_json(sent_data, ['$.confidentialOfficeAddress.id', '$.legalAddress.id',
                                                '$.licenses..id', '$.licenses..updateInfo', '$.id'])
        for lic_item in api_data['licenses']:
            lic_item['registrationDate'] = datetime.strftime(datetime.strptime(
                lic_item['registrationDate'], '%Y-%m-%dT%H:%M:%S.%fZ'), '%Y-%m-%dT%H:%M:%S.%fZ')
            lic_item['validThru'] = datetime.strftime(datetime.strptime(
                lic_item['validThru'], '%Y-%m-%dT%H:%M:%S.%fZ'), '%Y-%m-%dT%H:%M:%S.%fZ')
        diff_dicts = loads(diff(sent_data, api_data, dump=True))
        if diff_dicts:
            allure.attach(dumps(diff_dicts, indent=2, ensure_ascii=False),
                          'Разница между отправленными и скачанными данными',
                          allure.attachment_type.JSON)
        assert not diff_dicts, 'Ошибка! Полученные по API данные субъекта отличаются от отправленных'

    def sa_cmp_api_and_sent_object_data(self, obj_id, sent_data, api_data=None):
        """"""
        if not api_data:
            api_data = self.sa_get_sos_entity_data_by_id(entity_type='object', entity_id=obj_id)

        api_data = add_key_to_json(api_data, ['$.id', '$..agreements.*.id', '$..agreements.*.services.*.id',
                                              '$..agreements.*.services.*.resources.*.id', '$..updateInfo',
                                              '$.legalAddress.id', '$.physicalAddress.id', '$.postAddress.id'])
        sent_data = add_key_to_json(sent_data, ['$.id', '$..agreements.*.id', '$..agreements.*.services.*.id',
                                                '$..agreements.*.services.*.resources.*.id', '$..updateInfo',
                                                '$.legalAddress.id', '$.physicalAddress.id', '$.postAddress.id'])
        for agree_item in api_data['agreements']:
            agree_item['connectionDate'] = datetime.strftime(datetime.strptime(
                agree_item['connectionDate'], '%Y-%m-%dT%H:%M:%S.%fZ'), '%Y-%m-%dT%H:%M:%S.%fZ')
            agree_item['startDate'] = datetime.strftime(datetime.strptime(
                agree_item['startDate'], '%Y-%m-%dT%H:%M:%S.%fZ'), '%Y-%m-%dT%H:%M:%S.%fZ')
            agree_item['endDate'] = datetime.strftime(datetime.strptime(
                agree_item['endDate'], '%Y-%m-%dT%H:%M:%S.%fZ'), '%Y-%m-%dT%H:%M:%S.%fZ')
        diff_dicts = loads(diff(sent_data, api_data, dump=True))
        if diff_dicts:
            allure.attach(dumps(diff_dicts, indent=2, ensure_ascii=False),
                          'Разница между отправленными и скачанными данными',
                          allure.attachment_type.JSON)
        assert not diff_dicts, 'Ошибка! Полученные по API данные объекта отличаются от отправленных'

    def sa_cmp_api_and_sent_system_data(self, sys_id, sent_data, api_data=None):
        """"""
        if not api_data:
            api_data = self.sa_get_sos_entity_data_by_id(entity_type='system', entity_id=sys_id)
        api_data = add_key_to_json(api_data, ['$.id', '$..classifications..id', '$..resources..id'])
        sent_data = add_key_to_json(sent_data, ['$.id', '$..classifications..id', '$..resources..id'])
        diff_dicts = loads(diff(sent_data, api_data, dump=True))
        if diff_dicts:
            allure.attach(dumps(diff_dicts, indent=2, ensure_ascii=False),
                          'Разница между отправленными и скачанными данными',
                          allure.attachment_type.JSON)
        assert not diff_dicts, 'Ошибка! Полученные по API данные объекта отличаются от отправленных'

    def sa_edit_activation_sos_entity(self, entity_type, entity_data, need_activate=True):
        """"""
        if need_activate:
            result = self.pl_activate_sos_entity(entity_type, entity_data['id'], entity_data)
        else:
            result = self.pl_deactivate_sos_entity(entity_type, entity_data['id'], entity_data)
        allure.attach(self.LKO_URL + f'/{entity_type}s/list?{entity_type}Id={result["id"]}',
                      f'{self.entity_rus[entity_type]}: ссылка в UI для просмотра изменений',
                      allure.attachment_type.URI_LIST)
        return result['id']
