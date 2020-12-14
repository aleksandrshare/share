from framework.api_libs.user_client import AutoCheckUserClient


class TicketsCore(AutoCheckUserClient):
    """"""
    tickets_prefix = '/api/tickets'

    def create_new_ticket(self, json_data, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        url = self.auth_url + self.tickets_prefix
        with self.session():
            data = self.post(url=url, json=json_data, verify=False, allowed_codes=allowed_codes,
                             retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def get_ticket_data(self, ticket_id, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.tickets_prefix + '/{}'.format(ticket_id)
        with self.session():
            data = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def edit_ticket_info(self, ticket_id, edit_data, allowed_codes=[200], retry_attempts=5, retry_delay=1,
                         header={}):
        """"""
        url = self.auth_url + self.tickets_prefix + f'/{ticket_id}'
        with self.session():
            data = self.put(url=url, json=edit_data, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay, headers=header)
            if data.status_code != 200:
                self.log.error("Incorrect data for edition {}".format(ticket_id))
        return data.json()

    def change_ticket_status(self, json_data, entity_id, allowed_codes=[200], retry_attempts=0, retry_delay=1,
                             header={}):
        """"""
        url = self.auth_url + self.tickets_prefix + f'/{entity_id}/status'
        with self.session():
            data = self.post(url=url, json=json_data, verify=False, allowed_codes=allowed_codes,
                             retry_attempts=retry_attempts, retry_delay=retry_delay, headers=header)
        if data.text:
            return data.json()

    def set_ticket_summary(self, json_data, entity_id, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.tickets_prefix + f'/{entity_id}/summary'
        with self.session():
            data = self.post(url=url, json=json_data, verify=False, allowed_codes=allowed_codes,
                             retry_attempts=retry_attempts, retry_delay=retry_delay)
        if data.text:
            return data.json()

    def assign_operator_to_ticket(self, json_data, inc_id, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.tickets_prefix + f'/{inc_id}/assign'
        with self.session():
            self.post(url=url, json=json_data, verify=False, allowed_codes=allowed_codes,
                      retry_attempts=retry_attempts, retry_delay=retry_delay)

    def get_list_tickets(self, offset=0, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.tickets_prefix + '?offset=' + str(offset)
        with self.session():
            response = self.get(url=url, verify=False, allowed_codes=allowed_codes, retry_attempts=retry_attempts,
                                retry_delay=retry_delay)
        return response.json()

    def get_all_ticket_possible_statuses(self, allowed_codes=[200], retry_attempts=5, retry_delay=1):
        """"""
        url = self.auth_url + self.tickets_prefix + '/status'
        with self.session():
            data = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def get_list_tickets_possible_statuses(self, ids_list, allowed_codes=[200], retry_attempts=5, retry_delay=1):
        """"""
        if not isinstance(ids_list, list):
            ids_list = [ids_list]
        data = {
            "ids": ids_list
        }
        url = self.auth_url + self.tickets_prefix + '/status/possible'
        with self.session():
            data = self.post(url=url, json=data, verify=False, allowed_codes=allowed_codes,
                             retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()