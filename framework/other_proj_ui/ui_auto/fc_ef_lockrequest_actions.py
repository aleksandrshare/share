#!/usr/bin/env python
# -*- coding: utf-8 -*-

from framework.ui_libs.ui_lib import Page
from configs.modify_data import test_modify_data
from random import choice


class LockRequestEF(Page):

    def lr_lko_mw_click_create_lockrequest_response_btn(self):
        """ Кликнуть на кнопку Создать отчет о блокировке """
        self.find_and_click(*self.locators.MW_VIEW_LOCKREQUEST_RESPONSE_BTN)
        self.ba_wait_for_loading()

    def lr_lko_mw_click_add_to_request_btn(self):
        """ метод кликает кнопку Добавить к запросу  """
        self.find_and_click(*self.locators.MW_VIEW_LOCKREQUEST_ADD_BTN)
        self.ba_wait_for_loading()

    def lr_find_all_requests_edit_btn(self):
        """
        Находит все кнопки "Карандаш" для редактирования заявок
        приложенных к запросу на вкладке 'Заявки'
        """
        return self.search_elements(*self.locators.MW_VIEW_LOCKREQUEST_REQUEST_EDIT_BTN)

    def lr_find_all_requests_hypertext(self):
        """
        Находит все гиперссылки на заявки
        приложенные к запросу на вкладке 'Заявки'
        """
        return self.search_elements(*self.locators.MW_VIEW_LOCKREQUEST_REQUESTS)

    def lr_ef_compare_send_data_with_ef_data(self, send_data=None):
        """
        Сравнение данных, отправленных по API с отображаемыми в UI
        """
        lockrequest_requests = self.lr_find_all_requests_hypertext()

        for i in range(len(lockrequest_requests)):
            lockrequest_requests[i].click()
            self.lr_ef_compare_ef_and_send_data_common_info(send_data, i)
            self.find_and_click(*self.locators.MW_VIEW_LOCKREQUEST_PERSON_TAB)
            self.lr_ef_compare_ef_and_send_data_person_info(send_data, i)
            self.find_and_click(*self.locators.MW_VIEW_LOCKREQUEST_REQUEST_CLOSE)

    def lr_ef_edit_default_response(self, req_state):
        """
        Редактирование параметров ответа на запрос блокировки корр.счета
        """
        lockrequest_requests_edit = self.lr_find_all_requests_edit_btn()
        if not req_state:
            req_state = []
            states = ['Одобрено', 'Не обработано', 'Отказано']
            for _ in range(len(lockrequest_requests_edit)):
                req_state.append(choice(states))
            test_modify_data['lockrequest_response_state'] = req_state

        for i in range(len(lockrequest_requests_edit)):
            lockrequest_requests_edit[i].click()
            if req_state[i] == 'Одобрено':
                self.find_and_click(*self.locators.MW_EDIT_LOCKREQUEST_RESPONSE_STATE_ACCEPTED)
            elif req_state[i] == 'Отказано':
                self.find_and_click(*self.locators.MW_EDIT_LOCKREQUEST_RESPONSE_STATE_REJECTED)
            self.find_and_click(*self.locators.MW_EDIT_LOCKREQUEST_RESPONSE_SAVE_BTN)
            self.ba_wait_for_loading()

    def lr_check_lockrequest_requests_statuses(self):
        """Проверка статусов заявок на блокировку корр.счета в ответе"""
        badges_list = self.search_elements(*self.locators.MW_EDIT_LOCKREQUEST_RESPONSE_STATE_BADGE)
        for i in range(len(badges_list)):
            if test_modify_data['lockrequest_response_state'][i] != badges_list[i].text:
                test_modify_data['errors'].append(f"В заявке №{i + 1} не совпадает 'Статус заявки' "
                                                  f"в ответе на запрос  на {self.stand}: ожидаемое "
                                                  f"{test_modify_data['lockrequest_response_state'][i]}, "
                                                  f"отображаемое {badges_list[i].text}")

    def lr_lko_create_lockrequest_response(self, req_state=None):
        """
        Создать ответ на запрос блокировки корр. счета

        :param req_state: статус заявки, можно задать списком ['accepted', 'undefined', 'rejected']
        """
        self.lr_lko_mw_click_create_lockrequest_response_btn()
        self.lr_ef_edit_default_response(req_state)
        self.lr_lko_mw_click_add_to_request_btn()

    def lr_ef_close_btn(self):
        """ Нажать на кнопку 'Крестик' (Закрыть) """
        self.find_and_click(*self.locators.MW_VIEW_LOCKREQUEST_EF_CLOSE_BTN)

    def lr_compare_downloaded_lockrequest_response_with_ui(self, response_attach):
        """ сравнивает полученную по апи ЭФ ответа с данными, которые отображаются в UI
        """
        lockrequest_requests = self.lr_find_all_requests_hypertext()
        lockrequest_requests[0].click()
        self.lr_ef_compare_response_api_and_ui_data_common_info(response_attach)
        self.find_and_click(*self.locators.MW_VIEW_LOCKREQUEST_PERSON_TAB)
        self.lr_ef_compare_response_api_and_ui_data_person_info(response_attach)
        self.find_and_click(*self.locators.MW_VIEW_LOCKREQUEST_REQUEST_CLOSE)
