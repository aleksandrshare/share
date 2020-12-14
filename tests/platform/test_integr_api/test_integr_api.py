#!/usr/bin/env python
# -*- coding: utf-8 -*-
import allure
from configs.modify_data import test_modify_data


class TestIntegerApi:
    @allure.epic('Интеграционное API')
    @allure.feature('Text')
    @allure.story('Создание инцидента')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    def test_create_incident_integr_api(self, integr_api_lko_admin):
        with allure.step('Отправка запроса на создание инцидента'):
            integr_api_lko_admin.integr_api_send_incident()
        with allure.step('Проверка создания инцидента по async_id'):
            integr_api_lko_admin.integr_api_check_sent_incident(id_field='incidentId')
        with allure.step('Проверка наличия async_id сущности в БД'):
            integr_api_lko_admin.integr_api_check_entity_created_in_db()

    @allure.epic('Интеграционное API')
    @allure.feature('Text')
    @allure.story('Редактирование инцидента')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    def test_edit_incident_integr_api(self, integr_api_lko_admin, lko_admin):
        with allure.step('Получение id случайного инцидента для редактирования'):
            inc_id = lko_admin.ia_get_random_incident()
        with allure.step('Получение данных инцидента для редактирования'):
            inc_data = integr_api_lko_admin.integr_api_get_incident_data_by_id(inc_id)
        with allure.step('Отправка запроса на редактирование инцидента'):
            edit_inc_data = integr_api_lko_admin.integr_api_edit_incident(edit_inc_id=inc_id,
                                                                          if_match=inc_data['versionInfo']['etag'])
        with allure.step('Проверка редактирования инцидента по async_id'):
            try:
                integr_api_lko_admin.integr_api_check_sent_incident(id_field=None)
            except AssertionError:
                with allure.step('Инцидент недоступен для редактирования. Создание нового инцидента'):
                    with allure.step('Отправка запроса на создание инцидента'):
                        integr_api_lko_admin.integr_api_send_incident()
                    with allure.step('Проверка создания инцидента по async_id'):
                        integr_api_lko_admin.integr_api_check_sent_incident(id_field='incidentId')
                        inc_id = test_modify_data['integr_api_entity_id']
                    with allure.step('Получение данных инцидента для редактирования'):
                        inc_data = integr_api_lko_admin.integr_api_get_incident_data_by_id(inc_id)
                    with allure.step('Отправка запроса на редактирование инцидента'):
                        edit_inc_data = integr_api_lko_admin.integr_api_edit_incident(edit_inc_id=inc_id,
                                                                                      if_match=inc_data[
                                                                                          'versionInfo']['etag'])
                    with allure.step('Проверка редактирования инцидента по async_id'):
                        integr_api_lko_admin.integr_api_check_sent_incident(id_field=None)
        with allure.step('Проверка результата редактирования инцидента'):
            integr_api_lko_admin.integr_api_check_incident_edit(inc_id, edit_inc_data)

    @allure.epic('Интеграционное API')
    @allure.feature('Text')
    @allure.story('Получение информации об инциденте')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    def test_get_incident_data_integr_api(self, integr_api_lko_admin, lko_admin):
        with allure.step('Получение id случайного инцидента'):
            inc_id = lko_admin.ia_get_random_incident()
        with allure.step(f'Получение данных инцидента с id="{inc_id}"'):
            integr_api_lko_admin.integr_api_get_incident_data_by_id(inc_id)

    @allure.epic('Интеграционное API')
    @allure.feature('Text')
    @allure.story('Получение информации об инциденте')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    def test_get_several_incidents_data_integr_api(self, integr_api_lko_admin, lko_admin):
        with allure.step('Отправка запроса на создание и проверку нескольких инцидентов'):
            inc_count = 2
            incident_ids = lko_admin.ia_api_create_and_check_several_incidents(count=inc_count)
        with allure.step(f'Получение данных {inc_count} инцидентов'):
            all_data = integr_api_lko_admin.integr_api_get_several_incidents_data_by_ids(incident_ids)
        with allure.step(f'Проверка соответствия полученных данных инцидентов'):
            integr_api_lko_admin.integr_api_check_several_icidents_info(incident_ids, all_data)
