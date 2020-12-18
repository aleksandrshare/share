#!/usr/bin/env python
# -*- coding: utf-8 -*-
from framework.api_libs.user_client import IamUserClient


class IamCore(IamUserClient):
    iam_prefix = 'handler'

    def get_iam_sites(self):
        url = self.auth_url + self.iam_prefix + '/sites'
        with self.session():
            response = self.get(url=url, verify=False)
        return response.json()

    def get_iam_site_users(self, site_id):
        url = self.auth_url + self.iam_prefix + f'/users?siteId={site_id}'
        with self.session():
            response = self.get(url=url, verify=False)
        return response.json()
