#!/usr/bin/env python
# -*- coding: utf-8 -*-
import allure
import backoff
import pytest
from configs.modify_data import test_modify_data
from framework.platform.api_auto.pl_services.integration_api_services import IntegrApiServices
from json import dumps
from jsonpath import jsonpath
from random import choice
from time import sleep
from framework.api_libs.user_client import ApiException
from tools.utils import read_file_for_attach_upload
from tools.concept_wws_iwc import universal_comparison_function_for_post_keys


class IntegrationApiActions(IntegrApiServices):

    def integr_api_upload_file(self, file_path=None):
        """"""
        file_name, file_obj, file_size = read_file_for_attach_upload(file_path)
        response = self.upload_attachment(file_name, file_obj, file_size)
        if not test_modify_data.get('integr_api_attach_id'):
            test_modify_data['integr_api_attach_id'] = []
        test_modify_data['integr_api_attach_id'].append(response.get('id'))

    def integr_api_send_inbox(self, integr_api_inbox_data=None, source='isim', raw_type='incident'):
        """"""
        test_modify_data['integr_api_inbox_data'] = self.generator.give_json_and_change(
            handler=self.integr_api_prefix + '/inbox', rawData=integr_api_inbox_data,
            source=source, rawType=raw_type)
        result = self.post_inbox_integr_api(test_modify_data['integr_api_inbox_data'])
        test_modify_data['integr_api_async_id'] = result['id']

    @backoff.on_exception(backoff.expo, ApiException, max_time=30)
    def integr_api_check_sent_entity(self, async_id=None, expected_status='success'):
        """"""
        if not async_id:
            result = self.integr_api_check_async_id(test_modify_data['integr_api_async_id'])
        else:
            result = self.integr_api_check_async_id(async_id)
        allure.attach(dumps(result, indent=2, ensure_ascii=False), 'Ответ на запрос', allure.attachment_type.JSON)
        assert result['status'] == expected_status, \
            "Error! Expected request status: {}, got status {}.".format(expected_status, result['status'])
        return result

    def integr_api_check_sent_incident(self, async_id=None, expected_status='success', id_field='id'):
        """"""
        result = self.integr_api_check_sent_entity(async_id, expected_status)
        if result['status'] == 'success':
            if id_field:
                test_modify_data['integr_api_entity_id'] = result['data'][id_field]
                allure.attach(self.LKO_URL + f'/v2/incidents/view/{test_modify_data["integr_api_entity_id"]}',
                              'Ссылка на инцидент в UI', allure.attachment_type.URI_LIST)
        return result

    def integr_api_check_entity_created_in_db(self):
        """"""
        result = self.db_client.find_integr_api_rec_in_db(test_modify_data['integr_api_async_id'])
        assert result, f"Сущность с async_id='{test_modify_data['integr_api_async_id']}' не найдена в БД"

    def integr_api_form_incident(self):
        """"""
        inc_json = self.generator.give_json(self.incidents_prefix)
        return inc_json

    def integr_api_send_incident(self, incident_json=None):
        """"""
        if not incident_json:
            incident_json = self.integr_api_form_incident()
        result, _ = self.create_incident(incident_json)
        test_modify_data['integr_api_async_id'] = result['id']

    def integr_api_edit_incident(self, edit_inc_id, if_match=None, if_unmodified_since=None):
        """"""
        if not if_match:
            inc_data = self.integr_api_get_incident_data_by_id(edit_inc_id)
            if_match = inc_data['versionInfo']['etag']
        edit_incident_json = self.integr_api_form_incident()
        del edit_incident_json['source']
        edit_incident_json['id'] = edit_inc_id
        req_header = {
            'If-Match': if_match if isinstance(if_match, str) else str(if_match)
        }
        if if_unmodified_since:
            req_header['If-Unmodified-Since'] = if_unmodified_since
        result = self.edit_incident_info(incident_id=edit_inc_id, edit_data=edit_incident_json,
                                         header=req_header)
        test_modify_data['integr_api_async_id'] = result['id']
        return edit_incident_json

    def integr_api_get_incident_data_by_id(self, inc_id):
        """"""
        resp = self.get_incident_info(inc_id)
        allure.attach(dumps(resp, indent=2, ensure_ascii=False), f'Данные инцидента с id="{inc_id}"',
                      allure.attachment_type.JSON)
        return resp

    def integr_api_get_several_incidents_data_by_ids(self, ids_list):
        """"""
        if isinstance(ids_list, str):
            ids_list = [ids_list]
        ids_list = {'ids': ids_list}
        resp = self.get_several_incidents_info(ids_list)
        assert len(resp['items']) == len(ids_list['ids']), f"Ошибка! Получены данные {len(resp['items'])} " \
                                                           f"инцидентов вместо {len(ids_list['ids'])}"
        return resp

    def integr_api_change_status_incident(self, inc_id, status, if_match=None, if_unmodified_since=None):
        """"""
        if not if_match:
            inc_data = self.integr_api_get_incident_data_by_id(inc_id)
            if_match = inc_data['versionInfo']['etag']

        req_header = {
            'If-Match': if_match if isinstance(if_match, str) else str(if_match)
        }
        if if_unmodified_since:
            req_header['If-Unmodified-Since'] = if_unmodified_since
        allure.attach(dumps(req_header, indent=2, ensure_ascii=False), 'header POST-запроса',
                      allure.attachment_type.JSON)
        result = self.change_incident_status(json_data={'status': status}, inc_id=inc_id, header=req_header)
        test_modify_data['integr_api_async_id'] = result['id']

    @backoff.on_exception(backoff.expo, AssertionError, max_time=15)
    def integr_api_check_incident_data(self, inc_id, inc_field, expected_value):
        """"""
        inc_data = self.integr_api_get_incident_data_by_id(inc_id)
        assert inc_data.get(inc_field) == expected_value, f"Ошибка! Для инцидента '{inc_id}' в поле '{inc_field}' " \
                                                          f"ожидаемое значение '{expected_value}', " \
                                                          f"фактическое '{inc_data.get(inc_field)}'"

    def integr_api_check_async_id_error_type(self, error_json, error_path, error_text):
        """"""
        error_found = False
        err_values = jsonpath(error_json, error_path)
        for item in err_values:
            if item == error_text or error_text in item:
                error_found = True
                self.log.info(f"Ошибка в результате запроса по async_id в поле {error_path} найдена: '{item}'")
                break
        assert error_found, f'В результате запроса по async_id нет ожидаемой ошибки для в поле {error_path}' \
                            f'\nПолученный ответ: {err_values}'

    @backoff.on_exception(backoff.expo, AssertionError, max_time=15)
    def integr_api_check_incident_edit(self, inc_id, sent_edit_data):
        """"""
        if sent_edit_data.get('id'):
            del sent_edit_data['id']
        new_inc_data = self.integr_api_get_incident_data_by_id(inc_id)
        assert_dict = universal_comparison_function_for_post_keys(sent_edit_data, new_inc_data,
                                                                  for_skip=['updateDate'], need_assert=False)
        assert not assert_dict, f"Ошибка! Не все поля инцидента '{inc_id}' отредактированы: {assert_dict}"

    def integr_api_get_all_incidents_data(self, offset=0):
        """"""
        resp = self.get_list_incidents(offset)
        allure.attach(dumps(resp, indent=2, ensure_ascii=False), 'Данные всех инцидентов в системе',
                      allure.attachment_type.JSON)
        assert resp['items'], 'Ошибка! В системе отсутствуют инциденты'
        return resp

    def integr_api_check_several_icidents_info(self, incident_ids, incidents_data):
        """"""
        for incident_id in incident_ids:
            inc_data = self.integr_api_get_incident_data_by_id(incident_id)
            inc_data_from_list = [data for data in incidents_data['items'] if data['id'] == incident_id]
            if inc_data_from_list:
                assert_dict = universal_comparison_function_for_post_keys(sent=inc_data_from_list[0], incoming=inc_data,
                                                                          for_skip=['updateDate', 'versionInfo'])
                assert not assert_dict, f'Ошибка! Не совпадают данные инцидентов "{incident_id}":\n{assert_dict}'
            else:
                pytest.fail(f'Ошибка! В перечне данных инцидентов отсутствует инцидент с id="{incident_id}"')

    def integr_api_get_filtered_incidents_data(self, filter_data):
        """"""
        resp = self.get_incidents_by_filter(filter_data)
        allure.attach(dumps(resp, indent=2, ensure_ascii=False), f'Данные инцидентов в соответствии '
                                                                 f'с фильтром "{filter_data}"',
                      allure.attachment_type.JSON)
        assert resp['items'], f'Ошибка! В системе отсутствуют инциденты подходящие под фильтр: "{filter_data}"'
        return resp

    def integr_api_check_sent_alert(self, async_id=None, expected_status='success', id_field='id'):
        """"""
        result = self.integr_api_check_sent_entity(async_id, expected_status)
        if result['status'] == 'success':
            if id_field:
                test_modify_data['integr_api_entity_id'] = result['data'][id_field]
                allure.attach(self.LKO_URL + f'/v2/alerts/view/{test_modify_data["integr_api_entity_id"]}',
                              'Ссылка на алерт в UI', allure.attachment_type.URI_LIST)
        return result
