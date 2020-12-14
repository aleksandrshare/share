from framework.shared.services.configuration_service import ConfigurationCore
from framework.shared.services.custom_dictionaries_service import CustomDictionariesCore
from framework.shared.services.dictionaries_service import DictionariesCore
from framework.shared.services.sos_service import SubjectsObjectsSystemsCore
from framework.platform.api_auto.pl_services.int_api_services.connectors_service import ConnectorsCore
from framework.platform.api_auto.pl_services.int_api_services.history_service import HistoryCore
from framework.shared.services.fias_service import FiasCore
from framework.platform.api_auto.pl_services.int_api_services.notification_service import NotificationCore
from framework.platform.api_auto.pl_services.int_api_services.tickets_service import TicketsCore
from framework.platform.api_auto.pl_services.int_api_services.bulletins_service import BulletinsCore
from framework.platform.api_auto.pl_services.int_api_services.attachments_service import AttachmentsCore
from framework.shared.services.system_info_service import SystemInfoCore
from framework.platform.api_auto.pl_services.int_api_services.general_service import ConfigurationFilesCore
from framework.platform.api_auto.pl_services.int_api_services.references_sevice import ReferencesCore, TagsCore
from framework.platform.api_auto.pl_services.int_api_services.requests_service import RequestsCore
from framework.platform.api_auto.pl_services.int_api_services.comments_service import CommentCore
from framework.platform.api_auto.pl_services.int_api_services.reports_service import ReportsCore
from framework.platform.api_auto.pl_services.int_api_services.incidents_service import IncidentsCore


class ApiServices(CustomDictionariesCore, DictionariesCore, SubjectsObjectsSystemsCore, IncidentsCore,
                  ConfigurationCore, ConnectorsCore, FiasCore, HistoryCore, NotificationCore, TicketsCore,
                  BulletinsCore, AttachmentsCore, SystemInfoCore, ConfigurationFilesCore, ReferencesCore,
                  RequestsCore, CommentCore, TagsCore, ReportsCore):
    """
    Класс, объединяющий в себе все методы отправки API запросов всех возможных сервисов
    """
    pass
