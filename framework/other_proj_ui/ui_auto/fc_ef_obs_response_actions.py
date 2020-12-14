#!/usr/bin/env python
# -*- coding: utf-8 -*-

from framework.other_proj_ui.ui_auto.fc_request_actions import ExtendPage
from tools.utils import passport, inn_entity, get_sha256_hash
from time import sleep
from framework.other_proj_ui.ui_auto.fc_helpers import (
    collect_locator, choose_transfer_state, choose_transfer_suspension, collect_response_params)


class ObsResponseEF(ExtendPage):
    """Работа с модальным окном 'Электронная форма уведомления по Операции'"""

    def mw_obs_response_ready_btn(self):
        """Нажать на кнопку 'Готово'"""
        self.find_and_click(*self.locators.MW_OBS_RESPONSE_READY_BTN)

    def mw_obs_response_choose_company_org_type(self):
        """нажимает на кнопку 'Юридическое лицо' в открытой ЭФ ответ на запрос"""
        self.find_and_click(*self.locators.MW_OBS_RESPONSE_ORG_TYPE_COMPANY)

    def mw_obs_response_choose_individual_org_type(self):
        """нажимает на кнопку 'Физическое лицо' в открытой ЭФ ответ на запрос"""
        self.find_and_click(*self.locators.MW_OBS_RESPONSE_ORG_TYPE_INDIVIDUAL)

    def mw_obs_response_fill_payee_individual_passport_hash(self, text):
        """
        Модальное окно 'Электронная форма уведомления по Операции'
        Заполнить поле ввода 'Хеш-сумма серии и номера паспорта' для ФЛ
        """
        self.find_and_fill_element(text, *self.locators.MW_OBS_RESPONSE_PAYEE_INDIVIDUAL_PASSPORT_HASH)

    def mw_obs_response_fill_org_type_info(self, org_type):
        """ Модальное окно 'Электронная форма уведомления по Операции'
        Выбор типа лица получателя и заполнение обязательных полей в зависимости от типа лица
        """
        if org_type == 'company':
            self.mw_obs_response_choose_company_org_type()
            self.mw_obs_response_fill_payee_inn(inn_entity())
        else:
            self.mw_obs_response_choose_individual_org_type()
            self.mw_obs_response_fill_payee_individual_passport_hash(get_sha256_hash(passport()))

    def mw_obs_response_transfer_suspension_dropdown(self):
        """
        Модальное окно 'Электронная форма уведомления по Операции'
        Открыть выпадающий список 'Статус приостановления перевода'
        """
        self.find_and_click(*self.locators.MW_OBS_RESPONSE_TRANSFER_SUSPENSION_DROPDOWN)

    def mw_obs_response_transfer_suspension(self, transfer_suspension):
        """
        Модальное окно 'Электронная форма уведомления по Операции'
        Выбрать значение в списке 'Статус приостановления перевода'
        """
        transfer_suspension_text = choose_transfer_suspension(transfer_suspension)
        locator = collect_locator(self.locators.MW_OBS_RESPONSE_TRANSFER_SUSPENSION_PATTERN,
                                  transfer_suspension_text)
        self.find_and_click(*locator)

    def mw_obs_response_transfer_state_dropdown(self):
        """
        Модальное окно 'Электронная форма уведомления по Операции'
        Открыть выпадающий список 'Статус подтверждения перевода'
        """
        self.find_and_click(*self.locators.MW_OBS_RESPONSE_TRANSFER_STATE_DROPDOWN)

    def mw_obs_response_transfer_state(self, transfer_state):
        """
        Модальное окно 'Электронная форма уведомления по Операции'
        Выбрать значение в списке 'Статус подтверждения перевода'
        """
        transfer_state_text = choose_transfer_state(transfer_state)
        locator = collect_locator(self.locators.MW_OBS_RESPONSE_TRANSFER_STATE_PATTERN,
                                  transfer_state_text)
        self.find_and_click(*locator)

    def mw_obs_response_fill_obs_response(self):
        """Заполнение обязательных полей ЭФ уведомления по операции"""
        response_params = collect_response_params()
        self.mw_obs_response_fill_org_type_info(response_params['org_type'])
        self.mw_obs_response_transfer_suspension_dropdown()
        self.mw_obs_response_transfer_suspension(response_params['transfer_suspension'])
        self.mw_obs_response_transfer_state_dropdown()
        self.mw_obs_response_transfer_state(response_params['transfer_state'])
        self.mw_obs_response_ready_btn()
        self.wait_for_invisibility_element(*self.locators.CIRCULAR_LOADER)

    def mw_obs_response_fill_payee_inn(self, inn=None):
        """Заполняет поле ИНН в открытой ЭФ ответ на запрос"""
        if not inn:
            inn = inn_entity()
        sleep(1)
        self.find_and_clear_element(*self.locators.MW_OBS_RESPONSE_PAYEE_INN)
        self.find_and_fill_element(inn, *self.locators.MW_OBS_RESPONSE_PAYEE_INN)

    def mw_obs_response_choose_status_transfer_suspended(self):
        """Выбирвает Приостоновлен в 'Статус приостановления перевода' в открытой ЭФ ответ на запрос"""
        self.find_and_click(*self.locators.MW_OBS_RESPONSE_STATUS_SUSP_TRANSFER_SUSPENDED)

    def mw_obs_response_choose_status_confirmation_no_info(self):
        """Выбирает Нет информации в 'Статус подтверждения перевода' в открытой ЭФ ответ на запрос"""
        self.find_and_click(*self.locators.MW_OBS_RESPONSE_STATUS_CONFIRMATION_TRANSFER_NO_INFO)

    def mw_obs_response_click_create_new_version_btn(self):
        """ Нажимает кнопку Создать новую версию"""
        self.find_and_click(*self.locators.MW_OBS_RESPONSE_CREATE_NEW_VERSION)
