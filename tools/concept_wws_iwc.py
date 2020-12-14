#!/usr/bin/env python
# -*- coding: utf-8 -*-

__title__ = 'The concept of what was sent is what came'

import logging
from dateutil import parser

log = logging.getLogger(__name__)
asserts_dict = dict()


def check_isdate(string):
    """
    проверяет строку на возможность преобразовать ее в datetime, при ошибке пишет в лог инфу

    :param string: строка, которую пытаемся преобразовать в datetime
    :return: datetime
    """

    try:
        return parser.parse(string)
    except (TypeError, OverflowError):
        log.debug(f"Эта строка не дата {string}")


def collecting_assertions_in_list(first, second, key):
    """
    Функция проверяет значения first, second на равенство и при ошибке возвращает дикт, при положительном результате
    вернет пустой словарь.
    """
    if first != second:
        return {key: {'expected': first, 'actual': second}}
    else:
        return {}


# Функция для проверки концепции: что отправили на POST, то пришло на GET
def _universal_comparison_function_for_post_keys(sent, incoming, alert=None, for_skip=None, need_assert=True,
                                                 **for_change):
    """"""

    if not for_skip:
        for_skip = list()
    if for_skip and not isinstance(for_skip, list):
        for_skip = list(for_skip)
    if isinstance(sent, dict) and isinstance(incoming, dict):
        for key, value in sent.items():
            expected, actual = sent.get(key), incoming.get(key)
            if actual is None and expected is not None:
                asserts_dict.update({key: {'expected': expected, 'actual': actual}})
            elif key in for_change.keys():
                new_key = for_change[key]
                log.info(f'Заменен ключ {key} на {new_key}. Значения соответственно {expected} и {incoming[new_key]}')
                asserts_dict.update(collecting_assertions_in_list(expected, actual, key))
            elif key in for_skip:
                continue
            elif isinstance(value, list):
                index = 0
                for i in value:
                    if isinstance(i, dict):
                        _universal_comparison_function_for_post_keys(expected[index], actual[index], alert, for_skip,
                                                                     need_assert, **for_change)
                    else:
                        asserts_dict.update(collecting_assertions_in_list(expected[index], actual[index], key))
                    index += 1
            elif isinstance(value, dict):
                _universal_comparison_function_for_post_keys(expected, actual, alert, for_skip, need_assert,
                                                             **for_change)
            elif check_isdate(expected):
                log.info(f'Сравнивается даты {key}. Значения соответственно {expected} и {actual}')
                asserts_dict.update(collecting_assertions_in_list(check_isdate(expected).timestamp(),
                                                                  check_isdate(actual).timestamp(), key))
            else:
                log.info(f'Сравнивается ключи {key}. Значения соответственно {expected} и {actual}')
                asserts_dict.update(collecting_assertions_in_list(expected, actual, key))
    else:
        log.error("Значения в json'нах не равны. Ожидаемый {}, фактическтий {}".format(sent, incoming))
        asserts_dict.update(collecting_assertions_in_list(sent, incoming, key='error_dicts'))
    if need_assert:
        assert not asserts_dict, "Проблемы в сравнении json' ов, проблемные ключи: {}".format(str(asserts_dict))
    else:
        return asserts_dict


def universal_comparison_function_for_post_keys(sent, incoming, alert=None, for_skip=None, need_assert=True,
                                                **for_change):
    """"""
    asserts_dict.clear()
    temp_dict = _universal_comparison_function_for_post_keys(sent, incoming, alert, for_skip, need_assert,
                                                             **for_change)
    return temp_dict


if __name__ == "__main__":
    import datetime

    first = {'recurse': {'a': {'b': 'd'}, 'test': 'g', 'y': {'last': {'x': 'y'}}},
             'date': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00'),
             'list': [{'first': {'s': {'ddd': 're'},
                                 'ne': 'da',
                                 'rrrr': {'last': {'x': 'y'}}
                                 }},
                      'sec'],
             'str': 'string'
             }
    second = {'recurse': {'a': {'b': '1'}, 'netest': 'g', 'y': {'last': {'x': 'y'}}},
              'date': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00'),
              'list': [{'first': {'s': {'ddd': 're'},
                                  # 'ne': 'da',
                                  'rrrr': {'last': {'x': 'y'}}
                                  }},
                       'second'],
              'str': 'string'
              }
    print(universal_comparison_function_for_post_keys(first, second, need_assert=False))
    print(universal_comparison_function_for_post_keys(first, second, for_skip=['ne', 'test', 'b', 'list'],
                                                      need_assert=False))
    print(universal_comparison_function_for_post_keys(first, second, for_skip=['ne', 'test'], need_assert=False))
    print(universal_comparison_function_for_post_keys(first, second, need_assert=False, for_skip=['b']))
