#!/usr/bin/env python
# -*- coding: utf-8 -*-

from framework.other_proj_ui.ui_auto.fc_actions import (LoginPage, MainPageLKO, ReferenceInfoLoading, BaseActions,
                                                     ConfigPageLKO, MainPageLKU, NotificationsPageLKU, MalwareAnalysisEF)
from framework.other_proj_ui.ui_auto.fc_bulletins_actions import BulletinsLkuPage, BulletinsLkoPage
from framework.other_proj_ui.ui_auto.fc_incidents_actions import IncidentsPage
from framework.other_proj_ui.ui_auto.fc_participants_actions import ParticipantsPage
from framework.other_proj_ui.ui_auto.fc_request_actions import RequestsPageLKO, RequestsPageLKU
from framework.other_proj_ui.ui_auto.fc_ef_incident_actions import ModalWinNewIncidentEF
from framework.other_proj_ui.ui_auto.fc_ef_obs_response_actions import ObsResponseEF
from framework.other_proj_ui.ui_auto.fc_threats_actions import ThreatsPage
from framework.other_proj_ui.ui_auto.fc_ef_threat_actions import ThreatsEF
from framework.other_proj_ui.ui_auto.fc_ef_vulnerability_actions import VulnerabilityEF
from framework.other_proj_ui.ui_auto.fc_vulnerability_actions import VulnerabilityPage
from framework.other_proj_ui.ui_auto.fc_info_card_actions import InfoCardPage
from framework.other_proj_ui.ui_auto.fc_ef_pub_actions import PubEF
from framework.other_proj_ui.ui_auto.fc_ef_lockrequest_actions import LockRequestEF
from framework.other_proj_ui.ui_auto.fc_antifraud_actions import AntifraudPage
from framework.other_proj_ui.ui_auto.fc_ef_participant_actions import ParticipantEF
from framework.other_proj_ui.ui_auto.cp_incident_action import CertPortalIncidentsPage


class PagesActions(LoginPage, MainPageLKO, RequestsPageLKO, RequestsPageLKU, ModalWinNewIncidentEF, ParticipantsPage,
                   ReferenceInfoLoading, AntifraudPage, BaseActions, ConfigPageLKO, BulletinsLkoPage, IncidentsPage,
                   MainPageLKU, NotificationsPageLKU, BulletinsLkuPage, ThreatsPage, ThreatsEF, VulnerabilityEF,
                   VulnerabilityPage, InfoCardPage, PubEF, MalwareAnalysisEF, LockRequestEF, ParticipantEF, ObsResponseEF):
    pass


class CertPagesActions(BaseActions, CertPortalIncidentsPage):
    pass
