from framework.other_proj_ui.ui_auto import PagesActions
from framework.other_proj_ui.queries.fc_pg_queries import PgSQLQueries
from framework.other_proj_ui.ui_auto.locators.fc_locators import LocatorsLKU, LocatorsLKO
from framework.platform.api_auto.pl_services.int_api_services.incidents_service import IncidentsCore
from configs import settings


"""
Классы ниже наследуют все классы работы cо сраницами, используются как рабочие классы в тестах 
"""


class LKUclass(PagesActions):
    def __init__(self, driver, url, users_dss_pin):
        self.stand = 'lku'
        self.stands = settings.stands
        self.bd_stand = self.stands[url]['LKU_POSTGRES']
        self.db_client = PgSQLQueries(self.bd_stand)
        self.locators = LocatorsLKU()
        self.LOGIN = self.stands[url]['LKU_CRED_PAYER']['LOGIN']
        self.PASSWORD = self.stands[url]['LKU_CRED_PAYER']['PASSWORD']
        self.LKU_URL = self.stands[url]['LKU_URL']
        self.LOGIN_PAYEE = self.stands[url]['LKU_CRED_PAYEE']['LOGIN']
        self.PASSWORD_PAYEE = self.stands[url]['LKU_CRED_PAYEE']['PASSWORD']
        self.LOGIN_PARTICIPANT_EDIT = self.stands[url]['LKU_CRED_PARTICIPANT_EDIT']['LOGIN']
        self.PASSWORD_PARTICIPANT_EDIT = self.stands[url]['LKU_CRED_PARTICIPANT_EDIT']['PASSWORD']
        self.dss_pin_payer = users_dss_pin['PAYER']
        self.dss_pin_payee = users_dss_pin['PAYEE']
        super().__init__(driver, self.LKU_URL, self.LOGIN, self.PASSWORD)
        self.api_client = IncidentsCore(auth_url=self.LKU_URL, login=self.LOGIN, password=self.PASSWORD)
        self.api_client_payee = IncidentsCore(auth_url=self.LKU_URL,
                                           login=self.LOGIN_PAYEE, password=self.PASSWORD_PAYEE)
        self.api_client_participant_edit = IncidentsCore(auth_url=self.LKU_URL, login=self.LOGIN_PARTICIPANT_EDIT,
                                                      password=self.PASSWORD_PARTICIPANT_EDIT)


class LKOOclass(PagesActions):
    def __init__(self, driver, url):
        self.stand = 'lko'
        self.stands = settings.stands
        self.bd_stand = self.stands[url]['LKOO_POSTGRES']
        self.db_client = PgSQLQueries(self.bd_stand)
        self.locators = LocatorsLKO()
        self.LOGIN = self.stands[url]['LKO_CRED']['LOGIN']
        self.PASSWORD = self.stands[url]['LKO_CRED']['PASSWORD']
        self.LKOO_URL = self.stands[url]['LKOO_URL']
        super().__init__(driver, self.LKOO_URL, self.LOGIN, self.PASSWORD)
        self.api_client = IncidentsCore(auth_url=self.LKOO_URL, login=self.LOGIN, password=self.PASSWORD)


class LKOZclass(PagesActions):
    def __init__(self, driver, url):
        self.stand = 'lko'
        self.stands = settings.stands
        self.bd_stand = self.stands[url]['LKOZ_POSTGRES']
        self.db_client = PgSQLQueries(self.bd_stand)
        self.locators = LocatorsLKO()
        self.LOGIN = self.stands[url]['LKO_CRED']['LOGIN']
        self.PASSWORD = self.stands[url]['LKO_CRED']['PASSWORD']
        self.LKOZ_URL = self.stands[url]['LKOZ_URL']
        super().__init__(driver, self.LKOZ_URL, self.LOGIN, self.PASSWORD)
        self.api_client = IncidentsCore(auth_url=self.LKOZ_URL, login=self.LOGIN, password=self.PASSWORD)
