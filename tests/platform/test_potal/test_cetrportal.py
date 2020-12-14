#!/usr/bin/env python
# -*- coding: utf-8 -*-
import allure
import pytest


class TestPortal:
    @allure.epic('Получение obj от внешних систем')
    @allure.feature('Portal test')
    @allure.story('Получение obj ')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_certportal_bulletin(self, certportal_admin, lko_admin, is_gos_proj_bulletin_import_enabled):
        with allure.step('Portal. Отправка obj для всех ЦЕРТов'):
            with allure.step('Portal. Формирование JSON с вложением для всех Obj'):
                bulletin_json = certportal_admin.certp_api_create_new_bulletin_json()
            with allure.step('Portal. Отправка obj'):
                bulletin_id = certportal_admin.certp_api_create_bulletin(bulletin_json)
            with allure.step('Portal. Публикация obj'):
                certportal_admin.certp_publicate_bulletin(bulletin_id)
            with allure.step('Portal. Проверка, что obj опубликован'):
                certportal_admin.certp_api_check_bulletin_published(bulletin_id, 'publicated')
        with allure.step('Платформа. Проверка, что obj пришел в систему'):
            try:
                bulletin_data = lko_admin.ba_search_bulletin_by_field_value('hrid', bulletin_json['identifier'])
            except AssertionError:
                pytest.fail('Ошибка! obj не пришел в систему в течение 60 секунд')
        with allure.step('Платформа. Проверка соответствия данных полученного obj'):
            with allure.step('Платформа. Получение данных obj пришедшего'):
                pl_bulletin_data = lko_admin.ba_get_bulletin_data_by_id(bulletin_data['id'])
            lko_admin.ba_compare_platform_and_certportal_bulletin(pl_bulletin_data, bulletin_json)
            with allure.step('Платформа. Скачивание и проверка файла, приложенного к obj'):
                lko_admin.ba_check_bulletins_attachment(pl_bulletin_data)
