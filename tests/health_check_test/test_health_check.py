#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import logging
from tools.healthcheck import platform_health_check_services, health_check_db_rabbit
from configs import settings
import os

logger = logging.getLogger(__name__)
stands = settings.stands


def write_on_file(service_name):
    with open('service.name', 'w+') as file:
        if isinstance(service_name, str):
            file.write(service_name)
        else:
            file.write(' '.join(service_name))


def test_health(stand, lko_admin):
    logger.info("!!! Started services health check !!!")
    try:
        conf_check = lko_admin.check_config_draft()
        result_r_db = health_check_db_rabbit(stands[stand]['LKO_RABBIT'], stands[stand]['LKO_POSTGRES'])
        result_service, service_name = platform_health_check_services(stands[stand]['LKO_URL'], lko_admin)
    except KeyError as ex:
        write_on_file("ERROR probably the stand is not in the list of test stands, error text: " + str(ex))
        raise
    except Exception as ex:
        write_on_file("ERROR text: " + str(ex))
        raise
    if result_r_db and result_service and conf_check:
        logger.info('All services are available')
    else:
        os.environ["SERVICES_NAME"] = str(service_name)
        write_on_file(' '.join(service_name))
        pytest.fail(f"There are unavailable services {service_name} during health check!!! "
                    "see the test.log file for more detailed information ")
