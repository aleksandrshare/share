#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ui_library.ui_lib import Page
from tools.utils import now_timestamp, convert_date_to_rus, convert_date_with_time_to_rus
from configs.modify_data import test_modify_data
from framework.other_proj_ui.ui_auto.fc_helpers import decorator_for_change_selenium_wait_and_return_after
from framework.other_proj_ui.ui_auto.fc_helpers import collect_locator
from configs.dictionary_variables import threat_types, federal_districts
from base64 import b64decode


class ThreatsEF(Page):
    """ Класс для работы с ЭФ угрозы """

    def th_click_new_ef_version_btn(self):
        """ метод кликает по кнопке 'Создать новую версию' в ЭФ """
        self.find_and_click(*self.locators.MW_NEW_THREAT_EF_VERSION_BUTTON)
        self.wait_for_invisibility_element(*self.locators.CIRCULAR_LOADER)
        self.search_element(*self.locators.MW_EDIT_THREAT_MODAL)

    def th_ef_fill_threat_name(self, text):
        """ метод заполняет поле Название  """
        self.find_and_clear_element(*self.locators.MW_EDIT_THREAT_MODAL_NAME_INPUT)
        self.find_and_fill_element(text, *self.locators.MW_EDIT_THREAT_MODAL_NAME_INPUT)

    def th_ef_fill_threat_description(self, text):
        """ метод заполняет поле Описание  """
        self.find_and_clear_element(*self.locators.MW_EDIT_THREAT_MODAL_DESCRIPTION_INPUT)
        self.find_and_fill_element(text, *self.locators.MW_EDIT_THREAT_MODAL_DESCRIPTION_INPUT)

    def th_ef_click_add_to_request_btn(self):
        """ метод кликает кнопку Добавить к запросу  """
        self.find_and_click(*self.locators.MW_EDIT_THREAT_MODAL_ADD_BTN)
        self.wait_for_invisibility_element(*self.locators.CIRCULAR_LOADER)

    def th_ef_edit_fields_and_save_new_version(self):
        """ метод изменяет значения в полях Название и Описание и сохраняет новую версию ЭФ
        ЭФ для редактирования должны быть уже открыта """
        test_modify_data['threat_edit_name'] = 'Угроза ред ' + now_timestamp()
        test_modify_data['threat_edit_description'] = 'Описание ред ' + now_timestamp()
        self.th_ef_fill_threat_name(test_modify_data['threat_edit_name'])
        self.th_ef_fill_threat_description(test_modify_data['threat_edit_description'])
        self.th_ef_click_add_to_request_btn()

    def th_click_detection_on_ef(self):
        """ метод кликает Обнаружение и устранение в меню слева """
        self.find_and_click(*self.locators.MW_VIEW_THREAT_NAV_BAR_DETECTION)
        self.ba_lku_wait_for_loading()

    @decorator_for_change_selenium_wait_and_return_after(5)
    def th_compare_ef_and_send_data_on_type_info(self, send_data=None):
        """ метод сравнивает данные в ЭФ и отосланные данные на вкладке данных импакта """
        if not send_data:
            send_data = test_modify_data['threat_data'][0]['threat']
        threat_type = send_data['type']
        self.find_and_click(*collect_locator(self.locators.MW_VIEW_THREAT_NAV_BAR_ITEM_PATTERN,
                                             threat_types[threat_type]))
        self.wait_for_invisibility_element(*self.locators.CIRCULAR_LOADER)

        if threat_type == 'MLW':
            self.th_compare_ef_mlw_data(send_data)
        elif threat_type == 'EXP':
            self.th_compare_ef_exp_data(send_data)
        elif threat_type == 'DOS':
            self.th_compare_ef_dos_data(send_data)
        elif threat_type == 'BCC':
            self.th_compare_ef_bcc_data(send_data)
        elif threat_type == 'PHI':
            self.th_compare_ef_phi_data(send_data)
        elif threat_type == 'MLR':
            self.th_compare_ef_mlr_data(send_data)
        elif threat_type == 'TEL':
            self.th_compare_ef_tel_data(send_data)
        elif threat_type == 'OTH':
            self.th_compare_ef_oth_data(send_data)
        else:
            raise ValueError(f'Неизвестный тип угрозы: {threat_type}')

    def th_compare_ef_bcc_data(self, data):
        """ метод сравнения для BCC """
        send_data = data['impacts']['BCC']

        ip_domain = self.ba_return_elem_text_or_none(*self.locators.MW_VIEW_THREAT_BCC_IP_OR_DOMAIN)
        if ip_domain != send_data['source']:
            test_modify_data['errors'].append(f"Не совпадает 'IP-адрес или доменное имя' в ЭФ на "
                                              f"{self.stand}: ожидаемое {send_data['source']}, "
                                              f"отображаемое {ip_domain}")

        decr = self.ba_return_elem_text_or_none(*self.locators.MW_VIEW_THREAT_BCC_TYPE_AND_INFO)
        if decr != send_data['description']:
            test_modify_data['errors'].append(f"Не совпадает 'Тип и общие сведения о ботнет' в ЭФ на {self.stand}: "
                                              f"ожидаемое {send_data['description']}, отображаемое {decr}")

        how_detected = self.ba_return_elem_text_or_none(*self.locators.MW_VIEW_THREAT_BCC_HOW_DETECTED)
        if how_detected != send_data['howDetected']:
            test_modify_data['errors'].append(f"Не совпадает 'Каким образом выявлен' в ЭФ на {self.stand}: "
                                              f"ожидаемое {send_data['howDetected']}, отображаемое {how_detected}")

    def th_compare_ef_phi_data(self, data):
        """ метод сравнения для PHI """
        send_data = data['impacts']['PHI']

        ip_domain = self.ba_return_elem_text_or_none(*self.locators.MW_VIEW_THREAT_PHI_IP_OR_DOMAIN)
        if ip_domain != send_data['source']:
            test_modify_data['errors'].append(f"Не совпадает 'IP-адрес или доменное имя' в ЭФ на "
                                              f"{self.stand}: ожидаемое {send_data['source']}, "
                                              f"отображаемое {ip_domain}")

        detected = self.ba_return_elem_text_or_none(*self.locators.MW_VIEW_THREAT_PHI_DETECTED_AT)
        send_date = convert_date_to_rus(send_data['detectedAt'])
        if detected != send_date:
            test_modify_data['errors'].append(f"Не совпадает 'Дата обнаружения ресурса' в ЭФ на {self.stand}: "
                                              f"ожидаемое {send_date}, отображаемое {detected}")

        email_body = self.ba_return_elem_text_or_none(*self.locators.MW_VIEW_THREAT_PHI_EMAIL_BODY)
        if email_body != send_data['emailBody']:
            test_modify_data['errors'].append(f"Не совпадает 'Текст письма' в ЭФ на {self.stand}: "
                                              f"ожидаемое {send_data['emailBody']}, отображаемое {email_body}")

        headers = self.ba_return_elem_text_or_none(*self.locators.MW_VIEW_THREAT_PHI_EMAIL_HEADERS)
        if headers != send_data['emailSubjects']:
            test_modify_data['errors'].append(f"Не совпадает 'Технические заголовки письма' в ЭФ на {self.stand}: "
                                              f"ожидаемое {send_data['emailSubjects']}, отображаемое {headers}")

    def th_compare_ef_mlr_data(self, data):
        """ метод сравнения для MLR """
        send_data = data['impacts']['MLR']

        ip_domain = self.ba_return_elem_text_or_none(*self.locators.MW_VIEW_THREAT_MLR_IP_OR_DOMAIN)
        if ip_domain != send_data['source']:
            test_modify_data['errors'].append(f"Не совпадает 'IP-адрес или доменное имя' в ЭФ на {self.stand}: "
                                              f"ожидаемое {send_data['source']}, отображаемое {ip_domain}")

        detected_at = self.ba_return_elem_text_or_none(*self.locators.MW_VIEW_THREAT_MLR_DETECTED_AT)
        send_date = convert_date_to_rus(send_data['detectedAt'])
        if detected_at != send_date:
            test_modify_data['errors'].append(f"Не совпадает 'Дата обнаружения ресурса' в ЭФ на {self.stand}: "
                                              f"ожидаемое {send_date}, отображаемое {detected_at}")

        reasons = self.ba_return_elem_text_or_none(*self.locators.MW_VIEW_THREAT_MLR_REASONS)
        if reasons != send_data['reasons']:
            test_modify_data['errors'].append(f"Не совпадает 'Причины, почему ресурс подозревается вредоносным' в ЭФ на "
                                              f"{self.stand}: ожидаемое {send_data['reasons']}, отображаемое {reasons}")

    def th_compare_ef_tel_data(self, data):
        """ метод сравнения для TEL """
        send_data = data['impacts']['TEL']

        called_at = self.ba_return_elem_text_or_none(*self.locators.MW_VIEW_THREAT_TEL_DATE_AND_TIME)
        send_date = convert_date_with_time_to_rus(send_data['calledAt'])
        if called_at != send_date:
            test_modify_data['errors'].append(f"Не совпадает 'Дата и время звонка (смс)' в ЭФ на {self.stand}: "
                                              f"ожидаемое {send_date}, отображаемое {called_at}")

        number = self.ba_return_elem_text_or_none(*self.locators.MW_VIEW_THREAT_TEL_NUMBER)
        if number != send_data['sourceNumber']:
            test_modify_data['errors'].append(f"Не совпадает 'Номер телефона' в ЭФ на {self.stand}: "
                                              f"ожидаемое {send_data['sourceNumber']}, отображаемое {number}")

        sms = self.ba_return_elem_text_or_none(*self.locators.MW_VIEW_THREAT_TEL_SMS)
        if sms != send_data['sms']:
            test_modify_data['errors'].append(f"Не совпадает 'Текст SMS' в ЭФ на {self.stand}: "
                                              f"ожидаемое {send_data['sms']}, отображаемое {sms}")

    def th_compare_ef_oth_data(self, data):
        """ метод сравнения для OTH """
        send_data = data['impacts']['OTH']

        description = self.ba_return_elem_text_or_none(*self.locators.MW_VIEW_THREAT_OTH_DESCRIPTION)
        if description != send_data['description']:
            test_modify_data['errors'].append(f"Не совпадает 'Описание' в ЭФ на {self.stand}: "
                                              f"ожидаемое {send_data['description']}, отображаемое {description}")

    def th_compare_send_data_with_ef_data(self):
        """ метод, объединяющий сравнения данных на всей ЭФ """
        self.th_compare_ef_and_send_data_on_common_info()
        self.th_compare_ef_and_send_data_on_type_info()
        self.th_click_detection_on_ef()
        self.th_compare_ef_and_send_data_on_detection()