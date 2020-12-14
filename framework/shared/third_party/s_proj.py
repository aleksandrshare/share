from datetime import datetime, timedelta
import logging
from random import choice
from configs.dictionary_variables import severity, influence, incident_types
from tools.utils import now_timestamp, random_email
from time import sleep


class SiemActions:
    def __init__(self, siem_group_id):
        self.group_id = siem_group_id
        self.log = logging.getLogger(__name__)

    def siem_create_incident(self, robot):
        incident_id = robot.Создать_инцидент(расположение=self.group_id,
                                             описание=f'инцидент. Создан автотестами {now_timestamp()}')
        self.log.info(f'В SIEM создан инцидент с id {incident_id}')
        return incident_id

    def siem_get_assets_table_info(self, robot):
        """ Получить данные таблицы активов"""
        if self.group_id != '00000000-0000-0000-0000-000000000002':
            assets = robot.Получить_данные_таблицы_активов(запрос='select(Host.IpAddress, Host.Hostname)',
                                                           фильтр_групп=self.group_id)
        else:
            assets = robot.Получить_данные_таблицы_активов(запрос='select(Host.IpAddress, Host.Hostname)')
        return assets

    def siem_create_event(self, robot, correlation_type='event'):
        """ Создать событие. Оно создается для актива группы, указанной при инициализации класса"""
        assets = self.siem_get_assets_table_info(robot)
        if not assets:
            self.siem_create_asset(robot)
            assets = self.siem_get_assets_table_info(robot)
        asset = choice(assets)
        event_dict = dict()
        event_dict['event_src.host'] = asset['Host.Hostname']
        event_dict['event_src.ip'] = asset['Host.IpAddress']
        event_id = robot.Отправить_событие_в_SIEM(correlation_type=correlation_type,
                                                  correlation_name='ручная_корреляция',
                                                  **event_dict)
        self.log.info(f'В SIEM создано событие с id {event_id}')

        self.log.info('Ждем появление события в SIEM')
        robot.Дождаться_появления_отправленных_событий(event_id)
        self.log.info('Событие появилось в SIEM')

        return event_id

    def siem_create_linked_event_and_incident(self, robot, correlation_type='event'):
        """ Создать событие и инцидент и связать их"""
        event_id = self.siem_create_event(robot, correlation_type)
        incident_id = self.siem_create_incident(robot)
        inc_key = robot.Получить_ключ_инцидента(incident_id)

        self.log.info('В SIEM связываем событие и инцидент')
        robot.Связать_события_с_инцидентом(inc_key, event_id)
        return event_id, incident_id

    def siem_create_incidents_with_all_types(self, robot):
        """ Создать инциденты всех возможных типов """
        all_inc = list()
        for inc_type in incident_types:
            new_severity = choice(new_severity)
            new_influence = choice(new_influence)
            inc_id = robot.Создать_инцидент(расположение=self.group_id,
                                            описание=f'Siem инцидент. Создан автотестами {now_timestamp()}',
                                            тип=inc_type, влияние=new_influence, опасность=new_severity)
                                            #,ответственный=operator)
            self.log.info(f'В SIEM создан инцидент с id {inc_id}')
            inc_data = robot.Открыть_инцидент(inc_id)
            all_inc.append(inc_data)
        return all_inc

    def siem_edit_incident(self, robot, inc_id):
        """ Отредактировать инцидент """
        robot.Отредактировать_инцидент(inc_id, описание=f'Siem инцидент edit. Время редактирования {now_timestamp()}',
                                       дата_обнаружения=(datetime.utcnow() - timedelta(days=2)).strftime('%d.%m.%Y %H:%M:%S'),
                                       тип=choice(incident_types))
        inc_data = robot.Открыть_инцидент(inc_id)
        return inc_data

    def siem_create_asset(self, robot):
        """ Создать актив """
        return robot.Создать_актив(группы=self.group_id, ip_address=robot.Уникальный_IPAddress(),
                                   fqdn=robot.Уникальный_FQDN())

    def siem_change_incident_status(self, inc_id, robot, status):
        """ Изменить статус инцидента """
        robot.Изменить_статус_инцидента(inc_id, статус=status, сообщение=f'Изменен статус инцидента в {now_timestamp()}')

    def siem_check_incident_status(self, inc_id, robot, expected_status):
        """ Проверить, что статус инцидента совпадает с ожидаемым """
        robot.Проверить_инцидент(inc_id, статус=expected_status)

    def siem_create_operator(self, robot):
        """ Создать оператора для сием """
        return robot.Создать_пользователя_для_MPX(фамилия=f'Фамилия_{now_timestamp()}', имя=f'Имя_{now_timestamp()}',
                                                  электронная_почта=random_email())

    def siem_get_modified_date(self, robot, inc_id):
        """ Получить дату изменения инцидента """
        inc_data = robot.Открыть_инцидент(inc_id)
        return inc_data['modified']['date']

    def siem_wait_for_incident_change(self, inc_id, old_date, robot):
        """ Ждем, пока инцидент изменится """
        inc_data = None
        for i in range(30):
            inc_data = robot.Открыть_инцидент(inc_id)
            if inc_data['modified']['date'] != old_date:
                self.log.info(f'Итерация {i}. В SIEM инцидент {inc_id} изменен')
                break
            else:
                self.log.info(f'Итерация {i}. В SIEM инцидент {inc_id} не изменился')
                sleep(5)
        assert inc_data['modified']['date'] != old_date, f'Не дождались изменения инцидента {inc_id} в SIEM'

    def siem_link_event_with_incident(self, robot, event_id, incident_id):
        """ Связать событие и инцидент"""
        self.log.info('В SIEM связываем событие и инцидент')
        inc_key = robot.Получить_ключ_инцидента(incident_id)
        robot.Связать_события_с_инцидентом(inc_key, event_id)

    def siem_delete_link_between_event_and_incident(self, robot, event_id, incident_id):
        """ Удалить связь события с инцидентом"""
        self.log.info('В SIEM удаляем связь события и инцидента')
        robot.Отвязать_событие_от_инцидента(incident_id, event_id)
