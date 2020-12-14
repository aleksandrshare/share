#!/usr/bin/env python
# -*- coding: utf-8 -*-
from framework.platform.api_auto.pl_api_workers import CertPortalApiAdmin
import pytest


@pytest.fixture(scope='session')
def portal_admin():
    client = CertPortalApiAdmin()
    return client


@pytest.fixture(scope='session')
def is_gos_proj_bulletin_import_enabled(lko_admin):
    if not lko_admin.check_connector_part_enabled('gos_proj', 'Import'):
        pytest.skip('Не активен импорт из gos_proj: либо не настроен коннектор к gos_proj')
