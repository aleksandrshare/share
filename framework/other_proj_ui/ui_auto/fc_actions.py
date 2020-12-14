#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ui_library.ui_lib import Page
from ui_library.dad_file_with_js import drag_and_drop_file
import os
import sys
import glob
from tools.utils import check_file_size, check_file_content, wait_for_file_download, check_json_file_content
from framework.other_proj_ui.ui_auto.fc_request_actions import request_info_lku, request_info_lko
from time import sleep, time
import random
from framework.other_proj_ui.ui_auto.fc_helpers import decorator_for_change_selenium_wait_and_return_after
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import urlparse
from configs.modify_data import test_modify_data
from base64 import b64decode
import rarfile


class BaseActions(Page):
    """Класс собирает методы, которые могут быть использованы где угодно на сайте и/или на любом контуре"""

    def bp_reloading_locators(self):
        """Обнуляет локаторы, чтобы сбросить форматирование строковых значений"""
        from framework.other_proj_ui.ui_auto.locators.fc_locators import LocatorsLKO, LocatorsLKU
        self.log.info('Обнуляются локаторы класса %s' % self.locators.__class__.__name__)
        if self.locators.__class__.__name__ == 'LocatorsLKU':
            self.locators = LocatorsLKU()
        else:
            self.locators = LocatorsLKO()

    def ba_check_file(self, file_name, timeout=10, pattern=False):
        """проверяет что файл, скачанный через браузер, не пустой
        работает, при запуске на selenoid (linux)

        :param file_name: имя файла, без указания пути
        :type file_name: str
        :param timeout: сколько секундо ожидать скачки файла
        :type timeout: int
        :param pattern: если имя файла целиком не известно и надо инскать по маске
        :type pattern: bool
        """
        check_file = None
        if 'linux' in sys.platform:
            if pattern:
                sleep(timeout)
                for i in glob.glob(f"/home/for_browser/*{file_name}*"):
                    file_name = i
                    check_file = check_file_size(file_name, timeout=timeout, delete=False)
            else:
                check_file = check_file_size('/home/for_browser/%s' % file_name, timeout=timeout, delete=True)
            if check_file:
                self.log.info("Check file /home/for_browser/%s, size = %s" % (file_name, str(check_file)))
            else:
                self.log.info("путь к файлам: %s" % os.listdir(path='/home'))
                self.log.error("Содержание папки загрузки: %s" % os.listdir(path='/home/for_browser/'))
                raise FileExistsError("Проблема с файлом /home/for_browser/%s" % file_name)
        elif 'win' in sys.platform:
            load_path = os.path.join(os.path.expanduser('~'), 'Downloads')
            sleep(timeout)
            if pattern:
                for i in glob.glob(f"{load_path}/*{file_name}*"):
                    file_name = i
                    check_file = check_file_size(file_name, timeout=timeout, delete=False)
            else:
                check_file = check_file_size(f'{load_path}/%s' % file_name, timeout=timeout, delete=False)
            if check_file:
                self.log.info(f"Check file {load_path}/%s, size = %s" % (file_name, str(check_file)))
            else:
                self.log.error("Содержание папки загрузки: %s" % os.listdir(path=load_path))
                raise FileExistsError("Проблема с файлом %s" % file_name)
        else:
            self.log.info("Запуск тестов локальный, поэтому файл %s не проверяется" % file_name)

    def mp_click_feeds_btn(self):
        """нажать кнопку Фиды в главном меню"""
        self.find_and_click(*self.locators.MP_ANTIFROD_FIDS_BTN)

    @staticmethod
    def generate_str_and_return(str_len=30):
        return ''.join([random.choice(list('1234567890qwertypasdfghjklzxcvbnmQWERTYUIKLZXCVBNM'))
                        for _ in range(str_len)])

    def check_all_obs_in_status_processed_after_create_from_lku(self, where=None, obs=False, obs_quantity=2):
        """"""
        if where == 'lku':
            req_id = request_info_lku['id']
        else:
            req_id = request_info_lko['id']
        api_info = {'req_id': req_id, 'test': '123'}
        self.api_client.ia_check_incident_created_from_request(context=api_info, inc_quantity=1)
        if obs:
            self.api_client.aa_check_antifraud_created_from_incidents(obs_quantity, context=api_info)
            self.api_client.rs_check_all_obs_in_status_processed(api_info)

    def save_req_hrid_created_from_obs(self):
        """"""
        api_info = {'req_id': request_info_lku['id'], 'test': '123'}
        request_info_lku['hrid'] = None
        self.api_client.ia_check_incident_created_from_request(inc_quantity=1, context=api_info)
        self.api_client.aa_check_antifraud_created_from_incidents(obs_quantity=2, context=api_info)
        self.api_client.rs_check_request_created_from_obs(context=api_info)
        request_info_lku['hrid'] = api_info['request_from_obs']

    def ba_send_key(self, key):
        """"""
        ActionChains(self.driver).send_keys(key).perform()
        sleep(1)

    def ba_lku_wait_for_loading(self, timeout=60):
        """ метод ожидает загрузки в течении timeout """
        begin_time = time()
        self.log.info('WAIT method for animate or angular loading or loading-bar presence')
        while (self.ba_check_if_animated_elements_present() or self.ba_check_if_loading_bar_present()
               or not (self.ba_check_if_angular_is_loaded())) \
                and (time() < begin_time + timeout):
            sleep(0.5)

    def ba_wait_for_loading(self, timeout=60):
        """ метод ожидает загрузки кружка ожидания, анимации или лоад-бара в течении timeout """
        begin_time = time()
        self.log.info('WAIT method for animate or circular or loading-bar presence')
        while (self.ba_check_if_animated_elements_present() or self.ba_check_if_loader_icon_presents()
               or self.ba_check_if_loading_bar_present() or not (self.ba_check_if_angular_is_loaded())) \
                and (time() < begin_time + timeout):
            sleep(0.5)

    def ba_simple_wait_for_loading(self, timeout=60):
        """ метод ожидает загрузки в течении timeout без angular loaded"""
        begin_time = time()
        self.log.info('WAIT method for animate or loading-bar presence')
        while (self.ba_check_if_animated_elements_present() or self.ba_check_if_loading_bar_present()) \
                and (time() < begin_time + timeout):
            sleep(0.5)

    def ba_check_if_animated_elements_present(self):
        """ метод проверяет наличие анимации на странице """
        elem_query = "return document.getElementsByClassName('ng-animate').length"
        num_of_animated_elem = self.driver.execute_script(elem_query)
        self.log.info("Number of animations running: {}".format(num_of_animated_elem))
        return num_of_animated_elem > 0

    def ba_check_if_loader_icon_presents(self):
        """ метод проверяет наличие кружка загрузки на странице """
        elem_query = "return document.getElementsByClassName('circular').length"
        num_of_loaderd_elem = self.driver.execute_script(elem_query)
        self.log.info("Number of loader elements running: {}".format(num_of_loaderd_elem))
        return num_of_loaderd_elem > 0

    def ba_check_if_loading_bar_present(self):
        """ метод проверяет наличие лоад-бара на странице """
        loading_bar_query = "return document.getElementById('loading-bar')"
        loading_bar = self.driver.execute_script(loading_bar_query)
        self.log.info("Loading bar running: {}".format(loading_bar))
        return loading_bar is not None

    def ba_check_if_angular_is_loaded(self):
        has_angular_loaded = "return (window.angular != undefined) && (angular.element(document.body).injector() != " \
                             "undefined) && (angular.element(document.body).injector().get('$http')." \
                             "pendingRequests.length === 0)"
        angular_loaded = self.driver.execute_script(has_angular_loaded)
        self.log.info("Angular loaded: {}".format(angular_loaded))
        return angular_loaded

    def ba_set_cookie(self, payee=False, participant_edit=False):
        """ метод добавляет в куки драйвера авторизационные данные из апи клиента """
        if payee:
            api_cookies = self.api_client_payee._session.cookies.get_dict()
        elif participant_edit:
            api_cookies = self.api_client_participant_edit._session.cookies.get_dict()
        else:
            api_cookies = self.api_client._session.cookies.get_dict()
        hostname = urlparse(self.url).hostname
        for key in api_cookies:
            cookie = {'domain': hostname, 'name': key, 'value': api_cookies[key]}
            self.driver.add_cookie(cookie)

    def ba_is_enabled(self, *locator):
        """метод находит элемент и проверяет его активность"""
        element = self.search_element(*locator)
        return element.is_enabled()

    def ba_click_element_and_scroll_at_failure(self, *locator):
        from selenium.webdriver.common.keys import Keys
        try:
            self.find_and_click(*locator)
        except:
            self.log.info('Click element failed. Click PAGE_DOWN and try again')
            self.ba_send_key(Keys.PAGE_DOWN)
            sleep(2)
            self.find_and_click(*locator)

    def ba_scroll_element_into_view(self, *locator):
        elem = self.search_element(*locator)
        self.driver.execute_script('arguments[0].scrollIntoView(true)', elem)
        sleep(0.5)

    def ba_return_elem_text_or_none(self, *locator):
        """метод находит элемент и возвращает его текстовое значение. если элемент не найден, возвращается None """
        try:
            element = self.search_element(*locator)
            sleep(1)
            return element.text.strip()
        except:
            self.log.error(f'Не найдено значение для {locator}, установлено в None')
            return None

    def ba_confirm_file_download(self):
        try:
            self.find_and_click(*self.locators.CONFIRM_DOWNLOAD_SAVE_BUTTON)
        except:
            self.log.info('Окошко подтверждения не появилось')

    def ba_check_file_content(self, file_name, expected_content, timeout=15, delete=True):
        """проверяет содержимое файла, скачанного через браузер
         работает, при запуске на selenoid (linux) или локальном запуске на windows

         :param file_name: имя файла, без указания пути
         :type file_name: str
         :param expected_content: ожидаемое содержимое
         :param timeout: сколько секунд оожидать скачки файла
         :type timeout: int
         """
        if 'linux' in sys.platform:
            file_path = '/home/for_browser/%s' % file_name
            wait_for_file_download(file_path, timeout, delete)
            assert check_file_content(file_path, expected_content), 'Содержимое файла не соответствует ожидаемому'
        elif 'win' in sys.platform:
            file_path = os.path.join(os.path.expanduser('~'), 'Downloads', file_name)
            wait_for_file_download(file_path, timeout, delete)
            assert check_file_content(file_path, expected_content), 'Содержимое файла не соответствует ожидаемому'
        else:
            self.log.info("Запуск тестов не на linux и windows, поэтому файл %s не проверяется" % file_name)

    def ba_check_inc_file_content_json(self, schema, timeout=15, delete=True):
        """"""
        if schema == 'custom':
            file_name = f"{test_modify_data['req_attach_id'][0]}.json_ " \
                        f"filename_UTF-8_{test_modify_data['req_attach_id'][0]}.json"
        else:
            file_name = f"{test_modify_data['req_attach_id'][0]}-raw.incident.json"

        if 'linux' in sys.platform:
            file_path = '/home/for_browser/%s' % file_name
            wait_for_file_download(file_path, timeout, delete)
            file_diff = check_json_file_content(file_path, test_modify_data['attach_data']['attachments'][0]['data'])
            assert file_diff, "Содержимое файла c JSON ЭФ инцидента не соответствует отправленному JSON"
        elif 'win' in sys.platform:
            file_path = os.path.join(os.path.expanduser('~'), 'Downloads', file_name)
            wait_for_file_download(file_path, timeout, delete)
            file_diff = check_json_file_content(file_path, test_modify_data['attach_data']['attachments'][0]['data'])
            assert file_diff, "Содержимое файла c JSON ЭФ инцидента не соответствует отправленному JSON"
        else:
            self.log.info("Запуск тестов не на linux и windows, поэтому файл %s не проверяется" % file_name)

    def ba_unrar_file(self, file_name, password=None, timeout=15, delete=True):
        """"""
        if 'linux' in sys.platform:
            folder_path = '/home/for_browser/'
        elif 'win' in sys.platform:
            folder_path = os.path.join(os.path.expanduser('~'), 'Downloads')
            rarfile.UNRAR_TOOL = r'C:\Program Files\WinRAR\UnRAR.exe'
        else:
            self.log.info("Запуск тестов не на linux и windows, поэтому файл %s не проверяется" % file_name)
            return
        file_path = os.path.join(folder_path, file_name)
        wait_for_file_download(file_path, timeout, delete)
        rar_archive = rarfile.RarFile(file_path)
        rar_archive.extractall(path=folder_path, pwd=password)
        rar_archive.close()


class LoginPage(Page):
    """Класс для работы со страницей входа"""
    def __init__(self, driver, url, login, password):
        super().__init__(driver, url)
        self.LOGIN = login
        self.PASSWORD = password

    def lp_find_and_click_btn(self):
        """нажимает кнопку 'войти' """
        self.find_and_click(*self.locators.LP_LOGIN_BTN)

    def lp_find_and_fill_user_name_field(self, login, *locator):
        """заполняет поле 'имя пользователя' """
        self.find_and_fill_element(login, *locator)

    def lp_find_and_fill_password_field(self, password, *locator):
        """заполняет поле 'пароль' """
        self.find_and_fill_element(password, *locator)

    def lp_login_existing_user(self):
        """объединяет шаги для входа на сайт"""
        self.lp_find_and_fill_user_name_field(self.LOGIN, *self.locators.LP_USER_NAME)
        self.lp_find_and_fill_password_field(self.PASSWORD, *self.locators.LP_PASSWORD)
        self.lp_find_and_click_btn()

    def lp_login_custom_user(self, login, password):
        """объединяет шаги для входа на сайт, принимает логин и пароль

        :param login: логин
        :type login: str
        :param password: пароль
        :type password: str
        """
        self.lp_find_and_fill_user_name_field(login, *self.locators.LP_USER_NAME)
        self.lp_find_and_fill_password_field(password, *self.locators.LP_PASSWORD)
        self.lp_find_and_click_btn()


class MainPageLKO(Page):
    """ЛКО. Работа с главной страницей"""

    def mp_lko_find_and_click_participants_btn(self):
        """нажимает кнопку 'Участники' в главном меню"""
        self.ba_simple_wait_for_loading()
        self.find_and_click(*self.locators.MP_PARTICIPANTS)

    def mp_lko_click_system_btn(self):
        """нажимает кнопку 'система' в главном меню"""
        self.find_and_click(*self.locators.MP_SYSTEM_BTN)

    def mp_lko_click_reference_info_loading_btn(self):
        """нажимает кнопку 'Справочники' в главном меню"""
        self.find_and_click(*self.locators.MP_REFERENCE_INFO_LOADING_BTN)

    def mp_lko_click_antifrod_btn(self):
        """нажимает кнопку 'Антифрод' в главном меню"""
        self.find_and_click(*self.locators.MP_ANTIFROD_BTN)

    def mp_lko_click_requests_btn(self):
        """нажимает кнопку 'Запросы' в главном меню"""
        self.find_and_click(*self.locators.MP_REQUESTS_BTN)

    def mp_lko_register_req_btn(self):
        """Нажать на кнопку '+Новый запрос'"""
        self.find_and_click(*self.locators.MP_REGISTER_REQ_BTN)

    def mp_lko_register_incident_req_btn(self):
        """Нажать на кнопку 'Инцидент' в выпадающем списке 'О чем запрос'"""
        try:
            self.find_and_click(*self.locators.MP_LKO_REGISTER_INCIDENT_REQ)
        except Exception:
            self.log.info("кнопка не доступна")
            self.mp_lko_register_incident_req_btn_old()
        except:
            raise

    @decorator_for_change_selenium_wait_and_return_after(5)
    def mp_lko_register_incident_req_btn_old(self):
        """"""
        self.find_and_click(*self.locators.MP_LKO_REGISTER_INCIDENT_REQ_OLD)

    def mp_lko_click_configs_btn(self):
        """нажимает кнопку 'конфигурация' в главном меню"""
        self.find_and_click(*self.locators.MP_CONFIGS_BTN)

    def mp_open_bulletins_page(self):
        """ Метод открывает страницу со списком бюллетеней через навигационную панель """
        self.find_and_click(*self.locators.MP_KNOWLEDGE_BASE_BTN)
        self.find_and_click(*self.locators.MP_BULLETINS_LINK)
        assert self.search_element(*self.locators.BP_ACTION_BAR)
        self.ba_simple_wait_for_loading()

    def mp_open_incidents_page(self):
        """ Метод открывает страницу со списком инцидентов через навигационную панель """
        self.find_and_click(*self.locators.MP_INCIDENTS_BTN)
        self.find_and_click(*self.locators.MP_INCIDENTS_LINK)
        assert self.search_element(*self.locators.IP_ACTION_BAR)
        self.ba_wait_for_loading()

    def mp_fill_search_field(self, text):
        """метод заполняет поле поиска, которое общие для всех страниц"""
        self.find_and_fill_element(text, *self.locators.MP_LKO_SEARCH_FLD)


class MainPageLKU(Page):
    """ЛКУ. Работа с главной страницей"""
    def mp_lku_click_request_btn(self):
        """Нажимает кнопку 'Запросы' в главном меню"""
        self.find_and_click(*self.locators.MP_REQUESTS_BTN)

    def mp_lku_register_req_btn(self):
        """Нажать на кнопку '+Новый запрос'"""
        self.find_and_click(*self.locators.MP_REGISTER_REQ_BTN)

    def mp_lku_register_request_other_type_btn(self):
        """Нажать на кнопку 'Другое' в выпадающем списке 'О чем запрос'"""
        self.find_and_click(*self.locators.MP_LKU_REGISTER_OTHER_TYPE_REQ)

    def mp_lku_register_incident_req_btn(self):
        """Нажать на кнопку 'Инцидент' в выпадающем списке 'О чем запрос'"""
        try:
            self.find_and_click(*self.locators.MP_LKU_REGISTER_INCIDENT_REQ)
        except Exception:
            self.log.info("кнопка не найдена")
            self.mp_lku_register_incident_req_btn_old()
        except:
            raise

    @decorator_for_change_selenium_wait_and_return_after(5)
    def mp_lku_register_incident_req_btn_old(self):
        """"""
        self.find_and_click(*self.locators.MP_LKU_REGISTER_INCIDENT_REQ_OLD)

    def mp_lku_click_on_bell_btn(self):
        """нажать на колокольчик для проверки оповещений"""
        self.find_and_click(*self.locators.MP_BELL_BTN)

    def mp_lku_click_on_btn_all_notifications(self):
        """нажать на кнопку 'все оповещения' в выпадающем меню колокольчика
        ВАЖНО: использовать метод нужно после нажатия на колокольчик метод mp_lku_click_on_bell_btn"""
        self.find_and_click(*self.locators.MP_BTN_ALL_NOTIFICATIONS_IN_BELL_BTN)

    def mp_lku_open_bulletins_page(self):
        """ Нажать Рассылки центра в навигационной панели"""
        self.find_and_click(*self.locators.MP_LKU_BULLETINS_LINK)
        assert self.search_element(*self.locators.BP_LKU_BULLETINS_GRID)


class NotificationsPageLKU(Page):
    """Клас для работы со страницей с уведомлениями в ЛКУ контуре"""

    def np_lku_find_notification_via_id_request(self, request_id):
        """принимает id запроса и ищет его на страницы оповещений

        :param request_id: строка для поиска, лучше всего использовать id запроса
        :type request_id: str
        :return: webelement
        """
        self.log.info("Поиск запроса по ID: %s" % request_id)
        container = self.search_element(*self.locators.NP_CONTAINER_WITH_ALL_NOTIFICATIONS)
        notifications = container.find_elements(*self.locators.NP_NOTIFICATIONS)
        for request in notifications:
            if request_id in request.text:
                self.log.info("Найден запрос в уведомлениях, текст: %s" % request.text)
                return request
        raise Exception("No notification was found for this request id: %s" % request_id)

    def np_lku_search_request_and_check(self):
        """ищет запрос используя метод np_lku_find_notification_via_id_request и передавая ему
        переменную из класса RequestsPageLKO, которая хранит id запроса после создания его"""
        request_element = self.np_lku_find_notification_via_id_request(request_info_lko['hrid'])
        assert request_element

    def np_lku_search_bulletin_notification(self):
        element = self.np_lku_find_notification_via_id_request(self.bulletin_common_info['id'])
        if self.bulletin_common_info['type'] == 'Бюллетень':
            expected_text = 'Доступен новый бюллетень {} : {}'.format(self.bulletin_common_info['id'],
                                                                      self.bulletin_common_info['header'])
        elif self.bulletin_common_info['type'] == 'Уведомление':
            expected_text = 'Доступно новое уведомление {} : {}'.format(self.bulletin_common_info['id'],
                                                                        self.bulletin_common_info['header'])
        elif self.bulletin_common_info['type'] == 'Новость':
            expected_text = 'Доступна новость {} : {}'.format(self.bulletin_common_info['id'],
                                                              self.bulletin_common_info['header'])
        assert expected_text in element.text


class ReferenceInfoLoading(Page):
    RIL_REFERENCE_INFO_XML = os.getcwd() + '/test_data/20200220_ED807_full.xml'

    def ril_click_add_new_reference_info(self):
        """нажимает кнопку 'добавить справочник'"""
        self.find_and_click(*self.locators.RIL_ADD_NEW_REFERENCE_INFO_BTN)

    def ril_check_download_reference_info(self):
        """
        Скачивает справочник и проверяет, что файл не пустой

        :return:
        """
        self.find_and_click(*self.locators.RIL_DOWNLOAD_REFERENCE_BTN)
        self.ba_check_file('20200220_ED807_full.xml')

    def ril_choose_bic_swift_bac_ref(self):
        """выбирает справочник 'Справочник БИК и SWIFT BIC'"""
        self.find_and_click(*self.locators.RIL_REF_INFO_BIC_SWIFT_BIC)

    def ril_find_input_and_insert_file(self):
        """"""
        dad_input_element = self.find_and_click(*self.locators.RIL_INPUT_FILE_NEW_REFERENCE_INFO)
        drag_and_drop_file(dad_input_element, self.RIL_REFERENCE_INFO_XML)

    def ril_insert_file_click_submit_btn(self):
        """"""
        self.find_and_click(*self.locators.RIL_INPUT_FILE_SUBMIT_BTN)

    def ril_get_last_upd_date_value(self):
        """
        Получение значения даты в столбце 'Актуальная версия'

        :return:
        """
        return self.ba_return_elem_text_or_none(*self.locators.RIL_LAST_UPD_DATE_VALUE)

    def ril_get_last_upd_retry_date_value(self):
        """
        Получение значения даты в столбце 'Последняя попытка обновления'

        :return:
        """
        return self.ba_return_elem_text_or_none(*self.locators.RIL_LAST_UPD_RETRY_DATE_VALUE)

    def ril_compare_last_upd_date_and_curr_date(self, curr_date):
        """
        Сравнение даты загрузки и значения даты в столбце 'Актуальная версия'

        :return:
        """
        upd_date = self.ril_get_last_upd_date_value()
        assert curr_date == upd_date, f'В столбце "Актуальная версия" дата: "{upd_date}", ожидается: "{curr_date}"'

    def ril_compare_last_upd_retry_date_and_curr_date(self, curr_date):
        """
        Сравнение даты загрузки и значения даты в столбце 'Последняя попытка обновления'

        :return:
        """
        retry_date = self.ril_get_last_upd_retry_date_value()
        assert curr_date == retry_date, f'В столбце "Последняя попытка обновления" дата: "{retry_date}", ожидается: "{curr_date}"'

    @decorator_for_change_selenium_wait_and_return_after(5)
    def ril_check_modal_input_file_for_error(self):
        """Проверяет"""
        try:
            self.ba_wait_for_loading()
            from time import sleep
            sleep(4)
            if ('Ошибк' or 'ошибк') in self.return_text_ele(*self.locators.RIL_MODAL_INPUT_FILE):
                raise Exception("Проблема при загрузке справочника")
        except:
            self.log.info("Проблем при загрузке справочника не обнаружено")

    def ap_click_and_check_inn_recipient_btn(self):
        """скачивает фид inn.csv и проверяет, что он не пустой"""
        self.find_and_click(*self.locators.AP_FIDS_INN_RECIPIENT_BTN)
        self.ba_check_file('inn.csv')

    def ap_click_download_all_feeds_btn_and_check_zip(self):
        """скачивает фид Feeds.zip и проверяет, что он не пустой"""
        self.find_and_click(*self.locators.AP_DOWNLOAD_ALL_FIDS_BTN)
        self.ba_check_file('Feeds.zip')


class ConfigPageLKO(Page):
    """Класс для работы со страницей 'Конфигурация'"""
    def cp_download_active_configs(self):
        """скачать активную конфигурацию"""
        active_conf = self.search_element(*self.locators.CP_ACTIVE_CONFIGS)
        active_conf.find_element(*self.locators.CP_DOWBLOAD_CONFIGS).click()


class MalwareAnalysisEF(Page):
    def ma_ef_check_file_presence(self, send_data=None):
        if not send_data:
            send_data = test_modify_data['malware_analysis_data'][0]['malwareAnalysisRequestEF']

        send_name = '{}.rar'.format(send_data['malwareAnalysisRequest']['attachments'][0]['name'])
        file_name = self.ba_return_elem_text_or_none(*self.locators.MW_VIEW_MALWARE_ANALYSIS_FILE)
        if file_name != send_name:
            test_modify_data['errors'].append(f"Не совпадает 'Вложение' в ЭФ на {self.stand}: "
                                              f"ожидаемое {send_name}, отображаемое {file_name}")

    def ma_ef_download_file(self, file_num=1):
        elems = self.search_elements(*self.locators.MW_VIEW_MALWARE_ANALYSIS_FILE)
        elems[file_num-1].click()
        self.ba_confirm_file_download()

    def ma_ef_check_downloaded_file(self, send_data=None):
        if not send_data:
            send_data = test_modify_data['malware_analysis_data'][0]['malwareAnalysisRequestEF']
        send_name = send_data['malwareAnalysisRequest']['attachments'][0]['name']
        content = b64decode(send_data['malwareAnalysisRequest']['attachments'][0]['base64']).decode(encoding='utf8')
        self.ba_check_file_content(send_name, content, delete=False)

    def ma_ef_download_file_unpack_and_check_it(self, send_data=None):
        if not send_data:
            send_data = test_modify_data['malware_analysis_data'][0]['malwareAnalysisRequestEF']
        self.ma_ef_download_file()
        send_name_rar = '{}.rar'.format(send_data['malwareAnalysisRequest']['attachments'][0]['name'])
        self.ba_unrar_file(file_name=send_name_rar, password='infected', delete=False)
        self.ma_ef_check_downloaded_file(send_data)