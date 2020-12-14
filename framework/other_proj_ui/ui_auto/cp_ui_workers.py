from framework.other_proj_ui.ui_auto import CertPagesActions
from framework.other_proj_ui.ui_auto.locators.cp_locators import CertPortalLocators
from framework.api_libs.user_client import AutoCheckUserClient
from configs import settings


class CertPortalAdminClass(CertPagesActions):
    def __init__(self, driver, stand_group):
        self.locators = CertPortalLocators()
        self.stands = settings.stands
        self.LOGIN = self.stands[stand_group]['CERT_ADMIN_CRED']['LOGIN']
        self.PASSWORD = self.stands[stand_group]['CERT_ADMIN_CRED']['PASSWORD']
        self.URL = self.stands[stand_group]['CERT_URL']
        super().__init__(driver, self.URL)
        self.api_client = AutoCheckUserClient(auth_url=self.URL, login=self.LOGIN, password=self.PASSWORD)
