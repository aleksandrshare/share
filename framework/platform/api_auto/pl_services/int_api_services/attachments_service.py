# coding=utf-8
from uuid import uuid1
from framework.api_libs.user_client import AutoCheckUserClient


class AttachmentsCore(AutoCheckUserClient):
    """"""
    attachments_prefix = 'handler'

    def download_attachment(self, attach_id, allowed_codes=[200], retry_attempts=0, retry_delay=1):
        """"""
        url = self.auth_url + self.attachments_prefix + f'/{attach_id}/download'
        with self.session():
            data = self.get(url=url, verify=False, allowed_codes=allowed_codes,
                            retry_attempts=retry_attempts, retry_delay=retry_delay)
        return data.text, dict(data.headers)

    def upload_attachment(self, file_name, file_obj, file_size, allowed_codes=[200], retry_attempts=0,
                          retry_delay=1, need_auto_auth=True, need_response=True):
        """"""
        url = self.auth_url + self.attachments_prefix + '/upload'
        filedata = [('file', ('blob', file_obj, 'application/octet-stream'))]

        data = {
            "flowChunkNumber": 1,
            "flowChunkSize": 1048576,
            "flowCurrentChunkSize": file_size,
            "flowFilename": file_name,
            "flowId": str(uuid1()),
            "flowIdentifier": f"{file_size}-{file_name.replace('.', '')}",
            "flowRelativePath": file_name,
            "flowTotalChunks": 1,
            "flowTotalSize": file_size,
            "fileType": "other",
            "file": file_obj
        }
        with self.session():
            response = self.post(url=url, data=data, files=filedata, allowed_codes=allowed_codes,
                                 retry_attempts=retry_attempts, retry_delay=retry_delay,
                                 need_auto_auth=need_auto_auth)
        if need_response:
            return response.json()
