from framework.api_libs.user_client import AutoCheckUserClient


class NotificationCore(AutoCheckUserClient):
    """"""
    notification_prefix = '/api/notifications'

    def get_unread_notifications(self, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        url = self.auth_url + self.notification_prefix + '?filter=unread'
        with self.session():
            data = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()

    def mark_notifications_as_read(self, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        url = self.auth_url + self.notification_prefix + '/markAllAsRead'
        with self.session():
            data = self.post(url=url, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.json()