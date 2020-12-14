#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tools.database_client import DataBaseClient


class PgSQLQueries:

    def __init__(self, url):
        self.db = DataBaseClient(url, login='test', password='password')

    def find_feeds_in_db(self, feed_type=None, feed_value=None):
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)

        select_from_table = ['value', 'type']
        condition = table.c.type == feed_type
        condition &= table.c.value == feed_value
        return self.db.execute_select(table, select_from_table, condition=condition)

    def find_user_id_by_name(self, name):
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        select_from_table = 'Id'
        condition = table.c.UserName == name
        condition &= table.c.IsActive == True
        # request = f"""SELECT "Id" FROM "Users" WHERE "UserName" = '{name}' AND "IsActive" = 'true' """
        return self.db.execute_select(table, select_from_table, condition)

    def db_feed_value_check_attr(self, feed_type, feed_value=None, feed_criteria=None):
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        if feed_criteria:
            condition = table.c.type == feed_type
            condition &= table.c.value == feed_value
            condition &= table.c.criteria == feed_criteria
            return self.db.execute_select(table, condition=condition)
        elif not (feed_value and feed_criteria):
            select_from_table = ['value', 'last_af_operations_date', 'af_operations_count']
            condition = table.c.type == feed_type
            condition &= table.c.criteria != None
            condition &= table.c.irrelevant == False
            order_by = table.c.last_af_operations_date
            return self.db.execute_select(table, select_from_table, condition, order_by=order_by)
        else:
            condition = table.c.type == feed_type
            condition &= table.c.value == feed_value
            condition &= table.c.criteria == None
            return self.db.execute_select(table, condition=condition)

    def find_sent_mail(self, text, mail):
        db_name = 'test'
        table_name = 'test'
        select_from_columns = ['id', 'mailbox', 'content', 'created_at']
        table_join_name = 'emailcontact_relation'
        table = self.db._get_table(db_name, table_name)
        table_left_join = self.db._get_table(db_name, table_join_name)
        left_join = table.outerjoin(table_left_join, table.c.id == table_left_join.c.email_id)
        condition = table.c.content.like("%{}%".format(text))
        condition &= table.c.to_raw.like("%{}%".format(mail))
        condition &= table_left_join.c.errors == None
        group_by = table.c.id
        order_by = table.c.created_at
        return self.db.execute_select(table, select_from_columns, condition,
                                      group_by=group_by,
                                      order_by=order_by,
                                      from_obj=left_join)

    def get_cert_hrid_for_incident(self, inc_id):
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        select_columns_from = ['HumanReadableId']
        condition = table.c.IncidentId == inc_id
        return self.db.execute_select(table, select_columns_from, condition=condition)

    def get_cert_id_for_incident(self, inc_id):
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        select_columns_from = ['CertId']
        condition = table.c.IncidentId == inc_id
        return self.db.execute_select(table, select_columns_from, condition=condition)

    def find_token_in_tokens_table(self, token):
        db_name = 'test'
        table_name = 'test'
        table = self.db._get_table(db_name, table_name)
        condition = table.c.Token == token
        return self.db.execute_select(table,condition=condition)

    def db_request_by_id(self, request_id, user_id):
        db_name = 'test'
        schema_name = 'sp_{}'.format(user_id) # Специфично для ЛКУ, для конкретного участника существует своя схема
        table_name = 'test'
        table = self.db._get_table(db_name, table_name, schema=schema_name)
        select_columns_from = ['HrId', 'Subject']
        condition = table.c.Id == request_id
        return self.db.execute_select(table, select_columns_from, condition=condition)

    def db_request_by_list_id(self, request_ids, user_id):
        db_name = 'test'
        schema_name = 'sp_{}'.format(user_id)
        table_name = 'test'
        columns = ['HrId','Subject']
        table = self.db._get_table(db_name, table_name, schema=schema_name)
        condition = table.c.Id.in_(request_ids)
        return self.db.execute_select(table, columns, condition)

    # Служебные запросы
    def db_utc_current_time(self):
        db_name = 'test'
        table_name = 'test'
        self.db._get_table(db_name, table_name)
        return self.db.execute_select_timestamp()

    def pg_stat_activity_request(self):
        db_name = 'test'
        table_name = 'test'
        column_for_report = 'test'
        table = self.db._get_table(db_name, table_name, column=column_for_report)
        return self.db.execute_select_connections(table,column_for_report)
