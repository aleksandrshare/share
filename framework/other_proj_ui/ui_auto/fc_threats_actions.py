#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ui_library.ui_lib import Page
from configs.modify_data import test_modify_data
from framework.other_proj_ui.ui_auto.fc_helpers import decorator_for_change_selenium_wait_and_return_after
from configs.dictionary_variables import threat_types, federal_districts
from tools.utils import convert_date_to_inc_output
from framework.other_proj_ui.ui_auto.fc_helpers import collect_locator
import allure


class ThreatsPage(Page):
    """ Класс для работы с угрозами """

    def thp_open_detection_menu_item(self):
        """ нажать Обнаружение и устранение на странице создания угрозы"""
        self.find_and_click(*self.locators.THP_CREATE_EDIT_PAGE_NAV_BAR_DETECTION_ITEM)
        self.ba_wait_for_loading()

    def thp_click_save_btn(self):
        """ нажать кнопку Создать"""
        self.find_and_click(*self.locators.THP_CREATE_EDIT_PAGE_SAVE_BTN)
        self.ba_wait_for_loading()
        self.search_element(*self.locators.THP_THREAT_VIEW_PAGE)

    def thp_get_threat_id(self):
        """Получить id запроса"""
        self.ba_wait_for_loading()
        test_modify_data['threat_id'] = self.driver.current_url.partition('/threats/view/')[2]
        self.log.info('Получен id созданной угрозы: {}'.format(test_modify_data['threat_id']))
        allure.attach(self.driver.current_url, 'Ссылка на угрозу', allure.attachment_type.URI_LIST)

    def thp_create_threat_from_ef(self):
        """ метод, объединяющий шаги по созданию угрозы из ЭФ """
        self.thp_open_detection_menu_item()
        self.thp_click_save_btn()
        self.thp_get_threat_id()

    @staticmethod
    def thp_compare_detected_at_date(initial_date, current_date):
        no_errors = True
        initial_date_split = initial_date.split()
        after_sync_date_split = current_date.split()
        initial_date_minutes = initial_date_split[0]
        after_sync_date_minutes = after_sync_date_split[0]
        diff = int(after_sync_date_minutes) - int(initial_date_minutes)
        if abs(diff) > 1:
            no_errors = False
            return no_errors
        else:
            initial_date_split.pop(0)
            after_sync_date_split.pop(0)
            if not initial_date_split == after_sync_date_split:
                no_errors = False
                return no_errors
        return no_errors

    @decorator_for_change_selenium_wait_and_return_after(5)
    def thp_compare_threat_with_send_data_on_type_info(self, send_data=None):
        """ метод сравнения для данных по выбранному типу угрозы """
        if not send_data:
            send_data = test_modify_data['threat_data'][0]['threat']
        threat_type = send_data['type']
        self.find_and_click(*collect_locator(self.locators.THP_THREAT_VIEW_NAV_BAR_ITEM_PATTERN,
                                             threat_types[threat_type]))
        self.ba_wait_for_loading()

        if threat_type == 'MLW':
            self.thp_compare_mlw_data(send_data)
        elif threat_type == 'EXP':
            self.thp_compare_exp_data(send_data)
        elif threat_type == 'DOS':
            self.thp_compare_dos_data(send_data)
        elif threat_type == 'BCC':
            self.thp_compare_bcc_data(send_data)
        elif threat_type == 'PHI':
            self.thp_compare_phi_data(send_data)
        elif threat_type == 'MLR':
            self.thp_compare_mlr_data(send_data)
        elif threat_type == 'TEL':
            self.thp_compare_tel_data(send_data)
        elif threat_type == 'OTH':
            self.thp_compare_oth_data(send_data)
        else:
            raise ValueError(f'Неизвестный тип угрозы: {threat_type}')

    def thp_compare_dos_data(self, data=None):
        """ метод сравнения для DOS """
        if not data:
            data=test_modify_data['threat_data'][0]['threat']
        send_data = data['impacts']['DOS']

        ip = self.ba_return_elem_text_or_none(*self.locators.THP_THREAT_VIEW_DOS_IPS)
        if ip != send_data['sourceIp'].strip():
            test_modify_data['errors'].append(f"Не совпадают 'Атакующие IP-адреса' в угрозе, "
                                              f"ожидаемое {send_data['sourceIp'].strip()}, отображаемое {ip}")

        attack_type = self.ba_return_elem_text_or_none(*self.locators.THP_THREAT_VIEW_DOS_ATTACK_TYPE)
        if attack_type != send_data['type']:
            test_modify_data['errors'].append(f"Не совпадает 'Тип атаки, ожидаемое {send_data['sourceIp']}, "
                                              f"отображаемое {attack_type}")

        attack_power = self.ba_return_elem_text_or_none(*self.locators.THP_THREAT_VIEW_DOS_PREDICTED_ATTACK_POWER)
        if attack_power != send_data['predictedAttackPower']:
            test_modify_data['errors'].append(f"Не совпадает 'Ожидаемая мощность' в угрозе, "
                                              f"ожидаемое {send_data['predictedAttackPower']}, "
                                              f"отображаемое {attack_power}")

        attack_increase = self.ba_return_elem_text_or_none(*self.locators.THP_THREAT_VIEW_DOS_PREDICTED_ATTACK_INCREASE)
        if attack_increase != send_data['predictedAttackIncrease']:
            test_modify_data['errors'].append(f"Не совпадает 'Ожидаемое усиление, "
                                              f"ожидаемое {send_data['predictedAttackIncrease']}, "
                                              f"отображаемое {attack_increase}")

    def thp_compare_mlw_data(self, data=None):
        """ метод сравнения для MLW """
        if not data:
            data = test_modify_data['threat_data'][0]['threat']
        send_data = data['impacts']['MLW']

        antivir = self.ba_return_elem_text_or_none(*self.locators.THP_THREAT_VIEW_MLW_ANTIVIRUS)
        if antivir != send_data['detectedByAntiviruses']:
            test_modify_data['errors'].append(f"Не совпадает 'Обнаруживается антивирусными решениями' в угрозе, "
                                              f"ожидаемое {send_data['detectedByAntiviruses']}, "
                                              f"отображаемое {antivir}")
        indicators = self.ba_return_elem_text_or_none(*self.locators.THP_THREAT_VIEW_MLW_INDICATORS)
        if indicators != send_data['indicators']:
            test_modify_data['errors'].append(f"Не совпадает 'Индикаторы компрометации' в угрозе, "
                                              f"ожидаемое {send_data['indicators']}, отображаемое {antivir}")

    def thp_compare_exp_data(self, data=None):
        """ метод сравнения для EXP """
        if not data:
            data = test_modify_data['threat_data'][0]['threat']
        send_data = data['impacts']['EXP']

        ids = self.ba_return_elem_text_or_none(*self.locators.THP_THREAT_VIEW_EXP_IDS)
        if ids != send_data['identifiers']:
            test_modify_data['errors'].append(f"Не совпадает 'Идентификаторы уязвимости' в угрозе,"
                                              f" ожидаемое {send_data['identifiers']}, "
                                              f"отображаемое {ids}")
        method = self.ba_return_elem_text_or_none(*self.locators.THP_THREAT_VIEW_EXP_EXPLOITATION_METHOD)
        if method != send_data['exploatationMethod']:
            test_modify_data['errors'].append(f"Не совпадает 'Методика эксплуатации' в угрозе, "
                                              f"ожидаемое {send_data['exploatationMethod']}, отображаемое {method}")

    def thp_compare_bcc_data(self, data=None):
        """ метод сравнения для BCC """
        if not data:
            data = test_modify_data['threat_data'][0]['threat']
        send_data = data['impacts']['BCC']

        ip_domain = self.ba_return_elem_text_or_none(*self.locators.THP_THREAT_VIEW_BCC_IP_OR_DOMAIN)
        if ip_domain != send_data['source']:
            test_modify_data['errors'].append(f"Не совпадает 'IP-адрес или доменное имя' в угрозе, "
                                              f"ожидаемое {send_data['source']}, отображаемое {ip_domain}")

        decr = self.ba_return_elem_text_or_none(*self.locators.THP_THREAT_VIEW_BCC_TYPE_AND_INFO)
        if decr != send_data['description']:
            test_modify_data['errors'].append(f"Не совпадает 'Тип и общие сведения о ботнет' в угрозе, "
                                              f"ожидаемое {send_data['description']}, отображаемое {decr}")

        how_detected = self.ba_return_elem_text_or_none(*self.locators.THP_THREAT_VIEW_BCC_HOW_DETECTED)
        if how_detected != send_data['howDetected']:
            test_modify_data['errors'].append(f"Не совпадает 'Каким образом выявлен' в угрозе, "
                                              f"ожидаемое {send_data['howDetected']}, отображаемое {how_detected}")

    def thp_compare_phi_data(self, data=None):
        """ метод сравнения для PHI """
        if not data:
            data = test_modify_data['threat_data'][0]['threat']
        send_data = data['impacts']['PHI']

        ip_domain = self.ba_return_elem_text_or_none(*self.locators.THP_THREAT_VIEW_PHI_IP_OR_DOMAIN)
        if ip_domain != send_data['source']:
            test_modify_data['errors'].append(f"Не совпадает 'IP-адрес или доменное имя' в угрозе,"
                                              f" ожидаемое {send_data['source']}, отображаемое {ip_domain}")

        detected = self.ba_return_elem_text_or_none(*self.locators.THP_THREAT_VIEW_PHI_DETECTED_AT)
        send_date = convert_date_to_inc_output(send_data['detectedAt'])
        if detected != send_date:
            if not self.thp_compare_detected_at_date(send_date,detected):
                test_modify_data['errors'].append(f"Не совпадает 'Дата обнаружения ресурса' в угрозе, "
                                                    f"ожидаемое {send_date}, отображаемое {detected}")

        email_body = self.ba_return_elem_text_or_none(*self.locators.THP_THREAT_VIEW_PHI_EMAIL_BODY)
        if email_body != send_data['emailBody']:
            test_modify_data['errors'].append(f"Не совпадает 'Текст письма' в угрозе, "
                                              f"ожидаемое {send_data['emailBody']}, отображаемое {email_body}")

        headers = self.ba_return_elem_text_or_none(*self.locators.THP_THREAT_VIEW_PHI_EMAIL_HEADERS)
        if headers != send_data['emailSubjects']:
            test_modify_data['errors'].append(f"Не совпадает 'Технические заголовки письма' в угрозе, "
                                              f"ожидаемое {send_data['emailSubjects']}, отображаемое {headers}")

    def thp_compare_mlr_data(self, data=None):
        """ метод сравнения для MLR """
        if not data:
            data = test_modify_data['threat_data'][0]['threat']
        send_data = data['impacts']['MLR']

        ip_domain = self.ba_return_elem_text_or_none(*self.locators.THP_THREAT_VIEW_MLR_IP_OR_DOMAIN)
        if ip_domain != send_data['source']:
            test_modify_data['errors'].append(f"Не совпадает 'IP-адрес или доменное имя, "
                                              f"ожидаемое {send_data['source']}, отображаемое {ip_domain}")

        detected_at = self.ba_return_elem_text_or_none(*self.locators.THP_THREAT_VIEW_MLR_DETECTED_AT)
        send_date = convert_date_to_inc_output(send_data['detectedAt'])
        if detected_at != send_date:
            if not self.thp_compare_detected_at_date(send_date, detected_at):
                test_modify_data['errors'].append(f"Не совпадает 'Дата обнаружения ресурса' в угрозе, ожидаемое {send_date}, "
                                              f"отображаемое {detected_at}")

        reasons = self.ba_return_elem_text_or_none(*self.locators.THP_THREAT_VIEW_MLR_REASONS)
        if reasons != send_data['reasons']:
            test_modify_data['errors'].append(f"Не совпадает 'Причины, почему ресурс подозревается вредоносным' в угрозе, "
                                              f"ожидаемое {send_data['reasons']}, отображаемое {reasons}")

    def thp_compare_tel_data(self, data=None):
        """ метод сравнения для TEL """
        if not data:
            data = test_modify_data['threat_data'][0]['threat']
        send_data = data['impacts']['TEL']

        called_at = self.ba_return_elem_text_or_none(*self.locators.THP_THREAT_VIEW_TEL_DATE_AND_TIME)
        send_date = convert_date_to_inc_output(send_data['calledAt'])
        if called_at != send_date:
            if not self.thp_compare_detected_at_date(send_date, called_at):
                test_modify_data['errors'].append(f"Не совпадает 'Дата и время звонка (смс)' в угрозе, ожидаемое {send_date}, "
                                                    f"отображаемое {called_at}")

        number = self.ba_return_elem_text_or_none(*self.locators.THP_THREAT_VIEW_TEL_NUMBER)
        if number != send_data['sourceNumber']:
            test_modify_data['errors'].append(f"Не совпадает 'Номер телефона' в угрозе, ожидаемое {send_data['sourceNumber']}, "
                                              f"отображаемое {number}")

        sms = self.ba_return_elem_text_or_none(*self.locators.THP_THREAT_VIEW_TEL_SMS)
        if sms != send_data['sms']:
            test_modify_data['errors'].append(f"Не совпадает 'Текст SMS' в угрозе, ожидаемое {send_data['sms']}, "
                                              f"отображаемое {sms}")

    def thp_compare_oth_data(self, data=None):
        """ метод сравнения для OTH """
        if not data:
            data = test_modify_data['threat_data'][0]['threat']
        send_data = data['impacts']['OTH']

        description = self.ba_return_elem_text_or_none(*self.locators.THP_THREAT_VIEW_OTH_DESCRIPTION)
        if description != send_data['description']:
            test_modify_data['errors'].append(f"Не совпадает 'Описание' в угрозе, ожидаемое {send_data['description']}, "
                                              f"отображаемое {description}")

    def thp_click_detection_on_view(self):
        """ Нажать Обнаружение и устранение на странице просмотра угрозы """
        self.find_and_click(*self.locators.THP_THREAT_VIEW_NAV_BAR_DETECTION)
        self.ba_wait_for_loading()

    def thp_compare_send_data_with_threat_data(self):
        """ метод, объединяющий сравнения данных угрозы """
        self.thp_compare_threat_with_send_data_on_common_info()
        self.thp_compare_threat_with_send_data_on_type_info()
        self.thp_click_detection_on_view()
        self.thp_compare_threat_with_send_data_on_detection()
