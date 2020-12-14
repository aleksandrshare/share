#!/usr/bin/env python
# -*- coding: utf-8 -*-
from framework.platform.api_auto.pl_services.int_api_services import ApiServices
from tools.utils import new_source_id, string_generator


class DictionariesActions(ApiServices):
    """"""

    def da_check_dictionary(self, reference_id):
        """"""
        reference_data = self.get_reference_values(reference_id)
        if reference_data[0]['records']:
            self.log.info(f'Справочник "{reference_id}" заполнен')
            return True
        else:
            self.log.info(f'Справочник "{reference_id}" пустой')
            return False

    def da_fill_dictionary(self, reference_id, number_values=3):
        """"""
        for _ in range(number_values):
            reference_data = {
                "id": new_source_id(),
                "name": f"{reference_id}_{string_generator(5, 15)}"
            }
            self.post_reference_values(reference_id, reference_data)
