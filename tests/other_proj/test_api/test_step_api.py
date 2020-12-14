#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import allure
from random import choice

payee_no_response = ('eWallet', 'phoneNumber', 'other')
payee_with_response = ('bankAccount', 'paymentCard', 'retailAtm', 'swift')


class TestFeedFiles:
    @allure.feature("Text")
    @allure.story('Text')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    def test_feeds_files_download(self, lkoz_api, lku_api_payer):
        with allure.step('Text'):
            lkoz_api.upload_feeds()
        with allure.step('Text'):
            lkoz_api.publish_feeds()
        with allure.step('Text'):
            feed_types = 'hashPassport, hashSnils, inn, phoneNumber, accountNumber, cardNumber, swift, ewalletNumber,' \
                         'retailAtm, other'
            lkoz_api.download_feed_file(feed_types, lkoz_api)
            lku_api_payer.download_feed_file(feed_types, lkoz_api)
            lku_api_payer.check_lku_lko_files_equal(feed_types)

    @allure.feature('Text')
    @allure.story('Text')
    @allure.testcase('https://testrail.don_name', 'TestCase link on TestRail')
    @pytest.mark.parametrize('payee_type, feed_type', [("phoneNumber", "phoneNumber"), ("eWallet", "ewalletNumber"),
                                                       ("other", "other")])
    def test_feeds_files_reupload_without_response(self, lkoz_api, lku_api_payer, payee_type, feed_type,
                                                   dss_mode):
        jpath = '$..vectorCode: INT\n$..lawEnforcementRequest.request: NPL'
        with allure.step('Text'):
            lkoz_api.upload_feeds()
        with allure.step('Text'):
            lkoz_api.publish_feeds()
        with allure.step('Text'):
            lkoz_api.download_feed_file(feed_type, lkoz_api)
            lku_api_payer.download_feed_file(feed_type, lkoz_api)
        with allure.step('Text {}'.format(payee_type)):
            lku_api_payer.user_generate_param_request(inc_quantity=1, obs_quantity=1, request_param=jpath,
                                                      payee_type=payee_type)
        with allure.step('Text'):
            if dss_mode != 'no':
                with allure.step('Text'):
                    lkoz_api.check_request_signature(direction='incoming', ef_quantity=1, obs_quantity=1)
            lkoz_api.rs_admin_check_request(inc_quantity=1, obs_quantity=1)
            lkoz_api.check_obs_is_handled()
        with allure.step('Text'):
            lkoz_api.get_payee_attributes()
        with allure.step('Text'):
            lkoz_api.upload_feeds()
        with allure.step('Text'):
            lkoz_api.publish_feeds()
        with allure.step('Text'):
            lkoz_api.download_feed_file(feed_type, lkoz_api)
            lku_api_payer.download_feed_file(feed_type, lkoz_api)
            lkoz_api.check_payee_attr_in_feed_file(feed_type, 'added', lkoz_api.stand.upper())
            lku_api_payer.check_payee_attr_in_feed_file(feed_type, 'added', lku_api_payer.stand.upper())
            lku_api_payer.check_lku_lko_files_equal(feed_type)

    @allure.feature('Text')
    @allure.story('Text')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    @pytest.mark.parametrize('payee_type, feed_type', [("bankAccount", "accountNumber, hashPassport, hashSnils, inn"),
                                                       ("paymentCard", "cardNumber, hashPassport, hashSnils, inn"),
                                                       ("swift", "swift, hashPassport, hashSnils, inn"),
                                                       ("retailAtm", "retailAtm, hashPassport, hashSnils, inn")])
    def test_feeds_files_reupload_with_response(self, lkoz_api, lku_api_payer, lku_api_payee, payee_type, feed_type,
                                                dss_mode):
        jpath_req = '$..vectorCode: INT\n$..lawEnforcementRequest.request: NPL'
        jpath_resp = '$..transferState: rejected'
        with allure.step('Text'):
            lkoz_api.upload_feeds()
        with allure.step('Text'):
            lkoz_api.publish_feeds()
        with allure.step('Text'):
            lkoz_api.download_feed_file(feed_type, lkoz_api)
            lku_api_payer.download_feed_file(feed_type, lkoz_api)
        with allure.step('Text'):
            lku_api_payer.user_generate_param_request(inc_quantity=1, obs_quantity=1, request_param=jpath_req,
                                                      payee_type=payee_type)
        with allure.step('Text'):
            if dss_mode != 'no':
                with allure.step('Text'):
                    lkoz_api.check_request_signature(direction='incoming', ef_quantity=1, obs_quantity=1)
            lkoz_api.rs_admin_check_request(inc_quantity=1, obs_quantity=1)
            lkoz_api.check_payee_requests()
        with allure.step('Text'):
            lku_api_payee.user_creates_param_response(jpath_resp)
            if dss_mode != 'no':
                with allure.step('Text'):
                    lkoz_api.check_response_signature(direction='incoming')
        with allure.step('Text'):
            lkoz_api.aa_check_obs_status(expected_status='processed')
        with allure.step('Text'):
            lkoz_api.get_payee_attributes()
        with allure.step('Text'):
            lkoz_api.upload_feeds()
            lkoz_api.publish_feeds()
        with allure.step('Text'):
            lkoz_api.download_feed_file(feed_type, lkoz_api)
            lku_api_payer.download_feed_file(feed_type, lkoz_api)
            lkoz_api.check_payee_attr_in_feed_file(feed_type, 'added', lkoz_api.stand.upper())
            lku_api_payer.check_payee_attr_in_feed_file(feed_type, 'added', lku_api_payer.stand.upper())
            lku_api_payer.check_lku_lko_files_equal(feed_type)

    @allure.feature('Text')
    @allure.story('Text')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    def test_participant_output_request_registered(self, lkoz_api, lku_api_payer, dss_mode):
        with allure.step('Text'):
            lku_api_payer.user_generate_param_request(inc_quantity=1, obs_quantity=1, request_param={},
                                                      payee_type=None)
        with allure.step('Text'):
            if dss_mode != 'no':
                with allure.step('Text'):
                    lkoz_api.check_request_signature(direction='incoming', ef_quantity=1, obs_quantity=1)
            lkoz_api.rs_admin_check_request(inc_quantity=1, obs_quantity=1)
        with allure.step('Text'):
            lku_api_payer.check_notifications(user_role='participant',
                                              expected_notification='output_request_registered')
        with allure.step('Text'):
            lku_api_payer.check_email_notifications(user_role='participant',
                                                    expected_notification='output_request_registered')

    @allure.feature('Text')
    @allure.story('Text')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    def test_participant_new_message_in_request(self, lkoz_api, lku_api_payer, dss_mode):
        with allure.step('Text'):
            lku_api_payer.user_generate_param_request(inc_quantity=1, obs_quantity=1, request_param={},
                                                      payee_type=None)
        with allure.step('Text'):
            if dss_mode != 'no':
                with allure.step('Text'):
                    lkoz_api.check_request_signature(direction='incoming', ef_quantity=1, obs_quantity=1)
            lkoz_api.rs_admin_check_request(inc_quantity=1, obs_quantity=1)
        with allure.step('Text'):
            lkoz_api.create_msg_request_lko('new message from admin')
        with allure.step('Text'):
            lku_api_payer.check_notifications(user_role='participant',
                                              expected_notification='new_message_in_request')
        with allure.step('Text'):
            lku_api_payer.check_email_notifications(user_role='participant',
                                                    expected_notification='new_message_in_request')

    @allure.feature('Text')
    @allure.story('Text')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    def test_participant_input_obs_request(self, lkoz_api, lku_api_payer, lku_api_payee, dss_mode):
        payee_type = choice(payee_with_response)
        with allure.step('Text'):
            lku_api_payer.user_generate_param_request(inc_quantity=1, obs_quantity=1, request_param={},
                                                      payee_type=payee_type)
        with allure.step('Text'):
            if dss_mode != 'no':
                with allure.step('Text'):
                    lkoz_api.check_request_signature(direction='incoming', ef_quantity=1, obs_quantity=1)
            lkoz_api.rs_admin_check_request(inc_quantity=1, obs_quantity=1)
        with allure.step('Text'):
            lkoz_api.check_payee_requests()
        with allure.step('Text'):
            lku_api_payee.check_notifications(user_role='participant', expected_notification='input_obs_request')
        with allure.step('Text'):
            lku_api_payee.check_email_notifications(user_role='participant',
                                                    expected_notification='input_obs_request',
                                                    incoming_email=True)

    @allure.feature('Text')
    @allure.story('Text')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    def test_participant_request_status_changed(self, lkoz_api, lku_api_payer, dss_mode):
        with allure.step('Text'):
            lku_api_payer.user_generate_param_request(inc_quantity=1, obs_quantity=1, request_param={},
                                                      payee_type=None)
        with allure.step('Text'):
            if dss_mode != 'no':
                with allure.step('Text'):
                    lkoz_api.check_request_signature(direction='incoming', ef_quantity=1, obs_quantity=1)
            lkoz_api.rs_admin_check_request(inc_quantity=1, obs_quantity=1)
        with allure.step('Text'):
            lkoz_api.rs_change_parameter(value='closed', parameter='status')
        with allure.step('Text'):
            lku_api_payer.check_notifications(user_role='participant',
                                              expected_notification='request_status_changed')
        with allure.step('Text'):
            lku_api_payer.check_email_notifications(user_role='participant',
                                                    expected_notification='request_status_changed')

    @allure.feature('Text')
    @allure.story('Text')
    @allure.testcase('https://testrail.dom_name', 'TestCase link on TestRail')
    def test_participant_feed_published(self, lkoz_api, lku_api_payee):
        with allure.step('Text'):
            lkoz_api.publish_feeds()
        with allure.step('Text'):
            lku_api_payee.check_notifications(user_role='participant',
                                              expected_notification='feed_published')
        with allure.step('Text'):
            lku_api_payee.check_email_notifications(user_role='participant',
                                                    expected_notification='feed_published')


# and more more here
