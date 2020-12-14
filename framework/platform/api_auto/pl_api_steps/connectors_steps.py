#!/usr/bin/env python
# -*- coding: utf-8 -*-
from framework.platform.api_auto.pl_services.int_api_services import ApiServices
import allure
from json import dumps


class ConnectorsActions(ApiServices):
    """"""

    def check_connector_present(self, connector_name):
        """"""
        resp = self.get_connector_by_namespace(connector_name)
        allure.attach(dumps(resp, indent=2, ensure_ascii=False), f'Коннектор к {connector_name}',
                      allure.attachment_type.JSON)
        if not resp.get('items'):
            self.log.error(f'Коннектор к {connector_name} не настроен!')
            return False
        else:
            self.log.info(f'Коннектор к {connector_name} есть в списке коннекторов')
            return True

    def check_connector_part_enabled(self, connector_name, identifier):
        """"""
        if self.check_connector_present(connector_name):
            resp = self.get_connector_status_for_identifier_in_namespace(connector_name, identifier)
            allure.attach(dumps(resp, indent=2, ensure_ascii=False), f'Статус {identifier} коннектора {connector_name}',
                          allure.attachment_type.JSON)
            if resp['status'] == 'enabled':
                self.log.info(f'{identifier} в {connector_name} активен')
                return True
            else:
                self.log.error(f'{identifier} в {connector_name} не активен')
                return False
        else:
            return False
