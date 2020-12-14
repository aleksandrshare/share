#!/usr/bin/env python
# -*- coding: utf-8 -*-

import allure


class TestBulletinsExtApi:
    @allure.feature('Text')
    @allure.story('Story01')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    def test_check_bulletins_get_request_via_ext_api(self, ext_api_payer):
        with allure.step('Text'):
            ext_api_payer.ea_get_bulletins()
        with allure.step('Text'):
            ext_api_payer.ea_check_bulletins_not_empty()

    @allure.feature('Text')
    @allure.story('Story01')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    def test_check_bulletins_get_request_with_limit_via_ext_api(self, ext_api_payer):
        with allure.step('Text'):
            ext_api_payer.ea_get_bulletins_with_param('limit', '1')
        with allure.step('Text'):
            ext_api_payer.ea_check_bulletin_count_in_answer(1)

    @allure.feature('Text')
    @allure.story('Story01')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    def test_check_bulletins_get_request_with_offset_via_ext_api(self, ext_api_payer):
        with allure.step('Text'):
            ext_api_payer.ea_get_bulletins_with_param('offset', '3')
        with allure.step('Text'):
            ext_api_payer.ea_check_offset_in_answer(3)

    @allure.feature('Text')
    @allure.story('Story01')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    def test_get_bulletin_info_via_ext_api(self, ext_api_payer):
        with allure.step('Text'):
            ext_api_payer.ea_get_random_bull_ids(1)
        with allure.step('Text'):
            ext_api_payer.ea_get_bulletin_data()

    @allure.feature('Text')
    @allure.story('Story01')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    def test_get_bulletins_info_by_ids_list_via_ext_api(self, ext_api_payer):
        with allure.step('Text'):
            ext_api_payer.ea_get_random_bull_ids(2)
        with allure.step('Text'):
            ext_api_payer.ea_get_bulletin_data_for_list()


