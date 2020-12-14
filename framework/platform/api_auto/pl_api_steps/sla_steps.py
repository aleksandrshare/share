import pytest
from framework.platform.api_auto.pl_services.int_api_services import ApiServices
from tools.utils import user_assertion, is_property_appear_in_json, transform_date_to_timestamp,\
    search_dir_recursive, current_timestamp
import os
import backoff
import datetime
from copy import deepcopy


class SlaActions(ApiServices):
    """"""
    error_field_existence = "Incorrect JSON structure!!! Field '{}' is absent or null... in {}"

    def __init__(self, auth_url, login, password):
        self.sla_rules = self._get_all_sla_rules_data()
        self.sla_incident_criteria_list = self._form_sla_rule_criteria('incident')
        self.sla_ticket_criteria_list = self._form_sla_rule_criteria('ticket')
        self.sla_alert_criteria_list = self._form_sla_rule_criteria('alert')
        self.sla_rule_path = search_dir_recursive(os.getcwd(), 'SLA.rules.auto.yaml')
        self.sla_remote_directory = '/C:/ProgramData/Positive Technologies/PT IPC/Configurations/PT.SP.SlaService/work'
        super().__init__(auth_url, login, password)

    def _get_all_sla_rules_data(self):
        """"""
        sla_rules_table = self.db_client.get_active_sla_rules('data')
        assert sla_rules_table, "There are no SLA rules on stand!!!"
        sla_rules = []
        for row in sla_rules_table:
            sla_rules.append(dict(row['data']))
        return sla_rules

    def _get_entity_sla_rules_data(self, entity_type):
        """"""
        entity_rules = []
        entity_type = entity_type.capitalize()  # Все ивенты начина.тся с заглавной буквы
        for rule in self.sla_rules:
            event_types = rule['sla']['createOn'][0]['eventTypes']
            for event in event_types:
                if entity_type in event:
                    entity_rules.append(rule)
                    break
        return entity_rules

    def _form_sla_rule_criteria(self, entity_type):
        """"""
        rules_of_entity = self._get_entity_sla_rules_data(entity_type)
        rule_criteria_list = []
        rudiment = entity_type.lower() + '.'    # для удаления названия сущности из названия свойства сущности
        for rule in rules_of_entity:
            criteria_dict = dict()
            criteria_dict['title'] = rule['title']
            criteria_dict['time'] = rule['sla']['time']
            criteria_dict['criteria'] = {}
            event_types = rule['sla']['createOn'][0]['eventTypes']
            if 'conditions' in rule['sla']['createOn'][0]:
                criteria_dict['criteria']['properties'] = ''
                conditions = list(rule['sla']['createOn'][0]['conditions'].keys())  # форм-ние списка операторов условий
                if conditions[0] == '==':
                    prop_name = rule['sla']['createOn'][0]['conditions']['=='][0]['var']
                    prop_value = rule['sla']['createOn'][0]['conditions']['=='][1]
                    if rudiment in prop_name:
                        prop_name = prop_name.replace(rudiment, '')
                    criteria_dict['criteria']['properties'] = {
                        "{}".format(prop_name):
                            "{}".format(prop_value)}
                elif conditions[0] == '!!':
                    prop_name = rule['sla']['createOn'][0]['conditions']['!!'][0]['var']
                    if rudiment in prop_name:
                        prop_name = prop_name.replace(rudiment, '')
                    criteria_dict['criteria']['properties'] = prop_name
            for event in event_types:
                criteria_dict['criteria']['event'] = event
                rule_criteria_list.append(deepcopy(criteria_dict))
        for rule in rule_criteria_list:
            rule['time'] = self.sla_convert_deadline_to_seconds(rule['time'])
        return rule_criteria_list

    # -----------------------------------------------------------------------------------

    def sla_convert_deadline_to_seconds(self, time_value):
        """"""
        amount = time_value.split()[0]
        value = time_value.split()[1]
        if value in 'days':
            deadline_seconds = int(amount) * 24 * 60 * 60
        elif value in 'hours':
            deadline_seconds = int(amount) * 60 * 60
        elif value in 'minutes':
            deadline_seconds = int(amount) * 60
        else:
            assert False, "Format '{}' is not supported!".format(value)
        return deadline_seconds

    @backoff.on_exception(backoff.expo, AssertionError, max_tries=6, max_time=15)
    def sla_get_incident_deadline(self, inc_id, creation_date):
        """"""
        resp = self.get_incident_info(inc_id)
        # Проверка на присутствие SLA блока в json и на его наполненность
        prop = 'sla'
        err_dict = is_property_appear_in_json(resp, prop)
        assert not err_dict, err_dict
        sla_deadline = transform_date_to_timestamp(resp['sla']['deadline'])
        sla_deadline = int(str(sla_deadline).split('.')[0])
        return sla_deadline - creation_date

    def sla_check_deadline(self, actual_delta, expected_delta, entity_type, entity_id):
        """"""
        difference = actual_delta - expected_delta
        assert (0 < difference) < 59, \
            "There are mismatches in SLA deadline in {}".format(user_assertion(actual_delta, expected_delta,
                                                                               '==', entity_type, entity_id))
        self.log.info("Correct sla value of {} {}".format(entity_type, entity_id))

    @backoff.on_exception(backoff.expo, AssertionError, max_tries=6, max_time=15)
    def sla_check_status(self, expected_status, entity_type, entity_id):
        """"""
        if entity_type == 'incident':
            sla = self.get_incident_info(entity_id)['sla']
        elif entity_type == 'ticket':
            sla = self.get_ticket_data(entity_id)['sla']
        elif entity_type == 'alert':
            sla = self.get_alert_info(entity_id)['sla']
        else:
            assert False, "Unknown entity type '{}'".format(entity_type)
        status = sla.get('status')
        assert status == expected_status, "Incorrect SLA status! Expected '{}', actual '{}'." \
                                          " {} {}".format(expected_status, status, entity_type, entity_id)
        self.log.info("Correct sla status '{}' of {} {}".format(status, entity_type, entity_id))

    def sla_check_history_deadline(self, entity_id, entity_type):
        """"""
        pytest.xfail("Заблочен багой 229722")
        history = self.get_entity_history(entity_type, entity_id)['data']
        assert history, "Response has unsupported JSON structure! Entity id {}.".format(entity_id)
        flag = False
        for event in history:
            if 'sla' in event['message']:
                flag = True
                break
        if not flag:
            error = "Incorrect sla history of {} {}. No sla message!".format(entity_type, entity_id)
            self.log.error(error)
            pytest.fail(error)
        else:
            self.log.info("Correct sla history of {} {}".format(entity_type, entity_id))

    def sla_negative_check_deadline(self, json_data):
        """"""
        prop = 'sla'
        err_dict = is_property_appear_in_json(json_data, prop)
        return err_dict

    @backoff.on_predicate(backoff.expo, lambda err_dict: err_dict, max_tries=5, max_time=15)
    def sla_api_negative_check_incident_deadline(self, inc_id):
        """"""
        inc_json = self.get_incident_info(inc_id)
        err_dict = self.sla_negative_check_deadline(inc_json)
        return err_dict

    def sla_check_rule_existence(self, expected_rule, entity_type):
        """"""
        if entity_type == 'incident':
            entity_rules = self.sla_incident_criteria_list
        elif entity_type == 'ticket':
            entity_rules = self.sla_ticket_criteria_list
        elif entity_type == 'alert':
            entity_rules = self.sla_alert_criteria_list
        else:
            assert False, "SLA rules for entity type '{}' is not defined!".format(entity_type)
        deadline = None
        for actual_rule in entity_rules:
            actual_rule.get('criteria')
            reserve_dict = actual_rule.copy()
            reserve_dict['criteria'] = expected_rule
            if reserve_dict == actual_rule:
                deadline = reserve_dict['time']
                break
        return deadline

    def sla_get_new_deadline(self, condition, entity_type):
        """"""
        sla_deadline = self.sla_check_rule_existence(condition, entity_type)
        return sla_deadline

    def sla_upload_custom_rule_file(self):
        """"""
        self.ssh_client.ftp_move_file_to_dir(self.sla_rule_path, self.sla_remote_directory,
                                             service_to_restart='PT.SP.SLA')
        self.ssh_client.ssh_restart_win_service('PT.SP.SLA')
        self.sla_get_new_rules()

    def sla_get_new_rules(self):
        """"""
        self.sla_rules = self._get_all_sla_rules_data()
        self.sla_incident_criteria_list = self._form_sla_rule_criteria('incident')
        self.sla_ticket_criteria_list = self._form_sla_rule_criteria('ticket')
        self.sla_alert_criteria_list = self._form_sla_rule_criteria('alert')

    def sla_check_notifications_prerequisites(self):
        """"""
        self.mark_notifications_as_read()
        utc_date = datetime.datetime.utcnow()
        return utc_date

    @backoff.on_predicate(backoff.expo, lambda error: error, max_tries=11, max_time=60)
    def sla_check_notification(self, inc_id, expired):
        """"""
        resp = self.get_unread_notifications()
        if expired:
            error = "Нет уведомления о просрочке СЛА! {}.\n".format(inc_id)
        else:
            error = "Нет уведомления о скором истечении сроков СЛА! {}.\n".format(inc_id)
        notifications = resp.get('items')
        if notifications:
            for message in notifications:
                mes = message.get('message')
                if (inc_id in mes) and ('SLA' in mes):
                    if expired:
                        if 'истек' in mes:
                            self.log.info("Correct SLA expiration message. {}: '{}'".format(inc_id, mes))
                            error = ''
                            return error
                    else:
                        if 'истекает через' in mes:
                            self.log.info("Correct SLA warning message. {}: '{}'".format(inc_id, mes))
                            error = ''
                            return error
        else:
            error = "Нет новых уведомлений. {}\n".format(inc_id)
            self.log.error(error)
            return error
        self.log.error(error)
        return error

    def sla_check_operator_email(self, inc_id, operator, utc_date, expired):
        """"""
        if not operator['email']:
            error = "У оператора '{}' {} пустой email. Пропускаем проверку...\n".format(operator['login'],
                                                                                        operator['id'])
            self.log.error(error)
            return error
        if expired:
            error = "Email об истёкшем SLA не отправлен '{}' {}!\n".format(operator['login'], operator['id'])
            subject = 'Уведомление об окончании срока выполнения SLA'
        else:
            error = "Email о скором истечении сроков SLA не отправлен '{}' {}!\n".format(operator['login'],
                                                                                         operator['id'])
            subject = 'Уведомление о скором истечении времени выполнения SLA'
        db_resp = self.find_email_in_db(operator['email'], subject, utc_date)
        if not db_resp:
            self.log.error(error)
            return error
        for row in db_resp:
            row = dict(row)
            if (inc_id in row['content']) and ('SLA' in row['content']):
                if expired:
                    if 'истек' in row['content']:
                        error = ''
                        self.log.info("Incident {} has correct SLA email: {}".format(inc_id, row['content']))
                        return error
                else:
                    if 'истекает через' in row['content']:
                        error = ''
                        self.log.info("Incident {} has correct SLA email: {}".format(inc_id, row['content']))
                        return error
        self.log.error(error)
        return error

    def sla_api_check_notifications(self, entity_id, operator, utc_date, expired=False):
        """"""
        errors = self.sla_check_notification(entity_id, expired)
        errors += self.sla_check_operator_email(entity_id, operator, utc_date, expired)
        self.mark_notifications_as_read()
        return errors

    def sla_check_list_sorting(self, entity_list, message_list):
        """"""
        previous = 0
        cur_entity_id = ''
        for entity in entity_list:
            cur_entity_id = entity['id']
            sla = entity.get('sla')
            if sla:
                deadline = entity['sla'].get('deadline')
                if deadline:
                    deadline = transform_date_to_timestamp(deadline)
                    if deadline >= previous:
                        previous = deadline
                        sort_message = 'Then there will be only entities with deadline.'
                    else:
                        return cur_entity_id
                else:
                    sort_message = 'Then there will be only entities with empty deadline.'
            else:
                sort_message = 'Then there will be only entities with empty sla.'
        if not message_list:
            message_list.append(sort_message)
            self.log.info(sort_message)
        if sort_message != message_list[-1]:
            message_list.append(sort_message)
            self.log.info(sort_message)
            sort_breakpoint = message_list.count(sort_message)
            if sort_breakpoint != 1:
                return message_list, cur_entity_id
        return message_list, None

    def sla_api_check_default_sort_incidents(self):
        """"""
        resp = True
        offset = 0
        message_list = []
        while resp:
            resp = self.get_list_incidents(offset=offset)['items']
            if not resp:
                self.log.info("Incidents list is now empty. Sort verification stopped...")
                break
            offset += 100
            message_list, error_id = self.sla_check_list_sorting(resp, message_list)
            if error_id:
                pytest.fail("Incorrect default incidents sort. Last incident id {}".format(error_id))

    def sla_api_check_deadline(self, deadline, entity_id, entity_type='incident', expected_status='inProgress',
                               creation_date=None):
        """"""
        if not deadline:
            message = "There are no active rules for such criteria. {} {}".format(entity_type, entity_id)
            self.log.error(message)
            pytest.skip(message)
        if not creation_date:
            creation_date = current_timestamp()
        creation_date = int(str(creation_date).split('.')[0])
        if entity_type == 'incident':
            actual_deadline = self.sla_get_incident_deadline(entity_id, creation_date)
        elif entity_type == 'ticket':
            actual_deadline = self.sla_get_ticket_deadline(entity_id, creation_date)
        elif entity_type == 'alert':
            actual_deadline = self.sla_get_alert_deadline(entity_id, creation_date)
        else:
            assert False, "Unknown entity type '{}'".format(entity_type)
        assert actual_deadline, self.error_field_existence.format('sla', entity_id)
        self.sla_check_deadline(actual_deadline, deadline, entity_type, entity_id)
        self.sla_check_status(expected_status, entity_type, entity_id)
        # self.sla_check_history_deadline(ticket_id, entity_type='ticket')

    @backoff.on_exception(backoff.expo, AssertionError, max_tries=6, max_time=15)
    def sla_get_ticket_deadline(self, entity_id, creation_date):
        """"""
        resp = self.get_ticket_data(entity_id)
        prop = 'sla'
        err_dict = is_property_appear_in_json(resp, prop)
        assert not err_dict, err_dict
        sla_deadline = transform_date_to_timestamp(resp['sla']['deadline'])
        sla_deadline = int(str(sla_deadline).split('.')[0])
        return sla_deadline - creation_date

    @backoff.on_predicate(backoff.expo, lambda err_dict: err_dict, max_tries=5, max_time=15)
    def sla_api_negative_check_ticket_deadline(self, ticket_id):
        """"""
        data = self.get_ticket_data(ticket_id)
        err_dict = self.sla_negative_check_deadline(data)
        return err_dict

    def sla_api_check_default_sort_tickets(self):
        """"""
        resp = True
        offset = 0
        message_list = []
        while resp:
            resp = self.get_list_tickets(offset=offset)['items']
            if not resp:
                self.log.info("Tickets list is now empty. Sort verification stopped...")
                break
            offset += 100
            message_list, error_id = self.sla_check_list_sorting(resp, message_list)
            if error_id:
                pytest.fail("Incorrect default tickets sort. Last ticket id {}".format(error_id))

    def sla_api_check_default_sort_alerts(self):
        """"""
        resp = True
        offset = 0
        message_list = []
        while resp:
            resp = self.get_alerts(offset=offset)['items']
            if not resp:
                self.log.info("Alerts list is now empty. Sort verification stopped...")
                break
            offset += 100
            message_list, error_id = self.sla_check_list_sorting(resp, message_list)
            if error_id:
                pytest.fail("Incorrect default alerts sort. Last alert id {}".format(error_id))

    @backoff.on_exception(backoff.expo, AssertionError, max_tries=6, max_time=15)
    def sla_get_alert_deadline(self, entity_id, creation_date):
        """"""
        resp = self.get_alert_info(entity_id)
        prop = 'sla'
        err_dict = is_property_appear_in_json(resp, prop)
        assert not err_dict, err_dict
        sla_deadline = transform_date_to_timestamp(resp['sla']['deadline'])
        sla_deadline = int(str(sla_deadline).split('.')[0])
        return sla_deadline - creation_date
