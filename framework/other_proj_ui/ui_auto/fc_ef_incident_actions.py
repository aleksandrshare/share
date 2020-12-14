#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from selenium.webdriver.common.by import By
from framework.other_proj_ui.ui_auto.fc_request_actions import ExtendPage
from tools.utils import (
    inn_individual, passport, snils, random_url, string_generator, inn_entity, random_email,
    get_sha256_hash, bank_account, payment_card, random_ipv4, random_domain, utc_timestamp,
)
import string
from ui_library.dad_file_with_js import drag_and_drop_file
import os
from time import sleep
from random import choice, randint
from configs.modify_data import shared_obs_info, request_info_lku, participants_params_payee, participants_params_payer
from framework.other_proj_ui.ui_auto.fc_helpers import (
    collect_locator, choose_inc_vector_and_type, choose_law_enforcement_req_type, detected_by_value, get_antifraud_type,
    collect_inc_param, collect_obs_param
)


class ModalWinNewIncidentEF(ExtendPage):
    """"""
    inc_params = None
    obs_params = shared_obs_info
    response_params = None
    MALWARE_RAR = os.getcwd() + '/test_data/Doc_for_test.txt'
    MALWARE_EMAIL = os.getcwd() + '/test_data/Test_file.txt'
    ATTACHMENT = os.getcwd() + '/test_data/Doc_for_test.txt'

    def mw_increasing_counter_for_obs_locators(self):
        """
        Метод предназначен для форматирование строковых значений в классе локаторов, перед началом работы с локаторыми
        переопределяет переменную locators с помощью метода mw_overloading_locators, далее ищет все локаторы,
        имя которых содержит OBS и после форматирует их добавляя counter из словаря obs_params.
        Используется для создания нескольких ОБС в одном инциденте.
        """
        self.bp_reloading_locators()
        new_atr = list(self.locators.__class__.__base__.__dict__.keys())
        new_atr = [i for i in new_atr if "OBS" in i]
        for i in new_atr:
            if 'datetime' in self.locators.__class__.__base__.__dict__[i][1]:
                self.locators.__class__.__setattr__(self.locators, i,
                      (By.XPATH, self.locators.__getattribute__(i)[1].format(self.obs_params['counter'],
                                                                             self.obs_params['payer_type'])))
            elif '{}' in self.locators.__class__.__base__.__dict__[i][1]:
                self.locators.__class__.__setattr__(self.locators, i,
                                (By.XPATH, self.locators.__getattribute__(i)[1].format(self.obs_params['counter'])))
        self.log.info("Форматирование локаторов для ОБС, счетчик: %s" % self.obs_params['counter'])

    def mw_inc_all_dropdown_lists_choose_value(self, list_of_values, search_text):
        """
        метод выбирает в любой выпадашке электронной формы искомый пункт
        принимает список веб элементов и строку, которую необходмо выбрать

        :param list_of_values: список веб элементов
        :param search_text: строка (название пункта в выпадашке)
        """
        for selected_value in list_of_values:
            if selected_value.text == search_text:
                selected_value.click()
                break
        self.log.info("выбрано значение %s в выпадаеющем списке" % search_text)

    def mw_inc_ef_goto_tab(self, tab_text):
        """
        Переход по вкладкам

        :param tab_text: текст на вкладке модального окна
        """
        tab_locator = collect_locator(self.locators.MW_NEW_EF_INCIDENT_TAB_PATTERN, tab_text)
        self.find_and_click(*tab_locator)

    def mw_inc_menu_click_obs_btn(self):
        """
        Меню ЭФ нажать кнопку "Операции без согласия"
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCIDENT_MENU_OBS_BTN)

    def mw_inc_ef_continue_btn(self):
        """Нажать на кнопку 'Продолжить'"""
        self.find_and_click(*self.locators.MW_NEW_EF_INCIDENT_CONTINUE)

    def mw_inc_ef_save_btn(self):
        """Нажать на кнопку 'Сохранить'"""
        self.find_and_click(*self.locators.MW_SAVE_DRAFT_BTN)

    def mw_inc_ef_ready_btn(self):
        """Нажать на кнопку 'Готово'"""
        self.find_and_click(*self.locators.MW_READY_BTN)

    def mw_inc_ef_close_btn(self):
        """Нажать на кнопку 'Крестик' (Закрыть)"""
        self.find_and_click(*self.locators.MW_NEW_EF_INCIDENT_CLOSE)

    def mw_inc_ef_accept_close_btn(self):
        """Нажать на кнопку 'Да' для подтверждения закрытия модального окна"""
        self.find_and_click(*self.locators.MW_NEW_EF_INCIDENT_ACCEPT_CLOSE)

    def mw_inc_ef_cancel_close_btn(self):
        """Нажать на кнопку 'Отмена' для подтверждения закрытия модального окна"""
        self.find_and_click(*self.locators.MW_NEW_EF_INCIDENT_CANCEL_CLOSE)

    def mw_inc_ef_menu_click_results_btn(self):
        """
        Меню ЭФ инцендента
        нажать кнопку 'Итоги'
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCINDENT_RESULTS_BTN)

    def mw_inc_ef_results_click_damage_type_dropdown(self):
        """
        Раздел 'Итоги'
        нажать вып. список 'Тип ущерба'
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCINDENT_RESULTS_DAMAGE_TYPE_DROPDOWN)

    def mw_inc_ef_results_choose_damage_type(self):
        """
        Раздел 'Итоги'
        выбрать 'Тип ущерба' == Операционные расходы
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCINDENT_RESULTS_DAMAGE_TYPE_OPERATION_EX)

    def mw_open_assistance_dropdown(self):
        """открывает выпадашку 'Помощь' """
        self.find_and_click(*self.locators.MW_NEW_EF_INCIDENT_ASSISTANCE_DROPDOWN)

    def mw_inc_ef_assistance_need_btn(self):
        """
        Вкладка 'Общие сведения'
        Нажать на кнопку 'Требуется' в разделе 'Помощь'
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCIDENT_ASSISTANCE_NEED_BTN)

    def mw_inc_ef_assistance_nnd_btn(self):
        """
        Вкладка 'Общие сведения'
        Нажать на кнопку 'Не требуется' в разделе 'Помощь'
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCIDENT_ASSISTANCE_NND_BTN)

    def mw_inc_ef_description_fld(self, text):
        """
        Вкладка 'Общие сведения'
        Заполнить поле ввода 'Описание инцидента'
        """
        self.find_and_clear_element(*self.locators.MW_NEW_EF_INCIDENT_DESCRIPTION)
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_INCIDENT_DESCRIPTION)

    def mw_inc_ef_vector_dropdown(self):
        """
        Вкладка 'Общие сведения'
        Открыть список 'Вектор атаки'
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCIDENT_TYPE_DROPDOWN)

    def mw_inc_ef_attack_type_dropdown(self):
        """
        Вкладка 'Общие сведения'
        Открыть список 'Тип атаки'
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCIDENT_ATTACK_TYPE_DROPDOWN)

    def mw_inc_ef_choose_vector(self, vector):
        """
        Вкладка 'Общие сведения'
        Выбирает вектор атаки EXT или INT

        :param vector: 'Направлен на клиента участника' или 'Направлен на инфраструктуру участника'
        """
        locator = list(self.locators.MW_NEW_EF_INCENDENT_VECTOR_TYPE_CHOOSE)
        locator[1] = locator[1].format(vector)
        self.find_and_click(*locator)

    def mw_inc_ef_choose_attack_type(self, chosen_type):
        """
        Вкладка 'Общие сведения'
        Выбирает тип актаки из списка в функции choose_inc_vector_and_type

        :param chosen_type: значения берутся из диктов функции choose_inc_vector_and_type
        """
        locator = list(self.locators.MW_NEW_EF_INCENDENT_ATTACK_TYPE_CHOOSE)
        locator[1] = locator[1].format(chosen_type)
        self.find_and_click(*locator)

    def mw_inc_ef_type(self, inc_vector, inc_type):
        """
        Вкладка 'Общие сведения'
        объединяет шаги по выбору из списков 'вектор атаки' и 'Тип атаки'

        :param inc_vector: 'Направлен на клиента участника' или 'Направлен на инфраструктуру участника'
        :type inc_vector: str
        :param inc_type: значения берутся из диктов функции choose_inc_vector_and_type
        :type inc_type: str
        """
        vector, chosen_type = choose_inc_vector_and_type(inc_vector, inc_type)
        self.mw_inc_ef_vector_dropdown()
        self.mw_inc_ef_choose_vector(vector)
        self.mw_inc_ef_attack_type_dropdown()
        self.mw_inc_ef_choose_attack_type(chosen_type)

    def mw_inc_ef_detected_date(self, date_text):
        """
        Вкладка 'Общие сведения'
        Заполнить поле ввода 'Дата фиксации (обнаружения)', дата
        """
        self.find_and_fill_element(date_text, *self.locators.MW_NEW_EF_INCIDENT_FIXATION_DATE)

    def mw_inc_ef_location_federal_district_dropdown(self):
        """
        Вкладка 'Общие сведения'
        Заполнить поле ввода 'Федеральный округ', список
        """
        drop_down_list = self.search_element(*self.locators.MW_NEW_EF_INCIDENT_LOCATION_FEDERAL_DISTRICT_DROPDOWN)
        drop_down_list.click()
        sleep(0.5)
        return drop_down_list

    def mw_inc_ef_location_federal_district_random(self):
        """
        Вкладка 'Общие сведения'
        Заполнить поле ввода 'Федеральный округ', список
        """
        parent = self.mw_inc_ef_location_federal_district_dropdown()
        list_of_soi_type = parent.find_elements(*self.locators.MW_NEW_EF_INCINDENT_ALL_RANDOM_CHOOSE_LIST_DROPDOWN)
        random.choice(list_of_soi_type).click()

    def mw_inc_ef_location_subject_of_federation_dropdown(self):
        """
        Вкладка 'Общие сведения'
        Заполнить поле ввода 'Субъект федерации', список
        """
        drop_down_list = self.search_element(*self.locators.MW_NEW_EF_INCIDENT_LOCATION_SUBJECT_OF_FEDERATION_DROPDOWN)
        drop_down_list.click()
        sleep(0.5)
        return drop_down_list

    def mw_inc_ef_location_subject_of_federation_random(self):
        """
        Вкладка 'Общие сведения'
        Заполнить поле ввода 'Субъект федерации', список
        """
        parent = self.mw_inc_ef_location_subject_of_federation_dropdown()
        list_of_soi_type = parent.find_elements(*self.locators.MW_NEW_EF_INCINDENT_ALL_RANDOM_CHOOSE_LIST_DROPDOWN)
        random.choice(list_of_soi_type).click()

    def mw_inc_ef_location_locality(self, text):
        """
        Вкладка 'Общие сведения'
        Заполнить поле ввода 'Населённый пункт', список
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_INCIDENT_LOCATION_LOCALITY)

    def mw_inc_ef_department(self, text):
        """
        Вкладка 'Общие сведения'
        Заполнить поле ввода 'Подразделение'
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_INCIDENT_DEPARTMENT)

    def mw_inc_ef_tech_device(self, text):
        """
        Вкладка 'Общие сведения'
        Заполнить поле ввода 'Техническое средство'
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_INCIDENT_TECH_DEVICE)

    def mw_inc_ef_attacked_services_click_add_btn(self):
        """
        Вкладка 'Общие сведения'
        Атакованные сервисы
        Нажать кнопку добавить
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCIDENT_ATTACKED_SERVICES_ADD_BTN)

    def mw_inc_ef_attacked_services_type_service(self):
        """
        Вкладка 'Общие сведения'
        Атакованные сервисы
        открыть список 'Тип атакованного сервиса'
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCIDENT_ATTACKED_SERVICES_TYPE_DROPDOWN)

    def mw_inc_ef_attacked_services_type_service_random_choose(self):
        """
        Вкладка 'Общие сведения'
        Атакованные сервисы
        выбрать случайное значение из списка 'Тип атакованного сервиса'
        """
        parent = self.search_element(*self.locators.MW_NEW_EF_INCIDENT_ATTACKED_SERVICES_TYPE_DROPDOWN)
        list_of_soi_type = parent.find_elements(*self.locators.MW_NEW_EF_INCINDENT_ALL_RANDOM_CHOOSE_LIST_DROPDOWN)
        random.choice(list_of_soi_type).click()

    def mw_inc_ef_law_enforcement_request_dropdown(self):
        """
        Вкладка 'Общие сведения'
        Открыть выпадающий список 'Обращение в правоохранительные органы'
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCIDENT_LAW_ENFORCEMENT_REQUEST_DROPDOWN)

    def mw_inc_ef_law_enforcement_request_type(self, law_enforcement_req):
        """
        Вкладка 'Общие сведения'
        Выбрать значение в списке 'Обращение в правоохранительные органы'
        """
        law_text = choose_law_enforcement_req_type(law_enforcement_req)
        locator = collect_locator(self.locators.MW_NEW_EF_INCIDENT_LAW_ENFORCEMENT_REQUEST_PATTERN, law_text)
        self.find_and_click(*locator)

    def mw_inc_ef_type_description_dropdown(self):
        """
        Вкладка 'Вектор инцидента - EXT' или 'Вектор инцидента - INT'
        Открыть выпадающий список 'Тип инцидента'
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCIDENT_TYPE_DESCRIPTION_DROPDOWN)

    def mw_inc_ef_type_description_type(self):
        """
        Вкладка 'Вектор инцидента - EXT' или 'Вектор инцидента - INT'
        Выбрать значение в списке 'Тип инцидента'
        """
        parent = self.search_element(*self.locators.MW_NEW_EF_INCIDENT_TYPE_DESCRIPTION_DROPDOWN)
        list_of_soi_type = parent.find_elements(*self.locators.MW_NEW_EF_INCINDENT_ALL_RANDOM_CHOOSE_LIST_DROPDOWN)
        random.choice(list_of_soi_type).click()

    def mw_inc_ef_add_event_btn(self, int_type):
        """
        Вкладка 'Вектор инцидента - EXT' или 'Вектор инцидента - INT'
        Нажать на кнопку '+Добавить событие'
        """
        if int_type == 'INT':
            self.find_and_click(*self.locators.MW_NEW_EF_INCIDENT_TYPE_INT_ADD_EVENT)
        else:
            self.find_and_click(*self.locators.MW_NEW_EF_INCIDENT_TYPE_EXT_ADD_EVENT)

    def mw_inc_ef_save_event_btn(self):
        """
        Вкладка 'Вектор инцидента - EXT' или 'Вектор инцидента - INT'
        Модальное окно после нажатия на кнопку '+Добавить событие'
        Нажать на кнопку 'Сохранить'
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCIDENT_TYPE_SAVE_EVENT)

    def mw_inc_ef_add_event_ext_dropdown(self):
        """
        Вкладка 'Вектор инцидента - EXT'
        Модальное окно после нажатия на кнопку '+Добавить событие'
        Открыть выпадающий список 'Событие'
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCIDENT_EXT_TYPE_EVENT_DROPDOWN)

    def mw_inc_ef_ext_choose_event(self):
        """
        Вкладка 'Вектор инцидента - EXT' или 'Вектор инцидента - INT'
        Модальное окно после нажатия на кнопку '+Добавить событие'
        Выбрать случайное значение в списке 'Событие'
        """
        parent = self.search_element(*self.locators.MW_NEW_EF_INCIDENT_EXT_TYPE_EVENT_DROPDOWN)
        list_of_soi_type = parent.find_elements(*self.locators.MW_NEW_EF_INCINDENT_ALL_RANDOM_CHOOSE_LIST_DROPDOWN)
        random.choice(list_of_soi_type).click()

    def mw_inc_ef_add_event_int_dropdown(self):
        """
        Вкладка 'Вектор инцидента - INT'
        Модальное окно после нажатия на кнопку '+Добавить событие'
        Открыть выпадающий список 'Событие'
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCIDENT_INT_TYPE_EVENT_DROPDOWN)

    def mw_inc_ef_int_choose_event(self):
        """
        Вкладка 'Вектор инцидента - INT'
        Модальное окно после нажатия на кнопку '+Добавить событие'
        Выбрать случайное значение в списке 'Событие'
        """
        parent = self.search_element(*self.locators.MW_NEW_EF_INCIDENT_INT_TYPE_EVENT_DROPDOWN)
        list_of_soi_type = parent.find_elements(*self.locators.MW_NEW_EF_INCINDENT_ALL_RANDOM_CHOOSE_LIST_DROPDOWN)
        random.choice(list_of_soi_type).click()

    def mw_inc_ef_intruder_dropdown(self):
        """
        Вкладка 'Вектор инцидента - INT'
        Открыть выпадающий список 'Тип нарушителя'
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCIDENT_TYPE_INTRUDER_DROPDOWN)

    def mw_inc_ef_intruder_event(self):
        """
        Вкладка 'Вектор инцидента - INT'
        Модальное окно после нажатия на кнопку '+Добавить событие'
        Выбрать случайное значение в списке 'Тип нарушителя'
        """
        parent = self.search_element(*self.locators.MW_NEW_EF_INCIDENT_TYPE_INTRUDER_DROPDOWN)
        list_of_soi_type = parent.find_elements(*self.locators.MW_NEW_EF_INCINDENT_ALL_RANDOM_CHOOSE_LIST_DROPDOWN)
        random.choice(list_of_soi_type).click()

    def mw_inc_ef_type_use_dropdown(self):
        """
        Вкладка 'Вектор инцидента - EXT'
        Открыть выпадающий список 'Тип и способ использования...'
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCIDENT_TYPE_USE_DROPDOWN)

    def mw_inc_ef_type_use_event(self):
        """
        Вкладка 'Вектор инцидента - EXT'
        Модальное окно после нажатия на кнопку '+Добавить событие'
        Выбрать случайное значение в списке 'Тип и способ использования...'
        """
        parent = self.search_element(*self.locators.MW_NEW_EF_INCIDENT_TYPE_USE_DROPDOWN)
        list_of_soi_type = parent.find_elements(*self.locators.MW_NEW_EF_INCINDENT_ALL_RANDOM_CHOOSE_LIST_DROPDOWN)
        random.choice(list_of_soi_type).click()

    def mw_inc_menu_click_impacts_btn(self):
        """
        Меню электронной формы инциндента
        нажать кнопку 'Воздействие инцидента'
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_BTN)

    def mw_inc_click_add_impacts_tha_btn(self):
        """
        Раздел 'Воздействие инцидента'
        нажать кнопку 'добавить' TrafficHijackAttack
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_ADD_THA_BTN)

    def mw_inc_fill_impacts_sim_phone_num(self):
        """
        Раздел 'Воздействие инцидента'
        Sim заполнить номер мобильного для типа атаки 'Изменения IMSI на SIM-карте, смена IMEI телефона'
        """
        phone_number = ''.join([str(randint(0, 9)) for _ in range(10)])
        self.find_and_fill_element(phone_number, *self.locators.MW_NEW_EF_INCENDENT_IMPACTS_PHONE_NUMBER)

    def mw_inc_fill_impacts_sim(self):
        """ Заполнить все поля Воздействие инцидента типа Sim"""
        self.mw_inc_fill_impacts_sim_phone_num()

    def mw_inc_fill_impacts_traffic_hijack_attacks_le_as_path(self):
        """Воздействие инцидента типа TrafficHijackAttack
        заполнить поле Штатный AS-Path"""
        text = self.generate_str_and_return()
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_THA_LE_AS_PATH)

    def mw_inc_fill_impacts_traffic_hijack_attacks_wrong_as_path(self):
        """Воздействие инцидента типа TrafficHijackAttack
        заполнить поле Подставной AS-Path"""
        text = self.generate_str_and_return()
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_THA_W_AS_PATH)

    def mw_inc_fill_impacts_traffic_hijack_attacks_looking_glass(self):
        """Воздействие инцидента типа TrafficHijackAttack
        заполнить поле Ссылка на используемый Looking Glass """
        text = self.generate_str_and_return()
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_THA_LOOKING_GLASS)

    def mw_inc_fill_impacts_traffic_hijack_attacks_le_prefix(self):
        """Воздействие инцидента типа TrafficHijackAttack
        заполнить поле Штатный prefix"""
        text = self.generate_str_and_return()
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_THA_LE_PREFIX)

    def mw_inc_fill_impacts_traffic_hijack_attacks_wrong_prefix(self):
        """Воздействие инцидента типа TrafficHijackAttack
        заполнить поле Подставной prefix """
        text = self.generate_str_and_return()
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_THA_W_PREFIX)

    def mw_inc_fill_impacts_traffic_hijack_attacks(self):
        """ Заполнить все поля Воздействие инцидента типа TrafficHijackAttack"""
        self.mw_inc_click_add_impacts_tha_btn()
        self.mw_inc_fill_impacts_traffic_hijack_attacks_le_as_path()
        self.mw_inc_fill_impacts_traffic_hijack_attacks_wrong_as_path()
        self.mw_inc_fill_impacts_traffic_hijack_attacks_looking_glass()
        self.mw_inc_fill_impacts_traffic_hijack_attacks_le_prefix()
        self.mw_inc_fill_impacts_traffic_hijack_attacks_wrong_prefix()

    def mw_inc_fill_impacts_malware_add_btn(self):
        """
        Раздел 'Воздействие инцидента'
        нажать кнопку 'добавить' Malware
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_ADD_BTN)

    def mw_inc_fill_impacts_malware_target_ip(self, ip=None):
        """
        Раздел 'Воздействие инцидента' malware, заполнить поле IP значением
        """
        if not ip:
            ip = random_ipv4()
        self.find_and_fill_element(ip, *self.locators.MW_NEW_EF_INCIDENT_IMPACTS_MALWARE_TARGET_IP_INPUT)

    def mw_inc_fill_impacts_malware(self):
        """ Заполнить все необходимые поля Воздействие инцидента типа Malware"""
        self.mw_inc_fill_impacts_malware_add_btn()

    def mw_inc_fill_impacts_social_engineering_soi_type_dropdown(self):
        """
        Раздел 'Воздействие инцидента'
        SocialEngineering открывает выпадашку "Идентификатор способа реализации метода социальной инженерии"
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_SE_SOI_TYPE)

    def mw_inc_fill_impacts_social_engineering_random_choose_soi_type(self):
        """Раздел 'Воздействие инцидента'
        SocialEngineering рандомный выбор значения "Идентификатор способа реализации метода социальной инженерии"
        """
        parent = self.search_element(*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_SE_SOI_TYPE)
        list_of_soi_type = parent.find_elements(*self.locators.MW_NEW_EF_INCINDENT_ALL_RANDOM_CHOOSE_LIST_DROPDOWN)
        random.choice(list_of_soi_type).click()

    def mw_inc_fill_impacts_social_engineering(self):
        """Заполнить все необходимые поля Воздействие инцидента типа SocialEngineering"""
        self.mw_inc_fill_impacts_social_engineering_soi_type_dropdown()
        self.mw_inc_fill_impacts_social_engineering_random_choose_soi_type()

    def mw_inc_fill_impacts_ddos_click_add(self):
        """
        Раздел 'Воздействие инцидента'
        DdosAttack нажать кнопку "добавить"
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_DDOS_ADD_BTN)

    def mw_inc_fill_impacts_ddos_source_add_btn(self):
        """
        Раздел 'Воздействие инцидента'
        DdosAttack "IP-адреса источников" нажать кнопку "добавить"
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_DDOS_SOURCE_ADD_BTN)

    def mw_inc_fill_impacts_ddos_source_fill_ip_address(self):
        """
        Раздел 'Воздействие инцидента'
        DdosAttack "IP-адреса источников" заполнить поле ip адреса
        """
        ip_address = random_ipv4()
        self.find_and_fill_element(ip_address, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_DDOS_SOURCE_IP_ADR)

    def mw_inc_fill_impacts_ddos_attack_type_dropdown(self):
        """
        Раздел 'Воздействие инцидента'
        DdosAttack "Тип атаки" открыть список
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_DDOS_ATTACK_TYPE_DROPDOWN)

    def mw_inc_fill_impacts_ddos_attack_type_random_choose(self):
        """
        Раздел 'Воздействие инцидента'
        DdosAttack рандомный выбор значения "Тип атаки"
        """
        parent = self.search_element(*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_DDOS_ATTACK_TYPE_DROPDOWN)
        list_of_soi_type = parent.find_elements(*self.locators.MW_NEW_EF_INCINDENT_ALL_RANDOM_CHOOSE_LIST_DROPDOWN)
        random.choice(list_of_soi_type).click()

    def mw_inc_fill_impacts_ddos_fill_time_area(self):
        """
        Раздел 'Воздействие инцидента'
        DdosAttack заполнить время начала
        """
        start_time = utc_timestamp(date_format='%d.%m.%Y')
        self.find_and_fill_element(start_time, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_DDOS_TIME_AREA)

    def mw_inc_fill_impacts_ddos_fill_target_ip(self):
        """Раздел 'Воздействие инцидента' DdosAttack заполнить поле Адрес ресурса"""
        ip_address = random_ipv4()
        self.find_and_fill_element(ip_address, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_DDOS_TARGET_IP)

    def mw_inc_fill_impacts_ddos(self):
        """Заполнить все необходимые поля Воздействие инцидента типа DdosAttack"""
        self.mw_inc_fill_impacts_ddos_click_add()
        self.mw_inc_fill_impacts_ddos_source_add_btn()
        self.mw_inc_fill_impacts_ddos_source_fill_ip_address()
        self.mw_inc_fill_impacts_ddos_attack_type_dropdown()
        self.mw_inc_fill_impacts_ddos_attack_type_random_choose()
        self.mw_inc_fill_impacts_ddos_fill_time_area()

    def mw_inc_fill_impacts_atm_attack_type(self):
        """
        Раздел 'Воздействие инцидента'
        AtmAttack нажать на список "Тип Атаки"
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCINDENT_ATM_ATTACK_TYPE_DROPDOWN)

    def mw_inc_fill_impacts_atm_attack_type_random_choose(self):
        """
        Раздел 'Воздействие инцидента'
        AtmAttack рандомный выбор значения "Тип атаки"
        """
        parent = self.search_element(*self.locators.MW_NEW_EF_INCINDENT_ATM_ATTACK_TYPE_DROPDOWN)
        list_of_attack_type = parent.find_elements(*self.locators.MW_NEW_EF_INCINDENT_ALL_RANDOM_CHOOSE_LIST_DROPDOWN)
        random.choice(list_of_attack_type).click()

    def mw_inc_fill_impacts_atm_attack(self):
        """Заполнить все необходимые поля Воздействие инцидента типа AtmAttack"""
        self.mw_inc_fill_impacts_atm_attack_type()
        self.mw_inc_fill_impacts_atm_attack_type_random_choose()

    def mw_inc_fill_impacts_vulnerability_click_add_btn(self):
        """
        Раздел 'Воздействие инцидента'
        Vulnerability нажать кнопку "добавить"
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_VULNERABILITY_ADD_BTN)

    def mw_inc_fill_impacts_vulnerability_fill_target_ip(self):
        """
        Раздел 'Воздействие инцидента'
        Vulnerability Внешний адрес пострадавшей системы заполнить "IP-адрес"
        """
        ip = random_ipv4()
        self.find_and_fill_element(ip, *self.locators.MW_NEW_EF_INCIDENT_IMPACTS_VULNERABILITY_TARGET_IP)

    def mw_inc_fill_impacts_vulnerability_fill_sw_name(self):
        """
        Раздел 'Воздействие инцидента'
        Vulnerability заполнить "Наименование программного обеспечения"
        """
        text = self.generate_str_and_return()
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_VULNERABILITY_SW_NAME)

    def mw_inc_fill_impacts_vulnerability_fill_sw_ver(self):
        """
        Раздел 'Воздействие инцидента'
        Vulnerability заполнить "Версия программного обеспечения"
        """
        text = self.generate_str_and_return()
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_VULNERABILITY_SW_VER)

    def mw_inc_fill_impacts_vulnerability_sw_class_dropdown(self):
        """
        Раздел 'Воздействие инцидента'
        Vulnerability открыть список "Класс уязвимости"
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_VULNERABILITY_SW_CLASS_DROPDOWN)

    def mw_inc_fill_impacts_vulnerability_sw_class_random_choose(self):
        """
        Раздел 'Воздействие инцидента'
        Vulnerability рандомный выбор значения "Класс уязвимости"
        """
        parent = self.search_element(*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_VULNERABILITY_SW_CLASS_DROPDOWN)
        list_of_sw_class = parent.find_elements(*self.locators.MW_NEW_EF_INCINDENT_ALL_RANDOM_CHOOSE_LIST_DROPDOWN)
        random.choice(list_of_sw_class).click()

    def mw_inc_fill_impacts_vulnerability_fill_date(self):
        """
        Раздел 'Воздействие инцидента'
        Vulnerability заполнить дату
        """
        start_time = utc_timestamp(date_format='%d.%m.%Y')
        self.find_and_fill_element(start_time, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_VULNERABILITY_DATE)

    def mw_inc_fill_impacts_vulnerability_fill_base_cvss(self):
        """
        Раздел 'Воздействие инцидента'
        Vulnerability заполнить "базовый вектор уязвимости в соответствии с CVSS 3.0."
        """
        text = self.generate_str_and_return()
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_VULNERABILITY_BASE_CVSS)

    def mw_inc_fill_impacts_vulnerability_custom_status_dropdown(self):
        """
        Раздел 'Воздействие инцидента'
        Vulnerability открыть список "Статус уязвимости"
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_VULNERABILITY_CUSTOM_STATUS)

    def mw_inc_fill_impacts_vulnerability_custom_status_random_choose(self):
        """
        Раздел 'Воздействие инцидента'
        Vulnerability рандомный выбор значения "Статус уязвимости"
        """
        parent = self.search_element(*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_VULNERABILITY_CUSTOM_STATUS)
        list_of_sw_class = parent.find_elements(*self.locators.MW_NEW_EF_INCINDENT_ALL_RANDOM_CHOOSE_LIST_DROPDOWN)
        random.choice(list_of_sw_class).click()

    def mw_inc_fill_impacts_vulnerability_fill_custom_exploit(self):
        """
        Раздел 'Воздействие инцидента'
        Vulnerability заполнить "Наличие эксплойта"
        """
        text = self.generate_str_and_return()
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_VULNERABILITY_CUSTOM_EXPLOIT)

    def mw_inc_fill_impacts_vulnerability(self):
        """Заполнить все необходимые поля Воздействие инцидента типа Vulnerability"""
        self.mw_inc_fill_impacts_vulnerability_click_add_btn()
        self.mw_inc_fill_impacts_vulnerability_fill_sw_name()
        self.mw_inc_fill_impacts_vulnerability_fill_sw_ver()
        self.mw_inc_fill_impacts_vulnerability_sw_class_dropdown()
        self.mw_inc_fill_impacts_vulnerability_sw_class_random_choose()
        self.mw_inc_fill_impacts_vulnerability_fill_date()
        self.mw_inc_fill_impacts_vulnerability_fill_base_cvss()
        self.mw_inc_fill_impacts_vulnerability_custom_status_dropdown()
        self.mw_inc_fill_impacts_vulnerability_custom_status_random_choose()
        self.mw_inc_fill_impacts_vulnerability_fill_custom_exploit()

    def mw_inc_fill_impacts_brute_force_click_add_btn(self):
        """
        Раздел 'Воздействие инцидента'
        BruteForce нажать кнопку "добавить"
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_BRUT_FORCE_ADD_BTN)

    def mw_inc_fill_impacts_brute_force_fill_target_ip(self):
        """
        Раздел 'Воздействие инцидента'
        BruteForce Адрес пострадавшей системы заполнить IP-адрес
        """
        ip = random_ipv4()
        self.find_and_fill_element(ip, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_BRUT_FORCE_TARGET_IP)

    def mw_inc_fill_impacts_brute_force(self):
        """Заполнить все необходимые поля Воздействие инцидента типа BruteForce"""
        self.mw_inc_fill_impacts_brute_force_click_add_btn()

    def mw_inc_fill_impacts_spam_click_add_btn(self):
        """
        Раздел 'Воздействие инцидента'
        Spam нажать кнопку "добавить"
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_SPAM_ADD_BTN)

    def mw_inc_fill_impacts_spam_fill_date(self):
        """
        Раздел 'Воздействие инцидента'
        Spam заполнить дату
        """
        start_time = utc_timestamp(date_format='%d.%m.%Y')
        self.find_and_fill_element(start_time, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_SPAM_DATE)

    def mw_inc_fill_impacts_spam_click_add_address_btn(self):
        """
        Раздел 'Воздействие инцидента'
        Spam нажать кнопку "добавить" адрес эл.почты
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_SPAM_ADD_ADDRESS_BTN)

    def mw_inc_fill_impacts_spam_fill_email_address(self):
        """
        Раздел 'Воздействие инцидента'
        Spam заполнить поле адрес эл.почты
        """
        email = random_email()
        self.find_and_fill_element(email, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_SPAM_ADDRESS_FIELD)

    def mw_inc_fill_impacts_spam(self):
        """Заполнить все необходимые поля Воздействие инцидента типа Spam"""
        self.mw_inc_fill_impacts_spam_click_add_btn()
        self.mw_inc_fill_impacts_spam_fill_date()
        self.mw_inc_fill_impacts_spam_click_add_address_btn()
        self.mw_inc_fill_impacts_spam_fill_email_address()

    def mw_inc_fill_impacts_control_center_click_add_btn(self):
        """
        Раздел 'Воздействие инцидента'
        ControlCenter нажать кнопку "добавить"
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_CONTROL_CENTER_ADD_BTN)

    def mw_inc_fill_impacts_control_center_target_ip(self):
        """
        Раздел 'Воздействие инцидента'
        ControlCenter заполнить IP-адрес пострадавшей системы"
        """
        ip_address = random_ipv4()
        self.find_and_fill_element(ip_address,*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_CONTROL_CENTER_TARGET_IP)

    def mw_inc_fill_impacts_control_center_target_url(self):
        """
        Раздел 'Воздействие инцидента'
        ControlCenter заполнить Единый указатель ресурса"
        """
        url = random_url()
        self.find_and_fill_element(url,*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_CONTROL_CENTER_TARGET_URL)

    def mw_inc_fill_impacts_control_center_host_url(self):
        """
        Раздел 'Воздействие инцидента'
        ControlCenter заполнить URL с ЦУ"
        """
        url = random_url()
        self.find_and_fill_element(url,*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_CONTROL_CENTER_HOST_URL)

    def mw_inc_fill_impacts_control_center_intruder_ip(self):
        """
        Раздел 'Воздействие инцидента'
        ControlCenter заполнить IP-адрес злоумышленника
        """
        ip_address = random_ipv4()
        self.find_and_fill_element(ip_address,*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_CONTROL_CENTER_INTRUDER_IP)

    def mw_inc_fill_impacts_control_center_required_params(self):
        rand = random.choice([True, False])
        self.mw_inc_fill_impacts_control_center_target_ip()
        self.mw_inc_fill_impacts_control_center_target_url()
        if rand:
            self.mw_inc_fill_impacts_control_center_host_url()
        else:
            self.mw_inc_fill_impacts_control_center_intruder_ip()

    def mw_inc_fill_impacts_control_center(self):
        """ Нажать на [Добавить] и заполнить все необходимые поля Воздействие инцидента типа ControlCenter"""
        self.mw_inc_fill_impacts_control_center_click_add_btn()
        self.mw_inc_fill_impacts_control_center_required_params()

    def mw_inc_fill_impacts_phishing_attack_add_btn(self):
        """
        Раздел 'Воздействие инцидента'
        PhishingAttack нажать кнопку "добавить"
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_PHISHING_ATTACK_ADD_BTN)

    def mw_inc_fill_impacts_phishing_attack_ip_address(self):
        """
        Раздел 'Воздействие инцидента'
        PhishingAttack "IP-адреса" заполнить поле ip адреса
        """
        ip_address = random_ipv4()
        self.find_and_fill_element(ip_address, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_PHISHING_ATTACK_IP_ADR)

    def mw_inc_fill_impacts_phishing_attack_domain(self):
        """
        Раздел 'Воздействие инцидента'
        PhishingAttack заполнить "Домен"
        """
        domain = random_domain()
        self.find_and_fill_element(domain, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_PHISHING_ATTACK_DOMAIN)

    def mw_inc_fill_impacts_phishing_attack_add_resource_btn(self):
        """
        Раздел 'Воздействие инцидента'
        PhishingAttack нажать добавить "Фишинговый ресурс"
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_PHISHING_ADD_RESOURCE)

    def mw_inc_fill_impacts_phishing_attack_resource_ip_address(self):
        """
        Раздел 'Воздействие инцидента'
        PhishingAttack заполнить ip адрес в "Фишинговый ресурс"
        """
        ip_address = random_ipv4()
        self.find_and_fill_element(ip_address, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_PHISHING_RESOURCE_IP_ADR)

    def mw_inc_fill_impacts_phishing_attack_resource_url(self):
        """
        Раздел 'Воздействие инцидента'
        PhishingAttack заполнить URL в "Фишинговый ресурс"
        """
        url = random_url()
        self.find_and_fill_element(url, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_PHISHING_RESOURCE_URL)

    def mw_inc_fill_impacts_phishing_attack(self):
        """Заполнить все необходимые поля Воздействие инцидента типа PhishingAttack"""
        self.mw_inc_fill_impacts_phishing_attack_add_btn()
        self.mw_inc_fill_impacts_phishing_attack_ip_address()
        self.mw_inc_fill_impacts_phishing_attack_domain()
        self.mw_inc_fill_impacts_phishing_attack_add_resource_btn()
        self.mw_inc_fill_impacts_phishing_attack_resource_ip_address()
        self.mw_inc_fill_impacts_phishing_attack_resource_url()

    def mw_inc_fill_impacts_prohibited_content_click_add_btn(self):
        """
        Раздел 'Воздействие инцидента'
        ProhibitedContent нажать кнопку "добавить"
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_PROHIBITED_CONTENTS_ADD_BTN)

    def mw_inc_fill_impacts_prohibited_content_ip_address(self):
        """
        Раздел 'Воздействие инцидента'
        ProhibitedContent заполнить ip адрес
        """
        ip_address = random_ipv4()
        self.find_and_fill_element(ip_address, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_PROHIBITED_CONTENTS_IP_ADR)

    def mw_inc_fill_impacts_prohibited_content_url(self):
        """
        Раздел 'Воздействие инцидента'
        ProhibitedContent заполнить URL "Единый указатель ресурса"
        """
        url = random_url()
        self.find_and_fill_element(url, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_PROHIBITED_CONTENTS_URL)

    def mw_inc_fill_impacts_prohibited_content_type_content(self):
        """
        Раздел 'Воздействие инцидента'
        ProhibitedContent заполнить  "Тип запрещенного контента"
        """
        text = self.generate_str_and_return()
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_PROHIBITED_CONTENTS_TYPE_CONTENT)

    def mw_inc_fill_impacts_prohibited_content(self):
        """Заполнить все необходимые поля Воздействие инцидента типа ProhibitedContent"""
        self.mw_inc_fill_impacts_prohibited_content_click_add_btn()
        self.mw_inc_fill_impacts_prohibited_content_ip_address()
        self.mw_inc_fill_impacts_prohibited_content_url()
        self.mw_inc_fill_impacts_prohibited_content_type_content()

    def mw_inc_fill_impacts_malicious_resource_click_add_btn(self):
        """
        Раздел 'Воздействие инцидента'
        MaliciousResource нажать кнопку "добавить"
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_MALICIOUS_RESOURCE_ADD_BTN)

    def mw_inc_fill_impacts_malicious_resource_fill_type(self):
        """
        Раздел 'Воздействие инцидента'
        MaliciousResource заполнить "Тип вредоносной активности"
        """
        text = self.generate_str_and_return()
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_MALICIOUS_RESOURCE_TYPE)

    def mw_inc_fill_impacts_malicious_resource_click_target_add_btn(self):
        """
        Раздел 'Воздействие инцидента'
        MaliciousResource "Адреса ресурсов" нажать кнопку "добавить"
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCIDENT_IMPACTS_MALICIOUS_RESOURCE_TARGET_ADD_BTN)

    def mw_inc_fill_impacts_malicious_resource_fill_target_ip(self):
        """
        Раздел 'Воздействие инцидента'
        MaliciousResource "Адреса ресурсов" заполнить IP-адрес
        """
        ip = random_ipv4()
        self.find_and_fill_element(ip, *self.locators.MW_NEW_EF_INCIDENT_IMPACTS_MALICIOUS_RESOURCE_TARGET_IP)

    def mw_inc_fill_impacts_malicious_resource_fill_target_url(self):
        """
        Раздел 'Воздействие инцидента'
        MaliciousResource "Адреса ресурсов" заполнить Единый указатель ресурса
        """
        url = random_url()
        self.find_and_fill_element(url, *self.locators.MW_NEW_EF_INCIDENT_IMPACTS_MALICIOUS_RESOURCE_TARGET_URL)

    def mw_inc_fill_impacts_malicious_resource(self):
        """Заполнить все необходимые поля Воздействие инцидента типа MaliciousResource"""
        self.mw_inc_fill_impacts_malicious_resource_click_add_btn()
        self.mw_inc_fill_impacts_malicious_resource_fill_type()

    def mw_inc_fill_impacts_change_content_click_add_btn(self):
        """
        Раздел 'Воздействие инцидента'
        ChangeContent нажать кнопку "добавить"
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_CHANGE_CONTENT_ADD_BTN)

    def mw_inc_fill_impacts_change_content_target_ip(self):
        """Заполнить поле IP-адрес"""
        ip_address = random_ipv4()
        self.find_and_fill_element(ip_address, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_CHANGE_CONTENT_TARGET_IP)

    def mw_inc_fill_impacts_change_content_target_url(self):
        """Заполнить поле 'Единый указатель ресурса'"""
        url = random_url()
        self.find_and_fill_element(url, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_CHANGE_CONTENT_TARGET_URL)

    def mw_inc_fill_impacts_change_content_type(self):
        """Заполнить поле 'Тип изменённого контента'"""
        text = self.generate_str_and_return()
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_CHANGE_CONTENT_TYPE)

    def mw_inc_fill_impacts_change_content(self):
        """Кликнуть [Добавить] и заполнить все необходимые поля Воздействие инцидента типа ChangeContent"""
        self.mw_inc_fill_impacts_change_content_click_add_btn()
        self.mw_inc_fill_impacts_change_content_target_ip()
        self.mw_inc_fill_impacts_change_content_target_url()
        self.mw_inc_fill_impacts_change_content_type()

    def mw_inc_fill_impacts_scan_port_click_add_btn(self):
        """
        Раздел 'Воздействие инцидента'
        ScanPort нажать кнопку "добавить"
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_SCAN_PORT_ADD_BTN)

    def mw_inc_fill_impacts_scan_port_source_add_btn(self):
        """
        Раздел 'Воздействие инцидента'
        ScanPort нажать кнопку добавить "Источники сканирования"
        """
        self.find_and_click(*self.locators.MW_NEW_EF_INCINDENT_IMPACTS_SCAN_PORT_ADD_SOURCE_BTN)

    def mw_inc_fill_impacts_scan_port_ip_address(self):
        """
        Раздел 'Воздействие инцидента'
        ScanPort заполнить ip адрес "Источники сканирования"
        """
        ip_address = random_ipv4()
        self.find_and_fill_element(ip_address, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_SCAN_PORT_IP_ADR)

    def mw_inc_fill_impacts_scan_port_fill_date(self):
        """
        Раздел 'Воздействие инцидента'
        ScanPort заполнить дату "Время начала сканирования"
        """
        start_time = utc_timestamp(date_format='%d.%m.%Y')
        self.find_and_fill_element(start_time, *self.locators.MW_NEW_EF_INCINDENT_IMPACTS_SCAN_DATE)

    def mw_inc_fill_impacts_scan_port(self):
        """Заполнить все необходимые поля Воздействие инцидента типа ScanPort"""
        self.mw_inc_fill_impacts_scan_port_click_add_btn()
        self.mw_inc_fill_impacts_scan_port_source_add_btn()
        self.mw_inc_fill_impacts_scan_port_ip_address()
        self.mw_inc_fill_impacts_scan_port_fill_date()

    def mw_inc_fill_impacts_other(self):
        """Заполнить все необходимые поля Воздействие инцидента типа Other"""
        pass

    def mw_inc_choose_impacts_type_for_fill(self, attack_type):
        """
        ОСНОВНОЙ РАБОЧИЙ МЕТОД В РАЗДЕЛЕ ВОЗДЕЙСТВИЕ ИНЦИДЕНТА
        Раздел 'Воздействие инцидента'
        Метод на основании переданного аргумента "тип атаки" выбирает как заполнять воздействие
        """
        if attack_type == 'trafficHijackAttacks':
            self.mw_inc_fill_impacts_traffic_hijack_attacks()
        elif attack_type == 'malware':
            self.mw_inc_fill_impacts_malware()
        elif attack_type == 'socialEngineering':
            self.mw_inc_fill_impacts_social_engineering()
        elif attack_type == 'ddosAttacks':
            self.mw_inc_fill_impacts_ddos()
        elif attack_type == 'atmAttacks':
            self.mw_inc_fill_impacts_atm_attack()
        elif attack_type == 'vulnerabilities':
            self.mw_inc_fill_impacts_vulnerability()
        elif attack_type == 'bruteForces':
            self.mw_inc_fill_impacts_brute_force()
        elif attack_type == 'spams':
            self.mw_inc_fill_impacts_spam()
        elif attack_type == 'controlCenters':
            self.mw_inc_fill_impacts_control_center()
        elif attack_type == 'sim':
            self.mw_inc_fill_impacts_sim()
        elif attack_type == 'phishingAttacks':
            self.mw_inc_fill_impacts_phishing_attack()
        elif attack_type == 'prohibitedContents':
            self.mw_inc_fill_impacts_prohibited_content()
        elif attack_type == 'maliciousResources':
            self.mw_inc_fill_impacts_malicious_resource()
        elif attack_type == 'changeContent':
            self.mw_inc_fill_impacts_change_content()
        elif attack_type == 'scanPorts':
            self.mw_inc_fill_impacts_scan_port()
        elif attack_type == 'other':
            self.mw_inc_fill_impacts_other()

######################################################################################################################
    def mw_inc_ef_add_obs_btn(self):
        """
        Вкладка 'Операции без согласия'
        Нажать на кнопку '+ Добавить операцию'
        """
        self.find_and_click(*self.locators.MW_NEW_EF_OBS_ADD_OBS_BTN)

    def mw_inc_ef_obs_person_type(self):
        """
        Модальное окно 'Операции без согласия'
        Нажать на вып.списко 'Тип лица'
        """
        self.find_and_click(*self.locators.MW_NEW_EF_OBS_PERSON_TYPE_DROPDOWN)
        sleep(0.5)

    def mw_inc_ef_add_obs_payer_orgtype_btn(self, org_type):
        """
        Модальное окно 'Операции без согласия'
        Выбрать 'Юридическое лицо' или 'Физическое лицо' в выпадающем списке
        """
        local_org_type = "Юридическое лицо"
        if org_type == 'individual':
            local_org_type = "Физическое лицо"
        parent = self.search_element(*self.locators.MW_NEW_EF_OBS_PERSON_TYPE_DROPDOWN)
        list_of_payer_type = parent.find_elements(*self.locators.MW_NEW_EF_INCINDENT_ALL_RANDOM_CHOOSE_LIST_DROPDOWN)
        for i in list_of_payer_type:
            if i.text == local_org_type:
                i.click()

    def mw_inc_ef_add_obs_payer_add_hashes_btn(self):
        """
        Модальное окно 'Операции без согласия'
        Нажать на кнопку 'Добавить ХЕШИ'
        """
        self.find_and_click(*self.locators.MW_NEW_EF_OBS_PAYER_ADD_HASH_BTN)

    def mw_inc_ef_add_obs_payer_founder_hash(self, text):
        """
        Модальное окно 'Операции без согласия'
        Заполнить поле ввода 'Хеш-сумма серии и номера паспорта' для ЮЛ
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYER_FOUNDER_HASH_FLD)

    def mw_inc_ef_add_obs_payer_founder_snils(self, text):
        """
        Модальное окно 'Операции без согласия'
        Заполнить поле ввода 'Хеш-сумма СНИЛС' для ЮЛ
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYER_FOUNDER_SNILS_FLD)

    def mw_inc_ef_add_obs_payer_save_founder_btn(self):
        """
        Модальное окно 'Операции без согласия'
        Нажать на кнопку 'Галочка' для сохранения Учредителя
        """
        self.find_and_click(*self.locators.MW_NEW_EF_OBS_PAYER_SAVE_FOUNDER_BTN)

    def mw_inc_ef_add_obs_payer_inn(self, text):
        """
        Модальное окно 'Операции без согласия'
        Заполнить поле ввода 'ИНН'
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYER_INN_FLD)

    def mw_inc_ef_add_obs_detected_by_dropdown(self):
        """
        Модальное окно 'Операции без согласия'
        Открыть выпадающий список 'Обнаружено как'
        """
        dropdown = self.search_element(*self.locators.MW_NEW_EF_OBS_DETECTED_BY_DROPDOWN)
        self.find_and_click(*self.locators.MW_NEW_EF_OBS_DETECTED_BY_DROPDOWN)
        sleep(0.5)
        return dropdown

    def mw_inc_ef_add_obs_detected_by(self, vector, dropdown):
        """
        Модальное окно 'Операции без согласия'
        Выбрать значение в выпадающем списке 'Обнаружено как'
        """
        list_of_soi_type = dropdown.find_elements(*self.locators.MW_NEW_EF_INCINDENT_ALL_RANDOM_CHOOSE_LIST_DROPDOWN)
        text = detected_by_value(vector)
        self.mw_inc_all_dropdown_lists_choose_value(list_of_soi_type, text)

    def mw_inc_ef_add_obs_payer_type_dropdown(self):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты плательщика'
        Открыть выпадающий список 'Способ реализации перевода'
        """
        list_of_elements = self.search_element(*self.locators.MW_NEW_EF_OBS_PAYER_TYPE_DROPDOWN)
        list_of_elements.click()
        sleep(0.5)
        return list_of_elements

    def mw_inc_ef_add_obs_payer_type(self, payer_type, list_of_elements):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты плательщика'
        Выбрать значение в выпадающем списке 'Способ реализации перевода'
        """
        list_of_soi_type = list_of_elements.find_elements(*self.locators.MW_NEW_EF_INCINDENT_ALL_RANDOM_CHOOSE_LIST_DROPDOWN)
        text = get_antifraud_type(payer_type)
        self.mw_inc_all_dropdown_lists_choose_value(list_of_soi_type, text)

    def mw_inc_ef_add_obs_payee_type_dropdown(self):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты получателя'
        Открыть выпадающий список 'Способ реализации перевода'
        """
        list_of_elements = self.search_element(*self.locators.MW_NEW_EF_OBS_PAYEE_TYPE_DROPDOWN)
        list_of_elements.click()
        sleep(0.5)
        return list_of_elements

    def mw_inc_ef_add_obs_payee_type(self, payer_type, list_of_elements):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты получателя'
        Выбрать значение в выпадающем списке 'Способ реализации перевода'
        """
        list_of_soi_type = list_of_elements.find_elements(
            *self.locators.MW_NEW_EF_INCINDENT_ALL_RANDOM_CHOOSE_LIST_DROPDOWN)
        text = get_antifraud_type(payer_type)
        self.mw_inc_all_dropdown_lists_choose_value(list_of_soi_type, text)

    def mw_inc_ef_add_obs_payer_paymentcard_number(self, text):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты плательщика', способ перевода - 'Карта'
        Заполнить поле ввода 'Номер платежной карты'
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYER_PAYMENTCARD_NUMBER_FLD)

    def mw_inc_ef_add_obs_payer_paymentcard_rrn(self, text):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты плательщика', способ перевода - 'Карта'
        Заполнить поле ввода 'RRN'
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYER_PAYMENTCARD_RRN_FLD)

    def mw_inc_ef_add_obs_payer_phonenumber_number(self, text):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты плательщика', способ перевода - 'Телефон'
        Заполнить поле ввода 'Номер телефона'
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYER_PHONENUMBER_NUMBER_FLD)

    def mw_inc_ef_add_obs_payer_phone_sum(self):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты плательщика', способ перевода - 'Телефон'
        Заполнить поле ввода 'Сумма операции'
        """
        self.find_and_fill_element(random.randint(1000, 10**10), *self.locators.MW_NEW_EF_OBS_PAYER_PHONENUMBER_SUM_FLD)

    def mw_inc_ef_add_obs_payer_bankaccount_number(self, text):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты плательщика', способ перевода - 'Счет в банке'
        Заполнить поле ввода 'Номер банковского счета'
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYER_BANKACCOUNT_NUMBER_FLD)

    def mw_inc_ef_add_obs_payer_bankaccount_bik(self, text):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты плательщика', способ перевода - 'Счет в банке'
        Заполнить поле ввода 'БИК'
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYER_BANKACCOUNT_BIK_FLD)

    def mw_inc_ef_add_obs_payer_bankaccount_sum(self):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты плательщика', способ перевода - 'Счет в банке'
        Заполнить поле ввода 'Сумма операции'
        """
        self.find_and_fill_element(random.randint(1000, 10**10), *self.locators.MW_NEW_EF_OBS_PAYER_BANKACCOUNT_SUM_FLD)

    def mw_inc_ef_add_obs_payer_ewallet_number(self, text):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты плательщика', способ перевода - 'Электронный кошелек'
        Заполнить поле ввода 'Номер электронного кошелька'
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYER_EWALLET_NUMBER_FLD)

    def mw_inc_ef_add_obs_payer_ewallet_payment_sys(self, text):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты плательщика', способ перевода - 'Электронный кошелек'
        Заполнить поле ввода 'Название электронной платежной системы'
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYER_EWALLET_PAYMENT_SYSTEM_FLD)

    def mw_inc_ef_add_obs_payer_ewallet_sum(self):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты плательщика', способ перевода - 'Электронный кошелек'
        Заполнить поле ввода 'Сумма операции'
        """
        self.find_and_fill_element(random.randint(1000, 10**10), *self.locators.MW_NEW_EF_OBS_PAYER_EWALLET_SUM_FLD)

    def mw_inc_ef_add_obs_payer_swift_number(self, text):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты плательщика', способ перевода - 'SWIFT транзакция'
        Заполнить поле ввода 'Номер банковского счета'
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYER_SWIFT_NUMBER_FLD)

    def mw_inc_ef_add_obs_payer_swift_bik(self, text):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты плательщика', способ перевода - 'SWIFT транзакция'
        Заполнить поле ввода 'Swift-код' (Swift-БИК)
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYER_SWIFT_BIK_FLD)

    def mw_inc_ef_add_obs_payer_swift_sum(self):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты плательщика', способ перевода - 'SWIFT транзакция'
        Заполнить поле ввода 'Сумма операции'
        """
        self.find_and_fill_element(random.randint(1000, 10**10), *self.locators.MW_NEW_EF_OBS_PAYER_SWIFT_SUM_FLD)

    def mw_inc_ef_add_obs_payer_retail_sum(self):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты плательщика', способ перевода - 'Retail/ATM транзакция'
        Заполнить поле ввода 'Сумма операции'
        """
        self.find_and_fill_element(random.randint(1000, 10**10), *self.locators.MW_NEW_EF_OBS_PAYER_RETAIL_SUM_FLD)

    def mw_inc_ef_add_obs_payer_retail_bin(self, text):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты плательщика', способ перевода - 'Retail/ATM транзакция'
        Заполнить поле ввода 'BIN эквайера'
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYER_RETAIL_BIN_FLD)

    def mw_inc_ef_add_obs_payer_retail_merchant(self, text):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты плательщика', способ перевода - 'Retail/ATM транзакция'
        Заполнить поле ввода 'Мерчант'
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYER_RETAIL_MERCHANT_FLD)

    def mw_inc_ef_add_obs_payer_retail_mcc(self, text):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты плательщика', способ перевода - 'Retail/ATM транзакция'
        Заполнить поле ввода 'MCC'
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYER_RETAIL_MCC_FLD)

    def mw_inc_ef_add_obs_payer_other_number(self, text):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты плательщика', способ перевода - 'Иной идентификатор'
        Заполнить поле ввода 'Иной номер'
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYER_OTHER_NUMBER_FLD)

    def mw_inc_ef_add_obs_payer_other_sum(self):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты плательщика', способ перевода - 'Иной идентификатор'
        Заполнить поле ввода 'Сумма операции'
        """
        self.find_and_fill_element(random.randint(1000, 10**10), *self.locators.MW_NEW_EF_OBS_PAYER_OTHER_SUM_FLD)

    def mw_inc_ef_add_obs_payee_paymentcard_number(self, text):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты получателя', способ перевода - 'Карта'
        Заполнить поле ввода 'Номер платежной карты'
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYEE_PAYMENTCARD_NUMBER_FLD)

    def mw_inc_ef_add_obs_payee_phonenumber_number(self, text):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты получателя', способ перевода - 'Телефон'
        Заполнить поле ввода 'Номер телефона'
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYEE_PHONENUMBER_NUMBER_FLD)

    def mw_inc_ef_add_obs_payee_bankaccount_number(self, text):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты получателя', способ перевода - 'Счет в банке'
        Заполнить поле ввода 'Номер банковского счета'
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYEE_BANKACCOUNT_NUMBER_FLD)

    def mw_inc_ef_add_obs_payee_bankaccount_bik(self, text):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты получателя', способ перевода - 'Счет в банке'
        Заполнить поле ввода 'БИК'
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYEE_BANKACCOUNT_BIK_FLD)

    def mw_inc_ef_add_obs_payee_ewallet_number(self, text):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты получателя', способ перевода - 'Электронный кошелек'
        Заполнить поле ввода 'Номер электронного кошелька'
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYEE_EWALLET_NUMBER_FLD)

    def mw_inc_ef_add_obs_payee_ewallet_payment_sys(self, text):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты получателя', способ перевода - 'Электронный кошелек'
        Заполнить поле ввода 'Название электронной платежной системы'
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYEE_EWALLET_PAYMENT_SYSTEM_FLD)

    def mw_inc_ef_add_obs_payee_swift_number(self, text):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты получателя', способ перевода - 'SWIFT транзакция'
        Заполнить поле ввода 'Номер банковского счета'
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYEE_SWIFT_NUMBER_FLD)

    def mw_inc_ef_add_obs_payee_swift_bik(self, text):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты получателя', способ перевода - 'SWIFT транзакция'
        Заполнить поле ввода 'Swift-код' (Swift-БИК)
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYEE_SWIFT_BIK_FLD)

    def mw_inc_ef_add_obs_payee_retail_bin(self, text):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты получателя', способ перевода - 'Retail/ATM транзакция'
        Заполнить поле ввода 'BIN эквайера'
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYEE_RETAIL_BIN_FLD)

    def mw_inc_ef_add_obs_payee_retail_merchant(self, text):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты получателя', способ перевода - 'Retail/ATM транзакция'
        Заполнить поле ввода 'Мерчант'
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYEE_RETAIL_MERCHANT_FLD)

    def mw_inc_ef_add_obs_payee_retail_mcc(self, text):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты получателя', способ перевода - 'Retail/ATM транзакция'
        Заполнить поле ввода 'MCC'
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYEE_RETAIL_MCC_FLD)

    def mw_inc_ef_add_obs_payee_other_number(self, text):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты получателя', способ перевода - 'Иной идентификатор'
        Заполнить поле ввода 'Иной номер'
        """
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYEE_OTHER_NUMBER_FLD)

    def mw_inc_ef_add_obs_payer_sum(self, text):
        """
        Модальное окно 'Операции без согласия'
        'Реквизиты плательщика', способ перевода - 'Карта'
        Заполнить поле ввода 'Сумма операции'
        """
        self.find_and_clear_element(*self.locators.MW_NEW_EF_OBS_PAYER_SUM_FLD)
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYER_SUM_FLD)

    def mw_inc_ef_obs_continue_btn(self):
        """Нажать на кнопку 'Продолжить' для ОбС"""
        self.find_and_click(*self.locators.MW_NEW_EF_OBS_INCIDENT_CONTINUE_BTN)

    def mw_inc_ef_obs_save_btn(self):
        """Нажать на кнопку 'Сохранить' для ОбС"""
        self.find_and_click(*self.locators.MW_NEW_EF_OBS_INCIDENT_SAVE_BTN)

    def mw_inc_ef_obs_add_to_req_btn(self):
        """
        Нажать на кнопку 'Добавить к запросу' для ОбС
        """
        self.find_and_click(*self.locators.MW_READY_BTN)

    def mw_save_and_close_incident(self):
        """Сохранить и закрыть ЭФ Инцидента"""
        self.mw_inc_ef_save_btn()
        self.mw_inc_ef_close_btn()
        self.mw_inc_ef_accept_close_btn()

##################################################################################################
    def mw_obs_payer_list_dropdown(self):
        """ОБС. Открыть список 'Способ реализации перевода' для плательщика"""
        self.find_and_click(*self.locators.MW_NEW_EF_OBS_PAYER_DROPDOWN)

    def mw_choose_payment_card_method_transfer(self):
        """ОБС. В списоке 'Способ реализации перевода' выбрать карта"""
        self.find_and_click(*self.locators.MW_NEW_EF_OBS_PAYER_PAYMENTCARD_IN_DROPDOWN)

    def mw_fill_payment_card_number(self, text):
        """"""
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYER_PAYMENTCARD_NUMBER_FLD)

    def mw_fill_payment_card_sum_of_operation(self, text):
        """"""
        self.find_and_fill_element(text, *self.locators.MW_NEW_EF_OBS_PAYER_PAYMENTCARD_SUM_FLD)

    def mw_obs_payee_list_dropdown(self):
        """ОБС. Открыть список 'Способ реализации перевода' для получателя"""
        self.find_and_click(*self.locators.MW_NEW_EF_OBS_PAYEE_DROPDOWN)

    def mw_obs_choose_phone_method_transfer(self):
        """"""
        self.find_and_click(*self.locators.MW_NEW_EF_OBS_PAYER_PHONENUMBER_IN_DROPDOWN)

    def mw_insert_file_in_malware(self):
        """"""
        self.find_and_click(*self.locators.MW_MALWARE_SAMPLE_ADD_COLLECTION_BTN)
        dad_input_element = self.find_and_click(*self.locators.MW_INPUT_FILE_MALWARE)
        drag_and_drop_file(dad_input_element, self.MALWARE_RAR)
        no_error = True
        for i in range(30):
            upload_file_name = self.search_element(*self.locators.MW_MALWARE_UPLOAD_FILE_FIELD)
            file_rar = upload_file_name.text
            file_rar = file_rar.split('.')
            if file_rar[-1] == 'rar':
                self.log.info("Файл успешно загружен и проверен.")
                no_error = True
                break
            else:
                self.log.info("Файл еще не проверен!")
                no_error = False
                sleep(2)
        if not no_error:
            error_mes = 'File cannot be verified because timeout exceeded!!!'
            self.log.error(error_mes)

    def mw_insert_email_file_in_malware(self):
        """приложить файл в Файл эл. письма (секия Вредоносные письма) """
        dad_input_element = self.find_and_click(*self.locators.MW_INPUT_EMAIL_FILE_MALWARE)
        drag_and_drop_file(dad_input_element, self.MALWARE_EMAIL)
        self.wait_for_invisibility_element(*self.locators.PROGRESS_BAR)

    def mw_insert_file_in_attachments_tab(self):
        """приложить файл во Вложения """
        dad_input_element = self.find_and_click(*self.locators.MW_NEW_EF_INCIDENT_ATTACHMENT_TAB_FILE_UPLOAD)
        drag_and_drop_file(dad_input_element, self.ATTACHMENT)
        self.wait_for_invisibility_element(*self.locators.PROGRESS_BAR)

    def mw_check_sample_rar_in_request(self):
        """"""
        for i in range(16):
            try:
                sample = self.search_element(*self.locators.MW_SAMPLE_IN_REQUEST)
                if 'entities_description' in sample.text and ('Не' in sample.text or 'Сканируется' in sample.text):
                    self.log.info("Файл test.rar доступен в ЭФ запроса %s" % request_info_lku['hrid'])
                    break
                else:
                    continue
            except Exception:
                if i == 15:
                    raise AssertionError("Проблема с файлом приложенным как образец вредоносного ПО")
                sleep(1)
                continue

    def mw_obs_fill_date_operation(self, text, obs_param):
        """
        Модальное окно 'Операции без согласия'
        Заполнить Дата и время операции
        """
        locator = list(self.locators.MW_NEW_EF_OBS_OPERATION_DATE)
        locator[1] = locator[1].format(obs_param)
        self.find_and_fill_element(text, *locator)

    def mw_fill_incident_with_required_fields_general_information(self):
        """
        Заполнить раздел "Общие сведения"
        Заполнение обьязательных полей Эф инцидента. Без ОбС
        """
        self.mw_open_assistance_dropdown()
        if self.inc_params['assistance']:
            self.mw_inc_ef_assistance_need_btn()
        else:
            self.mw_inc_ef_assistance_nnd_btn()
        description_text = string_generator(min_length=10, max_length=100)
        self.mw_inc_ef_description_fld(text=description_text)
        self.mw_inc_ef_type(self.inc_params['vector'], self.inc_params['inc_type'])
        self.mw_inc_ef_detected_date(utc_timestamp(date_format='%d.%m.%Y'))
        self.mw_inc_ef_location_federal_district_random()
        self.mw_inc_ef_location_subject_of_federation_random()
        self.mw_inc_ef_location_locality(text=description_text)
        text = string_generator(min_length=10, max_length=100)
        self.mw_inc_ef_department(text)
        text = string_generator(min_length=10, max_length=100)
        self.mw_inc_ef_tech_device(text)
        self.mw_inc_ef_attacked_services_click_add_btn()
        self.mw_inc_ef_attacked_services_type_service()
        self.mw_inc_ef_attacked_services_type_service_random_choose()
        self.mw_inc_ef_law_enforcement_request_dropdown()
        self.mw_inc_ef_law_enforcement_request_type(self.inc_params['law_enforcement_request'])
        self.mw_inc_ef_continue_btn()

    def mw_fill_incident_with_required_fields(self, **kwargs):
        """ ОСНОВНОЙ ИСПОЛЬЗУЕМЫЙ МЕТОД Заполнения обязательных полей Эф инцидента. Без ОбС
        заполняет раздел общие сведения - метод mw_fill_incident_with_required_fields_general_information
        и далее заполняет раздел "Вектор инцидента"

        :param kwargs: пара ключ значение если нужно заменить параметры для инцидента

        пример: vector='EXT', assistance=True, law_enforcement_request='POL', inc_type='eWallet'
        значения из словарей incident_type_ext и incident_type_int и функции collect_inc_param
        """
        self.inc_params = collect_inc_param()
        if kwargs:
            self.parsing_args_for_incident(kwargs)
        self.log.info("Выбранные параметры для Инцидента %s" % str(self.inc_params))
        self.mw_fill_incident_with_required_fields_general_information()  # Заполнить раздел "Общие сведения"
        self.mw_inc_ef_type_description_dropdown()
        self.mw_inc_ef_type_description_type()
        self.mw_inc_ef_add_event_btn(self.inc_params['vector'])
        if self.inc_params['vector'] == 'EXT':
            self.mw_inc_ef_add_event_ext_dropdown()
            self.mw_inc_ef_ext_choose_event()
            self.mw_inc_ef_type_use_dropdown()
            self.mw_inc_ef_type_use_event()
        else:
            self.mw_inc_ef_add_event_int_dropdown()
            self.mw_inc_ef_int_choose_event()
            self.mw_inc_ef_intruder_dropdown()
            self.mw_inc_ef_intruder_event()
        self.mw_inc_menu_click_impacts_btn()
        self.mw_inc_choose_impacts_type_for_fill(self.inc_params['inc_type'])

    def parsing_args_for_incident(self, inc_args):
        """замена рандомно сгенерированных параметров для инцидента если были переданы другие"""
        param_intersection = set(self.inc_params.keys()).intersection(inc_args)
        for i in param_intersection:
            self.inc_params[i] = inc_args[i]

    def mw_inc_fill_org_type_info(self, org_type):
        """ относиться к заполнению ОБС
        Заполнение ИНН, Хэш паспорта и СНИЛС в соовтетсвии с типом лица в ОБС
        """
        self.mw_inc_ef_obs_person_type()
        self.mw_inc_ef_add_obs_payer_orgtype_btn(org_type)
        self.mw_inc_ef_add_obs_payer_add_hashes_btn()
        self.mw_inc_ef_add_obs_payer_founder_hash(get_sha256_hash(passport()))
        self.mw_inc_ef_add_obs_payer_founder_snils(get_sha256_hash(snils()))
        if org_type == 'company':
            self.mw_inc_ef_add_obs_payer_inn(inn_entity())
        else:
            self.mw_inc_ef_add_obs_payer_inn(inn_individual())

    def mw_inc_obs_fill_payer_areas(self, obs_params):
        """ относиться к заполнению ОБС
        Заполнение полей для плательщика, входит в состав заполения обязательных полей ОБС
        """
        if obs_params == 'paymentCard':
            self.mw_inc_ef_add_obs_payer_paymentcard_number(
                payment_card(participants_params_payer['paymentCard.number']))
            self.mw_inc_ef_add_obs_payer_sum(randint(100, 200000))
            self.mw_inc_ef_add_obs_payer_paymentcard_rrn(string_generator(min_length=12, max_length=12))
        elif obs_params == 'phoneNumber':
            number = ''.join([str(randint(0, 9)) for _ in range(10)])
            self.mw_inc_ef_add_obs_payer_phonenumber_number(number)
            self.mw_inc_ef_add_obs_payer_phone_sum()
        elif obs_params == 'bankAccount':
            self.mw_inc_ef_add_obs_payer_bankaccount_number(bank_account())
            self.mw_inc_ef_add_obs_payer_bankaccount_bik(participants_params_payer['bankAccount.bik'])
            self.mw_inc_ef_add_obs_payer_bankaccount_sum()
        elif obs_params == 'eWallet':
            self.mw_inc_ef_add_obs_payer_ewallet_number(''.join(choice(string.ascii_letters + string.digits)
                                                                for _ in range(15)))
            self.mw_inc_ef_add_obs_payer_ewallet_payment_sys(''.join(choice(string.ascii_letters + string.digits)
                                                                     for _ in range(20)))
            self.mw_inc_ef_add_obs_payer_ewallet_sum()
        elif obs_params == 'swift':
            self.mw_inc_ef_add_obs_payer_swift_number(self.generate_str_and_return())
            self.mw_inc_ef_add_obs_payer_swift_bik(participants_params_payer['swift.swiftBik'])
            self.mw_inc_ef_add_obs_payer_swift_sum()
        elif obs_params == 'retailAtm':
            self.mw_inc_ef_add_obs_payer_retail_sum()
            self.mw_inc_ef_add_obs_payer_retail_bin(participants_params_payer['retailAtm.acquirerId'])
            self.mw_inc_ef_add_obs_payer_retail_merchant(string_generator(min_length=10, max_length=50))
            self.mw_inc_ef_add_obs_payer_retail_mcc(''.join(choice(string.digits) for _ in range(4)))
        elif obs_params == 'other':
            self.mw_inc_ef_add_obs_payer_other_number(string_generator(min_length=10, max_length=50))
            self.mw_inc_ef_add_obs_payer_other_sum()
        self.mw_obs_fill_date_operation(utc_timestamp(date_format='%d.%m.%Y'), obs_params)

    def mw_inc_obs_fill_payee_areas(self, obs_params):
        """ относиться к заполнению ОБС
        Заполнение полей для получателя, входит в состав заполения обязательных полей ОБС
        """
        if obs_params == 'paymentCard':
            self.mw_inc_ef_add_obs_payee_paymentcard_number(payment_card(participants_params_payee['paymentCard.number']))
        elif obs_params == 'phoneNumber':
            number = ''.join([str(randint(0, 9)) for _ in range(10)])
            self.mw_inc_ef_add_obs_payee_phonenumber_number(number)
        elif obs_params == 'bankAccount':
            self.mw_inc_ef_add_obs_payee_bankaccount_number(bank_account())
            self.mw_inc_ef_add_obs_payee_bankaccount_bik(participants_params_payee['bankAccount.bik'])
        elif obs_params == 'eWallet':
            self.mw_inc_ef_add_obs_payee_ewallet_number(''.join(choice(string.ascii_letters + string.digits)
                                                                for _ in range(15)))
            self.mw_inc_ef_add_obs_payee_ewallet_payment_sys(''.join(choice(string.ascii_letters + string.digits)
                                                                for _ in range(20)))
        elif obs_params == 'swift':
            self.mw_inc_ef_add_obs_payee_swift_number(self.generate_str_and_return())
            self.mw_inc_ef_add_obs_payee_swift_bik(participants_params_payee['swift.swiftBik'])
        elif obs_params == 'retailAtm':
            self.mw_inc_ef_add_obs_payee_retail_bin(participants_params_payee['retailAtm.acquirerId'])
            self.mw_inc_ef_add_obs_payee_retail_merchant(string_generator(min_length=10, max_length=50))
            self.mw_inc_ef_add_obs_payee_retail_mcc(''.join(choice(string.digits) for _ in range(4)))
        elif obs_params == 'other':
            self.mw_inc_ef_add_obs_payee_other_number(string_generator(min_length=10, max_length=50))

    def mw_fill_incident_and_obs_with_required_fields(self, need_payee_request=None, **kwargs):
        """ ОСНОВНОЙ ИСПОЛЬЗУЕМЫЙ МЕТОД объединяет шаги по заполнению ОБС
        Заполнение обязательных полей ОбС

        :param kwargs: пара ключ значение если нужно заменить параметры для инцидента, пример
            org_type='company', payer_type='eWallet', payee_type='paymentCard'
            значения из функции collect_obs_param
        :param need_payee_request: bool
        """
        self.obs_params.update(collect_obs_param(need_payee_request))
        if kwargs:
            self.parsing_args_for_obs(kwargs)
        self.log.info("Выбранные параметры для ОБС %s" % str(self.obs_params))
        self.mw_increasing_counter_for_obs_locators()
        self.mw_inc_menu_click_obs_btn()
        self.mw_inc_ef_add_obs_btn()
        self.mw_inc_fill_org_type_info(self.obs_params['org_type'])

        self.mw_inc_ef_add_obs_detected_by(self.inc_params['vector'],
                                           self.mw_inc_ef_add_obs_detected_by_dropdown())
        self.mw_inc_ef_add_obs_payer_type(self.obs_params['payer_type'],self.mw_inc_ef_add_obs_payer_type_dropdown())
        self.mw_inc_obs_fill_payer_areas(self.obs_params['payer_type'])

        self.mw_inc_ef_add_obs_payee_type(self.obs_params['payee_type'],self.mw_inc_ef_add_obs_payee_type_dropdown())
        self.mw_inc_obs_fill_payee_areas(self.obs_params['payee_type'])
        self.obs_params['counter'] += 1

    def parsing_args_for_obs(self, inc_args):
        """замена рандомно сгенерированных параметров для ОБС если были переданы другие"""
        param_intersection = set(self.obs_params.keys()).intersection(inc_args)
        for i in param_intersection:
            self.obs_params[i] = inc_args[i]

    incident_info = {'description': None, 'department': None, 'tech_device': None, }
    obs_info = {'recipient_card': None, 'recipient_phone': '7'}

    def mw_fill_incident_and_two_obs_with_for_first_rule(self):
        """Заполнение  Эф инцидента c двумя ОбС для тест кейса 'Попадание атрибута в фиды по 1ому правилу'"""
        self.mw_fill_incident_with_required_fields(vector='INT', inc_type='scanPorts', assistance=False)
        self.mw_fill_incident_and_obs_with_required_fields(payer_type='paymentCard', payee_type='phoneNumber',
                                                           org_type='company')
        self.mw_fill_incident_and_obs_with_required_fields(payer_type='phoneNumber', payee_type='paymentCard')

    def mw_check_param_in_db(self, **kwargs):
        """метод проверяет в БД информацию по фидам после создания ОБС

         :param kwargs dict: принимает словарь тип: значение
         :type kwargs: dict
            пример: self.mw_check_param_in_db(phoneNumber='79091124618')
        """
        for key, value in kwargs.items():
            return self.db_client.find_feeds_in_db(feed_type=key, feed_value=value)

    def mw_check_after_two_obs(self):
        """
        метод проверяет результат в БД согласно тесткейсу 'Попадание атрибута в фиды по 1ому правилу'
        по первой обс данные должны быть в БД, по второй нет - т.к. необходим ответ

        :return:
        """
        check_first_obs = self.mw_check_param_in_db(phoneNumber=self.obs_info['recipient_phone'])
        if check_first_obs:
            self.log.info("Проверка по первой ОБС %s , ответ: %s" % (self.obs_info['recipient_phone'], check_first_obs))
        else:
            raise Exception("Информация по фиду %s не найдена" % self.obs_info['recipient_phone'])
        check_second_obs = self.mw_check_param_in_db(cardNumber=self.obs_info['recipient_card'])
        assert not check_second_obs
        self.log.info("ИНформация по карте не найдена т.к. ОБС еще не обработана")

    def mw_inc_ef_view_download_file(self):
        """ метод загрузки файла """
        self.ba_wait_for_loading()
        try:
            self.find_and_click(*self.locators.MW_INCIDENT_EF_FILE)
        except:
            sleep(1)
            self.driver.find_element(*self.locators.MW_INCIDENT_EF_FILE).click()
        self.ba_confirm_file_download()
