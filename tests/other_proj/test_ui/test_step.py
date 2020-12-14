#!/usr/bin/env python
# -*- coding: utf-8 -*-
import allure
import pytest
from configs.modify_data import request_info_lko, request_info_lku, test_modify_data
from tools.utils import now_timestamp, convert_date_to_rus


class TestAuthPage:
    @allure.feature('Login page')
    @allure.story('Check login')
    @allure.testcase("Open login page and enter")
    def test_existing_login_lkoo(self, lkoo):
        with allure.step('open page and login'):
            lkoo.open_page()
            lkoo.lp_login_existing_user()
            lkoo.mp_lko_click_requests_btn()

    @allure.feature('Login page Other contour')
    @allure.story('Check login')
    @allure.testcase("Open login page and enter")
    def test_custom_login_lku(self, lku):
        with allure.step('open page and login'):
            lku.open_page()
            lku.lp_login_custom_user(login='auto_user', password='Password')
            lku.mp_lku_register_req_btn()


class TestParticipants:
    @allure.feature('Text')
    @allure.story('Story01')
    @allure.testcase("https://testrail.dom_name", 'ссылка на Testrail')
    def test_edit_participant_cart(self, lkoz):
        with allure.step('открыть страницу и залогинится'):
            lkoz.open_page()
            lkoz.lp_login_existing_user()
        with allure.step('открыть и проверить страницу участников'):
            lkoz.mp_lko_find_and_click_participants_btn()
            lkoz.pp_check_participants_grid()
        with allure.step('найти нужного участника, выбрать его, нажать кнопку редактировать'):
            lkoz.pp_search_autotest_payer_participant()
            lkoz.pp_choose_test_participant()
            lkoz.pp_click_edit_participant()
        with allure.step('изменить поля ID в платежной системе и важность и сохранить изменения'):
            lkoz.pp_clear_and_fill_id_payment_system_field()
            lkoz.pp_click_dropdown_importance()
            lkoz.pp_random_choose_importance()
            lkoz.pp_click_save_btn()
        with allure.step('проверить что изменения сохранились'):
            lkoz.ba_wait_for_loading()
            lkoz.pp_check_participant_view()
            lkoz.pp_check_participant_importance()
            lkoz.pp_check_participant_id_payment_system()


class TestReferenceInfo:
    @allure.feature('Text')
    @allure.story('Story01')
    @allure.testcase("https://testrail.dom_name", 'ссылка на Testrail')
    def test_reference_info_loading(self, lkoz):
        with allure.step('Открыть страницу и залогиниться'):
            lkoz.open_page()
            lkoz.lp_login_existing_user()
        with allure.step('Перейти на страницу редактирования справочников'):
            lkoz.mp_lko_click_system_btn()
            lkoz.mp_lko_click_reference_info_loading_btn()
        with allure.step('Приложить справочник и проверить, что он загрузился'):
            lkoz.ril_choose_bic_swift_bac_ref()
            lkoz.ril_click_add_new_reference_info()
            lkoz.ril_find_input_and_insert_file()
            lkoz.ril_insert_file_click_submit_btn()
            download_datetime = now_timestamp(date_format='%Y-%m-%dT%H:%M:%SZ')
            day, months, _, time_hour, time_min, _ = convert_date_to_rus(input_date=download_datetime,
                                                                         time_delta=3,
                                                                         rus_date_format=None)
            text_download_datetime = f'{day} {months}, {time_hour}:{time_min}'
            lkoz.ba_wait_for_loading()
            lkoz.ril_check_modal_input_file_for_error()
            lkoz.driver.refresh()
        with allure.step('Проверить дату загрузки актуальной версии справочника'):
            lkoz.ril_compare_last_upd_date_and_curr_date(text_download_datetime)
        with allure.step('Проверить дату последней попытки обновления'):
            lkoz.ril_compare_last_upd_retry_date_and_curr_date(text_download_datetime)
        with allure.step('Скачать справочник'):
            lkoz.ril_check_download_reference_info()


@pytest.mark.usefixtures('clear_dir_for_browser')
class TestRequestPageMessages:
    @allure.feature('Text')
    @allure.story('отправка ответа на запрос')
    @allure.testcase("https://testrail.dom_name", 'ссылка на Testrail')
    @pytest.mark.dependency(name='requests_adding_message')
    def test_send_answer_on_request_lkoz(self, lkoz):
        with allure.step('открыть страницу и залогиниться'):
            lkoz.open_page()
            lkoz.lp_login_existing_user()
        with allure.step('перейти в Запросы и выбрать один из первых доступных'):
            lkoz.mp_lko_click_requests_btn()
            lkoz.rp_lko_search_request_fld('auto_payer')
            lkoz.rp_random_choose_request()
        with allure.step('добавить рандомный текст в ответ и отправить его'):
            lkoz.rp_send_answer_on_request_and_check_message('lko')

    @allure.feature('Text')
    @allure.story('проверка ответа на запрос')
    @allure.testcase("https://testrail.dom_name", 'ссылка на Testrail')
    @pytest.mark.dependency(depends=["requests_adding_message"])
    def test_check_answer_on_request_lku(self, lku):
        with allure.step('открыть страницу и залогиниться'):
            lku.open_page()
            lku.lp_login_existing_user()
        with allure.step('ищем запрос и проверяем, что сообщение отображается'):
            lku.mp_lku_click_request_btn()
            lku.rpu_search_request_after_send_from_lkoz()
            lku.rpu_find_and_check_message_from_lkoz()

# and more more here
