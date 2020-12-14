#!/usr/bin/env python
# -*- coding: utf-8 -*-

from framework.ui_libs.ui_lib import Page
from tools.utils import now_timestamp
from configs.modify_data import test_modify_data
from framework.other_proj_ui.ui_auto.fc_helpers import decorator_for_change_selenium_wait_and_return_after
from configs.dictionary_variables import pub_event_type
from base64 import b64decode


class PubEF(Page):
    """ Класс для работы с ЭФ публикации """

    def pb_ef_click_new_ef_version_btn(self):
        """ метод кликает по кнопке 'Создать новую версию' в ЭФ """
        self.find_and_click(*self.locators.MW_NEW_PUBLICATION_EF_VERSION_BUTTON)
        self.ba_lku_wait_for_loading()
        self.search_element(*self.locators.MW_EDIT_PUBLICATION_MODAL)

    def pb_ef_fill_publication_name(self, text):
        """ метод заполняет поле Наименование мероприятия """
        self.find_and_clear_element(*self.locators.MW_EDIT_PUBLICATION_MODAL_NAME_INPUT)
        self.find_and_fill_element(text, *self.locators.MW_EDIT_PUBLICATION_MODAL_NAME_INPUT)

    def pb_ef_fill_publication_description(self, text):
        """ метод заполняет поле Описание уязвимости и способов ее использования  """
        self.find_and_clear_element(*self.locators.MW_EDIT_PUBLICATION_MODAL_DESCRIPTION_INPUT)
        self.find_and_fill_element(text, *self.locators.MW_EDIT_PUBLICATION_MODAL_DESCRIPTION_INPUT)

    def pb_ef_click_add_to_request_btn(self):
        """ метод кликает кнопку Добавить к запросу  """
        self.find_and_click(*self.locators.MW_EDIT_PUBLICATION_MODAL_ADD_BTN)
        self.ba_lku_wait_for_loading()

    def pb_ef_edit_fields_and_save_new_version(self):
        """ метод изменяет значения в полях Наименование мероприятия и Описание и сохраняет новую версию ЭФ
        ЭФ для редактирования должны быть уже открыта """
        test_modify_data['pub_edit_name'] = 'Публикация ред ' + now_timestamp()
        test_modify_data['pub_edit_description'] = 'Описание ред ' + now_timestamp()
        self.pb_ef_fill_publication_name(test_modify_data['pub_edit_name'])
        self.pb_ef_fill_publication_description(test_modify_data['pub_edit_description'])
        self.pb_ef_click_add_to_request_btn()

    def pb_ef_click_even_link_on_ef(self):
        """ метод кликает ссылку Мероприятие """
        self.find_and_click(*self.locators.MW_VIEW_PUBLICATION_NAV_BAR_EVENT)
        self.ba_lku_wait_for_loading()

    def pb_ef_check_add_new_version_btn_absent(self):
        """ метод проверяет, что кнопка Создать новую версию отсутствует"""
        try:
            elems = self.search_elements(*self.locators.MW_NEW_PUBLICATION_EF_VERSION_BUTTON)
            if elems:
                test_modify_data['errors'].append('Кнопка "Создать новую версию" отображается, хотя должна '
                                                  'отсутствовать')
        except:
            self.log.info('Кнопка "Создать новую версию" отсутствует, как ожидалось')

    def pb_ef_close_btn(self):
        """ Нажать на кнопку 'Крестик' (Закрыть) """
        self.find_and_click(*self.locators.MW_VIEW_PUBLICATION_EF_CLOSE_BTN)

    def pb_ef_click_insert_changes_btn(self):
        """ метод нажимает кнопку Внести изменения """
        self.find_and_click(*self.locators.MW_VIEW_PUBLICATION_EF_INSERT_CHANGES_BTN)
        self.ba_wait_for_loading()

    def pb_ef_compare_send_data_with_ef_data(self, send_data=None):
        self.pb_ef_compare_ef_and_send_data_common_info(send_data)
        self.pb_ef_click_even_link_on_ef()
        self.ba_lku_wait_for_loading()
        self.pb_ef_compare_ef_and_send_data_event_info(send_data)

    @decorator_for_change_selenium_wait_and_return_after(5)
    def pb_ef_compare_ef_and_send_data_event_info(self, send_data=None):
        """ метод сравнивает данные в ЭФ и отосланные данные на вкладке Мероприятие """
        if not send_data:
            send_data = test_modify_data['pub_data'][0]['pub']

        event_type = self.ba_return_elem_text_or_none(*self.locators.MW_VIEW_PUBLICATION_EVENT_TYPE)
        if event_type != pub_event_type[send_data['typeofActivity'][0]]:
            test_modify_data['errors'].append(f"Не совпадает 'Тип мероприятия' в ЭФ на {self.stand}: "
                                              f"ожидаемое {pub_event_type[send_data['typeofActivity'][0]]}, "
                                              f"отображаемое {event_type}")

        event_text = self.ba_return_elem_text_or_none(*self.locators.MW_VIEW_PUBLICATION_EVENT_TEXT)
        if event_text != send_data['text']:
            test_modify_data['errors'].append(f"Не совпадает 'Текст мероприятия' в ЭФ на {self.stand}: "
                                              f"ожидаемое {send_data['text']}, отображаемое {event_text}")

        file_name = self.ba_return_elem_text_or_none(*self.locators.MW_VIEW_PUBLICATION_FILE)
        send_name = send_data['messageAttachment']['file']['name']
        if file_name != send_name:
            test_modify_data['errors'].append(f"Не совпадает 'Вложение' в ЭФ на {self.stand}: "
                                              f"ожидаемое {send_name}, отображаемое {file_name}")

    def pb_ef_check_file_presence(self):
        """ проверить наличие файла в ЭФ """
        send_data = test_modify_data['pub_data'][0]['pub']
        file_name = self.ba_return_elem_text_or_none(*self.locators.MW_VIEW_PUBLICATION_FILE)
        send_name = send_data['messageAttachment']['file']['name']
        if file_name != send_name:
            test_modify_data['errors'].append(f"Не совпадает 'Вложение' в ЭФ на {self.stand}: "
                                              f"ожидаемое {send_name}, отображаемое {file_name}")

    def pb_ef_download_file(self):
        """ скачать файл """
        self.find_and_click(*self.locators.MW_VIEW_PUBLICATION_FILE)
        self.ba_confirm_file_download()

    def pb_ef_check_downloaded_file(self):
        """ проверить содержимое файла """
        send_name = test_modify_data['pub_data'][0]['pub']['messageAttachment']['file']['name']
        content = b64decode(test_modify_data['pub_data'][0]['pub']['messageAttachment']['file']['base64']) \
            .decode(encoding='utf8')
        self.ba_check_file_content(send_name, content, delete=False)

    def pb_ef_download_file_and_check_it(self):
        """ скачать и проверить файл """
        self.pb_ef_download_file()
        self.pb_ef_check_downloaded_file()
