# coding=utf-8
import logging
import sqlalchemy as sa
from time import sleep


class DataBaseException(Exception):
    pass


class DataBaseClient:
    """Клиент для работы с БД от имени указанного пользователя"""

    def __init__(self, url, login, password):
        self.logger = logging.getLogger(__name__)
        self.login = login
        self.password = password
        self.host = url.split(':')[0]
        self.port = url.split(':')[1]
        self.connection = None
        self.engine = None
        self.retries = 3
        self.timeout = 2

    def _init_engine(self, db_name):
        try:
            self.engine = sa.create_engine('postgresql://{}:{}@{}:{}/{}'.format(self.login, self.password,
                                                                                self.host, self.port, db_name))
            self.connection = self.engine.connect()
            self.logger.debug('Connecting to database {}:{}'.format(self.host, self.port))
        except Exception:
            raise DataBaseException("Database connection failed: {}".format(self.host))

    def _get_table(self, db_name, table_name, schema=None, column=None):
        self._init_engine(db_name)
        if column:
            table = sa.table(table_name, sa.Column(column))
            return table
        metadata = sa.MetaData()
        if schema:
            metadata.schema = schema
        table = sa.Table(table_name, metadata, autoload=True, autoload_with=self.engine)
        return table

    def _close_engine(self):
        self.connection.close()

    def execute_request(self, request):
        try:
            for _ in range(self.retries):
                self.logger.info('Executing db request: {}'.format(request))
                execute_result = self.connection.execute(request)
                execute_result = execute_result.fetchall()
                self.logger.debug('Result: {}'.format(execute_result))
                if not execute_result:
                    sleep(self.timeout)
                else:
                    break
        except Exception:
            self._close_engine()
            self.logger.info('Close connection to database {}:{}'.format(self.host, self.port))
            raise DataBaseException("Failed executing db request")
        self._close_engine()
        return execute_result

    def execute_select_timestamp(self):
        request = sa.select([sa.func.current_timestamp().op('AT TIME ZONE')('UTC')])
        result = self.execute_request(request)
        return result

    def execute_select_connections(self, table, columns=None):
        column_for_report = table.c.get(columns)
        request = sa.select([sa.func.count(column_for_report)])
        result = self.execute_request(request)
        return result

    def execute_select(self, table, need_special_columns=None, condition=None, **kwargs):
        if need_special_columns:
            if isinstance(need_special_columns, list):
                specific_column = []
                for value in need_special_columns:
                    specific_column.append(table.c.get(value))
                request = sa.select(specific_column, condition, **kwargs)
            else:
                specific_column = table.c.get(need_special_columns)
                request = sa.select([specific_column], condition, **kwargs)
        else:
            request = sa.select([table], condition, **kwargs)
        result = self.execute_request(request)
        return result
