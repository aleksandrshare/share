#!/usr/bin/env python
# -*- coding: utf-8 -*-


from faker import Faker
import yaml
import random
from configs.settings import paths_map
from framework.api_libs.user_client import AutoCheckUserClient
import logging
from tools.utils import search_dir_recursive
import os
from pathlib import Path
import uuid
from copy import copy
from tools.utils import generate_str_and_return

logger = logging.getLogger(__name__)


class PlatformJsonGenerator:

    def __init__(self, schema=None, stand_url=None, login=None, password=None):
        # путь до папки контрактов
        self.repo_contracts = search_dir_recursive(os.getcwd(), 'department-center.contracts') + '/'
        self.full_path = None  # путь до основного контракта
        self.contract = None  # файл контракта
        self.handler = None  # ключ в paths
        self.schema = schema  # dict после вычетки yaml из контракта
        self.temp_list_paths = list()  # список для хранения
        self.result = dict()  # dict конечного результата генерации
        self.fake = Faker()  # проинициализированная библиотека Faker
        self.date_time_format = '%Y-%m-%dT%H:%M:%S+00:00'  # формат для времени UTC
        # клиент для запросов по API
        self.api_client = None
        self.stand_url = stand_url
        self.login = login
        self.password = password
        if self.stand_url and self.login and self.password:
            self.activate_api_client()

##################################################################################################
    def give_json(self, handler):
        """
        Функция 'запускник' генерации json из контракта, она же usage для класса

        :param handler: префикс api хендлера как в контракте, например /api/incident
        :return: dict
        """
        self.handler = handler
        self._find_path_and_choose_contract()
        self.check_paths()
        self.check_definition()
        self.delete_skips()
        result = copy(self.result)
        self.clear_to_end()
        return result

    def give_json_and_change(self, handler, temp=None, final=False, **kwargs):
        """
        Заменяет собой функцию give_json плюс принимает параметры, которые необходимо заменить в конечном json

        :param temp: служебный флаг, передавть только если есть вложенность словарей
        :param final: служебный флаг, передавть только если есть вложенность словарей
        :param handler: префикс api хендлера как в контракте, например /api/incident
        :param kwargs: ключ+значение которые необходимо заменить в итоговом json
        :return: dict
        """
        if not final:
            temp = self.give_json(handler)
        for i in kwargs.keys():
            for k, v in temp.items():
                if isinstance(v, dict):
                    self.give_json_and_change(handler, final=True, temp=v, **kwargs)
                if i == k:
                    temp[k] = kwargs[i]
        return temp

##################################################################################################
# Служебные и вспомогательные функции

    def activate_api_client(self):
        """
        Активирует API клиент если были переданы url и креды в класс при инициализации
        """
        self.api_client = AutoCheckUserClient(auth_url=self.stand_url, login=self.login, password=self.password)

    def _open_contract(self, contract=None):
        """
        Метод открывает контракт и возвращает dict

        :param contract: необязательный параментр, передавть только если нужен нестандартный запуск
        :return: dict
        """
        if not contract:
            contract = self.contract
        with open(contract, 'r', encoding='utf-8') as yaml_file:
            yaml_data = yaml.load(yaml_file, Loader=yaml.Loader)
            return yaml_data

    def _find_path_and_choose_contract(self, handler=None):
        """
        Читает контракт и ищет хендлер

        :param handler: необязательный параментр, передавть только если нужен нестандартный запуск
        """
        if not handler:
            handler = self.handler
        for k, v in paths_map.items():
            if handler in v:
                self.contract = self.repo_contracts + k
                self.schema = self._open_contract()
                self.full_path = Path(self.contract)
                return
        else:
            logger.error('Не найден такой путь {} в path_map словаре'.format(handler))
            raise SystemExit('Не найден такой путь {} в path_map словаре'.format(handler))

    @property
    def paths(self):
        """
        Проперти функция, возвращает dict с paths из контракта

        :return: dict
        """
        return self.schema['paths'][self.handler]

    def definitions(self, schema=None):
        """
        Возвращает dict с definitions из контракта

        :param schema: необязательный параментр, передавть только если нужен нестандартный запуск
        :return: dict
        """
        if not schema:
            schema = self.schema
        if not schema.get('definitions'):
            return schema.get('components')['schemas']
        return schema.get('definitions')

    @staticmethod
    def string_to_list_for_refs(item):
        """
        Добавляет в list переданные значения

        :param item: object
        :return: list
        """
        if not isinstance(item, list):
            tmp = list()
            tmp.append(item)
            return tmp
        return item

    @classmethod
    def format_refs(cls, list_items):
        """
        Ищет defenition в строке и возвращает

        :param list_items: object
        :return: list
        """
        temp_list = list()
        list_items = cls.string_to_list_for_refs(list_items)
        for i in list_items:
            if i.startswith('#'):
                temp = i.split('/')
                temp_list.append(temp[-1])
        return temp_list

    def delete_skips(self, item=None):
        """
        Рекурсивно удаляет все ключи со значениями skip

        :param item: dict необязательный параментр, передавть только если нужен нестандартный запуск
        """
        if not item:
            item = self.result
        for k, v in list(item.items()):
            if isinstance(v, dict):
                self.delete_skips(v)
            if v == 'skip':
                item.pop(k)

    def clear_to_end(self):
        self.temp_list_paths = list()
        self.result = dict()

# Функции парсинга paths

    def recurse_for_paths(self, item):
        """
        Рекурсивно ищет ссылки на definition в любой вложенной в dict структуре

        :param item: dict
        """
        for i, l in item.items():
            if i == 'responses':
                continue
            else:
                if i == '$ref':
                    self.temp_list_paths.append(l)
                else:
                    if isinstance(l, dict):
                        self.recurse_for_paths(l)
                    elif isinstance(l, list):
                        for list_item in l:
                            if isinstance(list_item, dict):
                                self.recurse_for_paths(list_item)

    def check_paths(self):
        """
        Запускает поиск ссылок на definition в paths контракте
        """
        for k, v in self.paths.items():
            if k != 'get':
                if isinstance(v, str):
                    logger.info(f'Найдено, но не обработано {v} - в paths контракта {self.contract}')
                elif 'param' in k:
                    logger.info(f'Блок {k} пропущен, т.к. пока в нем нет для нас полезной инфы')
                else:
                    self.recurse_for_paths(v)

# Функции парсинга definitions

    def check_definition(self, item=None, final=False, definition=None):
        """
        Основная функция парсинга в контрактах для генерации

        :param item: list список с difinitions
        :param final: служебный флаг, передавть только если есть вложенность словарей (необходим для рекурсии)
        :param definition: dict definitions
        """
        if not item:
            item = self.format_refs(self.temp_list_paths)
        if not definition:
            definition = self.definitions()
        for i in item:
            for k, v in definition[i].items():
                if k == 'items':
                    return self.ref_parse(v.get('$ref'))
                elif k == 'properties':
                    return self.properties_parse(v, final)
                elif k == 'allOf':
                    return self.allOf_parse(v, final)
                elif k == '$ref':
                    return self.ref_parse(v, final)
                elif k == 'enum':
                    return random.choice(v)
                else:
                    logger.debug('До сюда дойти было не должно... метод: check_definition класса '
                                'PlatformJsonGenerator значения key: %s value: %s' % (str(k), str(v)))

    def properties_parse(self, value, final=False):
        """
        Парсит properties в контрактах и заполняем конечный json

        :param value: dict
        :param final: служебный флаг, передавть только если есть вложенность словарей (необходим для рекурсии)
        """
        if final:
            return self.properties_when_final(value, final)
        for k, v in value.items():
            if v.get('type') == 'array':
                temp_list = list()
                temp_dict = dict()
                res = self.generate(v)
                if res == 'skip':
                    self.result[k] = res
                else:
                    temp_dict.update(res)
                    temp_list.append(temp_dict)
                    self.result[k] = temp_list
            else:
                self.result[k] = self.generate(v)

    def properties_when_final(self, value, final=False):
        """
        Парсинг вложенных словарей, наполняет словарь и возвращает его

        :param value: dict
        :param final: служебный флаг, передавть только если есть вложенность словарей (необходим для рекурсии)
        :return: dict
        """
        tem_dict = dict()
        for k, v in value.items():
            if v.get('x-qa-info'):
                tem_dict[k] = self.generate_x_qa_info(v.get('x-qa-info'))
                continue
            if v.get('$ref'):
                tem_dict[k] = self.ref_parse(v.get('$ref'), final)
            else:
                tem_dict[k] = self.generate_types(v)
        return tem_dict

    def ref_parse(self, item, final=False):
        """
        Прасит ссылки на definition и передает их в функцию check_definition

        :param item: dict или str
        :param final: служебный флаг, передавть только если есть вложенность словарей (необходим для рекурсии)
        """
        if isinstance(item, dict):
            ref = self.format_refs(self.string_to_list_for_refs(item.get('$ref')))
            if final:
                return self.check_definition(self.string_to_list_for_refs(ref[-1]), final=True)
        else:
            ref = self.format_refs(item)
            if item.startswith('.'):
                return self.second_contract(item)
            elif final:
                return self.check_definition(self.string_to_list_for_refs(ref[-1]), final=True)
        return self.check_definition(self.string_to_list_for_refs(ref[-1]))

    def allOf_parse(self, item, final=False):
        """
        Парсит блоки allOf в контракте

        :param item: list
        """
        temp_dict = dict()
        for i in item:
            for k, v in i.items():
                if "$ref" in k:
                    if final:
                        temp_dict.update(self.ref_parse(i.get("$ref"), final))
                    else:
                        self.ref_parse(i.get("$ref"), final)
                elif 'properties' in k:
                    if final:
                        temp_dict.update(self.properties_parse(v, final))
                    else:
                        self.properties_parse(v, final)
                else:
                    logger.info('Не учитываем данный ключ в allOf key: %s value: %s' %(k, v))
        return temp_dict

    def second_contract(self, item):
        """
        Прарсит дополнительный контракт если сслыка на definition из основного ведет в другой контракт

        :param item: str
        """
        temp = item.split('#')
        if temp[0].startswith('..'):
            second_contract_path = (self.full_path / temp[0]).resolve()
        else:
            second_contract_path = (self.full_path.parent / temp[0]).resolve()
        defenition_name = temp[-1].split('/')
        contract = PlatformJsonGenerator(stand_url=self.stand_url, login=self.login, password=self.password)
        contract.schema = contract._open_contract(second_contract_path)
        defenitions = contract.definitions()
        return contract.check_definition(item=contract.string_to_list_for_refs(defenition_name[-1]),
                                         definition=defenitions, final=True)

# Функции генерации после парсинга

    def generate(self, item):
        """
        Проверяет по разным условиям ключи для генерации и возвращает сгенерированные значения

        :param item: dict
        """
        if item.get('$ref') and item.get('x-qa-info'):
            return self.check_xqa_for_skip(item)
        elif item.get('x-qa-info'):
            return self.generate_x_qa_info(item.get('x-qa-info'))
        elif item.get('$ref'):
            return self.ref_parse(item.get('$ref'), final=True)
        elif item.get('enum'):
            return random.choice(item.get('enum'))
        elif item.get('type') == 'array':
            return self.logic_for_array(item)
        elif item.get('format'):
            return self.generate_types(item.get('format'))
        elif item.get('type'):
            return self.generate_types(item.get('type'))

    def logic_for_array(self, item):
        if item.get('items') and item.get('x-qa-info'):
            return self.check_xqa_for_skip(item)
        elif item.get('items').get("$ref"):
            return self.ref_parse(item.get('items'), final=True)
        else:
            return self.generate_types(item['type'])

    def check_xqa_for_skip(self, item):
        """
        Проверяет значения на skip и ссылку на definitions

        :param item: str или dict
        """
        if 'skip' in item.get('x-qa-info'):
            return 'skip'
        if isinstance(item, dict):
            return self.ref_parse(item.get('items'), final=True)
        else:
            return self.ref_parse(item.get('$ref'), final=True)

    def generate_types(self, types):
        """
        Генерирует данные для значений конечного json

        :param types: str или dict
        """
        if isinstance(types, dict):
            if types.get('type') and 'string' in types.get('type'):
                return 'random_str ' + generate_str_and_return(5)
            elif types.get('type') and 'bool' in types.get('type'):
                return random.choice([True, False])
            elif types.get('type') and types.get('type') == 'array':
                if types.get('items').get("$ref"):
                    temp_list = list()
                    temp_list.append(self.ref_parse(types.get('items').get("$ref"), final=True))
                    return temp_list
                else:
                    return [generate_str_and_return(5) for _ in range(2)]
            elif types.get('allOf'):
                for i in types.get('allOf'):
                    if '$ref' in i:
                        return self.ref_parse(i, final=True)
        elif 'string' in types:
            return 'random_str ' + generate_str_and_return(5)
        elif 'bool' in types:
            return random.choice([True, False])
        elif types == 'date-time':
            return self.fake.date_time().strftime(self.date_time_format)
        elif 'array' in types:
            return [generate_str_and_return(5) for _ in range(2)]

    def generate_x_qa_info(self, item):
        """
        Генерирует данные для x-qa-info

        :param item: str
        """
        if 'skip' in item:
            return 'skip'
        elif 'guid' in item:
            return str(uuid.uuid4())
        elif 'handler' in item:
            temp = random.choice(self.get_api_request(item[-1]))
            return temp['id']
        elif 'string_json' in item:
            return "{\"%s\": \"%s\"}" % (self.fake.word(), self.fake.word())

    def get_api_request(self, handler):
        """
        Делает запрос через API клиент

        :param handler: хендлер для запроса
        :return: dict
        """
        if not self.api_client:
            raise Exception("Проблема с API клиентом у генератора")
        else:
            allowed_codes = [200]; retry_attempts = 0; retry_delay = 1
            url = self.stand_url + handler
            logger.info(url)
            with self.api_client.session():
                response = self.api_client.get(url=url, verify=False, allowed_codes=allowed_codes,
                                    retry_attempts=retry_attempts, retry_delay=retry_delay)
            return response.json()


if __name__ == "__main__":
    from tools.utils import timeit

    @timeit
    def start():
        hand = '/api/v1/inbox'
        url = 'https://sp-ipc-qa-auto.rd.ptsecurity.ru'
        login = 'Administrator'
        password = 'P@ssw0rd'
        gen = PlatformJsonGenerator(stand_url=url, login=login, password=password)
        res = gen.give_json(hand)
        import json
        with open('./logs/sos3.json', 'w') as f:
            json.dump(res, f, ensure_ascii=False)
        print(res)
    start()
