#!/usr/bin/env python
# -*- coding: utf-8 -*-
from framework.platform.api_auto.pl_services.int_api_services import ApiServices
from random import choice, sample
import allure

from tools.concept_wws_iwc import universal_comparison_function_for_post_keys
from tools.utils import now_timestamp, transform_date_to_timestamp, compare_dictionaries
from tools.utils import utc_timestamp, new_source_id
from time import sleep
from json import dumps, loads
import pytest
import backoff
from framework.api_libs.user_client import ApiException
from jsonpath import jsonpath


class AlertsActions(ApiServices):
    """"""
    required_alert_fields = ['id', 'hrid', 'detectedAt', 'source', 'rawData', 'falsePositive', 'type',
                             'sourceId']
    all_alert_fields = ['id', 'hrid', 'detectedAt', 'description', 'source', 'sourceId', 'type', 'responsibleOperator',
                        'falsePositive', 'incident', 'sla', 'rawData', 'sourceId']

    def aa_get_random_alerts(self, alerts_count):
        """"""
        response = self.get_alerts()
        allure.attach(dumps(response, indent=2, ensure_ascii=False), 'Ответ на get-запрос списка алертов',
                      allure.attachment_type.JSON)
        if len(response['items']) < alerts_count:
            pytest.skip('Не достаточно алертов в системе для теста')
        alert_ids = list()
        while len(alert_ids) < alerts_count:
            a_id = choice(response['items'])['id']
            if a_id not in alert_ids:
                alert_ids.append(a_id)
                allure.attach(self.LKO_URL + f"/v2/alerts/view/{a_id}", 'Ссылка на алерт в UI',
                              allure.attachment_type.URI_LIST)
        allure.attach(str(alert_ids), 'IDs выбранных алертов', allure.attachment_type.TEXT)
        return alert_ids

    def aa_get_random_alert_source(self):
        """"""
        resp = self.get_custom_reference_values('alertSource')
        allure.attach(dumps(resp, indent=2, ensure_ascii=False), 'Полученные данные справочника alertSource',
                      allure.attachment_type.JSON)
        assert resp, 'Кастномный словарь alertSources пуст'
        return choice(resp)['id']

    def _create_random_alert_data(self):
        alert_source = self.aa_get_random_alert_source()

        alert_data = {
            "detectedAt": utc_timestamp(date_format='%Y-%m-%dT%H:%M:%S+00:00'),
            "description": "Описание алерта " + now_timestamp(date_format='%Y-%m-%dT%H:%M:%S'),
            "source": alert_source,
            "rawData": {"key": "value"},
            "type": "siemAlertType",
            "sourceId": new_source_id()
        }
        return alert_data

    def aa_create_alert_with_random_fields(self, desire_data=None):
        """"""
        alert_data = self.generator.give_json(self.alerts_prefix)
        if desire_data:
            alert_data.update(desire_data)
        response = self.create_alert(alert_data)
        assert response.get('id'), 'Не удалось получить id созданного алерта'
        self.log.info(f"Создан алерт с id {response.get('id')}")
        allure.attach(self.LKO_URL + f"/v2/alerts/view/{response['id']}", 'Ссылка на алерт в UI',
                      allure.attachment_type.URI_LIST)
        return response['id'], alert_data

    def aa_check_alert_data(self, alert_id, expected_data, etag=1):
        """"""
        resp = self.aa_get_alert_info_with_expected_etag(alert_id, etag)
        allure.attach(dumps(resp, indent=2, ensure_ascii=False), f'Ответ на get-запрос данных алерта {alert_id}',
                      allure.attachment_type.JSON)

        asserts = universal_comparison_function_for_post_keys(expected_data, resp)
        assert not asserts, "Проблемы в jsons после проверки: {}".format(str(asserts))

    def aa_mark_alerts_false_positive_and_check_it(self, alert_ids):
        """"""
        resp, status_code = self.mark_alerts_false_positive(alert_ids={'ids': alert_ids}, force_exclude=True,
                                                            allowed_codes=[200, 202])
        if status_code == 202:
            self.aa_wait_for_saga_running_finished(resp['sagaId'])
        for a_id in alert_ids:
            self.aa_check_alert_false_positive_flag(a_id, True)

    @backoff.on_exception(backoff.expo, AssertionError, max_time=15)
    def aa_check_alert_false_positive_flag(self, alert_id, expected_value):
        """"""
        resp = self.get_alert_info(alert_id)
        allure.attach(dumps(resp, indent=2, ensure_ascii=False), f'Ответ на get-запрос данных  {alert_id}',
                      allure.attachment_type.JSON)
        assert resp.get('falsePositive') is expected_value, \
            f'Значение поля falsePositive: {resp.get("falsePositive")} не совпадает с ожидаемым: {expected_value}'

    @backoff.on_exception(backoff.expo, ApiException, max_time=30)
    def aa_wait_for_saga_running_finished(self, saga_id):
        """"""
        for i in range(60):
            resp = self.get_saga(saga_id)
            self.log.info(f"Сага с id {saga_id} в статусе {resp.get('state')}")
            allure.attach(dumps(resp, indent=2, ensure_ascii=False), f'Ответ на get-запрос саги с id {saga_id}',
                          allure.attachment_type.JSON)
            if resp.get('state') == 'completed':
                return
            else:
                sleep(1)

    def aa_unmark_alerts_false_positive_and_check_it(self, alert_ids):
        """"""

        resp, status_code = self.unmark_alerts_false_positive(alert_ids={'ids': alert_ids}, allowed_codes=[200, 202])
        if status_code == 202:
            self.aa_wait_for_saga_running_finished(resp['sagaId'])
        for a_id in alert_ids:
            self.aa_check_alert_false_positive_flag(a_id, False)

    def aa_get_alerts_info_by_ids_ad_check_it(self, alert_ids):
        """"""
        resp = self.get_alerts_by_id_list(alert_ids)
        assert resp, 'Получен пустой ответ'
        assert resp.get('items'), 'Нет алертов в полученных данных'
        for a_id in alert_ids:
            found = False
            for item in resp.get('items'):
                if item['id'] == a_id:
                    found = True
                    break
            assert found, f"В полученном ответе не найден алерт с id {a_id}"

    def aa_check_required_alert_fields_presence(self, alert_info):
        """"""
        for key in self.required_alert_fields:
            # сравнение с None, так как значение, н-р, falsePositive может быть False
            assert alert_info.get(key) is not None, f'Нет поля {key} в алерте'

    def aa_get_alerts_and_check_it(self):
        """"""
        resp = self.get_alerts()
        allure.attach(dumps(resp, indent=2, ensure_ascii=False), 'Ответ на get-запрос списка алертов',
                      allure.attachment_type.JSON)
        # проверка наличия ключей, проверяю на None, так как items может быть [], а значение в hasMoreItems False
        assert resp.get('items') is not None, 'Нет поля items'
        assert resp.get('hasMoreItems') is not None, 'Нет поля hasMoreItems'
        # проверяем наличие обязательных полей по контракту
        if resp['items']:
            self.aa_check_required_alert_fields_presence(resp['items'][0])
        else:
            self.log.info('В системе нет алертов')

    def aa_get_alert_info_and_check_it(self, alert_id, etag=1):
        """"""
        info = self.aa_get_alert_info_with_expected_etag(alert_id, etag)
        allure.attach(dumps(info, indent=2, ensure_ascii=False), f'Ответ на get-запрос данных алерта {alert_id}',
                      allure.attachment_type.JSON)
        self.aa_check_required_alert_fields_presence(info)
        assert info['id'] == alert_id, 'Получена информация не для указанного id'

    def aa_assign_operator_to_alerts(self, alert_ids, operator_id):
        """"""
        resp, status_code = self.assign_operator_on_alerts(operator_id=operator_id, alert_ids=alert_ids,
                                                           allowed_codes=[200, 202])
        if status_code == 202:
            self.aa_wait_for_saga_running_finished(resp['sagaId'])

    def aa_assign_operator_to_alert(self, alert_id, operator_id):
        """"""
        self.assign_operator_on_alert(operator_id=operator_id, alert_id=alert_id)

    @backoff.on_exception(backoff.constant, (AssertionError, KeyError), max_time=60, interval=2)
    def aa_check_responsible_operator_id(self, alert_id, operator_id):
        """"""
        resp = self.get_alert_info(alert_id)
        allure.attach(dumps(resp, indent=2, ensure_ascii=False), f'Ответ на get-запрос данных алерта {alert_id}',
                      allure.attachment_type.JSON)
        assert resp['responsibleOperator']['id'] == operator_id, 'Не совпадает id назначенного оператора'

    @backoff.on_exception(backoff.expo, AssertionError, max_time=15)
    def aa_check_responsible_operator_absent(self, alert_id):
        """"""
        resp = self.get_alert_info(alert_id)
        allure.attach(dumps(resp, indent=2, ensure_ascii=False), f'Ответ на get-запрос данных алерта {alert_id}',
                      allure.attachment_type.JSON)
        assert resp.get('responsibleOperator') is None, f'У алерта есть назначенный оператор. Полученные данные: {resp}'

    def aa_unassign_operator_to_alerts(self, alert_ids):
        """"""
        resp, status_code = self.assign_operator_on_alerts(operator_id=None, alert_ids=alert_ids,
                                                           allowed_codes=[200, 202])
        if status_code == 202:
            self.aa_wait_for_saga_running_finished(resp['sagaId'])

    def aa_unassign_operator_to_alert(self, alert_id):
        """"""
        self.assign_operator_on_alert(operator_id=None, alert_id=alert_id)

    def aa_add_alerts_to_incident(self, alert_ids, inc_id):
        """"""
        resp, status_code = self.include_alerts_in_incident(inc_id=inc_id, alerts_ids=alert_ids,
                                                            allowed_codes=[200, 202])
        if status_code == 202:
            self.aa_wait_for_saga_running_finished(resp['sagaId'])

    @backoff.on_exception(backoff.expo, AssertionError, max_time=15)
    def aa_check_alert_and_incident_relation(self, alert_id, inc_id):
        """"""
        resp = self.get_alert_info(alert_id)
        allure.attach(dumps(resp, indent=2, ensure_ascii=False), f'Ответ на get-запрос данных алерта {alert_id}',
                      allure.attachment_type.JSON)
        assert resp.get('incident'), 'Нет поля incident в данных алерта'
        assert resp['incident']['id'] == inc_id, f"В алерте с id={alert_id} не совпадает id привязанного инцидента." \
                                                 f"Ожидаемый id: {inc_id}, полученный id{resp['incident']['id']}"

    def aa_exclude_alerts_from_incident(self, alert_ids):
        """"""
        resp, status_code = self.include_alerts_in_incident(inc_id=None, alerts_ids=alert_ids, allowed_codes=[200, 202])
        if status_code == 202:
            self.aa_wait_for_saga_running_finished(resp['sagaId'])

    @backoff.on_exception(backoff.expo, AssertionError, max_time=15)
    def aa_check_alert_not_included_in_incident(self, alert_id):
        """"""
        resp = self.get_alert_info(alert_id)
        allure.attach(dumps(resp, indent=2, ensure_ascii=False), f'Ответ на get-запрос данных алерта {alert_id}',
                      allure.attachment_type.JSON)
        assert resp.get('incident') is None, f'У алерта есть инцидента. Полученные данные: {resp}'

    def aa_create_alerts_if_not_enough(self, alerts_count):
        """"""
        response = self.get_alerts()
        if len(response['items']) < alerts_count:
            for i in range(alerts_count - len(response['items'])):
                self.log.debug('Создаем алерт')
                self.aa_create_alert_with_random_fields()

    @backoff.on_exception(backoff.expo, AssertionError, max_time=15)
    def aa_check_linked_alert_and_incident(self, alert_id, inc_id):
        """"""
        resp = self.get_incidents_for_alerts([alert_id])
        assert len(resp['items']) == 1, f'Получено более одного инцидента для алерта: \n{resp}'
        assert resp['items'][0]['id'] == inc_id, 'Не совпадает id инцидента с ожидаемым'

    def aa_check_alert_added_to_alerts_table_in_db(self, alert_id):
        """"""
        resp = self.db_client.find_record_in_alerts_table(alert_id)
        allure.attach(str(resp), 'Ответ на запрос к таблице Alerts базы incidents', allure.attachment_type.TEXT)
        assert resp, 'Не найдена запись в таблице Alerts базы incidents'

    def aa_check_response_contains_error(self, response, type_error):
        """"""
        error_found = False
        paths = jsonpath(response, '$..path')
        for item in paths:
            if item == f'$.{type_error}':
                error_found = True
                self.log.info(f'Валидационная ошибка для {type_error} найдена')
                break
        assert error_found, f'В ответе нет ожидаемой валидационной ошибки для {type_error}!\nПолученный ответ: {response}'

    def aa_create_several_alert_in_one_request(self, alert_count):
        """"""
        data = list()
        for i in range(alert_count):
            data.append(self.generator.give_json(self.alerts_prefix))
        resp = self.create_several_alerts({'alerts': data})
        return resp

    def aa_add_alert_to_incident(self, alert_id, inc_id):
        """"""
        resp = self.include_alert_in_incident(inc_id=inc_id, alert_id=alert_id)

    def aa_exclude_alert_from_incident(self, alert_id):
        """"""
        self.include_alert_in_incident(inc_id=None, alert_id=alert_id)

    def aa_find_alert_by_source_id(self, source_id):
        """"""
        result = None
        for i in range(20):
            result = self.db_client.find_alert_by_source_id(source_id)
            if result:
                self.log.info(f'Итерация {i}. Найден алерт {result[0][0]} с sourceId {source_id}')
                break
            else:
                self.log.info(f'Итерация {i}. В базе не найден алерт с sourceId {source_id}')
                sleep(5)
        assert result, f'В базе не найден алерт с sourceId={source_id}'
        allure.attach(self.LKO_URL + f"/v2/alerts/view/{result[0][0]}", 'Ссылка на алерт в UI',
                      allure.attachment_type.URI_LIST)
        return result[0][0]

    def aa_check_one_alert_found_by_source_id(self, source_id):
        """"""
        result = self.db_client.find_alert_by_source_id(source_id)
        assert result, f'В базе не найден алерт с sourceId={source_id}'
        assert len(result) == 1, f'Найдено более одного алерта с sourceId={source_id}'

    def aa_get_alert_info_and_check_source(self, alert_id, source):
        """"""
        info = self.get_alert_info(alert_id)
        allure.attach(dumps(info, indent=2, ensure_ascii=False), f'Ответ на get-запрос данных алерта {alert_id}',
                      allure.attachment_type.JSON)
        assert info['source'] == source, f'Не совпадает источник алерта. Полученный: {info["source"]},' \
                                         f'ожидаемый: {source}'

    def aa_get_alert_etag(self, alert_id):
        """  """
        resp = self.get_alert_info(alert_id)
        return resp['versionInfo']['etag']

    @backoff.on_exception(backoff.constant, (ApiException, AssertionError), max_time=15, interval=2)
    def aa_get_alert_info_with_expected_etag(self, alert_id, etag):
        return self.get_alert_info(alert_id, etag=etag)

    def aa_get_query_string_for_predefined_filter(self, predefined_filter):
        """"""
        filters = self.get_alerts_predefined_filters()
        query_string = ''
        for item in filters[0]['filters']:
            if item['id'] == predefined_filter:
                query_string = item['queryString']
        assert query_string, f'Не найден предустановленный фильтр с id {predefined_filter}'
        return query_string

    def aa_get_alerts_with_filters(self, false_positive=None, is_included=None, incident=None,
                                   source=None, fixation_date=None, responsible_operator=None,
                                   predefined_filter=None, search_query=None, limit=None):
        """"""
        filters = dict()
        query_string = None
        if predefined_filter:
            query_string = self.aa_get_query_string_for_predefined_filter(predefined_filter)
        if false_positive:
            filters['falsePositive'] = false_positive
        if is_included:
            filters['isIncluded'] = is_included
        if incident:
            filters['incident'] = incident
        if source:
            filters['source'] = source
        if fixation_date:
            filters['fixationDate'] = fixation_date
        if responsible_operator:
            filters['responsibleOperator'] = responsible_operator
        resp = self.get_alerts(query_string=query_string, user_filters=filters, search_query=search_query, limit=limit)
        allure.attach(dumps(resp, indent=2, ensure_ascii=False), 'Ответ на get-запрос списка алертов с фильтрами',
                      allure.attachment_type.JSON)
        return resp

    def aa_get_random_alerts_wth_user_filters(self, alert_count, false_positive=None, is_included=None, incident=None,
                                              source=None, fixation_date=None, responsible_operator=None):
        """"""
        response = self.aa_get_alerts_with_filters(false_positive=false_positive, is_included=is_included,
                                                   incident=incident, source=source, fixation_date=fixation_date,
                                                   responsible_operator=responsible_operator)
        if len(response['items']) < alert_count:
            pytest.skip('В системе нет достаточного числа алертов, удовлетворяющих фильтрам')
        alert_ids = list()
        result = sample(response['items'], alert_count)
        for item in result:
            alert_ids.append(item['id'])
            allure.attach(self.LKO_URL + f"/v2/alerts/view/{item['id']}", 'Ссылка на алерт в UI',
                          allure.attachment_type.URI_LIST)
        allure.attach(str(alert_ids), 'IDs выбранных алертов', allure.attachment_type.TEXT)
        return alert_ids

    def aa_get_all_alerts_count(self):
        """"""
        resp = self.get_alert_count()
        assert resp.get('total') is not None, f'Не удалось получить количество алертов в системе. Полученный ответ: ' \
                                              f'{resp}'
        self.log.info(f'Число алертов в системе: {resp["total"]}')
        return resp['total']

    def aa_check_result_for_all_predefined_filter(self, resp, limit=100):
        """"""
        total = self.aa_get_all_alerts_count()
        if limit < total:
            assert len(resp['items']) <= limit, f"Число полученных алертов {len(resp['items'])} не совпадает с " \
                                                f"ожидаемым {limit}"
        else:
            assert len(resp['items']) == total, f"Число полученных алертов {len(resp['items'])} не совпадает с " \
                                                f"ожидаемым {total}"

    def aa_check_result_for_new_predefined_filter(self, resp):
        """"""
        for alert in resp['items']:
            assert alert.get('incident') is None, f'Найден алерт {alert["id"]}, входящий в инцидент, что не ' \
                                                  f'удовлетворяет фильтру'
            assert alert.get('responsibleOperator') is None, f'Найден алерт {alert["id"]}, назначенный на ' \
                                                             f'пользователя, что не удовлетворяет фильтру'
            assert alert.get('falsePositive') is False, f'Найден алерт {alert["id"]}, являющийся ложным ' \
                                                        f'срабатыванием, что не удовлетворяет фильтру'
        self.log.info(f'Число найденных алертов, удовлетворяющих фильтру: {len(resp["items"])}')

    def aa_check_result_for_onthego_predefined_filter(self, resp, operator_id):
        """"""
        for alert in resp['items']:
            assert alert.get('incident') is None, f'Найден алерт {alert["id"]}, входящий в инцидент, что не ' \
                                                  f'удовлетворяет фильтру'
            assert alert.get('responsibleOperator')['id'] == operator_id, \
                f'Найден алерт {alert["id"]}, не назначенный на текущего пользователя, что не удовлетворяет фильтру'
            assert alert.get('falsePositive') is False, f'Найден алерт {alert["id"]}, являющийся ложным ' \
                                                        f'срабатыванием, что не удовлетворяет фильтру'
        self.log.info(f'Число найденных алертов, удовлетворяющих фильтру: {len(resp["items"])}')

    def aa_check_result_for_is_included_filter(self, resp, is_included):
        """"""
        for alert in resp['items']:
            if is_included == 'yes':
                assert alert.get('incident'), f'Найден алерт {alert["id"]}, не удовлетворяющий фильтру ' \
                                              f'is_included={is_included}'
            else:
                assert not alert.get('incident'), f'Найден алерт {alert["id"]}, не удовлетворяющий фильтру ' \
                                                  f'is_included={is_included}'
        self.log.info(f'Число найденных алертов, удовлетворяющих фильтру: {len(resp["items"])}')
        return len(resp['items'])

    def aa_check_result_for_false_positive_filter(self, resp, false_positive):
        """"""
        for alert in resp['items']:
            if false_positive == 'yes':
                assert alert.get('falsePositive'), f'Найден алерт {alert["id"]}, не удовлетворяющий фильтру ' \
                                                   f'falsePositive={false_positive}'
            else:
                assert not alert.get('falsePositive'), f'Найден алерт {alert["id"]}, не удовлетворяющий фильтру ' \
                                                       f'falsePositive={false_positive}'
        self.log.info(f'Число найденных алертов, удовлетворяющих фильтру: {len(resp["items"])}')
        return len(resp['items'])

    def aa_check_result_for_responsible_operator_filter(self, resp, operator_ids):
        """"""
        if not isinstance(operator_ids, list):
            operator_ids = [operator_ids]
        for alert in resp['items']:
            assert alert.get('responsibleOperator')['id'] in operator_ids, f'Найден алерт {alert["id"]}, не ' \
                                                                           f'удовлетворяющий фильтру ' \
                                                                           f'responsibleOperator={operator_ids}'
        self.log.info(f'Число найденных алертов, удовлетворяющих фильтру: {len(resp["items"])}')
        return len(resp['items'])

    def aa_check_result_for_source_filter(self, resp, sources):
        """"""
        if not isinstance(sources, list):
            sources = [sources]
        for alert in resp['items']:
            assert alert.get('source') in sources, f'Найден алерт {alert["id"]}, не удовлетворяющий фильтру ' \
                                                   f'source={sources}'
        self.log.info(f'Число найденных алертов, удовлетворяющих фильтру: {len(resp["items"])}')
        return len(resp['items'])

    def aa_check_result_for_fixation_date_filter(self, resp, period):
        """"""
        begin = transform_date_to_timestamp(period[0])
        end = transform_date_to_timestamp(period[1])
        for alert in resp['items']:
            detected_at = transform_date_to_timestamp(alert['detectedAt'])
            assert begin <= detected_at <= end, f'Найден алерт {alert["id"]}, не удовлетворяющий фильтру ' \
                                                f'дата обнаружения={period}'
        self.log.info(f'Число найденных алертов, удовлетворяющих фильтру: {len(resp["items"])}')
        return len(resp['items'])

    def aa_check_result_for_incident_filter(self, resp, inc_ids):
        """"""
        if not isinstance(inc_ids, list):
            inc_ids = [inc_ids]
        for alert in resp['items']:
            assert alert['incident']['id'] in inc_ids, f'Найден алерт {alert["id"]}, не удовлетворяющий фильтру ' \
                                                       f'инцидент={inc_ids}'
        self.log.info(f'Число найденных алертов, удовлетворяющих фильтру: {len(resp["items"])}')
        return len(resp['items'])

    def aa_check_response_for_search_query(self, resp, search_str, expected_alert_id=None, source=None):
        """"""
        self.log.info(f'Число найденных алертов: {len(resp["items"])}')
        if expected_alert_id:
            is_found = False
            for item in resp['items']:
                if item['id'] == expected_alert_id:
                    is_found = True
                    break
            assert is_found, f'В полученном ответе нет алерта с ожидаемым id {expected_alert_id}'
        for item in resp['items']:
            assert search_str.lower() in str(item['rawData']).lower(), f'Поисковая строка {search_str} не найдена в ' \
                                                                       f'алерте с id {item["id"]}'
            if source:
                assert item['source'] == source, f'Не совпадает источник у алерта {id}'

    def aa_get_alert_count_with_filters(self, false_positive=None, is_included=None, incident=None, source=None,
                                        fixation_date=None, responsible_operator=None, predefined_filter=None,
                                        search_query=None):
        """"""
        filters = dict()
        query_string = None
        if predefined_filter:
            query_string = self.aa_get_query_string_for_predefined_filter(predefined_filter)
        if false_positive:
            filters['falsePositive'] = false_positive
        if is_included:
            filters['isIncluded'] = is_included
        if incident:
            filters['incident'] = incident
        if source:
            filters['source'] = source
        if fixation_date:
            filters['fixationDate'] = fixation_date
        if responsible_operator:
            filters['responsibleOperator'] = responsible_operator
        resp = self.get_alerts_count(query_string=query_string, user_filters=filters, search_query=search_query)
        allure.attach(dumps(resp, indent=2, ensure_ascii=False), 'Ответ на get-запрос числа алертов с фильтрами',
                      allure.attachment_type.JSON)
        return resp

    def aa_check_db_do_not_contain_alert_with_source_id(self, source_id):
        """"""
        result = None
        for i in range(5):
            result = self.db_client.find_alert_by_source_id(source_id)
            if result:
                self.log.info(f'Итерация {i}. Найден алерт {result[0][0]} с sourceId {source_id}')
                break
            else:
                self.log.info(f'Итерация {i}. В базе не найден алерт с sourceId {source_id}')
                sleep(5)
        assert not result, f'В базе найден алерт с sourceId={source_id}'