# coding=utf-8
import glob
import os
import json
import logging
import urllib3
import random
import yaml
import zipfile
import io
import shutil
from time import sleep
from jsondiff import diff
from pathlib import Path
from dotted.collection import DottedCollection
from jsonpath import jsonpath
from configs.modify_data import test_modify_data
from dateutil import parser
import ruamel.yaml

logger = logging.getLogger(__name__)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger('chardet.charsetprober').setLevel(logging.WARNING)

TEST_ROOT_DIR = Path(__file__).parent.parent.absolute()
TEST_ARTIFACTS_DIR = str(TEST_ROOT_DIR / '_tests_artifacts')
TESTDATA_DIR = str(TEST_ROOT_DIR / '_testdata')


def current_timestamp():
    """
    Метод получения текущей даты в секундах

    "return: текущая дата в секундах
    """
    current_date = datetime.now()
    return datetime.timestamp(current_date)


def now_timestamp(date_format='%Y_%m_%d_%H_%M_%S'):
    """ получить текущее время в формате date_format """
    return datetime.now().strftime(date_format)


def transform_date_to_timestamp(date):
    return parser.parse(date).timestamp()


def generate_str_and_return(str_len=30):
    return ''.join([random.choice(list('1234567890qwertypasdfghjklzxcvbnmQWERTYUIKLZXCVBNM'))
                    for _ in range(str_len)])


def init_logging():
    full_path = os.getcwd() + r'/logs'
    if os.path.isdir(full_path) is False:
        os.mkdir(full_path)

    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(message)s (%(filename)s:%(lineno)d; %(name)s) %(processName)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler(r'{}/AutoTests-{}.log'.format(full_path, datetime.now().strftime("%d%m%Y")),
                                encoding='utf-8')
        ]
    )
    logger = logging.getLogger(__name__)
    return logger


def sort_dict(input_dict):
    """ отсортировать входящий словарь """
    result = dict(sorted(input_dict.items()))
    return result


def random_choice(list_params):
    return random.choice(list_params)


def yaml_loader(str_text):
    try:
        if isinstance(str_text, str):
            return yaml.load(str_text, Loader=yaml.Loader)
        else:
            return str_text
    except Exception:
        raise Exception("Error! Check YAML syntax in:\n{}".format(str_text))


def extract_number(some_str):
    """ Get list of integer digits in str

    :param some_str: some input string
    :return: list of digits in str, None if no digits
    """
    digits = list(filter(lambda x: x.isdigit(), some_str))
    if digits:
        return list(map(int, digits))
    else:
        return


def extract_domain_from_url(url):
    """
    Функция преобразует url в домен

    :param url: url адрес
    :return: домен, полученный из входного url
    """
    cut_http = url.split('//')
    if cut_http[0].find('http', 0, 4) == -1:
        cut_port = cut_http[0].split(':')
    else:
        cut_port = cut_http[1].split(':')
    return cut_port[0]


def byte_to_Gb(number):
    """
    Функция преобразует байты в гигобайты

    :param number: число для преобразования в байтах
    :return: преобразованное число в гигабайтах
    """
    number_Gb = float(number) / 1024 / 1024 / 1024
    return number_Gb


def to_fixed(number, digits=0):
    """
    Функция округляет вещественное число до определённого колличества знаков после запятой

    :param number: входное число для преобразования
    :param digits: колличество знаков после запятой
    :return: вещественное число, округлённое до указанного знака после запятой
    """
    number = float(number)
    return float('{:.{}f}'.format(number, digits))


def get_dict_value(search_dict, element_path):
    search_element = element_path.partition('.')
    if search_element[2] != "":
        if isinstance(search_dict.get(search_element[0]), dict):
            return get_dict_value(search_dict.get(search_element[0]),
                                  search_element[2])
        elif isinstance(search_dict.get(search_element[0]), list):
            list_search = search_element[2].partition('.')
            try:
                index = int(list_search[0][1])
            except Exception:
                raise Exception("Failed search by element path '{}'.\n"
                                "Index of element in list must be int"
                                .format(element_path))
            return get_dict_value(search_dict.get(search_element[0])[index], list_search[2])
    else:
        return search_dict.get(search_element[0])


def del_by_path(all_dict, all_del_path):
    """
    Удаление поля в JSON по заданному пути, модифицирует переданный json

    :param all_dict: исходный JSON
    :param all_del_path: упорядоченный список элементов до поля, которое нужно удалить
    """
    all_del_path = [int(x) if isinstance(x, str) and x.isdigit() else x for x in all_del_path]
    if len(all_del_path) > 1:
        empty = del_by_path(all_dict[all_del_path[0]], all_del_path[1:])
        if empty:
            del all_dict[all_del_path[0]]
    else:
        del all_dict[all_del_path[0]]
    return len(all_dict) == 0


def user_assertion(actual_result, expected_result, assert_operator, entity, entity_id):
    if assert_operator == '=' or assert_operator == '==':
        if actual_result != expected_result:
            return "{} {}: actual result '{}' should be equal '{}'".format(entity, entity_id,
                                                                           actual_result, expected_result)
    elif assert_operator == '!=' or assert_operator == '<>':
        if actual_result == expected_result:
            return "{} {}: actual result '{}' should be not equal '{}'".format(entity, entity_id,
                                                                               actual_result, expected_result)
    elif assert_operator == '>':
        if actual_result <= expected_result:
            return "{} {}: actual result '{}' should be > '{}'".format(entity, entity_id,
                                                                       actual_result, expected_result)
    elif assert_operator == '<':
        if actual_result > expected_result:
            return "{} {}: actual result '{}' should be < '{}'".format(entity, entity_id, actual_result,
                                                                       expected_result)
    elif assert_operator == 'in':
        if actual_result not in expected_result:
            return "{} {}: actual result '{}' not in '{}'".format(entity, entity_id, actual_result,
                                                                  expected_result)
    elif assert_operator == 'not in':
        if actual_result in expected_result:
            return "{} {}: actual result '{}' in '{}'".format(entity, entity_id, actual_result,
                                                              expected_result)


def get_time_delta(time_start, time_stop, str_time_format='%Y-%m-%d %H:%M:%S.%f'):
    if not isinstance(time_start, datetime):
        time_start = datetime.strptime(time_start, str_time_format)
    if not isinstance(time_stop, datetime):
        time_stop = datetime.strptime(time_stop, str_time_format)
    delta_time = time_stop - time_start

    return delta_time.total_seconds()


def convert_datetime(value, str_time_format='%d.%m.%Y %H:%M:%S'):
    if isinstance(value, datetime):
        return value.strftime(str_time_format)
    else:
        return value


def zip_save_and_extract(test_name, data, dir_name):
    test_artifact_path = TEST_ARTIFACTS_DIR + r'/{}/{}'.format(test_name, dir_name)
    if not os.path.exists(TEST_ARTIFACTS_DIR):
        os.makedirs(test_artifact_path)
    zip_archive = zipfile.ZipFile(io.BytesIO(data))
    zip_archive.extractall(test_artifact_path)
    return test_artifact_path


def dir_to_zip(path_to_dir):
    if os.path.exists(path_to_dir):
        shutil.make_archive(path_to_dir, 'zip', path_to_dir)
        archive_name = "{}.zip".format(os.path.split(path_to_dir)[1])
        path_to_zip = os.path.join(os.path.split(path_to_dir)[0], "{}.zip".format(os.path.split(path_to_dir)[1]))
        with open(path_to_zip, 'rb') as zip_archive:
            bin_archive = zip_archive.read()
        sizeof = os.path.getsize(path_to_zip)
        return bin_archive, archive_name, sizeof


def copy_dirs(path_to_dir, dir_to_copy):
    if os.path.exists(path_to_dir):
        main_path = os.path.split(path_to_dir)[0]
        path_to_copy_dir = os.path.join(main_path, dir_to_copy)
        if not os.path.exists(path_to_copy_dir):
            shutil.copytree(path_to_dir, path_to_copy_dir)
        return path_to_copy_dir


def read_yaml_from_file(path_to_file, file_name):
    if os.path.exists(path_to_file):
        full_path_to_file = os.path.join(path_to_file, file_name)
        with open(full_path_to_file, 'r', encoding='utf-8') as f:
            file_content = yaml.load(f, Loader=yaml.Loader)
        if file_content:
            return file_content
        else:
            raise Exception("Error! File '{}' is empty".format(full_path_to_file))


def write_yaml_to_file(path_to_file, file_name, data):
    """
    Функция записи текста в файл в формате yaml

    :param path_to_file: директория с файлом
    :param file_name: название файла
    :param data: текст
    :return: полный путь до файла
    """
    if os.path.exists(path_to_file):
        full_path_to_file = os.path.join(path_to_file, file_name)
        with open(full_path_to_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    return full_path_to_file


def read_yaml_from_file_with_ruyaml(path_to_file, file_name):
    if os.path.exists(path_to_file):
        ru_yaml = ruamel.yaml.YAML()
        ru_yaml.preserve_quotes = True
        full_path_to_file = os.path.join(path_to_file, file_name)
        with open(full_path_to_file, 'r', encoding='utf-8') as f:
            file_content = ru_yaml.load(f)
        if file_content:
            return file_content
        else:
            raise Exception("Error! File '{}' is empty".format(full_path_to_file))


def write_yaml_to_file_with_ruyaml(path_to_file, file_name, data):
    if os.path.exists(path_to_file):
        ru_yaml = ruamel.yaml.YAML()
        ru_yaml.preserve_quotes = True
        full_path_to_file = os.path.join(path_to_file, file_name)
        with open(full_path_to_file, 'wb') as f:
            ru_yaml.dump(data, f)


def copy_testdata_file_to_dir(test_name, configfile_name, dir_path):
    test_name = test_name.partition('[')[0]
    path_to_testdata = os.path.join(TESTDATA_DIR, os.path.join(test_name, configfile_name))
    shutil.copy(path_to_testdata, dir_path)


def remove_file(file_name):
    if os.path.isfile(file_name):
        os.remove(file_name)
    print("\nDELETE FILE: ", file_name)


def check_file_size(file_name, timeout=5, delete=False):
    """ Функция принимает путь до файла и проверяет его наличие и возвращает размер

    :param file_name: путь до файла
    :type file_name: str
    :param timeout: таймаут ожидания файл, необходим если проверяется скачивание файла
    :type timeout: int
    :param delete: при флаге True проверяет файл на наличие и удаляет, если файл существует
    :type delete: bool
    :return: размер файла
    :rtype: int
    """
    if delete:
        remove_file(file_name)
    while timeout > 0:
        if not os.path.isfile(file_name):
            timeout -= 1
            print('timeout for file download: ', timeout)
            sleep(1)
            continue
        return os.path.getsize(file_name)


def convert_date_to_rus(input_date, date_format="%Y-%m-%dT%H:%M:%SZ",
                        time_delta=3, rus_date_format="{} {}"):
    """ Функция конвертирует дату в русскую локаль, н-р, 22 апреля

    :param input_date: дата в строковом формате
    :param date_format: формат переданной даты
    :param time_delta: сдвиг времени в часах
    :param rus_date_format: формат получаемой даты
    :return: дата в виде число месяц на русском если задан параметр rus_date_format
    """
    utc_offset = timedelta(hours=time_delta)
    day = (datetime.strptime(input_date, date_format) + utc_offset).strftime("%e").strip()
    month = (datetime.strptime(input_date, date_format) + utc_offset).strftime("%m").strip()
    months = {'01': 'января', '02': 'февраля', '03': 'марта', '04': 'апреля', '05': 'мая', '06': 'июня',  '07': 'июля',
              '08': 'августа', '09': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря'}
    year = (datetime.strptime(input_date, date_format) + utc_offset).strftime("%Y").strip()
    time_hour = (datetime.strptime(input_date, date_format) + utc_offset).strftime("%H").strip()
    time_min = (datetime.strptime(input_date, date_format) + utc_offset).strftime("%M").strip()
    time_sec = (datetime.strptime(input_date, date_format) + utc_offset).strftime("%S").strip()
    if rus_date_format:
        rus_date = rus_date_format.format(day, months[month], year, time_hour, time_min, time_sec)
        return rus_date
    else:
        return day, months[month], year, time_hour, time_min, time_sec


def convert_date_with_time_to_rus(input_date, date_format="%Y-%m-%dT%H:%M:%SZ"):
    """ Функция конвертирует дату и время в русскую локаль, н-р, 22 апреля, 10:00

    :param input_date: дата в строковом формате
    :param date_format: формат переданной даты
    :return: дата и время на русском
    """
    rus_date = convert_date_to_rus(input_date, date_format)
    utc_offset = timedelta(hours=3)
    time_value = (datetime.strptime(input_date, date_format) + utc_offset).strftime("%H:%M").strip()
    return f'{rus_date}, {time_value}'


def convert_date_to_format(input_date, input_format="%Y-%m-%dT%H:%M:%SZ", output_format="%Y-%m-%dT%H:%M:%S.000Z"):
    """ функция преобразовывает дату из input_format в output_format """
    return datetime.strptime(input_date, input_format).strftime(output_format).strip()


def convert_date_to_inc_output(input_date, date_format="%Y-%m-%dT%H:%M:%SZ"):
    """ функция преобразовывает переданную дату input_date в формате date_format во время, прошедшее от текущего
    если оно больше суток, то отображается просто дата в русском формате """
    now = datetime.utcnow()
    value = datetime.strptime(input_date, date_format)
    diff = now - value
    if diff.days > 0:
        return convert_date_to_rus(input_date)
    else:
        if diff.seconds < 60:
            return "{} секунд назад".format(diff.seconds)
        elif 60 <= diff.seconds < 3600:
            return "{} минут назад".format(diff.seconds//60)
        else:
            return datetime.strptime(input_date, date_format).strftime('%H:%M')


def compare_dictionaries(dict1, dict2):
    """ функция сравнивает два словаря. для вложенных словарей рекурсивная проверка """
    if dict1 is None or dict2 is None:
        return False
    if type(dict1) is not dict or type(dict2) is not dict:
        return False
    shared_keys = set(dict2.keys()) & set(dict2.keys())
    if not (len(shared_keys) == len(dict1.keys()) and len(shared_keys) == len(dict2.keys())):
        return False
    dicts_are_equal = True
    for key in dict1.keys():
        if type(dict1[key]) is dict:
            dicts_are_equal = dicts_are_equal and compare_dictionaries(dict1[key], dict2[key])
        else:
            dicts_are_equal = dicts_are_equal and (dict1[key] == dict2[key])
    return dicts_are_equal


def check_file_content(file_path, expected_content):
    """функция принимает путь до файла и проверяет соответствие его содержимого ожидаемому
    если файл загружается, необходимо сначала вызвать метод wait_for_file_download, который дождется появления файла

    :param file_path: путь до файла
    :param expected_content: ожидаемое содержимое файла
    :return: возвращает True, если содержимое файла соответствует expected_content
    """
    with open(file_path, 'r', encoding='utf8') as f:
        content = f.read()
    # если первым символом пишется признак кодировки (UTF with BOM, код 65279), его удаляем
    if ord(content[0]) == 65279:
        content = content[1:]
    if ord(expected_content[0]) == 65279:
        expected_content = expected_content[1:]
    return content == expected_content


def check_json_file_content(file_path, send_content):
    """функция принимает путь до JSON файла и проверяет соответствие его содержимого ожидаемому словарю
    если файл загружается, необходимо сначала вызвать метод wait_for_file_download, который дождется появления файла

    :param file_path: путь до файла
    :param send_content: ожидаемое содержимое файла (dict)

    возвращает True, если содержимое файла соответствует expected_content
    """
    with open(file_path, 'r', encoding='utf8') as json_file:
        data = json.load(json_file)
    import allure
    allure.attach(json.dumps(send_content, indent=2, ensure_ascii=False), 'Отправленная по API ЭФ инцидента',
                  allure.attachment_type.JSON)
    allure.attach(json.dumps(data, indent=2, ensure_ascii=False), 'Скачанная через UI ЭФ инцидента',
                  allure.attachment_type.JSON)

    equal_dict_flag = compare_dictionaries(send_content, data)

    if not equal_dict_flag:
        diff_dicts = diff(send_content, data, dump=True)
        allure.attach(
            json.dumps(json.loads(diff_dicts), indent=2, ensure_ascii=False),
            'Разница между отправленной по API и скачанной через UI ЭФ инцидента',
            allure.attachment_type.JSON)
    return equal_dict_flag


def wait_for_file_download(file_path, timeout=15, delete=False):
    """функция ждет, пока файл скачается

    :param file_path: путь до файла
    :type file_path: str
    :param timeout: таймаут ожидания файла
    :type timeout: int
    :param delete: при флаге True проверяет файл на наличие и удаляет, если файл существует
    :type delete: bool
    """
    if delete:
        remove_file(file_path)
    while timeout > 0:
        if not os.path.isfile(file_path):
            timeout -= 1
            print('timeout for file download: ', timeout)
            sleep(1)
        else:
            break
    if not os.path.isfile(file_path):
        print(f"Содержание папки загрузки: {os.listdir(path=os.path.dirname(file_path))}")
        raise FileExistsError(f'Файл {file_path} не найден')


def add_key_to_json(input_json, path, new_key):
    dot_json = DottedCollection.factory(input_json)
    splitted_full_path = jsonpath(input_json, path, result_type='IPATH')
    if splitted_full_path:
        for one_path in splitted_full_path:
            dot_path = ".".join(one_path)
            dot_json[dot_path][new_key] = None
    else:
        raise Exception("Error! Not found JSON-path:\n{}".format("\n".join(path)))
    return dot_json.to_python()


def check_jpath_exist(input_json, path):
    splitted_full_path = jsonpath(input_json, path, result_type='IPATH')
    if splitted_full_path:
        return True
    else:
        return False


def get_jpath_value(input_json, path):
    dot_json = DottedCollection.factory(input_json)
    splitted_full_path = jsonpath(input_json, path, result_type='IPATH')
    if splitted_full_path:
        for one_path in splitted_full_path:
            dot_path = ".".join(one_path)
            return dot_json[dot_path]
    else:
        raise Exception("Error! Not found JSON-path:\n{}".format("\n".join(path)))


def find_value_in_system_dict(dict_name, search_by_field, value_in_field, return_field):
    """
    :param dict_name: название словаря в котором планируется поиск
    :param search_by_field: поле, по которому будет осуществляться поиск в словаре
    :param value_in_field: значение в поле, по которому будет осуществляться поиск в словаре
    :param return_field: имя поля, значение из которого нужно вернуть
    :return: значение поля return_field
    """
    for item in test_modify_data['dicts'][dict_name]:
        if item[search_by_field] == value_in_field:
            return item[return_field]


def get_params_values(params_list, input_json):
    """ Заполнение словаря с параметрами значениями из JSON-словаря

    :param params_list: список параметров в формате JSON-path
    :param input_json: JSON, в котором нужно взять значения
    :return: словарь формата {JSON-path: значение}
    """
    params_dict = {}
    for param in params_list:
        params_dict[param] = get_jpath_value(input_json, param)
    return params_dict


def search_dir_recursive(path, dir_name, one_result=True):
    """
    Ищет папку или файл по имени рекурсивно

    :param path: путь от куда начинать искать
    :param dir_name: шаблон по которому искать
    :param one_result: флаг, True если уверены, что результат должен быть один, плюс удаляет результаты в скрытых папках
        такие как ./.git и т.д. если результатов должно быть несколько нужно выставить в False
    :return: возвращает список
    """
    result = [y for x in os.walk(path) for y in glob.glob(os.path.join(x[0], dir_name))]
    if one_result:
        if len(result) > 1:
            for i in range(len(result)):
                if '\\.' in result[i] or '/.' in result[i]:
                    result.pop(i)
                    return result[-1]
        return result[-1]
    return result


def merge_dicts(base, update, override=False):
    """
    Ф-ия для слияния словарей

    :param base: базовый словарь
    :param update: словарь, который должен влиться в базовый
    :param override: True, если нужно переопределить значения ключей при слиянии
    :return: результат слияния словарей
    """
    for key, value in update.items():
        if key not in base:
            base[key] = value
            continue
        if isinstance(value, dict):
            merge_dicts(base[key] or {}, value, override)
        elif isinstance(value, list):
            assert isinstance(base[key], list)
            base[key] = base[key] + value
        elif override:
            base[key] = value
    return base


def timeit(function):
    """
    Декотратор для замера времени

    :param function: фукнция для декарирования
    :return: результат выполнения декортатор
    """
    def decor(*args, **kwargs):
        start = datetime.now()
        result = function(*args, **kwargs)
        print("function '%s' took time: " % function.__name__.upper(), datetime.now() - start)
        return result
    return decor


def is_property_appear_in_json(incoming_json, prop):
    """
    Метод проверки присутствия свойства внутри json

    :param incoming_json: json на проверку
    :param prop: название свойства
    :return: словарь ошибок
    """
    err_dict = {}
    if prop in incoming_json:
        if incoming_json[prop]:
            return err_dict
        else:
            logger.info(f"Waiting for property {prop} is filled in {incoming_json['id']}")
            err_dict[prop] = 'must not be empty'
    else:
        logger.info(f"Waiting for property {prop} is appeared in {incoming_json['id']}")
        err_dict[prop] = 'does not exist'
    return err_dict


def read_file_for_attach_upload(file_path):
    """
    Чтение файла в бинарном формате для дальнейшей загрузки

    :param file_path: путь к файлу относительно директории проекта
    :return: содержимое файла в бинарном формате, имя файла, размер файла
    """
    if not file_path:
        file_name_list = ['Test_file.txt', 'bob.png', 'Doc_for_test.txt']
        path_to_file = os.path.join(TEST_ROOT_DIR, 'test_data', choice(file_name_list))
    else:
        path_to_file = os.getcwd() + file_path
    file_name = os.path.basename(path_to_file)
    file_size = os.path.getsize(path_to_file)
    with open(path_to_file, 'rb') as test_file:
        file_obj = test_file.read()
    return file_name, file_obj, file_size


def create_time_period():
    """ Функция возвращает временной промежуток с рандомным началом и окончанием в текущем времени """
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    offset = timedelta(hours=randint(0, 24), minutes=randint(0, 60), days=randint(0, 365))
    past = (datetime.utcnow() - offset).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return [past, now]


def get_operator_name_for_ui(operator_data):
    """ Формирует строку с именем оператора, отображаемую в UI по правилу: имя фамилия (логин_оператора).
    На вход подаем данные оператора, их можно получить функцией sa_get_operator"""
    if not operator_data['firstName'] and not operator_data['lastName']:
        result = operator_data['login']
    else:
        result = operator_data['firstName'] + operator_data['lastName'] + f'({operator_data["login"]})'
    return result


def form_full_path_to_file(file_name):
    """
    Метод формирование полного пути внутри репозитория

    :param file_name: название файла внутри репозитория
    :return: полный путь
    """
    path = search_dir_recursive(os.environ.get("TESTS_ROOT_DIR"), file_name)
    return path

import hashlib
import string
import rstr
import requests
import tools.dictionary_variables as dv
import logging

from random import randint, choice
from datetime import datetime, timedelta
from uuid import uuid1
from base64 import b64decode, b64encode
from tools.utils import extract_domain_from_url

logger = logging.getLogger(__name__)

def inc_vector(): return choice(dv.vectorCode)


def antifraud_type(): return choice(dv.antifraudType)


def antifraud_type_2_1():
    return choice(dv.antifraudType2_1)


def utc_timestamp(date_format='%Y-%m-%dT%H:%M:%SZ'):
    return (datetime.utcnow() - timedelta(minutes=10)).strftime(date_format)


def new_source_id():
    return str(uuid1())


def is_list(item):
    return isinstance(item, list)


# ИНН ЮЛ
def inn_entity(): return inn(10)


# ИНН ИП
def inn_individual(): return inn(12)


# Проверка на контрольную сумму
def ctrl_sum(nums, n_type):
    ctrl_type = {
        'n2_12': [7, 2, 4, 10, 3, 5, 9, 4, 6, 8],
        'n1_12': [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8],
        'n1_10': [2, 4, 10, 3, 5, 9, 4, 6, 8],
    }
    n = 0
    l = ctrl_type[n_type]
    for i in range(0, len(l)):
        n += nums[i] * l[i]
    return n % 11 % 10


# СНИЛС
def snils():
    nums = [
        randint(1, 1) if x == 0
        else '-' if x == 3
        else '-' if x == 7
        else ' ' if x == 11
        else randint(0, 9)
        for x in range(0, 12)
        ]

    cont = (nums[10] * 1) + (nums[9] * 2) + (nums[8] * 3) + \
           (nums[6] * 4) + (nums[5] * 5) + (nums[4] * 6) + \
           (nums[2] * 7) + (nums[1] * 8) + (nums[0] * 9)

    if cont in (100, 101):
        cont = '00'

    elif cont > 101:
        cont = (cont % 101)
        if cont in (100, 101):
            cont = '00'
        elif cont < 10:
            cont = '0' + str(cont)

    elif cont < 10:
        cont = '0' + str(cont)

    nums.append(cont)
    return ''.join([str(x) for x in nums])


# Создание ИНН
def inn(l):
    nums = [
        randint(9, 9) if x == 0
        else randint(6, 6) if x == 1
        else randint(0, 9)
        for x in range(0, 9 if l == 10 else 10)
        ]

    if l == 10:
        n1 = ctrl_sum(nums, 'n1_10')
        nums.append(n1)

    elif l == 12:
        n2 = ctrl_sum(nums, 'n2_12')
        nums.append(n2)
        n1 = ctrl_sum(nums, 'n1_12')
        nums.append(n1)
    return ''.join([str(x) for x in nums])


def get_sha256_hash(value=None):
    if value is None:
        value = string_generator(1, 50)
    sha256_hash = hashlib.sha256()
    sha256_hash.update(value.encode('utf-8'))
    return sha256_hash.hexdigest()


def passport():
    nums = [
        ' ' if x == 2 or x == 5
        else randint(0, 9)
        for x in range(0, 12)
        ]
    return ''.join([str(x) for x in nums])


def phone_number(phone_code='+7'):
    # pattern: ^(\+?)([0-9]{1,3} ?([0-9]{3} ?){2}([0-9]{2} ?){2})$
    code = ''.join(phone_code.split())
    nums = [randint(0, 9) for x in range(0, 12 - len(code))]
    return code + ''.join([str(x) for x in nums])


def bank_account():
    nums = [
        randint(1, 5) if x == 0
        else randint(0, 9)
        for x in range(0, 20)
        ]
    return ''.join([str(x) for x in nums])


def payment_card(payee_bin):
    if len(payee_bin) == 6 or len(payee_bin) == 8:
        return payee_bin + ''.join(str(randint(0, 9)) for i in range(10))
    else:
        return payee_bin + ''.join(str(randint(0, 9)) for i in range(18 - len(payee_bin)))


def random_ipv4():
    return '.'.join(str(randint(0, 255)) for _ in range(4))


def random_ipv6():
    return ':'.join(''.join(choice(string.hexdigits.lower()) for _ in range(4)) for _ in range(8))


def random_email():
    length = randint(1, 64)
    local_part = ''.join(choice(string.ascii_letters + string.digits) for _ in range(length))
    return "{}@sptest.ru".format(local_part)


def random_domain():
    r_str = ''.join(choice(string.ascii_lowercase) for _ in range(randint(1, 15)))
    exten = ''.join(choice(string.ascii_lowercase) for _ in range(randint(2, 6)))
    return '{}.{}'.format(r_str, exten)


def random_url():
    return 'http://{0}.{1}/{2}/?{3}'.format(string.ascii_lowercase, rstr.letters(3), rstr.urlsafe(), rstr.urlsafe())


kirillic_letters = u"АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def string_generator(min_length, max_length, str_example=None):
    if min_length < 0:
        min_length = 1
    if max_length < 0:
        max_length = 100
    length = randint(min_length, max_length)
    if str_example is not None:
        r_str = ''.join(choice(kirillic_letters + string.ascii_letters + string.digits)
                        for _ in range(length - len(str_example) - 1))
        result = str_example + ' ' + r_str
        return result[0:max_length]
    else:
        return ''.join(choice(kirillic_letters + string.ascii_letters + string.digits) for _ in range(length))


def random_ip_or_domain():
    rand = choice((True, False))
    if rand:
        return random_ipv4()
    else:
        return random_domain()


def random_subnet():
    prefix = randint(0, 32)
    return "{}/{}".format(random_ipv4(), prefix)


# ОГРН ЮЛ
def random_ogrn():
    nums = [
        randint(1, 1) if x == 0
        else randint(0, 9)
        for x in range(0, 11)
    ]

    nums.append(ctrl_sum(nums, 'n1_12'))
    ogrn = (int(''.join(str(x) for x in nums)) % 11)
    nums.append(0) if ogrn == 10 else nums.append(ogrn)
    return ''.join([str(x) for x in nums])


def random_currency():
    return choice(dv.currency)


def random_base64():
    rand_str = string_generator(10, 1000)
    return b64encode(bytes(rand_str, encoding='utf-8')).decode('utf-8')


def size_in_bytes(b64string):
    decoded_str = b64decode(b64string)
    return len(decoded_str)


# Обернуть json-запроса
# def json_obj_wrapper(obj_type, obj_json):
#     result = {
#         "type": obj_type,
#         "data": obj_json
#     }
#     return result


# wrapper для 2.6.5
def json_obj_wrapper(obj_type, obj_json, version="1.0"):
    result = {
        "header":
            {
                "schemaType": obj_type,
                "schemaVersion": version,
                "sourceId": new_source_id()
            },
        obj_type: obj_json
    }
    return result


def exe_api_get_handler_request(url):
    try:
        logger.debug('GET {}'.format(url))
        response = requests.get(url)
    except ConnectionError:
        logger.error('Connection error {}!!!'.format(url))
        assert response, "Connection error {} occurred!".format(url)
    if response.status_code == 200:
        logger.info('Response code {} due request {}'.format(response.status_code, url))
        return response.json()
    else:
        logger.error('Unexpected status code {} {} !!!'.format(response.status_code, url))
        assert response, 'Unexpected status code {} {} !!!'.format(response.status_code, url)


def create_handler_url(url, handler):
    domain = extract_domain_from_url(url)
    addition_url = handler
    return 'http://' + domain + addition_url