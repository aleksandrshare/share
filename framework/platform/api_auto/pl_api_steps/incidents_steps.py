#!/usr/bin/env python
# -*- coding: utf-8 -*-
import allure
import backoff
from json import dumps
from framework.platform.api_auto.pl_services.int_api_services import ApiServices
from tools.concept_wws_iwc import universal_comparison_function_for_post_keys


class IncidentAction(ApiServices):
    def ia_create_new_incident(self):
        data = self.generator.give_json(self.incident_prefix)
        resp = self.ic_create_incident(data)
        allure.attach(self.LKO_URL + f"/v2/incidents/view/{resp['id']}", 'Ссылка на инцидент в UI',
                      allure.attachment_type.URI_LIST)
        return resp, resp['id']

    @backoff.on_exception(backoff.expo, AssertionError, max_time=15, max_tries=5)
    def ia_check_inc(self, inc_id, post_json):
        resp = self.ic_get_incident_info(inc_id)
        allure.attach(dumps(resp, indent=2, ensure_ascii=False), f'Ответ на GET инцидента {inc_id}',
                      allure.attachment_type.JSON)
        assert resp, f"Not resp {resp}"
        err_dict = universal_comparison_function_for_post_keys(post_json, resp)
        return err_dict

    def ia_create_and_check_incident(self):
        post_json, inc_id = self.ia_create_new_incident()
        err_dict = self.ia_check_inc(inc_id=inc_id, post_json=post_json)
        assert not err_dict, err_dict
