from framework.ui_libs.ui_lib import Page
from os import path
import allure


class CertPortalIncidentsPage(Page):
    def cp_ip_open_incident_by_id(self, inc_id):
        """ метод открывает страницу просмотра инцидента по его id """
        url = '{}/#/incidents/view/{}'.format(self.url, inc_id)
        self.log.info("Open page: %s" % url)
        self.driver.get(url)
        self.ba_wait_for_loading()

    def cp_ip_view_click_attachment_link_on_action_bar(self):
        """ метод кликает ссылку Вложения на странице просмотра инцидента """
        self.find_and_click(*self.locators.CP_IP_VIEW_ATTACHMENTS_MENU_ITEM)
        self.ba_wait_for_loading()

    def cp_ip_view_click_actions_link_on_action_bar(self):
        """ метод кликает ссылку Принятые меры на странице просмотра инцидента """
        self.find_and_click(*self.locators.CP_IP_VIEW_ACTIONS_MENU_ITEM)
        self.ba_wait_for_loading()

    def cp_ip_view_click_comments_link_on_action_bar(self):
        """ метод кликает ссылку Комментарии на странице просмотра инцидента """
        self.find_and_click(*self.locators.CP_IP_VIEW_COMMENTS_MENU_ITEM)
        self.ba_wait_for_loading()

    def cp_ip_view_click_malware_impact_link_on_action_bar(self):
        """ метод кликает ссылку для данных Вредоносного ПО на странице просмотра инцидента """
        self.find_and_click(*self.locators.CP_IP_VIEW_MALWARE_IMPACT_MENU_ITEM)
        self.ba_wait_for_loading()

    def cp_ip_view_download_file_in_attachments_tab(self):
        """ метод загрузки файла во вкладке Вложения"""
        self.ba_wait_for_loading()
        self.find_and_click(*self.locators.CP_IP_VIEW_ATTACHMENT_FILE_LINK)

    def cp_ip_view_download_malware_sample(self):
        """ вкладка Вредоносное ПО: метод загрузки файла с образцом вредоносного ПО"""
        self.ba_wait_for_loading()
        self.find_and_click(*self.locators.CP_IP_VIEW_MALWARE_SAMPLE_FILE)

    def cp_ip_view_download_malware_email_file(self):
        """ вкладка Вредоносное ПО: метод загрузки файла эл. письма """
        self.ba_wait_for_loading()
        self.find_and_click(*self.locators.CP_IP_VIEW_MALWARE_EMAIL_FILE)

    def cp_ip_view_check_downloaded_rar_file(self, file_name, source_file_path):
        """ метод проверки заархивированных файлов. разархивирует и проверяет содержимое файла """
        with open(source_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.log.info('Распаковка файла {}'.format(file_name))
        name = path.splitext(file_name)[0]
        self.ba_unrar_file(file_name=file_name, password='infected')
        self.log.info('Проверка файла {}'.format(name))
        self.ba_check_file_content(name, content, delete=False)

    def cp_ip_view_check_downloaded_file(self, file_name, source_file_path):
        """ метод проверки содержимого файла """
        with open(source_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.log.info('Проверка файла {}'.format(file_name))
        self.ba_check_file_content(file_name, content, delete=False)

    def _check_message_with_text(self, text, locator):
        """ обобщающий метод проверки наличия сообщения с текстом в заданном локаторе """
        elements = self.search_elements(*locator)
        allure.attach(name='screen', body=self.driver.get_screenshot_as_png(),
                      attachment_type=allure.attachment_type.PNG)
        is_found = False
        for elem in elements:
            if elem.text == text:
                is_found = True
                break
        assert is_found, f'Не найдено сообщение с текстом {text}'

    def cp_ip_check_message_present(self, text):
        """ метод проверяет, что сообщение отображается """
        self._check_message_with_text(text, self.locators.CP_IP_VIEW_CHAT_MESSAGE)

    def cp_ip_check_action_present(self, text):
        """ метод проверяет, что принятая мера отображается """
        self._check_message_with_text(text, self.locators.CP_IP_VIEW_ACTION)

    def cp_ip_check_recommend_present(self, text):
        """ метод проверяет, что рекомендация отображается """
        self._check_message_with_text(text, self.locators.CP_IP_VIEW_RECOMMENDATION)

    def cp_ip_check_comment_present(self, text):
        """ метод проверяет, что комментарий отображается """
        self._check_message_with_text(text, self.locators.CP_IP_VIEW_COMMENT)


