from framework.platform.api_auto.pl_services.int_api_services import ApiServices
from tools.concept_wws_iwc import universal_comparison_function_for_post_keys
from tools.utils import random_choice, is_property_appear_in_json
import backoff
import pytest
import allure
from json import dumps
from tools.utils import string_generator


class TicketsActions(ApiServices):
    error_value_mes = "Incorrect value in {} presented in response json of {}"

    def ta_api_create_and_check_ticket(self, desire_data=None):
        """"""
        ticket_id, data = self.ta_create_ticket(desire_data)
        data = self.ta_check_new_ticket(ticket_id, data)
        allure.attach(dumps(data, indent=2, ensure_ascii=False), f'Ответ на GET задачи {ticket_id}',
                      allure.attachment_type.JSON)
        return ticket_id

    def ta_form_ticket_data(self):
        """"""
        data = self.generator.give_json(self.tickets_prefix)
        return data

    def ta_create_ticket(self, desire_data):
        """"""
        data = self.ta_form_ticket_data()
        data['priority'] = random_choice([1, 3, 4, 5])
        if desire_data:
            data.update(desire_data)
        resp = self.create_new_ticket(data)
        assert resp, "Empty response!"
        data.update(resp)
        return resp['id'], data

    @backoff.on_exception(backoff.expo, AssertionError, max_tries=5, max_time=15)
    def ta_check_new_ticket(self, entity_id, expected_data):
        """"""
        cur_data = self.get_ticket_data(entity_id, retry_attempts=10)
        assert cur_data, f"Ticket {entity_id} has empty GET response!!!"
        errors = universal_comparison_function_for_post_keys(expected_data, cur_data, need_assert=False)
        new_fields = ['hrid', 'status']
        errors.update(self.check_additional_fields(cur_data, new_fields))
        assert not errors, errors
        return cur_data

    def ta_api_edit_and_check_ticket(self, entity_id, desire_json=None):
        """"""
        new_data = self.ta_edit_ticket(entity_id, desire_json)
        err_dict, cur_data = self.ta_check_edited_fields(entity_id, new_data)
        allure.attach(dumps(cur_data, indent=2, ensure_ascii=False), f'Ответ на GET задачи {entity_id}',
                      allure.attachment_type.JSON)
        if err_dict:
            pytest.fail("There are mismatches during ticket {} verification in {}".format(entity_id, err_dict))

    def ta_edit_ticket(self, entity_id, desire_json=None):
        """"""
        new_data = self.ta_form_ticket_data()
        new_data['priority'] = random_choice([1, 3, 4, 5])
        new_data['status'] = 'new'
        if desire_json:
            new_data.update(desire_json)
        new_data['id'] = entity_id
        self.edit_ticket_info(entity_id, new_data, allowed_codes=[200, 400, 403])
        return new_data

    @backoff.on_predicate(backoff.expo, lambda diff_dict: diff_dict[0], max_tries=6, max_time=15)
    def ta_check_edited_fields(self, entity_id, edited_data):
        """"""
        if edited_data:
            data = self.get_ticket_data(entity_id)
            diff_dict = universal_comparison_function_for_post_keys(edited_data, data, need_assert=False)
            return diff_dict, data
        assert edited_data, "Nothing to compare with!"

    def ta_api_change_and_check_ticket_status(self, entity_id, new_status=None):
        """"""
        if not new_status:
            new_status = self.select_random_status()
        self.ta_change_ticket_status(entity_id, new_status)
        err_dict = self.ta_check_ticket_status(entity_id, new_status)
        if err_dict:
            pytest.fail(self.error_value_mes.format('status', entity_id))

    def ta_change_ticket_status(self, entity_id, new_status):
        """"""
        change_status_json = self.ta_form_data_for_change_status(entity_id, new_status)
        self.change_ticket_status(change_status_json, entity_id)

    def ta_form_data_for_change_status(self, entity_id, new_status):
        """"""
        actual_json = self.get_ticket_data(entity_id)
        actual_status = actual_json['status']
        data = {
            "status": new_status,
            "comment": "Change status from {} to {}".format(actual_status, new_status)
        }
        return data

    def ta_check_ticket_status(self, entity_id, correct_status):
        """"""
        dict_of_changes = {
            'status': correct_status
        }
        err_dict, data = self.ta_check_edited_fields(entity_id, dict_of_changes)
        allure.attach(dumps(data, indent=2, ensure_ascii=False), f'Ответ на GET задачи {entity_id}',
                      allure.attachment_type.JSON)
        return err_dict

    def ta_negative_close_ticket_without_summary(self, entity_id):
        """"""
        current_json = self.get_ticket_data(entity_id)
        if current_json.get('summary'):
            pytest.skip("Ticket {} should have empty summary!". format(entity_id))
        data = self.ta_form_data_for_change_status(entity_id, new_status='closed')
        resp = self.change_ticket_status(data, entity_id, allowed_codes=[400])
        assert resp, "Incorrect response structure!"
        self.log.info(resp['detail'])
        err_dict = self.ta_check_ticket_status(entity_id, 'new')
        if err_dict:
            pytest.fail('Ticket {}. Incorrect status {}'.format(entity_id, err_dict))

    def ta_api_set_ticket_summary(self, entity_id):
        """"""
        data = {
            'summary': string_generator(1, 50)
        }
        self.set_ticket_summary(data, entity_id)
        err_dict, data = self.ta_check_edited_fields(entity_id, data)
        allure.attach(dumps(data, indent=2, ensure_ascii=False), f'Ответ на GET задачи {entity_id}',
                      allure.attachment_type.JSON)
        if err_dict:
            pytest.fail('Ticket {}. Incorrect summary {}'.format(entity_id, err_dict))

    def ta_api_assign_and_check_ticket(self, entity_id, operator_id):
        """"""
        data = {
            "operatorId": operator_id
        }
        self.assign_operator_to_ticket(data, entity_id)
        err_dict, data = self.ta_check_ticket_assignment(entity_id, operator_id)
        allure.attach(dumps(data, indent=2, ensure_ascii=False), f'Ответ на GET задачи {entity_id}',
                      allure.attachment_type.JSON)
        if err_dict:
            pytest.fail("Ticket {}. Incorrect responsible operator {}".format(entity_id, err_dict))

    @backoff.on_exception(backoff.expo, AssertionError, max_tries=5, max_time=15)
    def ta_check_ticket_assignment(self, entity_id, operator_id):
        """"""
        dict_of_changes = {}
        data = self.get_ticket_data(entity_id)
        prop = 'assignee'
        err_dict = is_property_appear_in_json(data, prop)
        assert not err_dict, err_dict
        dict_of_changes[prop] = {
            'id': operator_id
        }
        err_dict, data = self.ta_check_edited_fields(entity_id, dict_of_changes)
        return err_dict, data

    def ta_get_random_ticket(self):
        """"""
        resp = self.get_list_tickets()
        if not resp.get('total'):
            self.log.info('Нет задач в системе, создаем новую')
            ticket_id = self.ta_api_create_and_check_ticket()
        else:
            ticket_id = random_choice(resp['items'])['id']
        self.log.info(f'Выбрана задача с id={ticket_id}')
        allure.attach(self.LKO_URL + f"/tickets/view/{ticket_id}", 'Ссылка на задачу в UI',
                      allure.attachment_type.URI_LIST)
        return ticket_id

    def ta_check_possible_statuses(self, expected):
        """"""
        resp = self.get_all_ticket_possible_statuses()
        actual_statuses = []
        assert resp, "Possible statuses list is empty!"
        for value in resp:
            status = value.get('id')
            actual_statuses.append(status)
        assert expected == actual_statuses, "Status model is not updated!"
        self.log.info("New ticket status model has been uploaded! {}".format(actual_statuses))

    def ta_negative_change_status_ticket(self, entity_id, wrong_status='new'):
        """"""
        current_status = self.get_ticket_data(entity_id)['status']
        data = self.ta_form_data_for_change_status(entity_id, new_status=wrong_status)
        resp = self.change_ticket_status(data, entity_id, allowed_codes=[400])
        assert resp, "Incorrect response structure!"
        self.log.info(resp.get('detail'))
        status = self.ta_check_ticket_status(entity_id, current_status)
        if status == wrong_status:
            pytest.fail(self.error_value_mes.format('status', entity_id))