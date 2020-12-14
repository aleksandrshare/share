import allure
import pytest
import backoff
from json import dumps
from framework.shared.third_party.portal_services import CertPortalCore
from tools.utils import generate_str_and_return
from tools.utils import read_file_for_attach_upload


class CertPortalActions(CertPortalCore):
    """ Класс для описания шагов в Portal """

    def certp_api_create_new_bulletin_json(self):
        """
        Создание JSON obj

        :return: JSON бюллетеня
        """
        attach_id, file_name, file_size = self.certp_api_upload_file()
        sub_certs_ids = self.certp_api_get_all_sub_certs_ids()
        bulletin_json = {
            "identifier": f"ID_AutoTest_{generate_str_and_return(20)}",
            "header": f"Бюллетень_Автотест_{generate_str_and_return(30)}",
            "description": f"Описание_{generate_str_and_return(30)}",
            "attachment":
            {
                "id": attach_id,
                "fileName": file_name,
                "fileSize": file_size
            },
            "centerIds": sub_certs_ids
        }
        return bulletin_json

    def certp_api_upload_file(self, file_path=None):
        """
        Загрузка файла в через внутреннее API

        :param file_path: путь к файлу относитель директории проекта
        :return: id заруженного вложения, имя файла, размер файла
        """
        file_name, file_obj, file_size = read_file_for_attach_upload(file_path)
        attach_id = self.certp_upload_attach(file_name, file_obj, file_size)
        return attach_id, file_name, file_size

    def certp_api_get_all_sub_certs_ids(self):
        """
        Получение списка id всех подключенных

        :return: список id подключенных
        """
        all_certs = self.certp_get_users_groups()
        allure.attach(dumps(all_certs, indent=2, ensure_ascii=False), 'Данные всех ЦЕРТов в системе',
                      allure.attachment_type.JSON)
        if all_certs[0].get('children'):
            sub_cert_ids = [sub_cert['id'] for sub_cert in all_certs[0]['children']]
            return sub_cert_ids
        else:
            pytest.fail('Ошибка! На Portal отсутствуют добавленные obj')

    def certp_api_create_bulletin(self, bulletin_json):
        """
        Метод отправки запроса на создание в Portal

        :param bulletin_json: JSON
        :return: id бюллетеня
        """
        resp = self.certp_post_bulletin(bulletin_json)
        allure.attach(self.CERT_URL + f"/#/bulletins/list?bulletinId={resp['id']}", 'Ссылка на obj в UI',
                      allure.attachment_type.URI_LIST)
        return resp['id']

    @backoff.on_exception(backoff.expo, AssertionError, max_tries=5, max_time=20)
    def certp_api_check_bulletin_published(self, bulletin_id, expected_status):
        """
        Проверка что obj имеет ожидаемый статус

        :param bulletin_id: id obj
        :param expected_status: ожидаемый статус
        :return:
        """
        bulletin_data = self.certp_get_bulletin_data(bulletin_id)
        allure.attach(dumps(bulletin_data, indent=2, ensure_ascii=False), f'Данные obj "{bulletin_id}"',
                      allure.attachment_type.JSON)
        assert bulletin_data['status'] == expected_status, f'Ошибка! Ожидаемый статус obj: "{expected_status}",' \
                                                           f' фактический "{expected_status}"'
