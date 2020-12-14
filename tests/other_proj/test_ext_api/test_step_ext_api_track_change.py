#!/usr/bin/env python
# -*- coding: utf-8 -*-
import allure


class TestExtApiTrackChangeFull:
    @allure.feature('AText')
    @allure.story('Story01')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    def test_full_track_change(self, ext_api_payer):
        with allure.step('Text'):
            ext_api_payer.ea_send_track_change_and_check(timeout=54000)
