from json import dumps
from time import sleep
from contextlib import contextmanager
from pprint import pformat

import allure
import requests
import logging


class ApiException(Exception):
    pass


def decorator_for_allure_attach(req_method):
    def decorator_for_allure(method):
        def decor(self, url, **kwargs):
            req_data = kwargs.get('json') if kwargs.get('json') else " "
            allure.attach(dumps(req_data, indent=2, ensure_ascii=False), '%s запрос на %s' % (req_method, url),
                          allure.attachment_type.JSON)
            resp = method(self, url, **kwargs)
            try:
                allure.attach(dumps(resp.json(), indent=2, ensure_ascii=False), 'Ответ (код %s) на %s %s' %
                              (resp.status_code, req_method, url), allure.attachment_type.JSON)
            except Exception:
                allure.attach(resp.text, 'Ответ (код %s) на %s %s' % (resp.status_code, req_method, url),
                              allure.attachment_type.TEXT)
            return resp
        return decor
    return decorator_for_allure


class UserClient:
    """Клиент для GatewayAPI с автологином указанным пользователем

    Для работы нужно открыть сессию контекстным менеджером

    Пример использования::

        client = UserClient(
            auth_url='http://name:port',
            login='login',
            password='password')
        with client.session():
            result = client.get('https://name/api/hand')

    """
    REAUTH_ATTEMPTS = 3  # количество попыток переподключения в случае если логин не удался/отвалился

    GET = 'get'
    POST = 'post'
    PUT = 'put'
    DELETE = 'delete'

    def __init__(self, auth_url, login, password, timeout=None):
        self.auth_url = auth_url
        self.log = logging.getLogger(__name__)
        self.login = login
        self.password = password
        self.timeout = timeout
        self._session = None

    @contextmanager
    def session(self):
        if self._session is None:
            self._session = requests.Session()
            yield
            self._session = None
        else:
            # session presumably is already created
            yield

    def _base_request(self, method, url, log_data=True, **kwargs):
        if 'verify' not in kwargs:
            kwargs['verify'] = False  # default verify to False just in case
        if self.timeout is not None:
            kwargs['timeout'] = self.timeout
        request_data = kwargs
        if not log_data:
            request_data.pop('data')
        self.log.info('Making %s request, url - %s', method, url)
        self.log.debug('%s request, url - %s, kwargs:\n%s', method, url, pformat(request_data))
        if self._session is None:
            raise ApiException('No session is established')
        request = self._session.__getattribute__(method)
        resp = request(url, **kwargs)
        self.log.info('Response on %s %s recevied, status code - %s', method, url, resp.status_code)
        self.log.debug(u'Response on %s %s, body:\n%s', method, url, resp.text)
        return resp

    def _auth_post(self, url):
        credentials = {
            "login": self.login,
            "password": self.password
        }
        resp = self._base_request(self.POST, url, json=credentials, verify=False)
        if not resp.ok:
            raise ApiException('Authorization failed: {}'.format(resp.text))

    def _authorize(self):
        if ('access_token' in self._session.cookies) or ('.AspNet.Cookies' in self._session.cookies):
            return
        self._auth_post(self.auth_url + '/api/account/login')

    def _auto_auth_request(self, method, url, reauth_attempt=0, **kwargs):
        self._authorize()
        headers = kwargs.pop('headers', {})
        resp = self._base_request(method, url, **kwargs, headers=headers)
        if resp.status_code == 401:
            self.token = None
            if reauth_attempt > self.REAUTH_ATTEMPTS:
                raise ApiException('Exceeded {} re-authorizations attempts '.format(self.REAUTH_ATTEMPTS))
            self.log.debug('Re-authorizing')
            resp = self._auto_auth_request(method, url, reauth_attempt=reauth_attempt + 1, **kwargs)
        return resp

    def _request(self, method, url, **kwargs):
        try:
            resp = self._auto_auth_request(method, url, **kwargs)
            return resp.status_code, resp.text
        except ApiException:
            raise
        except Exception:
            self.log.exception('Connection issues occurred')
            raise ApiException('Connection issues occurred')

    def post(self, url, data, **kwargs):
        response_code, response_data = self._request(self.POST, url, json=data, **kwargs)
        return response_code, response_data

    def put(self, url, data, **kwargs):
        response_code, response_data = self._request(self.PUT, url, json=data, **kwargs)
        return response_code, response_data

    def get(self, url, **kwargs):
        response_code, response_data = self._request(self.GET, url, **kwargs)
        return response_code, response_data

    def delete(self, url, **kwargs):
        response_code, response_data = self._request(self.DELETE, url, **kwargs)
        return response_code, response_data


class AutoCheckUserClient(UserClient):

    def __init__(self, auth_url, login, password, timeout=None):
        super().__init__(auth_url=auth_url, login=login, password=password, timeout=timeout)
        if self._session is None:
            self.authorize()

    def _bare_request(self, method, url, allowed_codes=None, **kwargs):
        try:
            resp = self._auto_auth_request(method, url, **kwargs)
        except ApiException:
            raise
        except Exception:
            self.log.exception('Connection issues occurred')
            raise ApiException('Connection issues occurred')
        if 499 < resp.status_code < 600:
            allure.attach(resp.text, 'Ответ (код %s) на %s' % (resp.status_code, url),
                          allure.attachment_type.TEXT)
            assert False, 'Response code {} is not expected. Body: {}'.format(resp.status_code, resp.text)
        if allowed_codes is not None and resp.status_code not in allowed_codes:
            self.log.debug(u'Response on %s %s, body:\n%s', method, url, resp.text)
            allure.attach(resp.text, 'Ответ (код %s) на %s' % (resp.status_code, url),
                          allure.attachment_type.TEXT)
            raise ApiException('Response code {} is not expected, expected {}'.format(resp.status_code, allowed_codes))
        return resp

    def _request(self, method, url, allowed_codes=None, retry_attempts=0, retry_delay=1, **kwargs):
        for retry_attempt in range(retry_attempts + 1):
            try:
                resp = self._bare_request(
                    method=method,
                    url=url,
                    allowed_codes=allowed_codes,
                    **kwargs)
                return resp
            except ApiException:
                if retry_attempt < retry_attempts:
                    sleep(retry_delay)
                    continue
                else:
                    raise

    def authorize(self):
        if self._session is None:
            self._session = requests.Session()
        for retry_attempt in range(10):
            try:
                self._authorize()
                return
            except Exception:
                self.log.info('Failed to login to url %s with login %s and password %s, retry attempt %i',
                              self.auth_url, self.login, self.password, retry_attempt)
                if retry_attempt < 9:
                    sleep(5)
                    continue
                else:
                    raise

    @decorator_for_allure_attach('POST')
    def post(self, url, allowed_codes=None, **kwargs):
        resp = self._request(method=self.POST, url=url, allowed_codes=allowed_codes, **kwargs)
        return resp

    @decorator_for_allure_attach('PUT')
    def put(self, url, allowed_codes=None, **kwargs):
        resp = self._request(method=self.PUT, url=url, allowed_codes=allowed_codes, **kwargs)
        return resp

    def get(self, url, allowed_codes=None, **kwargs):
        return self._request(
            method=self.GET,
            url=url,
            allowed_codes=allowed_codes,
            **kwargs)

    def delete(self, url, allowed_codes=None, **kwargs):
        return self._request(
            method=self.DELETE,
            url=url,
            allowed_codes=allowed_codes,
            **kwargs)


class ExternalApiUserClient(AutoCheckUserClient):
    """ Клиент для External Api """

    def __init__(self, auth_url, login, password, timeout=None):
        super().__init__(auth_url=auth_url, login=login, password=password, timeout=timeout)
        self.token = None

    def get_token(self):
        return self.token

    def _base_request(self, method, url, **kwargs):
        if 'verify' not in kwargs:
            kwargs['verify'] = False
        if self.timeout is not None:
            kwargs['timeout'] = self.timeout
        request_data = kwargs
        self.log.info('Making %s request, url - %s', method, url)
        self.log.debug('%s request, url - %s, kwargs:\n%s', method, url, pformat(request_data))
        request = requests.__getattribute__(method)
        resp = request(url, **kwargs)
        self.log.info('Response on %s %s recevied, status code - %s', method, url, resp.status_code)
        self.log.debug('Response on %s %s, body:\n%s', method, url, resp.text)
        return resp

    def _authorize(self):
        url = self.auth_url + '/api/v1/account/login'
        credentials = {
            "login": self.login,
            "password": self.password
        }
        resp = self._base_request(self.POST, url, json=credentials)
        if not resp.ok:
            raise ApiException('Authorization failed: {}'.format(resp.text))
        self.token = resp.text

    def _auto_auth_request(self, method, url, reauth_attempt=0, need_auto_auth=True, **kwargs):
        if not self.token:
            self._authorize()
        headers = kwargs.pop('headers', {})
        headers['Authorization'] = 'Bearer {}'.format(self.token)
        resp = self._base_request(method, url, **kwargs, headers=headers)
        if resp.status_code == 401 and need_auto_auth:
            self.token = None
            if reauth_attempt > self.REAUTH_ATTEMPTS:
                raise ApiException('Exceeded %s re-auth attempts'.format(self.REAUTH_ATTEMPTS))
            self.log.debug('Re-authorizing')
            resp = self._auto_auth_request(method, url, reauth_attempt=reauth_attempt + 1, **kwargs)
        return resp

    def authorize(self, retry_attempts=0, retry_delay=1):
        for retry_attempt in range(retry_attempts + 1):
            try:
                self._authorize()
                return
            except Exception:
                self.log.debug('Failed to login to url %s with login %s and password %s',
                               self.auth_url, self.login, self.password)
                if retry_attempt < self.REAUTH_ATTEMPTS:
                    sleep(retry_delay)
                    continue
                else:
                    raise


class IamUserClient(AutoCheckUserClient):
    def __init__(self, auth_url, login, password, timeout=None):
        super().__init__(auth_url=auth_url, login=login, password=password, timeout=timeout)

    def _auth_post(self, url):
        credentials = {
            "username": self.login,
            "password": self.password
        }
        resp = self._base_request(self.POST, url, json=credentials, verify=False)
        if not resp.ok:
            raise ApiException('Authorization failed: {}'.format(resp.text))

    def _authorize(self):
        if ('access_token' in self._session.cookies) or ('.AspNet.Cookies' in self._session.cookies):
            return
        self._auth_post(self.auth_url + '/ui/login')
