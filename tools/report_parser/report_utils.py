#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import xml.etree.ElementTree as ET
import yaml
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

ROOT_DIR = root_dir = Path(os.path.abspath(os.getcwd()))


def load_xml_file(file_name):
    """
    Загрузка xml-файла с результатами прогона в объект ElementTree

    :param file_name: имя загружаемого xml-файла
    :return: объект ElementTree с данными прогона
    """
    abs_file_path = Path(os.path.join(ROOT_DIR, 'logs', f'{file_name}.xml'))
    p = Path(abs_file_path)
    if p.exists():
        abs_path = p.absolute()
        tree = ET.parse(abs_path)
        root = tree.getroot()
        return root
    else:
        raise FileNotFoundError(f"Error! File not exists: '{abs_file_path}'")


def find_xml_elem_by_tag(xml_root, tag_expression):
    """
    Поиск элементов в xml с заданными тегами

    :param xml_root: объект ElementTree с данными прогона
    :param tag_expression: строка с адресом тега относительно корня
    :return: список найденных элементов xml
    """
    xml_elements = xml_root.findall(tag_expression)
    if xml_elements:
        return xml_elements
    else:
        raise Exception(f"Error! Not found '{tag_expression}' in xml-file")


def parse_test_suite_data(xml_root):
    """
    Вспомогательная ф-ия для 'parse_test_result'. Парсинг общей информации о прогоне из xml

    :param xml_root: объект ElementTree с данными прогона
    :return: словарь с общей информацией о прогоне
    """
    testsuite = find_xml_elem_by_tag(xml_root, './testsuite')
    testrun_dict = {}
    testrun_dict['date'] = datetime.strptime(testsuite[0].attrib['timestamp'],
                                             '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')
    testrun_dict['quantity'] = int(testsuite[0].attrib['tests'])
    testrun_dict['failed'] = int(testsuite[0].attrib['failures'])
    testrun_dict['errors'] = int(testsuite[0].attrib['errors'])
    testrun_dict['skipped'] = int(testsuite[0].attrib['skipped'])
    return testrun_dict


def parse_test_case_data(xml_root):
    """
    Вспомогательная ф-ия для 'parse_test_result'. Парсинг информации о тест-кейсах из xml

    :param xml_root: объект ElementTree с данными прогона
    :return: словарь с информацией о прогоне тест-кейсов
    """
    test_data = {}
    testcases = find_xml_elem_by_tag(xml_root, './/testcase')
    for testcase in testcases:
        test_classname = testcase.attrib['classname'].rpartition('.')[-1]
        for test_tag in testcase:
            if test_tag.tag != 'system-out':
                if not test_data.get(test_classname):
                    test_data[test_classname] = {}
                if not test_data[test_classname].get(testcase.attrib['name']):
                    test_data[test_classname][testcase.attrib['name']] = {}
                if test_tag.attrib.get('message') and test_tag.tag == 'skipped':
                    if test_tag.attrib.get('message'):
                        if test_tag.attrib.get('type'):
                            skip_type = test_tag.attrib.get('type').rpartition('.')[-1]
                            test_data[test_classname][testcase.attrib['name']][skip_type] = test_tag.attrib.get(
                                'message')
                        else:
                            test_data[test_classname][testcase.attrib['name']][test_tag.tag] = test_tag.attrib.get(
                                'message')
                if test_tag.text and test_tag.tag != 'skipped':
                    if not test_data[test_classname][testcase.attrib['name']].get(test_tag.tag):
                        test_data[test_classname][testcase.attrib['name']][test_tag.tag] = {}
                    test_data[test_classname][testcase.attrib['name']][test_tag.tag]= test_tag.text
    for key, value in test_data.copy().items():
        if not value:
            del test_data[key]
    return test_data


def parse_test_result(xml_root):
    """
    Парсинг результатов прогона из xml

    :param xml_root: объект ElementTree с данными прогона
    :return: словари с общей информацией о прогоне и информацией о прогоне тест-кейсов
    """
    test_suite_dict = parse_test_suite_data(xml_root)
    test_case_dict = parse_test_case_data(xml_root)
    return test_suite_dict, test_case_dict


def concat_testsuite_data(suite_data_list):
    """
    Ф-ия объединяет словари из списка для получения единого словаря с информацией о прогоне

    :param suite_data_list: список словарей с общей информацией о нескольких прогонах
    :return: словарь, объединяющий в себе общую информацию о нескольких прогонах
    """
    if len(suite_data_list) == 1:
        return suite_data_list[0]
    else:
        sum_dict = {
            'date': '',
            'quantity': 0,
            'failed': 0,
            'errors': 0,
            'skipped': 0
        }
        for suite_data in suite_data_list:
            sum_dict['date'] = suite_data['date']
            sum_dict['quantity'] = sum_dict['quantity'] + suite_data['quantity']
            sum_dict['failed'] = sum_dict['failed'] + suite_data['failed']
            sum_dict['errors'] = sum_dict['errors'] + suite_data['errors']
            sum_dict['skipped'] = sum_dict['skipped'] + suite_data['skipped']
        return sum_dict


def collect_testsuite_info(suite_dict):
    """
    Ф-ия собирает текст из словаря с общей информацией о прогоне

    :param suite_dict: словарь с общими данными о прогоне
    :return: текст с общими данными о прогоне
    """
    report_text = f"Дата прогона: {suite_dict['date']}\n" \
                  f"Упавшие тесты: {suite_dict['failed']}/{suite_dict['quantity']}\n" \
                  f"Ошибки в тестах: {suite_dict['errors']}/{suite_dict['quantity']}\n" \
                  f"Пропущенные тесты: {suite_dict['skipped']}/{suite_dict['quantity']}"
    return report_text


def collect_dict_for_txt_report(testrun_name, suite_dict, testcase_dict):
    """
    Ф-ия собирает словарь с полной информацией о прогоне

    :param testrun_name: название прогона
    :param suite_dict: словарь с общей информацией о прогоне
    :param testcase_dict: словарь с информацией о прогоне тест-кейсов
    :return: словарь с информацией о прогоне
    """
    if testcase_dict:
        report_dict = {
            testrun_name:
                {
                    'Общая информация': collect_testsuite_info(suite_dict),
                    'Тест-кейсы': testcase_dict
                }
        }
    else:
        report_dict = {
            testrun_name:
                {
                    'Общая информация': collect_testsuite_info(suite_dict)
                }
        }
    return report_dict


def save_yaml_file(run_name, test_suite_data, test_case_data):
    """
    Сохранение словаря в файл формата txt в папку logs

    :param run_name: название прогона
    :param test_suite_data: словарь с краткой информацией о прогоне
    :param test_case_data: словарь с информацией о прохождении тест-кейсов
    """
    input_dict = collect_dict_for_txt_report(run_name, test_suite_data, test_case_data)
    abs_file_path = Path(os.path.join(ROOT_DIR, 'logs', 'testrun_report.txt'))
    with open(abs_file_path, 'w', encoding='cp1251') as res_file:
        yaml.dump(input_dict, res_file, default_flow_style=False, allow_unicode=True)


def save_html_file(run_name, test_suite_data, test_case_data):
    """
    Сохранение словаря в файл формата html в папку logs

    :param run_name: название прогона
    :param test_suite_data: словарь с краткой информацией о прогоне
    :param test_case_data: словарь с информацией о прохождении тест-кейсов
    """
    abs_file_path = Path(os.path.join(ROOT_DIR, 'logs', 'testrun_report.html'))
    template_path = str(Path(os.path.join(os.path.dirname(__file__))))
    env = Environment(loader=FileSystemLoader(template_path))
    report_temp = env.get_template('report_template.html')
    report_html = report_temp.render(testrun_name=run_name, testrun_info=collect_testsuite_info(test_suite_data),
                                     test_dict=test_case_data)
    with open(abs_file_path, 'w') as html_file:
        html_file.write(report_html)
