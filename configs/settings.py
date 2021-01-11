#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################################################
# settings for remote driver Grid/selenoid
url_to_selenoid = "{}.rd.ptsecurity.ru"
selenoid_driver_capabilities = {
    "firefox": {"browserName": "firefox",
                "version": "68.0",
                "enableVNC": True,
                "enableVideo": True,
                "videoName": None,
                },
    "chrome": {"browserName": "chrome",
               "version": "81.0",
               "enableVNC": True,
               "enableVideo": True,
               "videoName": None,
               'timeZone': "Europe/Moscow",
               "env": ["LANG=ru_RU.UTF-8", "LANGUAGE=ru:en", "LC_ALL=ru_RU.UTF-8"],
               'goog:chromeOptions': {'extensions': [], 'args': ['--ignore-certificate-errors']}

               }
}
#########################################################

#########################################################
# настройки для групп стендов

prometheus_api_url = 'http://dom_name:9090/api/v1/'

stands = {
        'DOM_NAME_ONE.RU': {
                            'URL': 'https://dom_name_one',
                            'CRED': {'LOGIN': 'login', 'PASSWORD': 'password'},
                            'POSTGRES': 'dom_name_one:5432',
                            'RABBIT': 'dom_name_one:15672',
                            'INTEGRATION_URL': 'https://dom_name_integration:3334',
                            'ONLY_ADMIN_CRED': {'LOGIN': 'login', 'PASSWORD': 'password'},
                            'GROUP_ID': '13c9ae00-9280-0001-0000-000000000005'
                            },
        'DOM_NAME_TWO.RU': {
                            'URL': 'https://dom_name_two',
                            'CRED': {'LOGIN': 'login', 'PASSWORD': 'password'},
                            'POSTGRES': 'dom_name_one:5432',
                            'RABBIT': 'dom_name_one:15672',
                            'INTEGRATION_URL': 'https://dom_name_integration:3334',
                            'ONLY_ADMIN_CRED': {'LOGIN': 'login', 'PASSWORD': 'password'},
                            'GROUP_ID': '13c9ae00-9280-0001-0000-000000000005'
                        },
}

#########################################################

