#!/usr/bin/env python
# -*- coding: utf-8 -*-

import allure
import pytest
from configs.modify_data import request_info_lku, cert_modify_data, test_modify_data
import os


class TestGosProjInteraction:

    @allure.feature('Text')
    @allure.story('Text')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    @pytest.mark.dependency(depends=['check_gos_proj_statuses_presence_in_lko_part3'])
    def test_check_gos_proj_statuses_presence_in_lko_part4(self, lkoz_ui):
        with allure.step('Text'):
            lkoz_ui.open_page()
            lkoz_ui.ba_set_cookie()
            lkoz_ui.ip_open_incident_by_id(test_modify_data['incident_ids'][0])
        with allure.step('Text'):
            lkoz_ui.ip_open_gos_proj_tab()
        with allure.step('Text'):
            lkoz_ui.ip_check_system_message_present_on_gos_proj_tab('changed to Close')

    @allure.feature('Text')
    @allure.story('Text')
    @allure.testcase("https://testrail.dom_name", "Ссылка на Testrail")
    @pytest.mark.dependency(name='check_file_in_malware_send_to_gos_proj_part1')
    def test_check_file_in_malware_send_to_gos_proj_part1(self, lku_ui, lkoz_ui, dss_mode, lkoz_admin_api):
        request_info_lku.clear()
        cert_modify_data.clear()
        test_modify_data.clear()
        inc_type = 'malware'
        with allure.step('Text'):
            lku_ui.open_page()
            lku_ui.ba_set_cookie(True)
            lku_ui.open_page()
        with allure.step(f'Text INT {inc_type}'):
            lku_ui.mp_lku_register_req_btn()
            lku_ui.mp_lku_register_incident_req_btn()
            lku_ui.mw_fill_incident_with_required_for_gos_proj_fields(vector='INT', inc_type=inc_type)
            lku_ui.mw_insert_file_in_malware()
            lku_ui.mw_insert_email_file_in_malware()
            lku_ui.mw_save_and_close_incident()
        with allure.step('Text'):
            lku_ui.rp_lku_fill_req_theme_and_msg()
            lku_ui.rp_lku_new_req_create_btn()
            lku_ui.rp_lku_add_signature_or_not(dss_mode, lku_ui.dss_pin_payee)
            lku_ui.rp_lku_save_request_hrid_after_create()
            lku_ui.rp_lku_get_request_id()
        with allure.step('Text'):
            test_modify_data.update({'req_id': request_info_lku['id']})
            lkoz_ui.api_client.ia_check_incident_created_from_request(1, test_modify_data)
        with allure.step('Text'):
            lkoz_ui.api_client.ga_wait_incident_send_to_gos_proj(test_modify_data)
            lkoz_ui.api_client.ga_get_gos_proj_events_count(test_modify_data)
            if test_modify_data['gos_proj_total'] < 2:
                test_modify_data['gos_proj_total'] = 2
            lkoz_admin_api.ga_get_incident_gos_proj_id(test_modify_data['incident_ids'][0], test_modify_data)

    @allure.feature('Text')
    @allure.story('Text')
    @allure.testcase("https://testrail.dom_name", "Ссылка на Testrail")
    @pytest.mark.dependency(depends=['check_file_in_malware_send_to_gos_proj_part1'])
    def test_check_file_in_malware_send_to_gos_proj_part2(self, lkoz_ui, cp_admin):
        with allure.step('Text'):
            cp_admin.open_page()
            cp_admin.ba_set_cookie()
            cp_admin.open_page()
        with allure.step('Text'):
            cp_admin.cp_ip_open_incident_by_id(test_modify_data['cert_incident_id'])
            cp_admin.cp_ip_view_click_malware_impact_link_on_action_bar()
        with allure.step('Text'):
            cp_admin.cp_ip_view_download_malware_sample()
            file_name = os.path.basename(lkoz_ui.MALWARE_RAR) + '.rar'
            cp_admin.cp_ip_view_check_downloaded_rar_file(file_name, lkoz_ui.MALWARE_RAR)
        with allure.step('Text'):
            cp_admin.cp_ip_view_download_malware_email_file()
            email_name = os.path.basename(lkoz_ui.MALWARE_EMAIL) + '.rar'
            cp_admin.cp_ip_view_check_downloaded_rar_file(email_name, lkoz_ui.MALWARE_EMAIL)

    @allure.feature('Text')
    @allure.story('Text')
    @allure.testcase("https://testrail.dom_name", "Ссылка на Testrail")
    @pytest.mark.dependency(depends=['check_file_in_attachments_send_to_gos_proj_part1'])
    def test_check_file_in_attachments_send_to_gos_proj_part2(self, lkoz_ui, cp_admin):
        with allure.step('Text'):
            cp_admin.open_page()
            cp_admin.ba_set_cookie()
            cp_admin.open_page()
        with allure.step('Text'):
            cp_admin.cp_ip_open_incident_by_id(test_modify_data['cert_incident_id'])
            cp_admin.cp_ip_view_click_attachment_link_on_action_bar()
        with allure.step('Text'):
            cp_admin.cp_ip_view_download_file_in_attachments_tab()
            file_name = os.path.basename(lkoz_ui.ATTACHMENT)
            cp_admin.cp_ip_view_check_downloaded_file(file_name, lkoz_ui.ATTACHMENT)




