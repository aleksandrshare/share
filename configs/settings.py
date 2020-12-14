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

#########################################################
inc_type_ext = ('malware', 'socialEngineering', 'vulnerabilities', 'spams',
             'controlCenters', 'phishingAttacks', 'prohibitedContents',
             'maliciousResources', 'other', 'sim')
inc_type_int = ('malware', 'socialEngineering', 'vulnerabilities', 'spams',
             'controlCenters', 'phishingAttacks', 'prohibitedContents',
             'maliciousResources', 'other', 'bruteForces', 'ddosAttacks',
             'scanPorts', 'trafficHijackAttacks', 'atmAttacks', 'changeContent')
#########################################################
# for json generator
paths_map = {
    'path/contract.yaml': ['/api/incidents', '/api/incidents/count', '/api/incidents/list',
                         '/api/incidents/{id}', '/api/incidents/{id}/status',
                         '/api/incidents/brief', '/api/incidents/{id}/actions',
                         '/api/incidents/{id}/recommendations', '/api/incidents/{id}/campaigns',
                         '/api/incidents/filters',
                         '/api/incidents/filters/{id}/values', '/api/incidents/projections/rebuild',
                         '/api/incidents/assign',
                         '/api/incidents/{id}/assign', '/api/incidents/status/possible',
                         '/api/incidents/status',
                         '/api/incidents/predefined-filters', '/api/incidents/validate/{path}',
                         '/api/incidents/short'],
    'path/contract_two.yaml': ['/api/alerts', '/api/alerts/ingest', '/api/alerts/count', '/api/alerts/list',
                               '/api/alerts/{id}', '/api/alerts/incidents', '/api/alerts/include',
                               '/api/alerts/{id}/include',
                               '/api/alerts/markAsFalsePositive', '/api/alerts/unmarkAsFalsePositive',
                               '/api/alerts/assign',
                               '/api/alerts/{id}/assign', '/api/alerts/sagas/{correlationId}',
                               '/api/alerts/filters',
                               '/api/alerts/filters/{id}/values', '/api/alerts/predefined-filters']
}
