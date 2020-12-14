#!/usr/bin/env python
# -*- coding: utf-8 -*-
from framework.api_libs.user_client import AutoCheckUserClient
from uuid import uuid1


class CertPortalCore(AutoCheckUserClient):
    """ Класс для работы в Портале """

    def certp_upload_attach(self, file_name, file_obj, file_size, allowed_codes=[200], retry_attempts=0,
                            retry_delay=1):
        """
        Внутреннее API Портала. Загрузка файла в систему (для дальнейшего прикрепления к сущности)

        :param file_name: имя файла с расширением
        :param file_obj: данные файла в бинарном формате
        :param file_size: размер файла
        :param allowed_codes: список стаус-кодов, корректных для выполняемого http-запроса
        :param retry_attempts: кол-во попыток для выполнения http-запроса
        :param retry_delay: ожидание в секундах перед выполнением http-запроса
        :return: json ответа на http-запрос
        """
        attach_id = str(uuid1())
        url = self.auth_url + f'/api/documents/attachments/{attach_id}/upload'
        filedata = [('file', ('blob', file_obj, 'application/octet-stream'))]
        data = {
            "flowChunkNumber": 1,
            "flowChunkSize": 1048576,
            "flowCurrentChunkSize": file_size,
            "flowFilename": file_name,
            "flowIdentifier": f"{file_size}-{file_name.replace('.', '')}",
            "flowRelativePath": file_name,
            "flowTotalChunks": 1,
            "flowTotalSize": file_size,
            "file": file_obj
        }
        with self.session():
            self.post(url=url, data=data, files=filedata, allowed_codes=allowed_codes,
                      retry_attempts=retry_attempts, retry_delay=retry_delay)
        return attach_id

    def certp_post_bulletin(self, bulletin_data, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """
        Внутреннее API Портала. Метод отправки запроса на бюллетеня в ЦертПортале

        :param bulletin_data: json
        :param allowed_codes: разрешённый статус-код при отправке запроса
        :param retry_attempts: кол-во попыток отправки запроса
        :param retry_delay: промежуток времени между попытками отправки в секундах
        :return: json ответа
        """
        url = self.auth_url + '/api/bulletins'
        with self.session():
            data = self.post(url=url, json=bulletin_data, verify=False, allowed_codes=allowed_codes,
                             retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def certp_get_users_groups(self, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """
        Внутреннее API Портала. Получение всех групп подключенных ЦЕРТов

        :param allowed_codes: разрешённый статус-код при отправке запроса
        :param retry_attempts: кол-во попыток отправки запроса
        :param retry_delay: промежуток времени между попытками отправки в секундах
        :return: json ответа
        """
        url = self.auth_url + '/api/groups/tree'
        with self.session():
            response = self.get(url=url, allowed_codes=allowed_codes, retry_attempts=retry_attempts,
                                retry_delay=retry_delay)
        return response.json()

    def certp_publicate_bulletin(self, bulletin_id, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """
        Внутреннее API Портала. Метод публикации бюллетеня в ЦертПортале

        :param bulletin_id: id бюллетеня
        :param allowed_codes: разрешённый статус-код при отправке запроса
        :param retry_attempts: кол-во попыток отправки запроса
        :param retry_delay: промежуток времени между попытками отправки в секундах
        :return: json ответа
        """
        url = self.auth_url + f'/api/bulletins/{bulletin_id}/publicate'
        json = {'isCopy': False}
        with self.session():
            self.post(url=url, json=json, verify=False, allowed_codes=allowed_codes,
                      retry_attempts=retry_attempts, retry_delay=retry_delay)

    def certp_get_bulletin_data(self, bulletin_id, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """
        Внутреннее API Портала. Получение данных бюллетеня

        :param bulletin_id: id
        :param allowed_codes: разрешённый статус-код при отправке запроса
        :param retry_attempts: кол-во попыток отправки запроса
        :param retry_delay: промежуток времени между попытками отправки в секундах
        :return: json ответа
        """
        url = self.auth_url + f'/api/bulletins/{bulletin_id}'
        with self.session():
            response = self.get(url=url, allowed_codes=allowed_codes, retry_attempts=retry_attempts,
                                retry_delay=retry_delay)
        return response.json()
