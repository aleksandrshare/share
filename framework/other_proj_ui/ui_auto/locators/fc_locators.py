#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium.webdriver.common.by import By


class BaseLocators:
    PROGRESS_BAR = (By.XPATH, '//progress-bar')
    CIRCULAR_LOADER = (By.CLASS_NAME, 'circular')
    LP_PASSWORD = (By.ID, 'password')
    LP_LOGIN_BTN = (By.ID, 'loginBtn')
    MW_NEW_EF_INCIDENT_CLOSE = (By.XPATH, '//button[@title="Закрыть"]')
    MW_NEW_EF_INCIDENT_ACCEPT_CLOSE = (By.ID, 'acceptBtn')
    MW_NEW_EF_INCIDENT_CANCEL_CLOSE = (By.ID, 'editBtn')
    MW_NEW_EF_INCIDENT_TAB_PATTERN = '//div[@role="button"]//div[@title="{}"]'
    MW_NEW_EF_INCIDENT_MENU_OBS_BTN = (By.XPATH, '//*[@data-test="mw_ef_tab_antifraud"]')
    MW_NEW_EF_INCIDENT_ASSISTANCE_NND_BTN = (By.XPATH, '//mc-select//span[text()="Не требуется"]')
    MW_NEW_EF_INCIDENT_DESCRIPTION = (By.XPATH, '//textarea[contains(@id, "description")]')
    MW_NEW_EF_INCIDENT_FIXATION_DATE = (By.XPATH, '//mc-datepicker[contains(@name, "fixationDate")]//input')
    MW_NEW_EF_INCIDENT_DEPARTMENT = (By.XPATH, '//input[contains(@id, "department")]')
    MW_NEW_EF_INCIDENT_TECH_DEVICE = (By.XPATH, '//input[contains(@id, "technicalDevice")]')
    MW_NEW_EF_INCIDENT_ATTACKED_SERVICES_TYPE_DROPDOWN = (By.XPATH, '//*[@data-test="mw_ef_serviceType[0].type"]')
    MW_EDIT_LOCKREQUEST_RESPONSE_STATE_REJECTED = (By.XPATH, '//*[@class="mc-btn-group"]//span[text()="Отказано"]')
    MW_EDIT_LOCKREQUEST_RESPONSE_SAVE_BTN = (By.XPATH, '//button[@id="saveBtn" and text()="Сохранить"]')
    MW_EDIT_LOCKREQUEST_RESPONSE_STATE_BADGE = (By.XPATH, '//correspondent-account-coordination-status-badge'
                                                          '/badge/span')
    MW_EDIT_LOCKREQUEST_RESPONSE_STATE_BADGE_ACCEPTED = (By.XPATH, '//correspondent-account-coordination-status-badge'
                                                        '/badge//span[contains(text(), "Одобрено")]')


class LocatorsLKU(BaseLocators):
    MP_LKU_REQUESTS_BTN = (By.XPATH, '//span[text()="Запросы"]')
    MP_LKU_BULLETINS_LINK = (By.XPATH, '//a[text()="Рассылки центра"]')
    RP_LKU_SEND_MSG_BTN = (By.ID, 'sendMessageBtn')
    RP_LKU_ADD_DS_YES_SIGNATURE_BTN = (By.XPATH, '//button[contains(text(), "Подписать")]')
    MP_REQUESTS_BTN = (By.LINK_TEXT, 'Запросы')
    BP_LKU_ITEM_PATTERN = '//bulletins-grid//div[text()=\'{}\']'


class LocatorsLKO(BaseLocators):
    PRELOADER = (By.CLASS_NAME, 'preloader')
    CONFIRM_DOWNLOAD_SAVE_BUTTON = (By.ID, 'downloadDangerousFile')
    LP_USER_NAME = (By.XPATH, '//input[(@id="usernameLocal") or (@id="username")]')
    MP_BULLETINS_LINK = (By.XPATH, '//a[text()="Рассылки центра"]')
    MP_INCIDENTS_BTN = (By.XPATH, '//button/span[text()="Инциденты"]')
    MP_INCIDENTS_LINK = (By.XPATH, '//a[text()="Инциденты"]')
    PP_DROPDOWN_IMPORTANCE_HIGH = (By.XPATH, '//mc-select[@id="participantImportance"]//span[text()="Высокая"]')
    PP_EDIT_ID_PAYMENT_SYSTEM = (By.XPATH, '//input[contains(@id, "paymentSystemMemberId")]')

# and more more here
