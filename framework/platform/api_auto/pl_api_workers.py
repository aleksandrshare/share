#!/usr/bin/env python
# -*- coding: utf-8 -*-
from configs import settings
from configs.service_ports import ports
from framework.platform.api_auto.pl_api_steps import ApiActions
from framework.shared.third_party.iam_steps import IamActions
from framework.platform.api_auto.pl_api_steps.integration_api_steps import IntegrationApiActions
from framework.shared.third_party.portal_steps import CertPortalActions
from framework.platform.queries.pl_pg_queries import PlatformPgSQLQueries
from urllib.parse import urlparse
from tools.generator import PlatformJsonGenerator
from framework.platform.SSH.ssh_client import PlatformSSHClient


class LKOApiAdmin(ApiActions):
    """ Клиент внутреннего API Платформы (все права) """
    def __init__(self, stand_group):
        self.stands = settings.stands
        self.bd_stand = self.stands[stand_group]['LKO_POSTGRES']
        self.db_client = PlatformPgSQLQueries(self.bd_stand)
        self.LOGIN = self.stands[stand_group]['LKO_CRED']['LOGIN']
        self.PASSWORD = self.stands[stand_group]['LKO_CRED']['PASSWORD']
        self.LKO_URL = self.stands[stand_group]['LKO_URL']
        self.generator = PlatformJsonGenerator(stand_url=self.LKO_URL, login=self.LOGIN, password=self.PASSWORD)
        self.ssh_client = PlatformSSHClient(self.LKO_URL)
        super().__init__(auth_url=self.LKO_URL, login=self.LOGIN, password=self.PASSWORD)


class IntegrationApiUser(IntegrationApiActions):
    """ Клиент интеграционного API Платформы"""
    def __init__(self, stand_group):
        self.stands = settings.stands
        self.bd_stand = self.stands[stand_group]['LKO_POSTGRES']
        self.db_client = PlatformPgSQLQueries(self.bd_stand)
        self.LOGIN = self.stands[stand_group]['LKO_CRED']['LOGIN']
        self.PASSWORD = self.stands[stand_group]['LKO_CRED']['PASSWORD']
        # self.LKO_URL нужен для построения URL созданной сущности
        self.LKO_URL = self.stands[stand_group]['LKO_URL']
        self.INTEGR_LKO_URL = self._collect_full_api_url(stand_group)
        self.generator = PlatformJsonGenerator(stand_url=self.LKO_URL, login=self.LOGIN, password=self.PASSWORD)
        super().__init__(auth_url=self.INTEGR_LKO_URL, login=self.LOGIN, password=self.PASSWORD)

    def _collect_full_api_url(self, stand_group):
        host_name = urlparse(self.stands[stand_group]['LKO_URL']).hostname
        api_port = ports.get('IntegrationApi')
        return f"http://{host_name}:{api_port}"


class IamApiAdmin(IamActions):
    """ Клиент внутреннего API """
    def __init__(self, stand_group):
        self.stands = settings.stands
        self.LOGIN = self.stands[stand_group]['LKO_CRED']['LOGIN']
        self.PASSWORD = self.stands[stand_group]['LKO_CRED']['PASSWORD']
        self.IAM_URL = self.stands[stand_group]['IAM_URL']
        self.ONLY_ADMIN_CRED = self.stands[stand_group]['ONLY_ADMIN_CRED']['LOGIN']
        super().__init__(auth_url=self.IAM_URL, login=self.LOGIN, password=self.PASSWORD)


class OnlyAdmin(ApiActions):
    """ Клиент внутреннего API Платформы с правом на администрирование """
    def __init__(self, stand_group):
        self.stands = settings.stands
        self.LOGIN = self.stands[stand_group]['ONLY_ADMIN_CRED']['LOGIN']
        self.PASSWORD = self.stands[stand_group]['ONLY_ADMIN_CRED']['PASSWORD']
        self.LKO_URL = self.stands[stand_group]['LKO_URL']
        self.bd_stand = self.stands[stand_group]['LKO_POSTGRES']
        self.db_client = PlatformPgSQLQueries(self.bd_stand)
        super().__init__(auth_url=self.LKO_URL, login=self.LOGIN, password=self.PASSWORD)


class CertPortalApiAdmin(CertPortalActions):
    """ Клиент внутреннего API  Portal"""
    def __init__(self):
        self.stands = settings.stands
        self.CERT_URL = self.stands['CERTAUTOFT']['CERT_URL']
        self.LOGIN = self.stands['CERTAUTOFT']['CERT_ADMIN_CRED']['LOGIN']
        self.PASSWORD = self.stands['CERTAUTOFT']['CERT_ADMIN_CRED']['PASSWORD']
        super().__init__(auth_url=self.CERT_URL, login=self.LOGIN, password=self.PASSWORD)
