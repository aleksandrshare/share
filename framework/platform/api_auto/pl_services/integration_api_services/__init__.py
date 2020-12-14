from framework.platform.api_auto.pl_services.integration_api_services.integration_api_service import IntegrationApiCore
from framework.platform.api_auto.pl_services.int_api_services.incidents_service import IncidentsCore
from framework.platform.api_auto.pl_services.int_api_services.attachments_service import AttachmentsCore


class IntegrApiIncidentsCore(IncidentsCore):
    incidents_prefix = '/api/v1/incidents'


class IntegrApiAttachmentsCore(AttachmentsCore):
    attachments_prefix = '/api/v1/attachments'


class IntegrApiServices(IntegrationApiCore, IntegrApiIncidentsCore, IntegrApiAttachmentsCore):
    pass
