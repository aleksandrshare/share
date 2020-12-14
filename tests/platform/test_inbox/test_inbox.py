#!/usr/bin/env python
# -*- coding: utf-8 -*-
import allure

shared_data = dict()


class TestInbox:
    @allure.epic('Тесты интеграции')
    @allure.feature('Inbox')
    @allure.story('Отправка без вложения')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_inbox_inc_without_attach(self, integr_api_lko_admin, lko_admin):
        with allure.step('IntegrAPI. Отправка инцидента без вложения через инбокс'):
            integr_api_lko_admin.integr_api_send_inbox()
            integr_api_lko_admin.integr_api_check_sent_incident()
        with allure.step('Проверка наличия async_id сущности в БД sp_integration_api'):
            integr_api_lko_admin.integr_api_check_entity_created_in_db()
        with allure.step('IntAPI. Проверка созданного инцидента'):
            lko_admin.ia_check_inbox_incident_by_id()

    @allure.epic('Тесты интеграции')
    @allure.feature('Inbox')
    @allure.story('Отправка с загрузкой вложения')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    def test_inbox_inc_with_attach(self, integr_api_lko_admin, lko_admin):
        with allure.step('IntegrAPI. Загрузка в систему файла-вложения'):
            integr_api_lko_admin.integr_api_upload_file()
        with allure.step('IntegrAPI. Отправка с вложением через инбокс'):
            integr_api_lko_admin.integr_api_send_inbox()
            integr_api_lko_admin.integr_api_check_sent_incident()
        with allure.step('Проверка наличия async_id сущности в БД'):
            integr_api_lko_admin.integr_api_check_entity_created_in_db()
        with allure.step('IntAPI. Проверка созданного инцидента'):
            lko_admin.ia_check_inbox_incident_by_id(attach_added=True)

    @allure.epic('Тесты интеграции')
    @allure.feature('Inbox')
    @allure.story('Отправка с загрузкой нескольких вложений')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    def test_inbox_inc_with_several_attach(self, integr_api_lko_admin, lko_admin):
        with allure.step('IntegrAPI. Загрузка в систему файла-вложения'):
            for i in range(3):
                with allure.step(f'Загрузка вложения № {i + 1}'):
                    integr_api_lko_admin.integr_api_upload_file()
        with allure.step('IntegrAPI. Отправка инцидента с вложением через инбокс'):
            integr_api_lko_admin.integr_api_send_inbox()
            integr_api_lko_admin.integr_api_check_sent_incident()
        with allure.step('Проверка наличия async_id сущности в БД'):
            integr_api_lko_admin.integr_api_check_entity_created_in_db()
        with allure.step('IntAPI. Проверка созданного obj'):
            lko_admin.ia_check_inbox_incident_by_id(attach_added=True)

# and more more here
