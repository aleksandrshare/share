#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import choice
from framework.ui_libs.ui_lib import Page
from time import sleep
import random
from tools.utils import string_generator, utc_timestamp
from framework.other_proj_ui.ui_auto.fc_helpers import (
    collect_locator, decorator_for_change_selenium_wait_and_return_after
)
from configs.modify_data import request_info_lko, request_info_lku, test_modify_data
import allure
from ui_library.dad_file_with_js import drag_and_drop_file
import os


def lko_decorator_for_check_emals_in_bd(action):
    """декоратор запоминает кол-во сообщений в запросе в БД emails ЛКО до переданного действия
    и после сравнивает по кол-ву результатов ответа БД

    :param action: объект метода класса для выполнения
    :type action: function

    ВАЖНО для выбора откуда брать hrid необходимо в декорируемую функцию передать агрумент hrid_stand
    значения hrid_stand='lku'
    """
    def check_in_bd(self, *args, **kwargs):
        hrid_stand = args[0] if args else kwargs['hrid_stand']
        if hrid_stand == 'lku':
            hrid = request_info_lku['hrid']
        else:
            hrid = request_info_lko['hrid']
        self.log.info("переданный hrid: %s" % hrid)
        in_db_before = self.rp_lko_request_in_db_emails(hrid)
        self.log.info("Проверка в БД информации по запросу %s перед действием, ответ %s" % (hrid, len(in_db_before)))
        action(self, *args, **kwargs)
        self.log.info("действие вызвавшее проверку в БД: %s" % action.__name__)
        in_db_after = self.rp_lko_request_in_db_emails(hrid, quantity_iter=len(in_db_before))
        self.log.info("Проверка в БД информации по запросу %s после действия, ответ %s" % (hrid, len(in_db_after)))
        assert len(in_db_before) != len(in_db_after)
    return check_in_bd


class ExtendPage(Page):
    def extract_all_list_items(self, *text_locator):
        """
        Возвращает текст всех элементов выпадающего списка

        :param text_locator: локатор к элементам списка
        :return: list строчек текста в списке
        """
        elements = self.search_elements(*text_locator)
        if elements:
            list_items = []
            for item in elements:
                list_items.append(item.text)
            list_items = list(filter(None, list_items))
            return list_items


class RequestsPageLKU(Page):
    """Работа со страницей в разделе 'Запросы'"""

    def rp_lku_search_request_fld(self, text):
        """Заполнить поле ввода 'Поиск запросов'"""
        self.wait_for_invisibility_element(*self.locators.CIRCULAR_LOADER)
        self.find_and_fill_element(text, *self.locators.RP_LKU_SEARCH_REQ_FLD)
        self.wait_for_invisibility_element(*self.locators.CIRCULAR_LOADER)

    def rp_lku_new_req_msg_fld(self, text):
        """Заполнить поле ввода 'Написать сообщение...' при создании запроса"""
        self.find_and_fill_element(text, *self.locators.RP_NEW_REQUEST_MESSAGE)

    def rp_lku_new_req_theme_fld(self, text):
        """Заполнить поле ввода 'Тема' при создании запроса"""
        self.find_and_fill_element(text, *self.locators.RP_NEW_REQUEST_THEME)

    def rp_lku_new_req_create_btn(self):
        """Нажать на кнопку 'Создать запрос' при создании запроса"""
        self.find_and_click(*self.locators.RP_LKU_CREATE_REQUEST_BTN)

    def rp_lku_send_message_btn(self):
        """Нажать на кнопку 'Отправить'"""
        self.find_and_click(*self.locators.RP_LKU_SEND_MSG_BTN)

    def rp_lku_new_req_delete_btn(self):
        """Нажать на кнопку 'Удалить запрос'"""
        self.find_and_click(*self.locators.RP_LKU_DELETE_REQUEST_BTN)

    @decorator_for_change_selenium_wait_and_return_after(5)
    def rp_lku_add_ds_modal_win(self):
        """Модальное окно 'Добавить цифровую подпись' при создании запроса"""
        try:
            if self.search_element(*self.locators.RP_LKU_ADD_DS_WIN):
                self.log.info("Модальное окно 'Добавить цифровую подпись' найдено")
                return True
        except Exception:
            self.log.info("Модальное окно 'Добавить цифровую подпись'не найдено")

    def rp_lku_add_ds_no_signature_btn(self):
        """
        Модальное окно 'Добавить цифровую подпись'
        Кнопка 'Отправить без подписи'
        """
        self.log.info("Поиск и нажатие на кнопку 'Отправить без подписи'")
        self.find_and_click(*self.locators.RP_LKU_ADD_DS_NO_SIGNATURE_BTN)

    def rp_lku_add_ds_yes_signature_btn(self):
        """
        Модальное окно 'Добавить цифровую подпись'
        Кнопка 'Подписать и отправить'
        """
        self.log.info("Поиск и нажатие на кнопку 'Подписать и отправить'")
        self.find_and_click(*self.locators.RP_LKU_ADD_DS_YES_SIGNATURE_BTN)

    def rp_lku_fill_req_theme_and_msg(self):
        """Заполнить тему и текст сообщения в запросе"""
        msg_text = 'UI_автотест_cообщение: ' + string_generator(min_length=10, max_length=50)
        self.rp_lku_new_req_msg_fld(msg_text)
        self.req_theme = '[{}] UI_автотест'.format(utc_timestamp(date_format='%Y-%m-%dT%H:%M:%S.%f'))
        request_info_lku['theme'] = self.req_theme
        request_info_lku['message'] = msg_text
        self.rp_lku_new_req_theme_fld(self.req_theme)

    def rp_lku_not_add_signature(self):
        """Отправить запрос из ЛКУ без ЭП"""
        try:
            if self.rp_lku_add_ds_modal_win():
                self.rp_lku_add_ds_no_signature_btn()
                self.wait_for_invisibility_element(*self.locators.CIRCULAR_LOADER)
        except:
            self.log.info('ЛКУ. Добавление ЭП к запросу не предусмотрено')
        self.wait_for_invisibility_element(*self.locators.CIRCULAR_LOADER)

    def rp_lku_add_signature(self, pincode):
        """Отправить запрос из ЛКУ c ЭП"""
        if self.rp_lku_add_ds_modal_win():
            self.find_and_fill_element(pincode, *self.locators.RP_LKU_ADD_DS_PIN_AREA)
            self.rp_lku_add_ds_yes_signature_btn()
            self.wait_for_invisibility_element(*self.locators.CIRCULAR_LOADER)

    def rp_lku_add_signature_or_not(self, dss, pin):
        if dss == 'prod' or dss == 'emul':
            self.rp_lku_add_signature(pin)
        else:
            self.rp_lku_not_add_signature()

    def rp_lku_show_obs_request(self):
        """Открыть запрос по операции без согласия для просмотра"""
        self.find_and_click(*self.locators.RP_LKU_OBS_REQ_EF)
        self.wait_for_invisibility_element(*self.locators.CIRCULAR_LOADER)

    def rp_lku_reply_obs_request_btn(self):
        """
        Модальное окно 'Электронная форма запрос по Операции'
        Нажать на кнопку 'Сформировать ответ'
        """
        self.find_and_click(*self.locators.RP_LKU_OBS_RESPONSE_BTN)

    def rpu_find_and_fill_search(self, search_text):
        """метод находит поле поиска и заполняет его, необходимо передать текст

        :param search_text: текст для поика
        :type search_text: str
        """
        self.find_and_fill_element(search_text, *self.locators.RP_SEARCH_AREA)

    def rpu_search_request_after_send_from_lkoz(self):
        """метод передает в rpu_find_and_fill_search ранее сохраненное значение в классе RequestsPageLKO
        для поиска нужного запроса"""
        self.rpu_find_and_fill_search(request_info_lko['hrid'])
        self.log.info("Поиск запроса {}".format(request_info_lko['hrid']))

    def rp_lku_search_request_after_create_from_lku(self):
        """метод передает в rpu_find_and_fill_search ранее сохраненное значение в классе RequestsPageLKU
        для поиска нужного запроса"""
        self.rpu_find_and_fill_search(request_info_lku['hrid'])
        self.log.info("Поиск запроса {}".format(request_info_lku['hrid']))

    def rpu_find_and_check_message_from_lkoz(self):
        """метод ищет последнее сообщение в запросе и сравнивает с ранее сохраненным значением в классе RequestsPageLKO
        используется после метода rpu_search_request_after_send_from_lkoz, который найдет нужный запрос"""
        all_messages = self.search_elements(*self.locators.RP_MESSAGES_IN_REQUEST)
        self.log.info("Текст отправленного В ЛКОЗ сообщения: %s" % request_info_lko['message'])
        text_for_check = all_messages[-1].find_element_by_xpath('div/div').text
        self.log.info("Текст отображаемого В ЛКУ сообщения: %s" % text_for_check)
        assert request_info_lko['message'] == text_for_check

    def rp_lku_save_request_hrid_after_create(self):
        """ищет hrid запроса, сохраняет его в request_info_lku и логирует"""
        request_info_lku['hrid'] = None
        self.ba_lku_wait_for_loading()
        for i in range(10):
            if '(ID назначается)' in self.return_text_ele(*self.locators.RP_REQUEST_HRID):
                if i == 5:
                    self.driver.refresh()
                sleep(0.5)
                continue
            else:
                request_info_lku['hrid'] = self.return_text_ele(*self.locators.RP_REQUEST_HRID)
                self.log.info("ID нового запроса: %s" % request_info_lku['hrid'])
                break

    def rp_lku_get_request_id(self):
        """Получить id запроса"""
        request_info_lku['id'] = self.driver.current_url.partition('/requests/list/')[2].split('?')[0]
        test_modify_data['req_id'] = request_info_lku['id']
        self.log.info('Запросу с hrid "{}" соотвествует guid "{}"'.format(request_info_lku['hrid'],
                                                                          request_info_lku['id']))
        allure.attach(self.driver.current_url, 'Ссылка на запрос', allure.attachment_type.URI_LIST)

    def rp_lku_fill_forms_request_other_type(self):
        """метод заполняет поля в запросе типа 'Другое' и сохраняет информацию о нем в request_info_lku"""
        self.rp_lku_fill_req_theme_and_msg()
        self.rp_lku_new_req_create_btn()
        if self.rp_lku_add_ds_modal_win():
            self.rp_lku_add_ds_no_signature_btn()
        self.rp_lku_save_request_hrid_after_create()
        self.rp_lku_get_request_id()

    def rp_lku_click_ef_in_request(self):
        """Нажимет на электронную форму в открытом Запросе"""
        self.ba_lku_wait_for_loading()
        self.find_and_click(*self.locators.RP_EF_IN_REQUEST)
        self.ba_lku_wait_for_loading()

    def rp_lku_click_antifraud_response(self):
        """Нажимает на сохраненный не отправленный ответ в Запросе"""
        self.find_and_click(*self.locators.RP_EF_ANTIFRAUD_RESONSE)

    def rp_lku_open_first_sent_response(self):
        """открывает первый отправленный ответ в Запросе"""
        self.ba_lku_wait_for_loading()
        self.find_and_click(*self.locators.RP_EF_SENT_RESPONSE)

    def rp_lku_click_antifraud_response_edit_pensil(self):
        """Нажимет кнопку 'редактировать' сохраненный ответ в открытом Запросе"""
        self.find_and_click(*self.locators.RP_EF_ANTIFRAUD_RESONSE_EDIT_PENSIL)

    def rp_lku_click_send_response(self):
        """Нажимет кнопку 'Отправить' в открытом Запросе"""
        self.find_and_click(*self.locators.RP_SEND_RESPONSE_BTN)
        if self.rp_lku_add_ds_modal_win():
            self.rp_lku_add_ds_no_signature_btn()

    def rp_lku_find_and_check_alert_on_response(self):
        """Находит и проверяет, что не полностью заполненный ответ не отправился"""
        alert = self.return_text_ele(*self.locators.RP_EF_RESPONSE_ALERT)
        assert alert == 'Заполните форму перед отправкой'

    def rp_lku_show_ef_lockrequest_response(self, ef_num=1):
        """
        Открыть Электронная форма отчета о блокировке в запросе для просмотра.
        Открывает ЭФ с номером ef_num
        """
        tries = 3
        for i in range(tries):
            elements = self.search_elements(*self.locators.RP_VIEW_EF_LOCKREQUEST_RESPONSE)
            if elements:
                elements[ef_num-1].click()
                break
            else:
                self.driver.refresh()
                self.ba_lku_wait_for_loading()
        assert elements, "ЭФ отчёт о блокировке корр. счёта не обнаружена в запросе!"

############################################################################
    def rp_lku_open_request_by_id(self, req_id=None):
        """ Открывает запроса по его id """
        if not req_id:
            req_id = test_modify_data['req_id']
        url = self.url + '/requests/list/{}'.format(req_id)
        self.log.info('Open page: ' + url)
        self.driver.get(url)
        self.ba_lku_wait_for_loading()

    def rp_lku_click_ef_with_number_in_request(self, number):
        """Нажимет на электронную форму с номером number в открытом Запросе"""
        self.ba_lku_wait_for_loading()
        elements = self.search_elements(*self.locators.RP_EF_IN_REQUEST)
        elements[number-1].click()
        self.ba_lku_wait_for_loading()

    def rp_lku_add_file_to_request(self, file_path=None):
        """ Добавляет вложение в запрос"""
        if not file_path:
            file_path = os.getcwd() + '/test_data/Doc_for_test.txt'
        test_modify_data['file_path'] = file_path
        self.find_and_click(*self.locators.RP_LKU_ADD_ATTACHMENT_TO_REQUEST_LINK)
        self.find_and_click(*self.locators.RP_LKU_ATTACHMENT_ITEM_FILE)
        element = self.search_element(*self.locators.RP_LKU_UPLOAD_FILE)
        drag_and_drop_file(element, file_path)
        self.wait_for_invisibility_element(*self.locators.PROGRESS_BAR)

    def rp_lku_fill_file_and_fields_in_request_other_type(self):
        """метод заполняет поля в запросе типа 'Другое', добавляет файл и сохраняет информацию в request_info_lku"""
        self.rp_lku_add_file_to_request()
        self.ba_lku_wait_for_loading()
        self.rp_lku_fill_req_theme_and_msg()
        self.ba_lku_wait_for_loading()
        self.rp_lku_new_req_create_btn()
        if self.rp_lku_add_ds_modal_win():
            self.rp_lku_add_ds_no_signature_btn()
        self.rp_lku_save_request_hrid_after_create()
        self.rp_lku_get_request_id()


class RequestsPageLKO(ExtendPage):
    """Работа со страницей в разделе 'Запросы' other contour"""

    def rp_lko_goto_requests_page(self):
        """Нажать на кнопку 'Запросы'"""
        self.find_and_click(*self.locators.RP_LKO_REQUESTS_BTN)
        self.ba_wait_for_loading()

    def rp_lko_search_request_fld(self, text):
        """Заполнить поле ввода 'Поиск запросов'"""
        self.find_and_fill_element(text, *self.locators.RP_LKO_SEARCH_REQ_FLD)
        self.log.info("В поле поиска введено: %s" % text)
        self.rp_lko_select_search_element(text)

    def rp_lko_select_search_element(self, text):
        """Выбрать элемент для поиска после ввода данных в поисковую строку"""
        locator = list(self.locators.RP_LKO_SELECT_SEARCH_ELEMENT_PATTERN)
        locator[1] = locator[1].format(text)
        self.log.info("Выбирается элемент в поле поиска с локатором: %s" % locator)
        self.find_and_click(*locator)

    def rp_lko_found_request_with_text(self, text):
        """Найти в списке запросов запрос с 'text'"""
        element = self.search_element(*collect_locator(self.locators.RP_LKO_FOUND_REQ_PATTERN, text))
        return element

    def rp_lko_save_request_hrid_after_create(self):
        """ищет hrid запроса, сохраняет его в request_info_lku и логирует"""
        request_info_lko['hrid'] = None
        self.ba_wait_for_loading()
        for i in range(10):
            if '(ID назначается)' in self.return_text_ele(*self.locators.RP_LKO_REQUEST_HRID):
                if i == 5:
                    self.driver.refresh()
                sleep(0.5)
                continue
            else:
                find_hrid = self.return_text_ele(*self.locators.RP_LKO_REQUEST_HRID)
                request_info_lko['hrid'] = self.rp_return_hrid_for_created_request(find_hrid)
                self.log.info("ID нового запроса: %s" % request_info_lko['hrid'])
                break

    @staticmethod
    def rp_return_hrid_for_created_request(text):
        """обрабатывает строку и возвращает hrid созданного запроса"""
        stop, start = None, None
        for i in text:
            if i == 'R':
                start = text.index(i)
            elif i == ':':
                stop = text.index(i)
        return text[start:stop]

    def rp_lko_get_request_id_from_url(self):
        """Получить id запроса"""
        request_info_lko['id'] = self.driver.current_url.partition('/requests/view/')[2]
        self.log.info('Запросу с hrid "{}" соотвествует guid "{}"'.format(request_info_lko['hrid'],
                                                                          request_info_lko['id']))
        allure.attach(self.driver.current_url, 'Ссылка на запрос', allure.attachment_type.URI_LIST)

    def rp_lko_search_request_after_create_from_lku(self):
        """метод передает в rpu_find_and_fill_search ранее сохраненное значение в классе RequestsPageLKU
        для поиска нужного запроса"""
        self.rp_lko_search_request_fld(request_info_lku['hrid'])

    def rp_lko_get_request_hrid(self, text):
        """Получить hrid найденного запроса"""
        element = self.rp_lko_found_request_with_text(text)
        if element:
            req_hrid = element.text
            self.log.info('Запросу с темой: "{}" назначен hrid: "{}"'.format(text, req_hrid))
            return req_hrid

    def rp_lko_show_request(self):
        """Открыть запрос для просмотра"""
        self.find_and_click(*collect_locator(self.locators.RP_LKO_SHOW_REQ_PATTERN, request_info_lko['hrid']))

    def rp_lko_show_ef_incident(self, ef_num=1, schema_version='custom'):
        """Открыть ЭФ инцидента в запросе для просмотра"""
        if schema_version == 'custom':
            inc_card_locator = self.locators.RP_LKO_VIEW_EF_INCIDENT
        else:
            inc_card_locator = self.locators.RP_LKO_VIEW_NOT_CUSTOM_EF_INCIDENT
        if ef_num == 1:
            self.find_and_click(*inc_card_locator)
            self.ba_wait_for_loading()
        else:
            elements = self.search_elements(*inc_card_locator)
            elements[ef_num - 1].click()
            self.ba_wait_for_loading()

    def rp_lko_download_ef_incident(self):
        """Скачать ЭФ инцидента при просмотре ЭФ"""
        self.find_and_click(*self.locators.RP_LKO_VIEW_EF_INCIDENT_DOWNLOAD_BTN)
        self.ba_check_file(request_info_lku['attach_id'], timeout=10, pattern=True)

    def rp_lko_download_ef_incident_and_check_content(self, schema_version='custom'):
        """Скачать ЭФ инцидента при просмотре ЭФ"""
        self.find_and_click(*self.locators.RP_LKO_VIEW_EF_INCIDENT_DOWNLOAD_BTN)
        self.ba_check_inc_file_content_json(schema=schema_version, timeout=20)

    def rp_lko_new_req_create_btn(self):
        """Нажать на кнопку 'Зарегистрировать запрос'"""
        self._wait_element('clickable', *self.locators.RP_LKO_CREATE_REQUEST_BTN)
        self.find_and_click(*self.locators.RP_LKO_CREATE_REQUEST_BTN)
        self.wait_for_invisibility_element(*self.locators.CIRCULAR_LOADER)

    def rp_lko_new_req_msg_fld(self, text):
        """Заполнить поле ввода 'Написать сообщение...'"""
        self.find_and_fill_element(text, *self.locators.RP_NEW_REQUEST_MESSAGE)

    def rp_lko_new_req_theme_fld(self, text):
        """Заполнить поле ввода 'Тема'"""
        self.find_and_fill_element(text, *self.locators.RP_NEW_REQUEST_THEME)

    def rp_lko_new_req_participant_dropdown(self):
        """Открыть выпадающий список 'Участник'"""
        self.find_and_click(*self.locators.RP_LKO_NEW_REQUEST_PARTICIPANT_DROPDOWN)

    def rp_lko_new_req_find_participant_fld(self, text):
        """
        Выпадающий список 'Участник'
        Заполнить поле ввода 'Быстрый поиск'
        """
        self.find_and_fill_element(text, *self.locators.RP_LKO_NEW_REQUEST_PARTICIPANT_SEARCH)

    def rp_lko_new_req_participant_click(self, text):
        """
        Выпадающий список 'Участник'
        Выбрать найденного участника
        """
        self.find_and_click(*collect_locator(self.locators.RP_LKO_NEW_REQUEST_PARTICIPANT_SEARCH_RESULT_PATTERN, text))

    def rp_lko_new_req_participant_sender_dropdown(self):
        """Открыть выпадающий список 'Отправитель'"""
        self.find_and_click(*self.locators.RP_LKO_NEW_REQUEST_PARTICIPANT_SENDER_DROPDOWN)

    def rp_lko_new_req_participant_sender(self):
        """Выбрать значение в списке 'Отправитель'"""
        elements = self.extract_all_list_items(*self.locators.RP_LKO_NEW_REQUEST_PARTICIPANT_SENDER_LIST_ITEMS_TEXT)
        self.find_and_click(*collect_locator(self.locators.RP_LKO_NEW_REQUEST_PARTICIPANT_SENDER_PATTERN,
                                             choice(elements)))

    def rp_lko_new_req_transport_dropdown(self):
        """Открыть выпадающий список 'Способ получения'"""
        self.find_and_click(*self.locators.RP_LKO_NEW_REQUEST_TRANSPORT_DROPDOWN)

    def rp_lko_new_req_transport(self):
        """Выбрать значение в списке 'Способ получения'"""
        elements = self.extract_all_list_items(*self.locators.RP_LKO_NEW_REQUEST_TRANSPORT_LIST_ITEMS_TEXT)
        self.find_and_click(*collect_locator(self.locators.RP_LKO_NEW_REQUEST_TRANSPORT_PATTERN, choice(elements)))

    def rp_lko_click_status_in_request(self):
        """нажать на кнопку 'статус' в запросе, откроет список со статусами"""
        self.find_and_click(*self.locators.RP_LIST_STATUS_IN_REQUEST)

    @lko_decorator_for_check_emals_in_bd
    def rp_lko_click_on_closed_status_in_request(self, hrid_stand):
        """выбрать статус 'закрытый' у запроса
        ВАЖНО: сначала нужно открыть список со статусами методом rp_lko_click_status_in_request

        :param hrid_stand: откуда брать hrid, н-р, hrid_stand='lku', передается в декоратор
        """
        self.find_and_click(*self.locators.RP_CLOSED_STATUS_IN_LIST_STATUS_IN_REQUEST)

    def rp_lko_select_closed_status_in_request(self):
        """выбрать статус 'закрытый' у запроса
        ВАЖНО: сначала нужно открыть список со статусами методом rp_lko_click_status_in_request"""
        self.find_and_click(*self.locators.RP_CLOSED_STATUS_IN_LIST_STATUS_IN_REQUEST)

    def rp_lko_select_waiting_for_closure_status_in_request(self):
        """выбрать статус 'Ожидает закрытия' у запроса
        ВАЖНО: сначала нужно открыть список со статусами методом rp_lko_click_status_in_request"""
        self.find_and_click(*self.locators.RP_WAITING_FOR_CLOSURE_STATUS_IN_LIST_STATUS_IN_REQUEST)

    def rp_lko_get_request_data(self, req_theme):
        """По теме запроса получить hrid и id апроса"""
        self.ba_wait_for_loading()
        self.mp_lko_click_requests_btn()
        self.rp_lko_search_request_fld(req_theme)
        self.ba_wait_for_loading()
        for _ in range(3):
            request_info_lko['hrid'] = self.rp_lko_get_request_hrid(req_theme)
            if request_info_lko['hrid'] is not None:
                break
            else:
                self.driver.refresh()
                self.ba_wait_for_loading()
        self.ba_wait_for_loading()

        assert request_info_lko['hrid'] is not None,\
            'Ошибка! Запросу с темой: "{}" не назначен hrid'.format(
            request_info_lko['theme'])
        self.rp_lko_get_request_id()

    def rp_lko_get_request_id(self):
        """Получить id запроса"""
        self.ba_wait_for_loading()
        self.rp_lko_show_request()
        request_info_lko['id'] = self.driver.current_url.partition('/requests/view/')[2].split('?')[0]

        assert request_info_lko['id'] is not None, \
            'Ошибка получения id запроса с темой: "{}"'.format(
                request_info_lko['theme'])
        self.log.info('Запросу с hrid "{}" соответствует guid "{}"'.format(request_info_lko['hrid'],
                                                                           request_info_lko['id']))

    def rp_lko_fill_req_theme_and_msg(self):
        """Заполнить тему и текст сообщения в запросе, выбрать отправителя"""
        msg_text = 'UI_автотест_ЛКО_cообщение: ' + string_generator(min_length=10, max_length=50)
        self.rp_lko_new_req_msg_fld(msg_text)
        request_info_lko['theme'] = '[{}] UI_автотест'.format(utc_timestamp(date_format='%Y-%m-%dT%H:%M:%S.%f'))
        self.rp_lko_new_req_theme_fld(request_info_lko['theme'])
        self.rp_lko_new_req_participant_dropdown()
        self.rp_lko_new_req_find_participant_fld('Автотесты_плательщик')
        self.rp_lko_new_req_participant_click('Автотесты_плательщик')
        self.rp_lko_new_req_participant_sender_dropdown()
        self.rp_lko_new_req_participant_sender()
        self.rp_lko_new_req_transport_dropdown()
        self.rp_lko_new_req_transport()

    def rp_lko_expand_request_realtions(self, text):
        """
        Просмотр запроса
        Нажать на кнопку 'клювик' дочернего элемента
        """
        element = collect_locator(self.locators.RP_LKO_CHILD_ELEMENT_EXPAND_PATTERN, text)
        self._wait_element('clickable', *element)
        self.find_and_click(*element)
        self.wait_for_invisibility_element(*self.locators.CIRCULAR_LOADER)

    def rp_random_choose_request(self):
        """метод ищет панель с запросами на странице запросов и рандомно переходит в один из N первых запросов"""
        if self.ba_wait_for_loading():
            self.search_element(*self.locators.RP_PANEL_WITH_REQUESTS)
        random_x = random.randrange(0, 19)
        random_request = self.search_elements(*self.locators.RP_FIRST_22_REQUESTS)[random_x]
        self.log.info("Выбран Запрос, %s" % random_request.text)
        request_info_lko['hrid'] = random_request.text
        random_request.click()

    def rp_click_send_answer_btn(self):
        """метод нажимает кнопку отправить ответ на странице запроса"""
        self.find_and_click(*self.locators.RP_SEND_ANSWER_BTN)
        self.ba_wait_for_loading()

    def rp_send_answer_on_request(self):
        """метод находит текстовое поле ответа на запрос и отправляет рандоную строчку

        :return: str возвращает сгенерированную строчку для сравнения в будущем"""
        r_str = self.generate_str_and_return()
        self.find_and_fill_element(r_str, *self.locators.RP_ANSWER_TEXT_AREA)
        self.rp_click_send_answer_btn()
        return r_str

    @lko_decorator_for_check_emals_in_bd
    def rp_send_answer_on_request_and_check_message(self, hrid_stand):
        """метод находит все сообщения в переписке запроса и проверяет, что последнее соответствует отправленному
        методом rp_send_answer_on_request"""
        all_massages_on_start = self.search_elements(*self.locators.RP_MESSAGES_IN_REQUEST)
        new_message = self.rp_send_answer_on_request()
        self.log.info("Текст отправленного В ЛКОЗ сообщения: %s" % new_message)
        all_massages_after_send = self.search_elements(*self.locators.RP_MESSAGES_IN_REQUEST)
        i = 10
        while len(all_massages_on_start) == len(all_massages_after_send) and i > 0:
            sleep(1)
            i -= 1
            all_massages_after_send = self.search_elements(*self.locators.RP_MESSAGES_IN_REQUEST)
            continue
        text_for_check = all_massages_after_send[-1].find_element_by_xpath('div/div').text
        self.log.info("Текст отображаемого В ЛКОЗ сообщения: %s" % text_for_check)
        assert new_message == text_for_check
        request_info_lko['message'] = text_for_check

    def rp_click_new_request_btn(self):
        """метод нажимает на кнопку 'Направить запрос' на странице запросов"""
        self.find_and_click(*self.locators.RP_NEW_REQUEST_BTN)

    def rp_new_request_find_and_fill_them_area(self):
        """метод заполняет рандомной строкой тему в создании нового запроса"""
        self.req_theme = self.generate_str_and_return()
        self.find_and_fill_element(self.req_theme, *self.locators.RP_NEW_REQ_THEM_AREA)

    def rp_new_request_choose_participant(self):
        """метод выбирает участника 'Автотесты_плательщик' в создании нового запроса"""
        self.find_and_click(*self.locators.RP_NEW_REQ_PARTICIPANT_DROPDOWN)
        self.find_and_fill_element('Автотесты_плательщик', *self.locators.RP_NEW_REQ_PARTICIPANT_QUICK_SEARCH)
        self.find_and_click(*self.locators.RP_NEW_REQ_PARTICIPANT_QUICK_SEARCH_CHOOSE)

    def rp_new_request_fill_answer_area(self):
        """"""
        r_str = self.generate_str_and_return()
        self.find_and_fill_element(r_str, *self.locators.RP_NEW_REQ_ANSWER_AREA)

    def rp_new_request_click_submit_btn(self):
        """метод находит и нажимет кнопку 'Зарегистрировать запрос' в создании нового запроса"""
        self.find_and_click(*self.locators.RP_NEW_REQ_SUBMIT_BTN)

    def rp_lko_request_in_db_emails(self, text, mail='@sptest.ru', quantity_iter=0):
        """метод делает запрос в БД и достает информацию

        :param text: текст для поиска в БД
        :type text: str
        :param mail: email для поиска в БД
        :type mail: str
        :param quantity_iter: len результатов при прошлом запросе
        :type quantity_iter: int
        """
        if not quantity_iter:
            return self.db_client.find_sent_mail(text, mail)
        for i in range(10):
            result = self.db_client.find_sent_mail(text, mail)
            if len(result) > quantity_iter:
                return result
            else:
                self.log.info("Новых сообщений по запросу в БД нет, пробуем еще раз, интерация № %s" % i)
                sleep(5)

    def rp_lko_send_new_request_to_participant_and_check_email_db(self):
        """метод объединяет шаги по созданию запроса из ЛКО участнику и проверку в БД, что сообщение на почту
        было отправлено"""
        self.rp_new_request_find_and_fill_them_area()
        self.rp_new_request_fill_answer_area()
        self.rp_new_request_choose_participant()
        self.rp_lko_new_req_create_btn()
        self.rp_lko_save_request_hrid_after_create()

    def rp_lko_open_request_by_id(self, req_id=None):
        """
        Открывает страницу просмотра запроса по его id

        :param req_id: id запроса, если не указан, берем из test_modify_data
        """
        if not req_id:
            req_id = test_modify_data['req_id']
        url = self.url + '/requests/view/{}'.format(req_id)
        self.log.info('Open page: ' + url)
        allure.attach(url, 'Ссылка на запрос', allure.attachment_type.URI_LIST)
        self.driver.get(url)
        self.ba_wait_for_loading()

    def rp_lko_show_ef_threat(self, ef_num=1):
        """Открыть ЭФ угрозы в запросе для просмотра. Открывает ЭФ с номером ef_num"""
        elements = self.search_elements(*self.locators.RP_LKO_VIEW_EF_THREAT)
        elements[ef_num-1].click()
        self.ba_wait_for_loading()

    def rp_lko_ef_click_create_threat_btn(self):
        """ Кликнуть Перейти к созданию угрозы на ЭФ угрозы """
        self.find_and_click(*self.locators.MW_CREATE_THREAT_BUTTON)
        self.search_element(*self.locators.THP_CREATE_THREAT_PAGE_HEADER)

    def rp_send_new_ef_version_and_check_it(self):
        """ метод кликает по кнопке Добавить к запросу и проверяет, что новая ЭФ появляется """
        all_messages_on_start = self.search_elements(*self.locators.RP_MESSAGES_IN_REQUEST)
        self.rp_click_send_answer_btn()
        for i in range(10):
            self.log.info(f'iteration: {i}')
            all_messages_after_send = self.search_elements(*self.locators.RP_MESSAGES_IN_REQUEST)
            if len(all_messages_after_send) > len(all_messages_on_start):
                break
            sleep(1)
        allure.attach(name='screen', body=self.driver.get_screenshot_as_png(),
                      attachment_type=allure.attachment_type.PNG)
        assert len(all_messages_on_start) < len(all_messages_after_send), 'Не появилось новое сообщение!'

    def rp_lko_show_ef_vulnerability(self, ef_num=1):
        """Открыть ЭФ уязвимости в запросе для просмотра. Открывает ЭФ с номером ef_num"""
        elements = self.search_elements(*self.locators.RP_LKO_VIEW_EF_VULNERABILITY)
        elements[ef_num-1].click()
        self.ba_wait_for_loading()

    def rp_lko_ef_click_create_vulnerability_btn(self):
        """ Кликнуть Перейти к созданию уязвимости на ЭФ уязвимости """
        self.find_and_click(*self.locators.MW_CREATE_VULNERABILITY_BUTTON)
        self.ba_wait_for_loading()
        self.search_element(*self.locators.VP_CREATE_VULNERABILITY_PAGE_HEADER)

    def rp_lko_show_ef_pub(self, ef_num=1):
        """Открыть ЭФ публикации в запросе для просмотра. Открывает ЭФ с номером ef_num"""
        elements = self.search_elements(*self.locators.RP_LKO_VIEW_EF_PUBLICATION)
        elements[ef_num-1].click()
        self.ba_wait_for_loading()

    def rp_lko_ef_click_create_pub_btn(self):
        """ Кликнуть Перейти к созданию публикации на ЭФ публикации """
        self.find_and_click(*self.locators.MW_CREATE_PUBLICATION_BUTTON)
        self.ba_wait_for_loading()
        self.search_element(*self.locators.ICP_CREATE_INFO_CARD_PAGE_HEADER)

    def rp_lko_show_ef_malware_analysis(self, ef_num=1):
        """Открыть ЭФ запроса на анализ ВПО в запросе для просмотра. Открывает ЭФ с номером ef_num"""
        elements = self.search_elements(*self.locators.RP_LKO_VIEW_EF_MALWARE_ANALYSIS)
        elements[ef_num-1].click()
        self.ba_wait_for_loading()

    def rp_lko_show_old_schema_ef_incident(self, ef_num=1):
        """Открыть ЭФ инцидента со старой схемой в запросе для просмотра"""
        elements = self.search_elements(*self.locators.RP_LKO_VIEW_EF_INCIDENT_OLD_SCHEMA)
        elements[ef_num - 1].click()
        self.ba_wait_for_loading()

    def rp_lko_show_transaction_notification_ef(self, ef_num=1):
        """Открыть ЭФ уведомления по Операции в запросе для просмотра"""
        elements = self.search_elements(*self.locators.RP_LKO_VIEW_EF_TRANSACTION_NOTIFICATION)
        elements[ef_num - 1].click()
        self.ba_wait_for_loading()

    def rp_lko_show_ef_lockrequest(self, ef_num=1):
        """
        Открыть ЭФ запроса на блокировку корр.счета в запросе для просмотра.
        Открывает ЭФ с номером ef_num
        """
        elements = self.search_elements(*self.locators.RP_VIEW_EF_LOCKREQUEST)
        elements[ef_num-1].click()
        self.ba_wait_for_loading()

    def rp_lko_show_ef_participant(self, ef_num=1):
        """
        Открыть ЭФ запроса с данными участника
        Открывает ЭФ с номером ef_num
        """
        elements = self.search_elements(*self.locators.RP_VIEW_EF_PARTICIPANT_EDIT)
        elements[ef_num-1].click()
        self.ba_wait_for_loading()

    def rp_check_message_with_text_present(self, expected_text):
        """метод ищет сообщение в запросе с заданным текстом """
        all_messages = self.search_elements(*self.locators.RP_MESSAGES_IN_REQUEST)
        for item in all_messages:
            text_for_check = item.find_element_by_xpath('div/div').text
            self.log.info("Текст отображаемого сообщения: %s" % text_for_check)
            if text_for_check == expected_text:
                self.log.info("Сообщение найдено")
                return
        raise AssertionError(f'Сообщение с текстом {expected_text} не найдено')

    def rp_check_message_with_text_absent(self, expected_text):
        """метод проверяет, что в запросе нет сообщения с заданным текстом """
        all_messages = self.search_elements(*self.locators.RP_MESSAGES_IN_REQUEST)
        for item in all_messages:
            text_for_check = item.find_element_by_xpath('div/div').text
            self.log.info("Текст отображаемого сообщения: %s" % text_for_check)
            assert text_for_check != expected_text, f'Сообщение "{expected_text}" найдено'
        self.log.info(f'Проверка окончена, сообщение с текстом "{expected_text}" отсутствует, как и ожидалось')
