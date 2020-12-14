#!/usr/bin/env python
# -*- coding: utf-8 -*-

from framework.ui_libs.ui_lib import Page
from configs.modify_data import test_modify_data
import allure


class InfoCardPage(Page):
    """ Класс для работы со страницей информационных карточек"""

    def icp_open_calc_menu_item(self):
        """ нажать 'Калькулятор рейтинга публикации' на странице создания публикации"""
        self.find_and_click(*self.locators.ICP_CREATE_EDIT_PAGE_NAV_BAR_CALC_ITEM)
        self.ba_wait_for_loading()

    def icp_click_save_btn(self):
        """ нажать кнопку Создать"""
        self.find_and_click(*self.locators.ICP_CREATE_EDIT_PAGE_SAVE_BTN)
        self.ba_wait_for_loading(120)
        self.search_element(*self.locators.ICP_INFO_CARD_VIEW_PAGE)

    def icp_get_info_card_id(self):
        """Получить id инфокарты"""
        self.ba_wait_for_loading()
        test_modify_data['info_card_id'] = self.driver.current_url.partition('/infoCards/view/')[2]
        self.log.info('Получен id созданной инфокарты: {}'.format(test_modify_data['info_card_id']))
        allure.attach(self.driver.current_url, 'Ссылка на инфокарту', allure.attachment_type.URI_LIST)

    def icp_create_info_card_from_ef(self):
        """ метод, объединяющий шаги по созданию инфокарты из ЭФ публикации """
        self.icp_open_calc_menu_item()
        self.icp_click_save_btn()
        self.icp_get_info_card_id()

    def icp_click_common_info_link_on_view_page(self):
        """ нажать "Общие сведения" на странице просмотра инфокарты """
        self.find_and_click(*self.locators.ICP_INFO_CARD_VIEW_NAV_BAR_COMMON_INFO)
        self.ba_wait_for_loading()

    def icp_click_event_link_on_view_page(self):
        """ нажать "Мероприятие" на странице просмотра инфокарты """
        self.find_and_click(*self.locators.ICP_INFO_CARD_VIEW_NAV_BAR_EVENT)
        self.ba_wait_for_loading()

    def icp_click_calc_link_on_view_page(self):
        """ нажать "Калькулятор рейтинга публикации" на странице просмотра инфокарты """
        self.find_and_click(*self.locators.ICP_INFO_CARD_VIEW_NAV_BAR_CALC)
        self.ba_wait_for_loading()

    def icp_compare_send_data_with_info_card_data(self, send_data=None):
        """ сравнить отображаемые данные в инфокарте в данными, заданными при создании """
        self.icp_compare_info_card_with_send_data_on_common_info(send_data)
        self.icp_click_event_link_on_view_page()
        self.icp_compare_info_card_with_send_data_on_event(send_data)
