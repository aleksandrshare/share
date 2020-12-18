# coding=utf-8
from framework.api_libs.user_client import AutoCheckUserClient


class AlertsCore(AutoCheckUserClient):
    """"""

    alerts_prefix = 'handler'

    def get_alerts(self, limit=100, offset=None, user_filters=None, search_query=None, filter=None, query_string=None,
                   allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.alerts_prefix + '?'
        if query_string:
            url += f'&{query_string}'
        if limit:
            url += f'&limit={limit}'
        if offset:
            url += f'&offset={offset}'
        if user_filters:
            url += f'&userFilters={user_filters}'
        if search_query:
            url += f'&searchQuery={search_query}'
        if filter:
            url += f'&filter={filter}'
        with self.session():
            response = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                                retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()

    def create_alert(self, data, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.alerts_prefix
        with self.session():
            response = self.post(url=url, json=data, verify=False, allowed_codes=allowed_codes,
                                 retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()

    def create_several_alerts(self, data, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.alerts_prefix + '/ingest'
        with self.session():
            response = self.post(url=url, json=data, verify=False, allowed_codes=allowed_codes,
                                 retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()

    def get_alert_count(self, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.alerts_prefix + '/count'
        with self.session():
            response = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                                retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()

    def get_alerts_by_id_list(self, body, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.alerts_prefix + '/list'
        with self.session():
            response = self.post(url=url, json=body, verify=False, allowed_codes=allowed_codes,
                                 retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()

    def get_alert_info(self, alert_id, etag=None, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        headers = dict()
        if etag:
            headers.update({'If-Match': str(etag)})
        url = self.auth_url + self.alerts_prefix + f'/{alert_id}'
        with self.session():
            response = self.get(url=url, verify=False, headers=headers, allowed_codes=allowed_codes,
                                retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()

    def get_incidents_for_alerts(self, alert_ids=None, body=None, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        if alert_ids:
            body = {
                'alertFilter': {
                    'ids': alert_ids
                }
            }
        if not body:
            raise ValueError('Не указаны параметры запроса! Нужно указать либо id алертов, либо полное тело запроса!')
        url = self.auth_url + self.alerts_prefix + '/incidents'
        with self.session():
            response = self.post(url=url, json=body, verify=False, allowed_codes=allowed_codes,
                                 retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()

    def include_alerts_in_incident(self, inc_id, alerts_ids, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.alerts_prefix + '/include'
        body = {'ids': alerts_ids, 'incidentId': inc_id}
        with self.session():
            response = self.post(url=url, json=body, verify=False, allowed_codes=allowed_codes,
                                 retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json(), response.status_code

    def include_alert_in_incident(self, inc_id, alert_id, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.alerts_prefix + f'/{alert_id}/include'
        body = {'incidentId': inc_id}
        with self.session():
            response = self.post(url=url, json=body, verify=False, allowed_codes=allowed_codes,
                                 retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.text

    def mark_alerts_false_positive(self, alert_ids, force_exclude=False,
                                   allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.alerts_prefix + f'/markAsFalsePositive?forceExclude={force_exclude}'
        with self.session():
            response = self.post(url=url, json=alert_ids, verify=False, allowed_codes=allowed_codes,
                                 retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json(), response.status_code

    def unmark_alerts_false_positive(self, alert_ids, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.alerts_prefix + f'/unmarkAsFalsePositive'
        with self.session():
            response = self.post(url=url, json=alert_ids, verify=False, allowed_codes=allowed_codes,
                                 retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json(), response.status_code

    def assign_operator_on_alerts(self, operator_id, alert_ids, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.alerts_prefix + '/assign'
        body = {'ids': alert_ids, 'operatorId': operator_id}
        with self.session():
            response = self.post(url=url, json=body, verify=False, allowed_codes=allowed_codes,
                                 retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json(), response.status_code

    def assign_operator_on_alert(self, operator_id, alert_id, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.alerts_prefix + f'/{alert_id}/assign'
        body = {'operatorId': operator_id}
        with self.session():
            response = self.post(url=url, json=body, verify=False, allowed_codes=allowed_codes,
                                 retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.text

    def get_alerts_filters(self, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.alerts_prefix + '/filters'
        with self.session():
            response = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                                retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()

    def get_alerts_filter_values(self, filter_id, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.alerts_prefix + f'/filters/{id}/values'
        with self.session():
            response = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                                retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()

    def get_alerts_predefined_filters(self, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.alerts_prefix + '/predefined-filters'
        with self.session():
            response = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                                retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()

    def get_saga(self, correlation_id, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.alerts_prefix + f'/sagas/{correlation_id}'
        with self.session():
            response = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                                retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()

    def get_alerts_count(self, user_filters=None, search_query=None, filter=None, query_string=None,
                         allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.alerts_prefix + '/count?'
        if query_string:
            url += f'&{query_string}'
        if user_filters:
            url += f'&userFilters={user_filters}'
        if search_query:
            url += f'&searchQuery={search_query}'
        if filter:
            url += f'&filter={filter}'
        with self.session():
            response = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                                retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()


class IncidentsCore(AutoCheckUserClient):
    """"""
    incidents_prefix = '/api/incidents'

    def create_incident(self, inc_data, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.incidents_prefix
        with self.session():
            data = self.post(url=url, json=inc_data, verify=False, allowed_codes=allowed_codes,
                             retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json(), data.status_code

    def get_incident_info(self, incident_id, allowed_codes=[200], retry_attempts=5, retry_delay=1):
        """"""
        url = self.auth_url + self.incidents_prefix + f'/{incident_id}'
        with self.session():
            data = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def edit_incident_info(self, incident_id, edit_data, allowed_codes=[200], retry_attempts=5, retry_delay=1,
                           header={}):
        """"""
        url = self.auth_url + self.incidents_prefix + f'/{incident_id}'
        with self.session():
            data = self.put(url=url, json=edit_data, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay, headers=header)
            if data.status_code != 200:
                self.log.error("Incorrect data for edition {}".format(incident_id))
        return data.json()

    def get_several_incidents_info(self, ids_list, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.incidents_prefix + '/list'
        with self.session():
            data = self.post(url=url, json=ids_list, verify=False, allowed_codes=allowed_codes,
                             retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def change_incident_status(self, json_data, inc_id, allowed_codes=[200], retry_attempts=0, retry_delay=1,
                               header={}):
        """"""
        url = self.auth_url + self.incidents_prefix + f'/{inc_id}/status'
        with self.session():
            data = self.post(url=url, json=json_data, verify=False, allowed_codes=allowed_codes,
                             retry_attempts=retry_attempts, retry_delay=retry_delay, headers=header)
        if data.text:
            return data.json()

    def change_several_incidents_statuses(self, json_data, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.incidents_prefix + '/status'
        with self.session():
            data = self.post(url=url, json=json_data, verify=False, allowed_codes=allowed_codes,
                             retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def sync_statuses_incident(self, json_data, inc_id, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.incidents_prefix + f'/{inc_id}/syncStatuses'
        with self.session():
            data = self.post(url=url, json=json_data, verify=False, allowed_codes=allowed_codes,
                             retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def assign_operator_to_incident(self, json_data, inc_id, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.incidents_prefix + f'/{inc_id}/assign'
        with self.session():
            self.post(url=url, json=json_data, verify=False, allowed_codes=allowed_codes,
                      retry_attempts=retry_attempts, retry_delay=retry_delay)

    def assign_operator_to_several_incidents(self, json_data, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.incidents_prefix + '/assign'
        with self.session():
            data = self.post(url=url, json=json_data, verify=False, allowed_codes=allowed_codes,
                             retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def get_list_incidents(self, offset=0, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.incidents_prefix + '?offset=' + str(offset)
        with self.session():
            response = self.get(url=url, verify=False, allowed_codes=allowed_codes, retry_attempts=retry_attempts,
                                retry_delay=retry_delay)
        return response.json()

    def get_incidents_by_filter(self, filter_data, allowed_codes=[200], retry_attempts=5, retry_delay=1):
        """"""
        url = self.auth_url + self.incidents_prefix + f'?filter={filter_data}'
        with self.session():
            data = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def get_all_incident_possible_statuses(self, allowed_codes=[200], retry_attempts=5, retry_delay=1):
        """"""
        url = self.auth_url + self.incidents_prefix + '/status'
        with self.session():
            data = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def get_list_incidents_possible_statuses(self, ids_list, allowed_codes=[200], retry_attempts=5, retry_delay=1):
        """"""
        if not isinstance(ids_list, list):
            ids_list = [ids_list]
        data = {
            "ids": ids_list
        }
        url = self.auth_url + self.incidents_prefix + '/status/possible'
        with self.session():
            data = self.post(url=url, json=data, verify=False, allowed_codes=allowed_codes,
                             retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()
