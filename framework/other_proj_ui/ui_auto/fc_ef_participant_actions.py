#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ui_library.ui_lib import Page
from configs.modify_data import test_modify_data


class ParticipantEF(Page):
    def pr_ef_compare_send_data_with_ef_data(self, send_data=None):
        self.pr_ef_compare_ef_and_send_data_participant_info(send_data)
        self.pr_ef_click_persons_tab_on_ef()
        self.pr_ef_compare_ef_and_send_data_all_persons_info(send_data)

    def pr_ef_click_persons_tab_on_ef(self):
        """ Кликнуть на вкладку 'Ответственные лица' """
        self.find_and_click(*self.locators.MW_VIEW_PARTICIPANT_PERSONS_TAB)

    def pr_ef_click_changes_tab_on_ef(self):
        """ Кликнуть на вкладку 'Список изменений' """
        self.find_and_click(*self.locators.MW_VIEW_PARTICIPANT_DIFFS_TAB)
        self.ba_wait_for_loading()

    def pr_ef_mw_person_mw_close_btn(self):
        """ Закрыть модалку просмотра пользователя Участника """
        self.find_and_click(*self.locators.MW_VIEW_PARTICIPANT_PERSON_MW_CLOSE)

    def pr_ef_check_add_new_version_btn_absent(self):
        """ метод проверяет, что кнопка Создать новую версию отсутствует"""
        try:
            elems = self.search_elements(*self.locators.MW_NEW_PARTICIPANT_EF_NEW_VERSION_BUTTON)
            if elems:
                test_modify_data['errors'].append('Кнопка "Создать новую версию" отображается, хотя должна '
                                                  'отсутствовать')
        except:
            self.log.info('Кнопка "Создать новую версию" отсутствует, как ожидалось')

    def pr_ef_close_btn(self):
        """ Нажать на кнопку 'Крестик' (Закрыть) """
        self.find_and_click(*self.locators.MW_VIEW_PARTICIPANT_EF_CLOSE_BTN)
