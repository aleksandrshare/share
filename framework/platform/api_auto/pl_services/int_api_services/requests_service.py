from framework.api_libs.user_client import AutoCheckUserClient


class RequestsCore(AutoCheckUserClient):
    """"""
    requests_prefix = 'handler'

    def get_requests(self, search_query=None, req_filter=None, user_filters=None, sort=None, sort_order=None,
                     assigned_to=None, participant=None, limit=None, offset=None, min_created_date=None,
                     max_created_date=None, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.requests_prefix + '?'
        if search_query:
            url += f'&searchQuery={search_query}'
        if req_filter:
            url += f'&filter={req_filter}'
        if user_filters:
            url += f'&userFilters={user_filters}'
        if sort:
            url += f'&sort={sort}'
        if sort_order:
            url += f'&sortOrder={sort_order}'
        if assigned_to:
            url += f'&assignedTo={assigned_to}'
        if participant:
            url += f'&participant={participant}'
        if limit:
            url += f'&limit={limit}'
        if offset:
            url += f'&offset={offset}'
        if min_created_date:
            url += f'&minCreatedDate={min_created_date}'
        if max_created_date:
            url += f'&maxCreatedDate={max_created_date}'
        with self.session():
            response = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                                retry_attempts=retry_attempts, retry_delay=retry_delay)
        return response.json()
