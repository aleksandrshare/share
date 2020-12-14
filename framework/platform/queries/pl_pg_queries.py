#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy.sql.expression import func
from tools.database_client import DataBaseClient


class PlatformPgSQLQueries:

    def __init__(self, url):
        self.db = DataBaseClient(url, login='user', password='password')

    def find_integr_api_rec_in_db(self, entity_id):
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        select_from_table = ['Id']
        condition = table.c.Id == entity_id
        return self.db.execute_select(table, select_from_table, condition=condition)

    def get_mt_events_records_with_type(self, event_type):
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        condition = table.c.type == event_type
        return self.db.execute_select(table, condition=condition)

    def get_mt_events_records_by_stream_id_with_type(self, stream_id, event_type):
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        condition = table.c.stream_id == stream_id
        condition &= table.c.type == event_type
        return self.db.execute_select(table, condition=condition)

    def find_record_in_alerts_table(self, alert_id):
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        condition = table.c.Id == alert_id
        return self.db.execute_select(table, condition=condition)

    def get_default_sla_deadline(self, rule_name):
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        select_from_table = ['time']
        condition = table.c.title == rule_name
        return self.db.execute_select(table, select_from_table, condition=condition)

    def get_active_sla_rules(self, column):
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        condition = table.c.is_active
        select_from_table = ['id', column]
        order_by = 'id'
        return self.db.execute_select(table, select_from_table, condition=condition, order_by=order_by)

    def find_alert_by_source_id(self, source_id):
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        condition = table.c.SourceId == source_id
        select_from_table = ['Id']
        return self.db.execute_select(table, select_from_table, condition=condition)

    def find_incident_by_source_id(self, source_id):
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        condition = table.c.SourceId == source_id
        select_from_table = ['Id']
        return self.db.execute_select(table, select_from_table, condition=condition)

    def find_fias_node_value(self, node_type='ActiveNode'):
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        select_from_table = ['Value']
        condition = table.c.Id == f'{node_type}Name'
        return self.db.execute_select(table, select_from_table, condition=condition)

    def find_fias_oktmo_codes(self, fias_node, limit=100):
        db_name = fias_node
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        select_from_table = ['oktmo']
        condition = (table.c.postalcode != None) & (table.c.oktmo != None)
        condition &= (table.c.actstatus == True) & (table.c.livestatus == True)
        order_by = func.random()
        return self.db.execute_select(table, select_from_table, condition=condition,
                                      limit=limit, order_by=order_by)

    def db_find_subject_by_id(self, subj_id, spec_column=None):
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        condition = table.c.Id == subj_id
        return self.db.execute_select(table, condition=condition, need_special_columns=spec_column)

    def db_find_object_by_id(self, obj_id, spec_column=None):
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        condition = table.c.Id == obj_id
        return self.db.execute_select(table, condition=condition, need_special_columns=spec_column)

    def db_find_system_by_id(self, sys_id, spec_column=None):
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        condition = table.c.Id == sys_id
        return self.db.execute_select(table, condition=condition, need_special_columns=spec_column)

    def db_find_email_by_address_and_subject(self, address, subject, date_after=None):
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        condition = table.c.to_raw == address
        condition &= table.c.subject == subject
        if date_after:
            condition &= table.c.created_at >= date_after
        return self.db.execute_select(table, condition=condition)

    def db_find_unassigned_incidents(self):
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        condition = table.c.Responsible != None
        return self.db.execute_select(table, condition=condition)

    def db_find_incidents_assigned_to_userid(self, user_id):
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        condition = table.c.Responsible == user_id
        return self.db.execute_select(table, condition=condition)

    def db_find_incidents_by_user_active(self, is_active):
        db_name = 'test'
        table_name_users = 'test'
        table_users = self.db._get_table(db_name, table_name_users)
        table_name_inc = 'test'
        table_inc = self.db._get_table(db_name, table_name_inc)
        left_join = table_inc.outerjoin(table_users, table_users.c.Id == table_inc.c.Responsible)
        condition = table_users.c.IsActive == is_active

        return self.db.execute_select(table_inc, condition=condition, from_obj=left_join)

    def db_find_incidents_with_status(self, expected_status, limit=100):
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        select_from_table = ['Id']
        condition = table.c.Status == expected_status
        return self.db.execute_select(table, select_from_table, condition=condition, limit=limit)

    def find_alerts_with_is_included_filter(self, is_included=True, limit=None):
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        if is_included:
            condition = table.c.IncidentId != None
        else:
            condition = table.c.IncidentId == None
        if limit:
            return self.db.execute_select(table, condition=condition, limit=limit)
        else:
            return self.db.execute_select(table, condition=condition)

    def find_alerts_with_false_positive_filter(self, is_false_positive=True, limit=None):
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        if is_false_positive:
            condition = table.c.FalsePositive == True
        else:
            condition = table.c.FalsePositive == False
        if limit:
            return self.db.execute_select(table, condition=condition, limit=limit)
        else:
            return self.db.execute_select(table, condition=condition)

    def find_alerts_with_responsible_operator_filter(self, operators_list, limit=None):
        if not isinstance(operators_list, list):
            operators_list = [operators_list]
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        condition = table.c.ResponsibleOperator.in_(operators_list)
        if limit:
            return self.db.execute_select(table, condition=condition, limit=limit)
        else:
            return self.db.execute_select(table, condition=condition)

    def find_alerts_with_source_filter(self, sources_list, limit=None):
        if not isinstance(sources_list, list):
            sources_list = [sources_list]
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        condition = table.c.Source.in_(sources_list)
        if limit:
            return self.db.execute_select(table, condition=condition, limit=limit)
        else:
            return self.db.execute_select(table, condition=condition)

    def find_alerts_with_fixation_date_filter(self, start_interval, finish_interval, limit=None):
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        condition = table.c.DetectedAt.between(start_interval, finish_interval)
        if limit:
            return self.db.execute_select(table, condition=condition, limit=limit)
        else:
            return self.db.execute_select(table, condition=condition)

    def find_alerts_with_incident_filter(self, incident_list, limit=None):
        if not isinstance(incident_list, list):
            incident_list = [incident_list]
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        condition = table.c.IncidentId.in_(incident_list)
        if limit:
            return self.db.execute_select(table, condition=condition, limit=limit)
        else:
            return self.db.execute_select(table, condition=condition)
