from framework.platform.api_auto.pl_api_steps.alerts_steps import AlertsActions
from framework.platform.api_auto.pl_api_steps.additional_steps import AdditionalActions
from framework.platform.api_auto.pl_api_steps.sos_steps import SosActions
from framework.platform.api_auto.pl_api_steps.connectors_steps import ConnectorsActions
from framework.platform.api_auto.pl_api_steps.sla_steps import SlaActions
from framework.platform.api_auto.pl_api_steps.tickets_steps import TicketsActions
from framework.platform.api_auto.pl_api_steps.bulletins_steps import BulletinsActions
from framework.platform.api_auto.pl_api_steps.dictionaries_steps import DictionariesActions
from framework.platform.api_auto.pl_api_steps.workflow_engine_steps import WorkflowEngineActions
from framework.platform.api_auto.pl_api_steps.relations_steps import RelationsActions
from framework.platform.api_auto.pl_api_steps.requests_steps import RequestsActions
from framework.platform.api_auto.pl_api_steps.comments_steps import CommentsActions
from framework.platform.api_auto.pl_api_steps.history_steps import HistoryActions
from framework.platform.api_auto.pl_api_steps.tags_steps import TagsActions
from framework.platform.api_auto.pl_api_steps.reports_steps import ReportsActions
from framework.platform.api_auto.pl_api_steps.incidents_steps import IncidentAction


class ApiActions(AlertsActions, SosActions, ConnectorsActions, SlaActions, IncidentAction,
                 AdditionalActions, TicketsActions, BulletinsActions, DictionariesActions, WorkflowEngineActions,
                 RelationsActions, RequestsActions, CommentsActions, HistoryActions, TagsActions, ReportsActions):
    pass
