from framework.ui_libs.ui_lib import Page
from framework.other_proj_ui.ui_auto.fc_helpers import collect_locator
from random import choice
from tools.utils import get_jpath_value
from configs.modify_data import test_modify_data, cert_modify_data
import allure
from tools.utils import now_timestamp


class IncidentsPage(Page):

    incident_info = {'type': None, 'description': None, 'id': None}

    def ip_open_random_incident(self):
        """ метод запрашивает список инцидентов, выбирает случайный из него и открывает страницу просмотра по
        прямой ссылке """
        rand_incident = choice(self.api_client.get_all_incidents())
        self.incident_info['id'] = rand_incident['id']
        self.ip_open_incident_by_id(rand_incident['id'])

    def ip_click_create_bulletin_link(self):
        """ метод кликает ссылку Сформировать рассылку, должна быть открыта страница просмотра инцидента"""
        self.find_and_click(*self.locators.IP_INCIDENT_VIEW_MORE_BUTTON)
        self.find_and_click(*self.locators.IP_CREATE_BULLETIN_LINK)
        self.ba_simple_wait_for_loading()
        assert self.search_element(*self.locators.BP_CREATE_FROM_PAGE)

    def ip_get_incident_fields_for_bulletin(self):
        """ Получение значение типа инцидента в старом варианте для заголовка бюллетеня """
        inc_type = self.return_text_ele(*collect_locator(self.locators.IP_INCIDENT_VIEW_ITEM_PATTERN,
                                                                           'Тип инцидента'))
        inc_type = inc_type.split(') ')
        self.incident_info['type'] = inc_type[-1]
        try:
            self.incident_info['description'] = self.return_text_ele(
                *collect_locator(self.locators.IP_INCIDENT_VIEW_ITEM_PATTERN, 'Описание инцидента'))
        except:
            self.log.info('Описание инцидента не заполнено')
            self.incident_info['description'] = None

    def ip_open_incident_by_id(self, inc_id):
        """ открыть инцидент на просмотр по его id """
        url = '{}/v2/incidents/view/{}'.format(self.url, inc_id)
        self.log.info("Open page: %s" % url)
        self.driver.get(url)
        allure.attach(url, 'Ссылка на инцидент', allure.attachment_type.URI_LIST)
        self.ba_simple_wait_for_loading()

    def ip_click_antifraud_link_on_action_bar(self):
        """ нажать "Операции без согласия" на странице просмотра инцидента """
        self.find_and_click(*self.locators.IP_INCIDENT_VIEW_ANTIFRAUD_LINK_ITEM)

    def ip_open_obs_card(self, obs_num=1):
        """ открыть просмотр карточки обс в инциденте """
        elems = self.search_elements(*self.locators.IP_INCIDENT_VIEW_OBS_CARD)
        elems[obs_num-1].click()
        self.ba_simple_wait_for_loading()

    def ip_check_payer_passport_hashes_in_obs(self, schema):
        """ проверка хешей паспорта """
        if schema == '2_1':
            payer_hashes = get_jpath_value(test_modify_data['attach_data'], '$.[*].payer.hash')
        else:
            payer_hashes = get_jpath_value(test_modify_data['attach_data'], '$.[*].payer.hashes')
        elems = self.search_elements(*self.locators.IP_INCIDENT_VIEW_PAYER_PASSPORT_HASHES)
        inc_hashes = list()
        for item in elems:
            inc_hashes.append(item.text.strip())
        if schema == '2_1':
            assert payer_hashes in inc_hashes, f"{payer_hashes} не найден в хешах паспорта плательщика"
        else:
            for item in payer_hashes:
                if item.get('hash'):
                    assert item['hash'] in inc_hashes, f"{item['hash']} не найден в хешах паспорта плательщика"

    def ip_check_payer_snils_hashes_in_obs(self, schema):
        """ проверка хешей снилс """
        if schema == '2_1':
            payer_hashes = get_jpath_value(test_modify_data['attach_data'], '$.[*].payer.hashSnils')
        else:
            payer_hashes = get_jpath_value(test_modify_data['attach_data'], '$.[*].payer.hashes')
        elems = self.search_elements(*self.locators.IP_INCIDENT_VIEW_PAYER_SNILS_HASHES)
        inc_hashes = list()
        for item in elems:
            inc_hashes.append(item.text.strip())
        if schema == '2_1':
            assert payer_hashes in inc_hashes, f"{payer_hashes} не найден в хешах паспорта плательщика"
        else:
            for item in payer_hashes:
                if item.get('hashSnils'):
                    assert item['hashSnils'] in inc_hashes, f"{item['hashSnils']} не найден в хешах снилс плательщика"

    def ip_click_analitic_form_link_on_obs_card(self):
        """ нажать Аналитическая форма в карточке обс, открытой в инциденте """
        self.find_and_click(*self.locators.IP_INCIDENT_VIEW_OBS_CARD_ANALITIC_FORM_LINK)
        self.ba_simple_wait_for_loading()

    def ip_check_checkbox_checked_for_new_receiver(self):
        """ проверить, что выбран чек-бокс для нового получателя """
        class_attr = self.return_attrs_element(
            'class', *self.locators.IP_INCIDENT_VIEW_OBS_CARD_ANALITIC_FORM_NEW_RECEIVER_CHECKBOX)
        if 'mc-checked' not in class_attr:
            allure.attach(name='screen', body=self.driver.get_screenshot_as_png(),
                          attachment_type=allure.attachment_type.PNG)
            raise AssertionError('Чек-бокс для значения newReceiver не выбран')

    def ip_check_checkbox_checked_for_cross_country(self):
        class_attr = self.return_attrs_element('class',
                                               *self.locators.IP_INCIDENT_VIEW_OBS_CARD_ANALITIC_FORM_CROSS_COUNTRY_CHECKBOX)
        if 'mc-checked' not in class_attr:
            allure.attach(name='screen', body=self.driver.get_screenshot_as_png(),
                          attachment_type=allure.attachment_type.PNG)
            raise AssertionError('Чек-бокс для значения crossCountry не выбран')

    def ip_check_checkbox_checked_for_low_time_interval(self):
        class_attr = self.return_attrs_element('class',
                                               *self.locators.IP_INCIDENT_VIEW_OBS_CARD_ANALITIC_FORM_LOW_TIME_INTERVAL_CHECKBOX)
        if 'mc-checked' not in class_attr:
            allure.attach(name='screen', body=self.driver.get_screenshot_as_png(),
                          attachment_type=allure.attachment_type.PNG)
            raise AssertionError('Чек-бокс для значения lowTimeInterval не выбран')

    def ip_check_checkbox_checked_for_odd_place(self):
        class_attr = self.return_attrs_element('class',
                                               *self.locators.IP_INCIDENT_VIEW_OBS_CARD_ANALITIC_FORM_ODD_PLACE_CHECKBOX)
        if 'mc-checked' not in class_attr:
            allure.attach(name='screen', body=self.driver.get_screenshot_as_png(),
                          attachment_type=allure.attachment_type.PNG)
            raise AssertionError('Чек-бокс для значения oddPlace не выбран')

    def ip_click_description_link(self):
        """ нажать Описание на странице просмотра инцидента """
        self.find_and_click(*self.locators.IP_INCIDENT_VIEW_DESCRIPTION_LINK_ITEM)

    def ip_check_description_field(self):
        """ проверить значение поля Описание """
        expected_description = get_jpath_value(test_modify_data['attach_data'], '$..incident.description')
        description = self.ba_return_elem_text_or_none(*self.locators.IP_INCIDENT_VIEW_INCIDENT_DESCRIPTION)
        assert description == expected_description, (f'Не совпадает описание инцидента, '
                                                     f'ожидаемое {expected_description}, отображаемое {description}')

    def ip_open_gos_tab(self):
        """ метод кликает по вкладке Взаимодействие"""
        self.find_and_click(*self.locators.IP_INCIDENT_VIEW_GOS_TAB)

    def _check_message_with_text(self, text, locator):
        """ обобщающий метод проверки наличия сообщения с текстом в заданном локаторе """
        allure.attach(name='screen', body=self.driver.get_screenshot_as_png(),
                      attachment_type=allure.attachment_type.PNG)
        elements = self.search_elements(*locator)
        is_found = False
        for elem in elements:
            self.log.info(f'Текс сообщения: {elem.text}')
            if elem.text == text:
                is_found = True
                break
        assert is_found, f'Не найдено сообщение с текстом {text}'

    def ip_check_system_message_present_on_gos_tab(self, text):
        """ метод проверки отображения системного сообщения на вкладке Взаимодействие с  """
        self._check_message_with_text(text, self.locators.IP_INCIDENT_VIEW_GOS_SYSTEM_MESSAGE)

    def ip_check_message_present_on_gos_tab(self, text=None):
        """ метод проверки отображения сообщения на вкладке Взаимодействие с  """
        if not text:
            text = cert_modify_data['send_message']
        self._check_message_with_text(text, self.locators.IP_INCIDENT_VIEW_GOS_MESSAGE)

    def ip_check_action_present_on_gos_tab(self, text=None):
        """ метод проверки отображения принятой меры на вкладке Взаимодействие с  """
        if not text:
            text = cert_modify_data['send_action']
        self._check_message_with_text(text, self.locators.IP_INCIDENT_VIEW_GOS_ACTION)

    def ip_check_recommendation_present_on_gos_tab(self, text=None):
        """ метод проверки отображения рекомендации на вкладке Взаимодействие с  """
        if not text:
            text = cert_modify_data['send_recommendation']
        self._check_message_with_text(text, self.locators.IP_INCIDENT_VIEW_GOS_RECOMMENDATION)

    def ip_click_compete_interaction_on_gos_tab(self):
        """ метод кликает чек-бок Завершить взаимодействие  на вкладке Взаимодействие с """
        self.find_and_click(*self.locators.IP_INCIDENT_VIEW_GOS_COMPLETE_INTERACTION)

    def ip_click_send_btn_on_gos_tab(self):
        """ метод нажимает кнопку Отправить на вкладке Взаимодействие"""
        self.find_and_click(*self.locators.IP_INCIDENT_VIEW_GOSSOPKA_SEND_BTN)

    def ip_click_gos_message_type_select(self):
        """ метод кликает по выпадашке с типами сообщений на вкладке Взаимодействие с """
        self.find_and_click(*self.locators.IP_INCIDENT_VIEW_GOS_MESSAGE_TYPE_SELECT)

    def ip_gos_select_message(self):
        """ метод выбирает тип Сообщение в выпадашке с типами на вкладке Взаимодействие с """
        self.find_and_click(*self.locators.IP_INCIDENT_VIEW_GOS_SELECT_MESSAGE_ITEM)

    def ip_gos_select_action(self):
        """ метод выбирает тип Принятая мера в выпадашке с типами на вкладке Взаимодействие с """
        self.find_and_click(*self.locators.IP_INCIDENT_VIEW_GOS_SELECT_ACTION_ITEM)

    def ip_gos_select_comment(self):
        """ метод выбирает тип Комментарий в выпадашке с типами на вкладке Взаимодействие с """
        self.find_and_click(*self.locators.IP_INCIDENT_VIEW_GOS_SELECT_COMMENT_ITEM)

    def ip_gos_fill_message_input(self, text):
        """ метод вводит текст в поле для сообщений на вкладке Взаимодействие с """
        self.find_and_clear_element(*self.locators.IP_INCIDENT_VIEW_GOS_MESSAGE_INPUT)
        self.find_and_fill_element(text, *self.locators.IP_INCIDENT_VIEW_GOS_MESSAGE_INPUT)

    def ip_send_message_to_gos(self, text=None):
        """ объединяющий шаги метод для отправки сообщения в  """
        if not text:
            text = 'Сообщение от  ' + now_timestamp()
        test_modify_data['fc_message'] = text
        self.ip_click_gos_message_type_select()
        self.ip_gos_select_message()
        self.ip_gos_fill_message_input(text)
        self.ip_click_send_btn_on_gos_tab()

    def ip_send_action_to_gos(self, text=None):
        """ объединяющий шаги метод для отправки принятой меры в  """
        if not text:
            text = 'Принятая мера от  ' + now_timestamp()
        test_modify_data['fc_action'] = text
        self.ip_click_gos_message_type_select()
        self.ip_gos_select_action()
        self.ip_gos_fill_message_input(text)
        self.ip_click_send_btn_on_gos_tab()

    def ip_send_comment_to_gos(self, text=None):
        """ объединяющий шаги метод для отправки комментария в  """
        if not text:
            text = 'Комментарий от  ' + now_timestamp()
        test_modify_data['fc_comment'] = text
        self.ip_click_gos_message_type_select()
        self.ip_gos_select_comment()
        self.ip_gos_fill_message_input(text)
        self.ip_click_send_btn_on_gos_tab()
