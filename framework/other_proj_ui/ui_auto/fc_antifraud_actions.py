#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ui_library.ui_lib import Page
from time import sleep
from framework.other_proj_ui.ui_auto.fc_helpers import decorator_for_change_selenium_wait_and_return_after
from configs.modify_data import test_modify_data
from tools.utils import get_jpath_value
import allure


class AntifraudPage(Page):
    """"""
    def ap_check_generate_status_fids(self):
        """"""
        for i in range(5):
            text_status_inn_fid = self.return_text_ele(*self.locators.AP_GENERATE_STATUS_FOR_INN_RECIPIENT)
            if 'Выполнен' in text_status_inn_fid:
                return True
            else:
                sleep(1)
                continue

    def ap_check_status_fids_and_click_generate_fids_btn(self):
        """"""
        if self.ap_check_generate_status_fids():
            self.ap_click_generate_fids_btn()

    @decorator_for_change_selenium_wait_and_return_after(60)
    def ap_check_clickable_generate_fids_btn(self):
        """"""
        if self._wait_element('clickable', *self.locators.AP_GENERATE_FIDS_BTN):
            if self.ap_check_generate_status_fids():
                self.log.info("генерация фидов окончена, статус 'Выполнена'")

    def ap_click_generate_fids_btn(self):
        """нажать кнопку 'сформировать '"""
        self.find_and_click(*self.locators.AP_GENERATE_FIDS_BTN)

    def ap_click_publish_fids_btn(self):
        """нажать кнопку 'опубликовать '"""
        self.find_and_click(*self.locators.AP_PUBLISH_FIDS_BTN)

    def ap_check_status_publish_fids(self):
        """находит статус публикации и возвращает ее

        :return: str
        """
        return self.return_text_ele(*self.locators.AP_PUBLISH_STATUS_FOR_INN_RECIPIENT)

    def ap_check_date_publish_feeds(self):
        """находит дату публикации ИНН и возвращает ее"""
        return self.return_text_ele(*self.locators.AP_PUBLISH_DATE_FOR_INN_RECIPIENT)

    @decorator_for_change_selenium_wait_and_return_after(40)
    def ap_click_publish_and_check_status_date_publish_fids_inn(self):
        """нажимает кнопку 'опубликовать', сравнивает дату публикации, и проверяет статус"""
        status_before = self.ap_check_status_publish_fids()
        self.log.info("feeds publish status before %s" % status_before)
        date_before = self.ap_check_date_publish_feeds()
        self.log.info("дата до начала публикации:  %s" % date_before)
        self.ap_click_publish_fids_btn()
        sleep(1)
        if self._wait_element('clickable', *self.locators.AP_PUBLISH_FIDS_BTN):
            self.log.info("кнопка опубликовать кликабельна")
            for i in range(10):  # данный слип вынужденный, т.к. дата на фронте обновляется дольше нужного
                date_after = self.ap_check_date_publish_feeds()
                if date_after != date_before:
                    self.log.info("feeds publish date after %s" % date_after)
                    break
                else:
                    self.log.info("feeds publish date after %s" % date_after)
                    sleep(1)
                    continue
            assert date_before != date_after
            assert 'Выполнен' in self.ap_check_status_publish_fids()

    def ap_open_obs_by_id(self, obs_id):
        url = '{}/antifraud/view/{}'.format(self.url, obs_id)
        self.log.info("Open page: %s" % url)
        self.driver.get(url)
        allure.attach(url, 'Ссылка на обс', allure.attachment_type.URI_LIST)
        self.ba_simple_wait_for_loading()

    def ap_click_payer_info_link(self):
        self.find_and_click(*self.locators.AP_ANTIFRAUD_VIEW_PAYER_INFO_LINK)

    def ap_check_payer_passport_hashes(self, schema):
        if schema == '2_1':
            payer_hashes = get_jpath_value(test_modify_data['attach_data'], '$.[*].payer.hash')
        else:
            payer_hashes = get_jpath_value(test_modify_data['attach_data'], '$.[*].payer.hashes')
        elems = self.search_elements(*self.locators.AP_ANTIFRAUD_VIEW_PAYER_PASSPORT_HASHES)
        obs_hashes = list()
        for item in elems:
            obs_hashes.append(item.text.strip())
        if schema == '2_1':
            assert payer_hashes in obs_hashes, f"{payer_hashes} не найден в хешах паспорта плательщика"
        else:
            for item in payer_hashes:
                if item.get('hash'):
                    assert item['hash'].lower() in obs_hashes, f"{item['hash']} не найден в хешах паспорта плательщика"

    def ap_check_payer_snils_hashes(self, schema):
        if schema == '2_1':
            payer_hashes = get_jpath_value(test_modify_data['attach_data'], '$.[*].payer.hashSnils')
        else:
            payer_hashes = get_jpath_value(test_modify_data['attach_data'], '$.[*].payer.hashes')
        elems = self.search_elements(*self.locators.AP_ANTIFRAUD_VIEW_PAYER_SNILS_HASHES)
        obs_hashes = list()
        for item in elems:
            obs_hashes.append(item.text.strip())
        if schema == '2_1':
            assert payer_hashes in obs_hashes, f"{payer_hashes} не найден в хешах паспорта плательщика"
        else:
            for item in payer_hashes:
                if item.get('hashSnils'):
                    assert item['hashSnils'].lower() in obs_hashes, f"{item['hashSnils']} не найден в хешах снилс плательщика"

    def ap_click_analitic_form_link(self):
        self.find_and_click(*self.locators.AP_ANTIFRAUD_VIEW_ANALITIC_FORM_LINK)
        self.ba_simple_wait_for_loading()

    def ap_check_checkbox_checked_for_new_receiver(self):
        class_attr = self.return_attrs_element('class',
                                               *self.locators.AP_ANTIFRAUD_VIEW_ANALITIC_FORM_NEW_RECEIVER_CHECKBOX)
        if 'fa-check-square-o' not in class_attr:
            allure.attach(name='screen', body=self.driver.get_screenshot_as_png(),
                          attachment_type=allure.attachment_type.PNG)
            raise AssertionError('Чек-бокс для значения newReceiver не выбран')

    def ap_check_checkbox_checked_for_cross_country(self):
        class_attr = self.return_attrs_element('class',
                                               *self.locators.AP_ANTIFRAUD_VIEW_ANALITIC_FORM_CROSS_COUNTRY_CHECKBOX)
        if 'fa-check-square-o' not in class_attr:
            allure.attach(name='screen', body=self.driver.get_screenshot_as_png(),
                          attachment_type=allure.attachment_type.PNG)
            raise AssertionError('Чек-бокс для значения crossCountry не выбран')

    def ap_check_checkbox_checked_for_low_time_interval(self):
        class_attr = self.return_attrs_element('class',
                                               *self.locators.AP_ANTIFRAUD_VIEW_ANALITIC_FORM_LOW_TIME_INTERVAL_CHECKBOX)
        if 'fa-check-square-o' not in class_attr:
            allure.attach(name='screen', body=self.driver.get_screenshot_as_png(),
                          attachment_type=allure.attachment_type.PNG)
            raise AssertionError('Чек-бокс для значения lowTimeInterval не выбран')

    def ap_check_checkbox_checked_for_odd_place(self):
        class_attr = self.return_attrs_element('class',
                                               *self.locators.AP_ANTIFRAUD_VIEW_ANALITIC_FORM_ODD_PLACE_CHECKBOX)
        if 'fa-check-square-o' not in class_attr:
            allure.attach(name='screen', body=self.driver.get_screenshot_as_png(),
                          attachment_type=allure.attachment_type.PNG)
            raise AssertionError('Чек-бокс для значения oddPlace не выбран')

    def ap_click_payee_info_link(self):
        self.find_and_click(*self.locators.AP_ANTIFRAUD_VIEW_PAYEE_INFO_LINK)

    def ap_check_payee_passport_hashes(self):
        payee_hashes = get_jpath_value(test_modify_data['responses'], '$.[*].payee.hashes')
        elems = self.search_elements(*self.locators.AP_ANTIFRAUD_VIEW_PAYEE_PASSPORT_HASHES)
        obs_hashes = list()
        for item in elems:
            obs_hashes.append(item.text.strip())
        for item in payee_hashes:
                if item.get('hash'):
                    assert item['hash'].lower() in obs_hashes, f"{item['hash']} не найден в хешах паспорта получателя"

    def ap_check_payee_snils_hashes(self):
        payee_hashes = get_jpath_value(test_modify_data['responses'], '$.[*].payee.hashes')
        elems = self.search_elements(*self.locators.AP_ANTIFRAUD_VIEW_PAYEE_SNILS_HASHES)
        obs_hashes = list()
        for item in elems:
            obs_hashes.append(item.text.strip())
        for item in payee_hashes:
            if item.get('hashSnils'):
                assert item['hashSnils'].lower() in obs_hashes, f"{item['hashSnils']} не найден в хешах снилс получателя"

    def ap_check_payee_org_type(self, expected_type):
        payee_type = self.search_element(*self.locators.AP_ANTIFRAUD_VIEW_PAYEE_ORG_TYPE).text
        assert payee_type == expected_type, f'Не совпадает тип лица, ожидаемое: {expected_type}, отображаемое {payee_type}'

    def ap_check_payee_inn(self, inn=None):
        if not inn:
            inn = get_jpath_value(test_modify_data['responses'], '$.[*].payee.inn')
        payee_inn = self.search_element(*self.locators.AP_ANTIFRAUD_VIEW_PAYEE_INN).text
        assert payee_inn == inn, f'Не совпадает тип лица, ожидаемое: {inn}, отображаемое {payee_inn}'

    def ap_click_transfer_info_link(self):
        self.find_and_click(*self.locators.AP_ANTIFRAUD_VIEW_TRANSFER_INFO_LINK)

    def ap_check_transfer_state(self, expected_value):
        transfer_state = self.search_element(*self.locators.AP_ANTIFRAUD_VIEW_PAYEE_TRANSFER_STATE).text
        assert transfer_state == expected_value, f'Не совпадает Статус подтверждения перевода, ' \
                                                 f'ожидаемое: {expected_value}, отображаемое {transfer_state}'

    def ap_check_transfer_suspension(self, expected_value):
        transfer_suspension = self.search_element(*self.locators.AP_ANTIFRAUD_VIEW_PAYEE_TRANSFER_SUSPENSION).text
        assert transfer_suspension == expected_value, f'Не совпадает Статус приостановления перевода, ' \
                                                 f'ожидаемое: {expected_value}, отображаемое {transfer_suspension}'

    def ap_click_legitimacy_criteria_link(self):
        self.find_and_click(*self.locators.AP_ANTIFRAUD_VIEW_LEGITIMACY_CRITERIA_LINK)

    def ap_check_checkbox_checked_for_large_trading_network(self):
        class_attr = self.return_attrs_element(
            'class', *self.locators.AP_ANTIFRAUD_VIEW_LEGITIMACY_CRITERIA_FORM_LARGE_TRADING_NETWORK_CHECKBOX)
        if 'fa-check-square-o' not in class_attr:
            allure.attach(name='screen', body=self.driver.get_screenshot_as_png(),
                          attachment_type=allure.attachment_type.PNG)
            raise AssertionError('Чек-бокс для значения largeTradingNetwork не выбран')

    def ap_check_checkbox_checked_for_regular_receiver(self):
        class_attr = self.return_attrs_element(
            'class', *self.locators.AP_ANTIFRAUD_VIEW_LEGITIMACY_CRITERIA_REGULAR_RECEIVER_CHECKBOX)
        if 'fa-check-square-o' not in class_attr:
            allure.attach(name='screen', body=self.driver.get_screenshot_as_png(),
                          attachment_type=allure.attachment_type.PNG)
            raise AssertionError('Чек-бокс для значения regularReceiver не выбран')

    def ap_check_checkbox_checked_for_regular_operations(self):
        class_attr = self.return_attrs_element(
            'class', *self.locators.AP_ANTIFRAUD_VIEW_LEGITIMACY_CRITERIA_FORM_REGULAR_OPERATIONS_CHECKBOX)
        if 'fa-check-square-o' not in class_attr:
            allure.attach(name='screen', body=self.driver.get_screenshot_as_png(),
                          attachment_type=allure.attachment_type.PNG)
            raise AssertionError('Чек-бокс для значения regularOperations не выбран')

    def ap_check_checkbox_checked_for_other_accounts(self):
        class_attr = self.return_attrs_element(
            'class', *self.locators.AP_ANTIFRAUD_VIEW_LEGITIMACY_CRITERIA_FORM_OTHER_ACCOUNTS_CHECKBOX)
        if 'fa-check-square-o' not in class_attr:
            allure.attach(name='screen', body=self.driver.get_screenshot_as_png(),
                          attachment_type=allure.attachment_type.PNG)
            raise AssertionError('Чек-бокс для значения otherAccounts не выбран')