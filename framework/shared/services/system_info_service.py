#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib.parse import urlparse

from configs.service_ports import platform_ports
from tools.api_client.user_client import AutoCheckUserClient


class SystemInfoCore(AutoCheckUserClient):

    SYS_INFO_PREFIX = ":7042/api/systemInfo/version"

    def sysInfo_get_all_service(self, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """
        Запрашивает у systemInfo все сервисы, которые должны быть на стенде

        :param allowed_codes: верные коды ответа
        :param retry_attempts: повторы
        :param retry_delay: delay для повтора
        :return: json объект
        """
        host_name = "http://" + urlparse(self.auth_url).hostname
        url = host_name + self.SYS_INFO_PREFIX
        with self.session():
            data = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def sysInfo_get_for_health_check(self, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """
        Через метод sysInfo_get_all_service берет все сервисы и обрабатывает их для Health Check

        :param allowed_codes: верные коды ответа
        :param retry_attempts: повторы
        :param retry_delay: delay для повтора
        :return: list список сервисов, которые надо проверить
        """
        data = self.sysInfo_get_all_service(allowed_codes, retry_attempts, retry_delay)
        service = list()
        for i in data:
            if i.get("type").casefold() != "ui" and platform_ports.get(i.get("serviceName")):
                service.append(i.get("serviceName"))
        return service


if "__main__" == __name__:
    sys_get = SystemInfoCore("https://sp-ipc-qa-auto.rd.ptsecurity.ru", "Administrator", "P@ssw0rd")
    data = sys_get.sysInfo_get_all_service()
    print(data)



