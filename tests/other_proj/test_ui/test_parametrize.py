#!/usr/bin/env python
# -*- coding: utf-8 -*-

import allure
import pytest
from configs.settings import inc_type_int, inc_type_ext


test_list_int = {i: 'INT' for i in inc_type_int}
test_list_ext = {i: 'EXT' for i in inc_type_ext}
result_list_for_inc = list(test_list_int.items()) + list(test_list_ext.items())


class TestIncidents:
    @allure.feature('Text')
    @allure.story('Text')
    @allure.testcase("Test obj with different parameters")
    @pytest.mark.parametrize('inc_type, vector', result_list_for_inc)
    @pytest.mark.parametrize('contour', ("lku", "lkoz"))
    def test_create_incidents(self, lku, lkoz, contour, inc_type, vector, dss_mode):
        with allure.step('Text'):
            if contour == "lku":
                test_contour = lku
            else:
                test_contour = lkoz
            test_contour.open_page()
            test_contour.ba_set_cookie()
            test_contour.open_page()
        with allure.step(f'Text {vector} {inc_type}'):
            if contour == "lku":
                test_contour.mp_lku_register_req_btn()
                test_contour.mp_lku_register_incident_req_btn()
            else:
                lkoz.mp_lko_register_req_btn()
                lkoz.mp_lko_register_incident_req_btn()
            test_contour.mw_fill_incident_with_required_fields(vector=vector, inc_type=inc_type)
            test_contour.mw_save_and_close_incident()
        with allure.step('Text'):
            if contour == "lku":
                test_contour.rp_lku_fill_req_theme_and_msg()
                test_contour.rp_lku_new_req_create_btn()
                test_contour.rp_lku_add_signature_or_not(dss_mode, lku.dss_pin_payer)
                test_contour.rp_lku_save_request_hrid_after_create()
                test_contour.rp_lku_get_request_id()
            else:
                lkoz.rp_lko_fill_req_theme_and_msg()
                lkoz.rp_lko_new_req_create_btn()
                lkoz.ba_wait_for_loading()
                lkoz.rp_lko_save_request_hrid_after_create()
                lkoz.rp_lko_get_request_id_from_url()
        with allure.step('Text'):
            lkoz.check_all_obs_in_status_processed_after_create_from_lku(where=contour)
