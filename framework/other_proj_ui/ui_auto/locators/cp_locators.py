#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium.webdriver.common.by import By


class CertPortalLocators:
    # example only
    CP_LP_USER_NAME = (By.ID, 'loginInputEmail')
    CP_LP_PASSWORD = (By.ID, 'loginInputPassword')
    CP_LP_LOGIN_BTN = (By.ID, 'loginBtn')
    CP_IP_VIEW_COMMON_INFO_MENU_ITEM = (By.XPATH, '//mc-list//li/a/span[text()="Общие сведения"]')
    CP_IP_VIEW_INCIDENT_DESCRIPTION_MENU_ITEM = (By.XPATH, '//mc-list//li/a/span[text()="Описание инцидента"]')
    CP_IP_VIEW_ATTACHMENTS_MENU_ITEM = (By.XPATH, '//mc-list//li/a/span[text()="Вложения"]')
    CP_IP_VIEW_ACTIONS_MENU_ITEM = (By.XPATH, '//mc-list//li/a/span[text()="Полученные рекомендации и принятые меры"]')
    CP_IP_VIEW_COMMENTS_MENU_ITEM = (By.XPATH, '//mc-list//li/a/span[text()="Комментарии"]')
    CP_IP_VIEW_MALWARE_IMPACT_MENU_ITEM = (By.XPATH,
                                           '//li/div[text()="Вредоносное ПО"]/following-sibling::ul/li/a/span')
    CP_IP_VIEW_ATTACHMENT_FILE_LINK = (By.XPATH, '//incidents-view-attachments//a')

# and more more here
