#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ui_library.ui_lib import Page
import random


class ParticipantsPage(Page):
    """класс для работы со страницей участников"""
    participant_check = {'org_type': None, 'importance': None, 'id_payment': None}

    def pp_check_participants_grid(self):
        """метод проверки доступен ли рездел 'участники' на странице участников"""
        assert self.search_element(*self.locators.PP_PARTICIPANTS_GRID)

    def pp_find_and_click_test_participant(self):
        """метод для поиска и нажатия на участника autotest_ui"""
        self.find_and_click(*self.locators.PP_PARTICIPANTS_TEST)

    def pp_choose_test_participant(self):
        """метод находит родительский элемент участника autotest_ui и нажимает на него, чтобы проверить выделение
        строки"""
        test_parcitipant = self.search_element(*self.locators.PP_PARTICIPANTS_TEST)
        test_parcitipant.find_element(*self.locators.PP_PARTICIPANTS_TEST_PARENT).click()

    def pp_search_autotest_payer_participant(self):
        """вводит в поле поиска 'Автотесты_плательщик' для поиска """
        self.mp_fill_search_field('Автотесты_плательщик')

    def pp_click_edit_participant(self):
        """метод нажатия на кнопку 'редактировать участника'"""
        self.find_and_click(*self.locators.PP_EDIT_PARTICIPANT)

    def pp_click_dropdown_org_type(self):
        """метод находит и нажимает на выпад.список 'тип организации' в разделе редактирования участника"""
        self.find_and_click(*self.locators.PP_DROPDOWN_ORD_TYPE_ELEMENT)

    def pp_random_choose_org_type(self):
        """метод выбирает один из 3х вариантов типа организации в разделе 'редактирования участника'
        ВАЖНО: метод работает после открытия выпад.списока pp_click_dropdown_org_type"""
        list_of_elemets_org_type = [self.locators.PP_DROPDOWN_ORG_TYPE_FIRST,
                                    self.locators.PP_DROPDOWN_ORG_TYPE_SECOND,
                                    self.locators.PP_DROPDOWN_ORG_TYPE_THIRD]
        ran_int = random.randint(0, 2)
        self.participant_check['org_type'] = self.search_element(*list_of_elemets_org_type[ran_int]).text
        self.find_and_click(*list_of_elemets_org_type[ran_int])

    def pp_clear_and_fill_id_payment_system_field(self):
        """заполнить поле 'ID в платежной системе' при редактировании участника"""
        self.find_and_clear_element(*self.locators.PP_EDIT_ID_PAYMENT_SYSTEM)
        self.participant_check['id_payment'] = random.randint(1000, 2000)
        self.find_and_fill_element(self.participant_check['id_payment'], *self.locators.PP_EDIT_ID_PAYMENT_SYSTEM)

    def pp_check_participant_id_payment_system(self):
        """проверить что после рекдактирования 'ID в платежной системе' изменения применились
        ВАЖНО использовать после метода pp_clear_and_fill_id_payment_system_field"""
        assert str(self.participant_check['id_payment']) in self.return_text_ele(*self.locators.PP_ID_PAYMENT_SYSTEM)

    def pp_click_save_btn(self):
        """нажимает на кнопку сохранить в разделе 'редактирования участника'"""
        self.find_and_click(*self.locators.PP_EDIT_PARTICIPANT_SAVE_BTN)

    def pp_click_dropdown_importance(self):
        """метод находит и нажимает на выпад.список важность в разделе 'редактирования участника'"""
        self.find_and_click(*self.locators.PP_DROPDOWN_IMPORTANCE_ELEMENT)

    def pp_random_choose_importance(self):
        """метод выбирает один из 3х вариантов важности в разделе 'редактирования участника'
        ВАЖНО: метод работает после открытия выпад.списока pp_click_dropdown_importance"""
        list_of_elemets_importance = [self.locators.PP_DROPDOWN_IMPORTANCE_HIGH,
                                      self.locators.PP_DROPDOWN_IMPORTANCE_AVERAGE,
                                      self.locators.PP_DROPDOWN_IMPORTANCE_LOW]
        ran_int = random.randint(0, 2)
        self.participant_check['importance'] = self.search_element(*list_of_elemets_importance[ran_int]).text
        self.find_and_click(*list_of_elemets_importance[ran_int])

    def pp_check_participant_view(self):
        """метод проверки доступен ли раздел 'Параметры участника'"""
        self.search_element(*self.locators.PP_VIEW_PARTICIPANT)

    def pp_check_participant_org_type(self):
        """метод находит разделе 'Параметры участника' элемент 'тип организации' и сравнивает со значением,
        которое было сохранено после изменения в методе pp_random_choose_org_type"""
        check = self.search_element(*self.locators.PP_VIEW_PARTICIPANT_ORG_TYPE)
        assert check.text == self.participant_check['org_type']

    def pp_check_participant_importance(self):
        """метод находит разделе 'Параметры участника' элемент 'важность' и сравнивает со значением,
        которое было сохранено после изменения в методе pp_random_choose_importance"""
        check = self.search_element(*self.locators.PP_VIEW_PARTICIPANT_IMPORTANCE)
        assert check.text == self.participant_check['importance'], ("старое значение: %s | новое значение: %s" %
                                                                    (self.participant_check['importance'], check.text))
