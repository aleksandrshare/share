from framework.ui_libs.ui_lib import Page
from ui_library.dad_file_with_js import drag_and_drop_file
from framework.other_proj_ui.ui_auto.fc_helpers import decorator_for_change_selenium_wait_and_return_after
from tools.utils import now_timestamp
from selenium.webdriver.common.keys import Keys
from random import choice
from framework.other_proj_ui.ui_auto.fc_helpers import collect_locator
import os
from time import sleep
import pytest


class BulletinsLkoPage(Page):
    """"""

    # В словарях храним данные, которыми заполнили бюллетень, для проверки на других контурах.
    bulletin_common_info = {'header': None, 'id': None, 'description': None, 'type': None, 'sub_type': None}
    bulletin_files = {'source': None, 'published': None, 'additional': []}
    bulletin_participants_info = {'participants': None, 'mail_groups': None}
    bulletin_mailing_groups = {'name': None}

    # пути к файлам для загрузки в бюллетень
    BP_FILE_1 = os.getcwd() + '/test_data/Doc_for_test.txt'
    BP_FILE_2 = os.getcwd() + '/test_data/fc_ИР.pdf'
    BP_FILE_3 = os.getcwd() + '/test_data/entities_description.xlsx'
    BP_FILE_4 = os.getcwd() + '/test_data/other.csv'
    BP_FILE_5 = os.getcwd() + '/test_data/Протокол.docx'
    BP_FILE_6 = os.getcwd() + '/test_data/test.rar'
    BP_FILE_7 = os.getcwd() + '/test_data/Учебный_материал_по_ОТ.doc'
    BP_FILE_8 = os.getcwd() + '/test_data/specprojects.pdf'

    def bp_clear_info_data_before_test(self):
        """ метод обнуляет значения в словарях """
        for key in self.bulletin_common_info.keys():
            self.bulletin_common_info[key] = None
        self.bulletin_files['source'] = None
        self.bulletin_files['published'] = None
        self.bulletin_files['additional'] = []
        self.bulletin_participants_info['participants'] = None
        self.bulletin_participants_info['mail_groups'] = None
        self.bulletin_mailing_groups['name'] = None

    def bp_open_create_bulletin_page(self):
        """ Метод открывает страницу создания новой рассылки """
        self.find_and_click(*self.locators.BP_ADD_BULLETINS)
        assert self.search_element(*self.locators.BP_CREATE_PAGE)
        self.ba_simple_wait_for_loading()

    def bp_fill_bulletin_header(self, text):
        """ Метод заполнения заголовка рассылки """
        self.find_and_fill_element(text, *self.locators.BP_BULLETIN_HEADER)

    def bp_fill_bulletin_id(self, text):
        """ Метод заполнения ID рассылки """
        self.find_and_fill_element(text, *self.locators.BP_BULLETIN_ID)

    def bp_fill_bulletin_description(self, text):
        """ Метод заполнения краткого описания рассылки """
        self.find_and_fill_element(text, *self.locators.BP_BULLETIN_DESCRIPTION)

    def bp_select_bulletin_type(self, type_locator):
        """ Метод заполнения типа рассылки """
        self.find_and_click(*self.locators.BP_BULLETIN_TYPE)
        self.find_and_click(*type_locator)

    def bp_select_bulletin_subtype(self, subtype_locator):
        """ Метод заполнения подтипа рассылки """
        self.find_and_click(*self.locators.BP_BULLETIN_SUBTYPE)
        self.find_and_click(*subtype_locator)

    def bp_participants_choose_selected(self, name):
        """ Метод выбирает 'Выбранные участники' и конкретного участника с именем name для рассылки """
        self.find_and_click(*self.locators.BP_PARTICIPANTS_SELECTED)
        self.find_and_click(*self.locators.BP_PARTICIPANTS_MULTI_SELECT)
        self.find_and_fill_element(name, *self.locators.BP_PARTICIPANTS_MULTI_SELECT_SEARCH)
        self.ba_simple_wait_for_loading()
        self.find_and_click(*collect_locator(self.locators.BP_PARTICIPANTS_MULTI_SELECT_ITEM_PATTERN, name))
        self.ba_send_key(Keys.ESCAPE)
        self.bulletin_participants_info['participants'] = name

    def bp_remove_participants_in_choosed(self):
        try:
            elems = self.search_elements(*self.locators.BP_PARTPICIPANTS_MULTI_SELECT_DELETE_ICONS)
            for elem in elems:
                elem.click()
        except:
            self.log.info('Нет выбранных участников, некого удалять')

    def bp_participants_choose_not_chosen(self):
        """ Метод выбирает 'Не выбрано' в выборе участников рассылки """
        self.find_and_click(*self.locators.BP_PARTICIPANTS_NOT_CHOSEN)

    def bp_participants_choose_all(self):
        """ Метод выбирает 'Все участники' в выборе участников рассылки """
        self.find_and_click(*self.locators.BP_PARTICIPANTS_ALL)

    def bp_save_bulletin(self):
        """ Метод кликает кнопку сохранить и ждет, пока загрузится форма просмотра"""
        self.find_and_click(*self.locators.BP_SAVE_BULLETIN_BTN)
        self.ba_simple_wait_for_loading()
        assert self.search_element(*self.locators.BP_BULLETIN_VIEW_PAGE)

    def bp_upload_source_attachment(self, file_path):
        """ Метод заполняет Исходный файл """
        element = self.search_element(*self.locators.BP_SOURCE_ATTACHMENT_UPLOAD)
        drag_and_drop_file(element, file_path)
        self.bulletin_files['source'] = os.path.basename(file_path)
        self.wait_for_invisibility_element(*self.locators.PROGRESS_BAR)

    def bp_upload_published_attachment(self, file_path):
        """ Метод заполняет Публикуемый файл """
        element = self.search_element(*self.locators.BP_PUBLISHED_ATTACHMENT_UPLOAD)
        drag_and_drop_file(element, file_path)
        self.bulletin_files['published'] = os.path.basename(file_path)
        self.wait_for_invisibility_element(*self.locators.PROGRESS_BAR)

    def bp_upload_additional_attachment(self, file_path):
        """ Метод заполняет Дополнительный файл """
        element = self.search_element(*self.locators.BP_ADDITIONAL_ATTACHMENT_UPLOAD)
        drag_and_drop_file(element, file_path)
        self.bulletin_files['additional'].append(os.path.basename(file_path))
        self.wait_for_invisibility_element(*self.locators.PROGRESS_BAR)

    def bp_check_max_number_of_files_uploaded(self):
        """ Метод проверяет, что появилась надпись о максимальном числе дополнительных файлов """
        assert self.search_element(*self.locators.BP_MAX_FILES_UPLOADED)

    def bp_fill_bulletin_fields_without_files_and_participant(self):
        """ Метод заполняет поля в бюллетене, кроме файлов и участников рассылки """
        self.bulletin_common_info['header'] = 'Рассылка ' + now_timestamp()
        self.bp_fill_bulletin_header(self.bulletin_common_info['header'])
        self.bulletin_common_info['id'] = 'ID ' + now_timestamp()
        self.bp_fill_bulletin_id(self.bulletin_common_info['id'])
        self.bulletin_common_info['description'] = 'Краткое описание ' + now_timestamp()
        self.bp_fill_bulletin_description(self.bulletin_common_info['description'])
        type_locator = choice((self.locators.BP_BULLETIN_TYPE_ITEM_BULLETIN,
                               self.locators.BP_BULLETIN_TYPE_ITEM_NEWS,
                               self.locators.BP_BULLETIN_TYPE_ITEM_NOTIFICATION))
        self.bp_select_bulletin_type(type_locator)
        self.bulletin_common_info['type'] = self.return_text_ele(*self.locators.BP_BULLETIN_TYPE)
        self.bp_select_bulletin_subtype(self.locators.BP_BULLETIN_SUBTYPE_ITEM_1)
        self.bulletin_common_info['sub_type'] = self.return_text_ele(*self.locators.BP_BULLETIN_SUBTYPE)
        self.log.info(f"Данные создаваемого бюллетеня: {self.bulletin_common_info}")

    def bp_upload_source_and_publishing_attachments(self):
        """ Метод объединенной загрузки исходного и публикуемого файла """
        self.bp_upload_source_attachment(self.BP_FILE_1)
        self.bp_upload_published_attachment(self.BP_FILE_2)

    def bp_upload_all_additional_attachments(self):
        """ Метод добавляет максимальное число дополнительных файлов """
        self.bp_upload_additional_attachment(self.BP_FILE_3)
        self.bp_upload_additional_attachment(self.BP_FILE_4)
        self.bp_upload_additional_attachment(self.BP_FILE_5)
        self.bp_upload_additional_attachment(self.BP_FILE_6)
        self.bp_upload_additional_attachment(self.BP_FILE_7)
        self.bp_check_max_number_of_files_uploaded()

    def bp_delete_attachment(self, file_name):
        """ Метод удаляет файл с заданным именем """
        self.find_and_click(*collect_locator(self.locators.BP_DELETE_ATTACHMENT_PATTERN, file_name))
        self.wait_for_invisibility_element(*collect_locator(self.locators.BP_ATTACHMENT_LINK_PATTERN, file_name))

    def bp_delete_additional_attachment(self, file_name):
        """ Метод удаляет файл с заданным именем и удаляет его из списка дополнительных файлов """
        self.bp_delete_attachment(file_name)
        self.bulletin_files['additional'].remove(file_name)

    def bp_delete_random_additional_attachment(self):
        """ Метод удаляет рандомный дополнительный файл, должны быть загружены все 5 файлов по методу
        bp_upload_all_additional_attachments """
        random_file = choice((self.BP_FILE_3, self.BP_FILE_4, self.BP_FILE_5, self.BP_FILE_6, self.BP_FILE_7))
        self.bp_delete_additional_attachment(os.path.basename(random_file))

    def bp_select_first_template_in_list(self):
        self.find_and_click(*self.locators.BP_BULLETIN_TEMPLATE)
        self.find_and_click(*self.locators.BP_BULLETIN_TEMPLATE_ITEM_1)

    def bp_click_drafts_filter(self):
        """ метод выбирает предфильтр Черновики, должен быть открыт список рассылок"""
        self.find_and_click(*self.locators.BP_DRAFT_FILTER_IN_ALL)
        self.wait_for_invisibility_element(*self.locators.CIRCULAR_LOADER)

    def bp_click_published_filter(self):
        """ метод выбирает предфильтр Опубликованные, должен быть открыт список рассылок"""
        self.find_and_click(*self.locators.BP_PUBLISHED_FILTER_IN_ALL)
        self.wait_for_invisibility_element(*self.locators.CIRCULAR_LOADER)

    def bp_select_first_draft_in_list(self):
        """ метод выбирает первый черновик в списке (только селект, не открывает его) """
        self.find_and_click(*self.locators.BP_FIRST_DRAFT_IN_LIST)
        self.ba_simple_wait_for_loading()

    def bp_open_first_draft_in_list(self):
        """ метод открывает первый черновик в списке """
        self.find_and_click(*self.locators.BP_FIRST_DRAFT_IN_LIST_LINK)
        self.ba_simple_wait_for_loading()

    def bp_click_edit_btn_on_action_bar(self):
        """ метод нажимает кнопку Редактировать на странице со списком бюллетеней """
        self.find_and_click(*self.locators.BP_EDIT_BULLETIN_BUTTON_ON_ACTION_BAR)
        self.ba_simple_wait_for_loading()
        assert self.search_element(*self.locators.BP_EDIT_PAGE)

    def bp_click_edit_btn_on_view_page(self):
        """ метод нажимает кнопку Редактировать на странице просмотра бюллетеня """
        self.find_and_click(*self.locators.BP_EDIT_BULLETIN_BUTTON_ON_VIEW_PAGE)
        self.ba_simple_wait_for_loading()
        assert self.search_element(*self.locators.BP_EDIT_PAGE)

    def bp_click_publish_btn_on_view_page(self):
        """ метод нажимает кнопку Опубликовать на странице просмотра бюллетеня """
        self.find_and_click(*self.locators.BP_PUBLISH_BULLETIN_ON_VIEW_PAGE)
        self.ba_simple_wait_for_loading()
        assert self.search_element(*self.locators.BP_PUBLISH_MODAL_VIEW)

    def bp_click_publish_btn_on_modal(self):
        """ метод нажимает кнопку Опубликовать в модальном окне публикации """
        self.find_and_click(*self.locators.BP_PUBLISH_BTN_MODAL)
        self.wait_for_invisibility_element(*self.locators.BP_PUBLISH_MODAL_VIEW)
        self.ba_simple_wait_for_loading()

    def bp_publish_bulletin_from_view_page(self):
        """ объединяющий метод, открывает окно публикации и публикует рассылку"""
        self.bp_click_publish_btn_on_view_page()
        self.bp_click_publish_btn_on_modal()

    def bp_click_cancel_on_publish_view(self):
        """ метод нажимает кнопку Отмена в модальном окне публикации """
        self.find_and_click(*self.locators.BP_CANCEL_PUBLISH_BTN)
        self.wait_for_invisibility_element(*self.locators.BP_PUBLISH_MODAL_VIEW)
        self.ba_simple_wait_for_loading()

    def bp_check_bulletin_status(self, expected_status):
        """ метод проверяет, что статус рассылки совпадает с ожидаемой,
        должна быть открыта страница просмотра рассылки """
        status = self.return_text_ele(*self.locators.BP_BULLETIN_STATUS)
        assert status == expected_status, 'Не соответствует статус! Текущий статус: {}, ожидаемый {}'\
            .format(status, expected_status)

    @decorator_for_change_selenium_wait_and_return_after(150)
    def bp_wait_for_scan_finishing(self):
        """ метод ожидает, пока окончится сканирование файлов, должна быть открыта страница просмотра рассылки """
        self.ba_simple_wait_for_loading()
        self.wait_for_invisibility_element(*self.locators.BP_FILE_SCAN_ONGOING)

    def bp_check_files_present_on_page(self):
        """ метод проверяет наличие файлов, должна быть открыта страница просмотра рассылки """
        if self.bulletin_files['source']:
            assert self.search_element(*collect_locator(self.locators.BP_ATTACHMENT_LINK_PATTERN,
                                                        self.bulletin_files['source']))
        if self.bulletin_files['published']:
            assert self.search_element(*collect_locator(self.locators.BP_ATTACHMENT_LINK_PATTERN,
                                                        self.bulletin_files['published']))
        for file in self.bulletin_files['additional']:
            assert self.search_element(*collect_locator(self.locators.BP_ATTACHMENT_LINK_PATTERN, file))

    def bp_check_scan_result_present_for_files(self):
        """ метод проверяет наличие результатов сканирования для файлов,
        должна быть открыта страница просмотра рассылки """
        if self.bulletin_files['source']:
            assert self.search_element(*collect_locator(self.locators.BP_FILE_SCAN_RESULT_PATTERN,
                                                        self.bulletin_files['source']))
        if self.bulletin_files['published']:
            assert self.search_element(*collect_locator(self.locators.BP_FILE_SCAN_RESULT_PATTERN,
                                                        self.bulletin_files['published']))
        for file in self.bulletin_files['additional']:
            assert self.search_element(*collect_locator(self.locators.BP_FILE_SCAN_RESULT_PATTERN, file))

    def bp_check_files_download(self):
        """ метод проверяет, что файлы загружаются """
        if self.bulletin_files['source']:
            self.find_and_click(*collect_locator(self.locators.BP_ATTACHMENT_LINK_PATTERN,
                                                 self.bulletin_files['source']))
            self.ba_confirm_file_download()
            self.ba_check_file(self.bulletin_files['source'])
        if self.bulletin_files['published']:
            self.ba_click_element_and_scroll_at_failure(*collect_locator(self.locators.BP_ATTACHMENT_LINK_PATTERN,
                                                                         self.bulletin_files['published']))
            self.ba_confirm_file_download()
            self.ba_check_file(self.bulletin_files['published'])
        for item in self.bulletin_files['additional']:
            self.ba_click_element_and_scroll_at_failure(*collect_locator(self.locators.BP_ATTACHMENT_LINK_PATTERN,
                                                                         item))
            self.ba_confirm_file_download()
            self.ba_check_file(item)

    def bp_download_and_check_source_file(self):
        """ метод проверяет, что скачивается исходный файл """
        self.find_and_click(*collect_locator(self.locators.BP_ATTACHMENT_LINK_PATTERN, self.bulletin_files['source']))
        self.ba_confirm_file_download()
        self.ba_check_file(self.bulletin_files['source'])

    def bp_check_notification_in_email_db(self, email='auto_payer@sptest.ru'):
        """ метод проверяет, что на почту email отправляется сообщение """
        if self.bulletin_common_info['type'] == 'Бюллетень':
            text = 'Опубликован новый бюллетень {}: {}.'.format(self.bulletin_common_info['id'],
                                                                self.bulletin_common_info['header'])
        elif self.bulletin_common_info['type'] == 'Новость':
            text = 'Опубликована новость {}: {}.'.format(self.bulletin_common_info['id'],
                                                         self.bulletin_common_info['header'])
        elif self.bulletin_common_info['type'] == 'Уведомление':
            text = 'Опубликовано новое уведомление {}: {}.'.format(self.bulletin_common_info['id'],
                                                                   self.bulletin_common_info['header'])
        else:
            raise ValueError('Unexpected type: {}'.format(self.bulletin_common_info['type']))
        db_response = self.rp_lko_request_in_db_emails(text, email)
        self.log.info('Получен ответ на запрос: {}'.format(db_response))
        assert len(db_response) > 0, 'Не найден запрос в базе для {}'.format(email)

    def bp_check_notification_in_email_db_without_body(self, email='auto_payer@sptest.ru'):
        """ метод проверяет, что на почту email отправляется сообщение, в тексте ищем только id бюллетеня """
        text = '{}'.format(self.bulletin_common_info['id'])
        db_response = self.rp_lko_request_in_db_emails(text, email)
        self.log.info('Получен ответ на запрос: {}'.format(db_response))
        assert len(db_response) > 0, 'Не найден запрос в базе для {}'.format(email)

    def bp_fill_not_filled_from_incident_fields(self):
        """ метод заполнения обязательных полей, не предхаполненных из инцидента """
        self.bulletin_common_info['id'] = 'ID ' + now_timestamp()
        self.bp_fill_bulletin_id(self.bulletin_common_info['id'])
        self.bulletin_common_info['type'] = self.return_text_ele(*self.locators.BP_BULLETIN_TYPE)
        self.bp_select_bulletin_subtype(self.locators.BP_BULLETIN_SUBTYPE_ITEM_1)
        self.bulletin_common_info['sub_type'] = self.return_text_ele(*self.locators.BP_BULLETIN_SUBTYPE)
        if not self.incident_info['description']:
            self.bulletin_common_info['description'] = 'Описание в инциденте отсутствует, заполняем сами'
            self.bp_fill_bulletin_description(self.bulletin_common_info['description'])
        else:
            self.bulletin_common_info["description"] = self.incident_info['description']

    def bp_check_incident_prefilled_fields(self):
        self.ba_simple_wait_for_loading()
        header = self.return_attrs_element('value', *self.locators.BP_BULLETIN_HEADER)
        self.log.info(f'Полученное значение в поле Заголовок: {header}')
        assert header == 'Угроза с типом "{}"'.format(self.incident_info['type'])
        self.bulletin_common_info['header'] = header
        description = self.return_attrs_element('value', *self.locators.BP_BULLETIN_DESCRIPTION)
        self.log.info(f'Полученное значение в поле Описание: {description}')
        assert description == self.incident_info['description']
        try:
            source_file = self.return_text_ele(*collect_locator(self.locators.BP_FILE_LINK_ON_EDIT_PAGE_PATTERN,
                                                                'Исходный файл'))
            self.bulletin_files['source'] = source_file
        except:
            raise FileNotFoundError('Не найден исходный файл')

    def bp_get_bulletin_fields_from_view_page(self):
        """ метод сохраняет данные со вкадки Общие сведения, должна быть открыта страница просмотра бюллетеня """
        self.ba_simple_wait_for_loading()
        value = self.return_text_ele(*self.locators.BP_VIEW_HEADER).split(': ')
        self.bulletin_common_info['id'] = value[0].strip()
        self.bulletin_common_info['header'] = value[1].strip()
        self.bulletin_common_info['description'] = self.return_text_ele(*collect_locator(self.locators.
                                                                                         BP_VIEW_PAGE_VALUE_PATTERN,
                                                                                         'Описание'))
        self.bulletin_common_info['type'] = self.return_text_ele(
            *collect_locator(self.locators.BP_VIEW_PAGE_VALUE_PATTERN, 'Тип'))
        self.bulletin_common_info['sub_type'] = self.return_text_ele(
            *collect_locator(self.locators.BP_VIEW_PAGE_VALUE_PATTERN, 'Подвид'))
        self.log.info(f"Полученная информация о бюллетене: {self.bulletin_common_info}")

    def bp_get_files_names_from_view_page(self):
        """ метод сохраняет файлы со вкадки Общие сведения, должна быть открыта страница просмотра бюллетеня """
        import selenium.common.exceptions
        try:
            elem = self.driver.find_element(*collect_locator(self.locators.BP_VIEW_PAGE_FILE_PATTERN, 'Исходный файл'))
            self.bulletin_files['source'] = elem.text
        except selenium.common.exceptions.NoSuchElementException:
            self.log.info('Исходный файл не найден')
        try:
            elem = self.driver.find_element(*collect_locator(self.locators.BP_VIEW_PAGE_FILE_PATTERN, 'Публикуемый файл'))
            self.bulletin_files['published'] = elem.text
        except selenium.common.exceptions.NoSuchElementException:
            self.log.info('Публикуемый файл не найден')

        try:
            elems = self.driver.find_elements(*collect_locator(self.locators.BP_VIEW_PAGE_FILE_PATTERN,
                                                               'Дополнительные публикуемые файлы'))
            for elem in elems:
                self.bulletin_files['additional'].append(elem.text)
        except selenium.common.exceptions.NoSuchElementException:
            self.log.info('Дополнительные публикуемые файлы не найдены')

    def bp_get_participants_from_participants_view(self):
        """ метод считывает участников из получателей рассылки на странице просмотра бюллетеня, должна быть открыта
        вкладка 'Получатели рассылки'"""
        self.bulletin_participants_info['participants'] = self.ba_return_elem_text_or_none(
            *collect_locator(self.locators.BP_VIEW_PAGE_VALUE_PATTERN, 'Участники'))
        return self.bulletin_participants_info['participants']

    def bp_get_mailg_groups_from_participants_view(self):
        """ метод считывает группы рассылки из получателей рассылки на странице просмотра бюллетеня, должна быть
        открыта вкладка 'Получатели рассылки' """
        self.bulletin_participants_info['mail_groups'] = self.ba_return_elem_text_or_none(
            *collect_locator(self.locators.BP_VIEW_PAGE_VALUE_PATTERN, 'bp_get_mailg_groups_from_participants_view'))
        return self.bulletin_participants_info['mail_groups']

    def bp_click_on_bulletin_in_list(self, bul_id):
        """ метод кликает по ссылке на бюллетень, ищется по id бюллетеня """
        self.find_and_click(*collect_locator(self.locators.BP_BULLETIN_LINK_PATTERN, bul_id))
        self.ba_simple_wait_for_loading()

    def bp_open_bulletin(self):
        """ метод открывает бюллетень, id которого сохранен в bulletin_common_info """
        self.bp_click_on_bulletin_in_list(self.bulletin_common_info['id'])

    def bp_click_cancel_btn_on_edit_page(self):
        """ метод кликает Отмена на странице редактирования бюллетеня """
        self.find_and_click(*self.locators.BP_CANCEL_BULLETIN_BTN)
        self.ba_simple_wait_for_loading()
        assert self.search_element(*self.locators.BP_ACTION_BAR)

    def bp_open_participants_on_view_page(self):
        """ метод открывает вкладку Получатели рассылки, должна быть открыта страница просмотра бюллетеня """
        self.find_and_click(*self.locators.BP_PARTICIPANTS_LINK_ON_VIEW_PAGE)
        self.ba_simple_wait_for_loading()
        assert self.search_element(*self.locators.BP_PARTICIPANTS_HEADER_ON_VIEW_PAGE)

    def bp_open_common_info_on_view_page(self):
        """ метод открывает вкладку Общие сведения, должна быть открыта страница просмотра бюллетеня """
        self.find_and_click(*self.locators.BP_COMMON_INFO_LINK_ON_VIEW_PAGE)
        self.ba_simple_wait_for_loading()
        assert self.search_element(*self.locators.BP_COMMON_HEADER_ON_VIEW_PAGE)

    def bp_check_bulletin_common_info_from_view_page(self):
        """ метод сравнивает данные на странице просмотра бюллетеня с сохраненными данными """
        self.ba_simple_wait_for_loading()
        self.bp_open_common_info_on_view_page()
        heading = self.bulletin_common_info['id'] + ': ' + self.bulletin_common_info['header']
        assert self.return_text_ele(*self.locators.BP_VIEW_HEADER) == heading, 'Заголовок не совпадает'
        assert self.bulletin_common_info['description'] == self.return_text_ele(
            *collect_locator(self.locators.BP_VIEW_PAGE_VALUE_PATTERN, 'Описание')), 'Описание не совпадает'
        assert self.bulletin_common_info['type'] == self.return_text_ele(
            *collect_locator(self.locators.BP_VIEW_PAGE_VALUE_PATTERN, 'Тип')), 'Тип рассылки не совпадает'
        assert self.bulletin_common_info['sub_type'] == self.return_text_ele(
            *collect_locator(self.locators.BP_VIEW_PAGE_VALUE_PATTERN, 'Подвид')), 'Подвид не совпадает'
        if self.bulletin_files['source']:
            assert self.bulletin_files['source'] == self.return_text_ele(*collect_locator(
                self.locators.BP_VIEW_PAGE_FILE_PATTERN, 'Исходный файл')), 'Исходный файл не совпадает'
        if self.bulletin_files['published']:
            assert self.bulletin_files['published'] == self.return_text_ele(*collect_locator(
                self.locators.BP_VIEW_PAGE_FILE_PATTERN, 'Публикуемый файл')), 'Публикуемый файл не совпадает'
        if self.bulletin_files['additional']:
            file_list = list()
            elems = self.driver.find_elements(*collect_locator(self.locators.BP_VIEW_PAGE_FILE_PATTERN,
                                                               'Дополнительные публикуемые файлы'))
            for elem in elems:
                file_list.append(elem.text)
            difference = set(file_list) ^ set(self.bulletin_files['additional'])
            assert len(difference) == 0, 'Дополнительные публикуемые файлы не совпадают: {}'.format(difference)

    def bp_check_participants_info(self, expected_name):
        """ метод проверяет, что на вкладке Получатели рассылки Участники соответствуют переданным expected_name """
        self.bp_open_participants_on_view_page()
        assert expected_name == self.ba_return_elem_text_or_none(
            *collect_locator(self.locators.BP_VIEW_PAGE_VALUE_PATTERN, 'Участники')), 'Участники не совпадают'

    def bp_check_mail_groups_info(self, expected_name):
        """ метод проверяет, что на вкладке Получатели рассылки Группы рассылки соответствуют переданным
        expected_name """
        self.bp_open_participants_on_view_page()
        assert expected_name == self.ba_return_elem_text_or_none(
            *collect_locator(self.locators.BP_VIEW_PAGE_VALUE_PATTERN, 'Группы рассылки')), \
            'Группы рассылки не совпадают'

    def bp_check_parent_incident_relation_present(self):
        """ метод проверяет, что отображается связь бюллетеня с инцидентом, из которого он создан """
        assert self.search_element(*collect_locator(self.locators.BP_PARENT_INCIDENTS_RELATION_LINK_PATTERN,
                                                    self.incident_info['id']))

    def bp_click_edit_mailing_group_link(self):
        """ метод кликает по ссылке Редактировать группы рассылки """
        self.find_and_click(*self.locators.BP_EDIT_MAILING_GROUPS_LINK)
        self.ba_simple_wait_for_loading()
        assert self.search_element(*self.locators.BP_MAILING_GROUPS_HEADER)

    def bp_check_buttons_on_edit_mailing_group_modal(self):
        """ метод проверяет активность кнопок в модальном окне расссылок"""
        assert self.ba_is_enabled(*self.locators.BP_ADD_MAILING_GROUP_BTN) is True, 'Кнопка "Добавить" не активна'
        assert self.ba_is_enabled(*self.locators.BP_EDIT_MAILING_GROUP_BTN) is False, 'Кнопка "Редактировать" активна'
        assert self.ba_is_enabled(*self.locators.BP_REMOVE_MAILING_GROUP_BTN) is False, 'Кнопка "Удалить" активна'

    def bp_click_add_mailing_group_btn(self):
        """ метод кликает по кнопке Добавить группу в модальном окне групп рассылок"""
        self.find_and_click(*self.locators.BP_ADD_MAILING_GROUP_BTN)
        self.ba_simple_wait_for_loading()
        assert self.search_element(*self.locators.BP_ADD_MAILING_GROUP_MODAL), "Окно добавления группы не появилось"

    def bp_click_cancel_on_add_mailing_group(self):
        """ метод кликает по кнопке Отмена в модальном окне содания новой группы рассылок"""
        self.find_and_click(*self.locators.BP_CANCEL_NEW_MAILING_GROUP_BTN)
        self.wait_for_invisibility_element(*self.locators.BP_ADD_MAILING_GROUP_MODAL)

    def bp_click_save_on_add_mailing_group(self):
        """ метод кликает Сохранить в модальном окне добавления группы рассылки и проверяет, что окно закрылось """
        self.find_and_click(*self.locators.BP_SAVE_MAILING_GROUP_BTN)
        self.wait_for_invisibility_element(*self.locators.BP_ADD_MAILING_GROUP_MODAL)
        self.ba_simple_wait_for_loading()

    def bp_fill_mailing_group_name(self, name):
        """ метод заполняет имя группы рассылки """
        self.find_and_fill_element(name, *self.locators.BP_MAILING_GROUP_NAME_INPUT)

    def bp_fill_mailing_group_email(self, email):
        """ метод заполняет email в группе рассылки """
        self.find_and_fill_element(email, *self.locators.BP_MAILING_GROUP_EMAIL_INPUT)

    def bp_mailing_group_choose_participants(self):
        """ метод кликает Выбранные участники на форме добавления новой группы """
        self.find_and_click(*self.locators.BP_MAILING_GROUP_CHOOSE_PARTICIPANTS_ITEM)
        self.ba_simple_wait_for_loading()

    def bp_choose_participant_for_mailing_group(self, name):
        """ метод заполяет участника: кликает по селекту, вводит имя участника и выбирает его """
        self.find_and_click(*self.locators.BP_MAILING_GROUP_PARTICIPANTS_MULTI_SELECT)
        self.find_and_fill_element(name, *self.locators.BP_MAILING_GROUP_PARTICIPANTS_MULTI_SELECT_SEARCH_INPUT)
        self.find_and_click(*collect_locator(self.locators.BP_MAILING_GROUP_PARTICIPANTS_MULTI_SELECT_ITEM_PATTERN,
                                             name))
        # self.find_and_click(*self.locators.BP_MAILING_GROUP_CHOOSE_PARTICIPANTS_ITEM)

    def bp_fill_mandatory_fields_in_mailing_group(self, email='auto_payer@sptest.ru'):
        """ объединяющий метод для заполнения полей новой группы """
        self.bulletin_mailing_groups['name'] = 'auto_' + now_timestamp()
        self.bp_fill_mailing_group_name(self.bulletin_mailing_groups['name'])
        self.bp_fill_mailing_group_email(email)

    def bp_check_new_group_present_in_table(self):
        """ метод проверяет, что группа отображается в таблице. Скроллит список, если в текущем нет искомого элемента,
         пока не дойдет до конца списка"""
        elements = self.driver.find_elements(*self.locators.BP_MAILING_GROUP_TABLE_ELEMENTS)
        last_elem = elements[-2]
        last_text = last_elem.text
        while True:
            try:
                assert self.driver.find_element(*collect_locator(self.locators.BP_MAILING_GROUP_TABLE_ITEM_PATTERN,
                                                                 self.bulletin_mailing_groups['name']))
                self.log.info('Группа отображается в списке')
                break
            except Exception:
                self.log.info('Группа не найдена в списке. Скроллим.')
            last_elem.click()
            self.driver.execute_script('arguments[0].scrollIntoView(true)', last_elem)
            elements = self.driver.find_elements(*self.locators.BP_MAILING_GROUP_TABLE_ELEMENTS)
            new_last_text = elements[-2].text
            if new_last_text == last_text:
                self.log.info('Достигнут конец списка')
                assert self.driver.find_element(
                    *collect_locator(self.locators.BP_MAILING_GROUP_TABLE_ITEM_PATTERN,
                                     self.bulletin_mailing_groups['name'])), 'Новая группа не отображается в списке'
            last_elem = elements[-2]
            last_text = last_elem.text

    def bp_check_group_not_present_in_table(self):
        """ метод проверяет, что группа не отображается в таблице. Скроллит таблицу, пока не дойдет до конца списка """
        elements = self.driver.find_elements(*self.locators.BP_MAILING_GROUP_TABLE_ELEMENTS)
        last_elem = elements[-2]
        last_text = last_elem.text
        while True:
            is_found = False
            try:
                self.driver.find_element(*collect_locator(self.locators.BP_MAILING_GROUP_TABLE_ITEM_PATTERN,
                                                          self.bulletin_mailing_groups['name']))
                is_found = True
            except Exception:
                self.log.info('Группа не найдена в списке. Скроллим.')
            if is_found:
                pytest.fail('Группа найдена в списке, хотя не должна была!')
            last_elem.click()
            self.driver.execute_script('arguments[0].scrollIntoView(true)', last_elem)
            self.ba_simple_wait_for_loading()
            elements = self.driver.find_elements(*self.locators.BP_MAILING_GROUP_TABLE_ELEMENTS)
            new_last_text = elements[-2].text
            if new_last_text == last_text:
                self.log.info('Достигнут конец списка. Группа не найдена, как и ожидалось.')
                break
            last_elem = elements[-2]
            last_text = last_elem.text

    def bp_close_mailing_group_modal(self):
        """ метод кликает по крестику в модальном окне Группа рассылок и ждет, пока окно пропадет"""
        self.find_and_click(*self.locators.BP_MAILING_GROUP_CLOSE_MODAL_BTN)
        self.wait_for_invisibility_element(*self.locators.BP_MAILING_GROUPS_HEADER)

    def bp_choose_mailing_group(self, group_name=None):
        """ Метод выбирает группу рассылки с указанным именем """
        if group_name is None:
            group_name = self.bulletin_mailing_groups['name']
        self.find_and_click(*self.locators.BP_MAILING_GROUP_MULTI_SELECT)
        self.find_and_fill_element(group_name, *self.locators.BP_MAILING_GROUP_SELECT_SEARCH_INPUT)
        self.find_and_click(*collect_locator(self.locators.BP_MAILING_GROUP_MULTI_SELECT_ITEM_PATTERN, group_name))
        self.ba_send_key(Keys.ESCAPE)

    def bp_create_draft_if_absent(self):
        """ метод проверяет, есть ли черновики и в случае отсутсвия создает его по апи """
        if not self.api_client.check_if_bulletin_drafts_present():
            self.api_client.create_bulletin_draft_for_all()
        else:
            self.log.info('Черновики рассылок есть в системе')


class BulletinsLkuPage(Page):
    """ Класс для работы с рассылками центра (бюллетенями) в ЛКУ """

    def bp_lku_select_bulletin_item(self):
        """ метод выбирает бюллетень в списке, id берем из bulletin_common_info """
        self.find_and_click(*collect_locator(self.locators.BP_LKU_ITEM_PATTERN, self.bulletin_common_info['id']))
        self.wait_for_invisibility_element(*self.locators.CIRCULAR_LOADER)

    def bp_lku_check_bulletin_fields(self):
        """ метод проверяет, что поля бюллетеня совпадают со значениями из bulletin_common_info """
        for key in self.bulletin_common_info.keys():
            if key:
                assert self.search_element(*collect_locator(self.locators.BP_LKU_BULLETIN_VIEW_PATTERN,
                                                            self.bulletin_common_info[key]))
        self.log.info('Bulletin fields check finished')

    def bp_lku_check_files_present(self):
        """ метод проверяет, что файлы бюллетеня совпадают со значениями из bulletin_files """
        if self.bulletin_files['published']:
            assert self.search_element(*collect_locator(self.locators.BP_LKU_BULLETIN_VIEW_PATTERN,
                                                        self.bulletin_files['published']))
        for item in self.bulletin_files['additional']:
            assert self.search_element(*collect_locator(self.locators.BP_LKU_BULLETIN_VIEW_PATTERN, item))
        self.log.info('Bulletin files check finished')

    def bp_lku_check_files_download(self):
        """ метод проверяет загрузку файлов """
        if self.bulletin_files['published']:
            self.find_and_click(*collect_locator(self.locators.BP_LKU_BULLETIN_VIEW_PATTERN,
                                                 self.bulletin_files['published']))
            self.ba_check_file(self.bulletin_files['published'])
        for item in self.bulletin_files['additional']:
            self.find_and_click(*collect_locator(self.locators.BP_LKU_BULLETIN_VIEW_PATTERN, item))
            self.ba_check_file(item)
