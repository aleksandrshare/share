from framework.api_libs.user_client import AutoCheckUserClient


class ReportsCore(AutoCheckUserClient):
    """"""
    reports_prefix = 'handler'

    def get_task_id_incident_export_report(self, allowed_codes=[200], retry_attempts=5, retry_delay=1):
        """"""
        data = {
            "url": self.auth_url + self.incidents_prefix
        }
        url = self.auth_url + self.reports_prefix + '/export/10000000/csv'
        with self.session():
            data = self.post(url=url, json=data, verify=False, allowed_codes=allowed_codes,
                             retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def get_task_id_ticket_export_report(self, allowed_codes=[200], retry_attempts=5, retry_delay=1):
        """"""
        data = {
            "url": self.auth_url + self.tickets_prefix
        }
        url = self.auth_url + self.reports_prefix + '/export/18000000/csv'
        with self.session():
            data = self.post(url=url, json=data, verify=False, allowed_codes=allowed_codes,
                             retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def get_report_id(self, task_id, allowed_codes=[200], retry_attempts=5, retry_delay=1):
        """"""
        url = self.auth_url + self.reports_prefix + '/export/status/' + task_id
        with self.session():
            data = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()