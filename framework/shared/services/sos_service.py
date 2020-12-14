# coding=utf-8
from tools.api_client.user_client import AutoCheckUserClient


class SubjectsObjectsSystemsCore(AutoCheckUserClient):
    """Класс набора функций для работы с сервисом PT SP SubjectsObjectsSystems"""

    sos_prefix = '/api'

    def get_lko_users_list(self, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        url = self.auth_url + self.sos_prefix + '/users'
        with self.session():
            data = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def get_lko_active_users_list(self, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        url = self.auth_url + self.sos_prefix + '/users?isActive=true'
        with self.session():
            data = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def pl_get_current_user_info(self, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """
        Получение информации о текущем пользователе

        :param allowed_codes: список стаус-кодов, корректных для выполняемого http-запроса
        :param retry_attempts: кол-во попыток для выполнения http-запроса
        :param retry_delay: ожидание в секундах перед выполнением http-запроса
        :return: json ответа на http-запрос
        """
        url = self.auth_url + self.sos_prefix + '/account/userinfo'
        with self.session():
            data = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def pl_get_groups_tree(self, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """
        Получение дерева групп в системе

        :param allowed_codes: список стаус-кодов, корректных для выполняемого http-запроса
        :param retry_attempts: кол-во попыток для выполнения http-запроса
        :param retry_delay: ожидание в секундах перед выполнением http-запроса
        :return: json ответа на http-запрос
        """
        url = self.auth_url + self.sos_prefix + '/groups/tree'
        with self.session():
            data = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def pl_get_brief_sos_entity_info(self, entity_type, entity_id, allowed_codes=[200],
                                     retry_attempts=0, retry_delay=1):
        """
        Получение краткой информации о сущности PT SP SOS

        :param entity_type: тип сущности, допустимые значения: "subject", "object", "system"
        :param entity_id: id сущности
        :param allowed_codes: список стаус-кодов, корректных для выполняемого http-запроса
        :param retry_attempts: кол-во попыток для выполнения http-запроса
        :param retry_delay: ожидание в секундах перед выполнением http-запроса
        :return: json ответа на http-запрос
        """
        url = self.auth_url + self.sos_prefix + f'/{entity_type}s/brief/{entity_id}'
        with self.session():
            data = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def pl_create_sos_entity(self, entity_type, json, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """
        Создание новой сущности PT SP SOS

        :param entity_type: тип сущности, допустимые значения: "subject", "object", "system"
        :param json: json с данными новой сущности
        :param allowed_codes: список стаус-кодов, корректных для выполняемого http-запроса
        :param retry_attempts: кол-во попыток для выполнения http-запроса
        :param retry_delay: ожидание в секундах перед выполнением http-запроса
        :return: json ответа на http-запрос
        """
        url = self.auth_url + self.sos_prefix + f'/{entity_type}s'
        with self.session():
            data = self.post(url=url, json=json, verify=False, allowed_codes=allowed_codes,
                             retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def pl_get_sos_entities(self, entity_type, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """
        Получение данных обо всех сущностях PT SP SOS заданного типа

        :param entity_type: тип сущности, допустимые значения: "subject", "object", "system"
        :param allowed_codes: список стаус-кодов, корректных для выполняемого http-запроса
        :param retry_attempts: кол-во попыток для выполнения http-запроса
        :param retry_delay: ожидание в секундах перед выполнением http-запроса
        :return: json ответа на http-запрос
        """
        url = self.auth_url + self.sos_prefix + f'/{entity_type}s'
        with self.session():
            data = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def pl_get_sos_entity_info(self, entity_type, entity_id, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """
        Получение данных о сущности PT SP SOS заданного типа и определенным id

        :param entity_type: тип сущности, допустимые значения: "subject", "object", "system"
        :param entity_id: id сущности
        :param allowed_codes: список стаус-кодов, корректных для выполняемого http-запроса
        :param retry_attempts: кол-во попыток для выполнения http-запроса
        :param retry_delay: ожидание в секундах перед выполнением http-запроса
        :return: json ответа на http-запрос
        """
        url = self.auth_url + self.sos_prefix + f'/{entity_type}s/{entity_id}'
        with self.session():
            data = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def pl_activate_sos_entity(self, entity_type, entity_id, entity_json, allowed_codes=[200],
                               retry_attempts=0, retry_delay=1):
        """
        Активировать сущность PT SP SOS заданного типа и определенным id

        :param entity_type: тип сущности, допустимые значения: "subject", "object", "system"
        :param entity_id: id сущности
        :param entity_json: JSON с данными сущности
        :param allowed_codes: список стаус-кодов, корректных для выполняемого http-запроса
        :param retry_attempts: кол-во попыток для выполнения http-запроса
        :param retry_delay: ожидание в секундах перед выполнением http-запроса
        :return: json ответа на http-запрос
        """
        url = self.auth_url + self.sos_prefix + f'/{entity_type}s/{entity_id}/activate'
        with self.session():
            data = self.post(url=url, json=entity_json, verify=False, allowed_codes=allowed_codes,
                             retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def pl_deactivate_sos_entity(self, entity_type, entity_id, entity_json, allowed_codes=[200],
                                 retry_attempts=0, retry_delay=1):
        """
        Деактивировать сущность PT SP SOS заданного типа и определенным id

        :param entity_type: тип сущности, допустимые значения: "subject", "object", "system"
        :param entity_id: id сущности
        :param entity_json: JSON с данными сущности
        :param allowed_codes: список стаус-кодов, корректных для выполняемого http-запроса
        :param retry_attempts: кол-во попыток для выполнения http-запроса
        :param retry_delay: ожидание в секундах перед выполнением http-запроса
        :return: json ответа на http-запрос
        """
        url = self.auth_url + self.sos_prefix + f'/{entity_type}s/{entity_id}/deactivate'
        with self.session():
            data = self.post(url=url, json=entity_json, verify=False, allowed_codes=allowed_codes,
                             retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def pl_filter_sos_entity(self, entity_type, filter_json, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """
        Задать настройки фильтрации для сущностей PT SP SOS заданного типа

        :param entity_type: тип сущности, допустимые значения: "subject", "object", "system"
        :param filter_json: JSON с настройками фильтрации
        :param allowed_codes: список стаус-кодов, корректных для выполняемого http-запроса
        :param retry_attempts: кол-во попыток для выполнения http-запроса
        :param retry_delay: ожидание в секундах перед выполнением http-запроса
        """
        url = self.auth_url + self.sos_prefix + f'/{entity_type}s/filter'
        with self.session():
            self.post(url=url, json=filter_json, verify=False, allowed_codes=allowed_codes,
                      retry_attempts=retry_attempts, retry_delay=retry_delay)

    def pl_delete_filter_sos_entity(self, entity_type, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """
        Удалить настройки фильтрации для сущностей PT SP SOS  заданного типа

        :param entity_type: тип сущности, допустимые значения: "subject", "object", "system"
        :param allowed_codes: список стаус-кодов, корректных для выполняемого http-запроса
        :param retry_attempts: кол-во попыток для выполнения http-запроса
        :param retry_delay: ожидание в секундах перед выполнением http-запроса
        """
        url = self.auth_url + self.sos_prefix + f'/{entity_type}s/filter'
        with self.session():
            self.delete(url=url, json={}, verify=False, allowed_codes=allowed_codes,
                        retry_attempts=retry_attempts, retry_delay=retry_delay)

    def pl_put_edit_sos_entity(self, entity_type, entity_id, edit_json, allowed_codes=[200],
                               retry_attempts=0, retry_delay=1):
        """
        Редактирование сущности PT SP SOS

        :param entity_type: тип сущности, допустимые значения: "subject", "object", "system"
        :param entity_id: id сущности
        :param edit_json: JSON с изменениями данных сущности
        :param allowed_codes: список стаус-кодов, корректных для выполняемого http-запроса
        :param retry_attempts: кол-во попыток для выполнения http-запроса
        :param retry_delay: ожидание в секундах перед выполнением http-запроса
        :return: json ответа на http-запрос
        """
        url = self.auth_url + self.sos_prefix + f'/{entity_type}s/{entity_id}'
        with self.session():
            data = self.put(url=url, json=edit_json, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()
