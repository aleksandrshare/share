from random import choice
from selenium.webdriver.common.by import By
from configs.settings import type_ext, type_int


def collect_inc_param():
    vector_code = ('EXT', 'INT')
    law_enforcement_request = ('POL', 'NPL', 'UNKW')
    vector = choice(vector_code)
    if vector == 'EXT':
        inc_type = choice(type_ext)
    else:
        inc_type = choice(type_int)
    params = {
        'vector': vector,
        'inc_type': inc_type,
        'assistance': choice([True, False]),
        'law_enforcement_request': choice(law_enforcement_request)
    }
    return params


def collect_obs_param(need_payee_request=None):
    org_type = ('company', 'individual')
    antifraud_type_with_payee_req = ('paymentCard', 'bankAccount', 'swift', 'retailAtm')
    antifraud_type_without_payee_req = ('phoneNumber', 'eWallet', 'other')
    antifraud_type_payer = antifraud_type_with_payee_req + antifraud_type_without_payee_req
    if need_payee_request is True:
        antifraud_type_payee = antifraud_type_with_payee_req
    elif need_payee_request is False:
        antifraud_type_payee = antifraud_type_without_payee_req
    else:
        antifraud_type_payee = antifraud_type_with_payee_req + antifraud_type_without_payee_req
    params = {
        'org_type': choice(org_type),
        'payee_type': choice(antifraud_type_payee),
        'payer_type': choice(antifraud_type_payer)
    }
    return params


def collect_response_params():
    org_type = ('company', 'individual')
    transfer_suspension = ('suspended', 'unableToSuspend')
    transfer_state = ('unknown', 'rejected', 'confirmed', 'notConfirmed')

    params = {
        'org_type': choice(org_type),
        'transfer_suspension': choice(transfer_suspension),
        'transfer_state': choice(transfer_state)
    }
    return params


def choose_transfer_suspension(suspension_key):
    transfer_suspension = {
        'suspended': 'Приостановлен',
        'unableToSuspend': 'Невозможно приостановить'
    }
    return transfer_suspension[suspension_key]


def choose_transfer_state(state_key):
    transfer_state = {
        'unknown': 'Нет информации',
        'rejected': 'Возврат денежных средств',
        'confirmed': 'Подтверждение получено',
        'notConfirmed': 'Подтверждение не получено'
    }
    return transfer_state[state_key]


def collect_locator(locator_pattern, *text):
    return By.XPATH, locator_pattern.format(*text)


def choose_inc_vector_and_type(inc_vector, inc_type):
    inc_vector_dict = {
        'EXT': 'Направлен на клиента участника',
        'INT': 'Направлен на инфраструктуру участника'
    }

    inc_ext_type = {

        'malware': 'Использование вредоносного программного обеспечения',
        'socialEngineering': 'Использование методов социальной инженерии',
        'vulnerabilities': 'Эксплуатация уязвимостей информационной инфраструктуры',
        'spams': 'Реализация спам рассылки',
        'controlCenters': 'Взаимодействие с центрами ботнетов',
        'sim': 'Изменения IMSI на SIM-карте, смена IMEI телефона',
        'phishingAttacks': 'Использование фишинговых ресурсов',
        'prohibitedContents': 'Размещение запрещенного контента в интернете',
        'maliciousResources': 'Размещение вредоносного ресурса в интернете',
        'other': 'Иная компьютерная атака'
    }

    inc_int_type = {
        'trafficHijackAttacks': 'Изменение маршрутно-адресной информации',
        'malware': 'Использование вредоносного программного обеспечения',
        'socialEngineering': 'Использование методов социальной инженерии',
        'atmAttacks': 'Реализация несанкционированного доступа к банкоматам и платежным терминалам',
        'vulnerabilities': 'Эксплуатация уязвимостей информационной инфраструктуры',
        'bruteForces': 'Компрометация аутентификационных (учетных) данных',
        'ddosAttacks': 'Реализация атаки типа «отказ в обслуживании»',
        'spams': 'Реализация спам рассылки',
        'controlCenters': 'Взаимодействие с центрами ботнетов',
        'phishingAttacks': 'Использование фишинговых ресурсов',
        'prohibitedContents': 'Размещение запрещенного контента в интернете',
        'maliciousResources': 'Размещение вредоносного ресурса в интернете',
        'scanPorts': 'Выполнение сканирования портов',
        'changeContent': 'Выполнение изменения контента',
        'other': 'Иная компьютерная атака'
    }

    vector = inc_vector_dict[inc_vector]
    if inc_vector == 'EXT':
        chosen_type = inc_ext_type[inc_type]
    else:
        chosen_type = inc_int_type[inc_type]
    return vector, chosen_type


def detected_by_value(vector):
    detected_by = {
        'EXT': ['Обнаружено Antifraud КО', 'Обнаружено клиентом КО'],
        'INT': 'Для INT инцидентов'
    }
    detected_types = detected_by[vector]
    if isinstance(detected_types, list):
        text = choice(detected_types)
    else:
        text = detected_types
    return text


def choose_law_enforcement_req_type(law_enforcement_req):
    law_enforcement_req_type = {
        'POL': 'Совершено',
        'NPL': 'Не совершено',
        'UNKW': 'Нет информации',
    }
    law_text = law_enforcement_req_type[law_enforcement_req]
    return law_text


def get_antifraud_type(obs_type):
    antifraud_type = {
        'paymentCard': 'Карта',
        'phoneNumber': 'Телефон',
        'eWallet': 'Электронный кошелек',
        'bankAccount': 'Счет в банке',
        'other': 'Иной идентификатор',
        'swift': 'SWIFT транзакция',
        'retailAtm': 'Retail/ATM транзакция'
    }
    return antifraud_type[obs_type]


def decorator_for_change_selenium_wait_and_return_after(new_wait=20):
    # принимает параметр для выставления таймаута int
    def wait_decorator(action):
        """декоратор запоминает старое значение selenium wait, устанавливает переданное
        и после вызывает передаваемую функцию

        :param action: обект метода класса для выполнения
        :type action: function
        """
        def change_wait(self, *args, **kwargs):
            from selenium.webdriver.support.ui import WebDriverWait
            old_wait = self.wait._timeout
            self.wait = WebDriverWait(self.driver, new_wait)
            self.log.info("Изменение таймаута selenium wait, старый: %s \t новый: %s" % (old_wait, self.wait._timeout))
            result = action(self, *args, **kwargs)
            self.wait = WebDriverWait(self.driver, old_wait)
            self.log.info("Вернули дефолтный таймаут selenium wait: %s" % self.wait._timeout)
            return result
        return change_wait
    return wait_decorator



