from framework.platform.api_auto.pl_services.int_api_services import ApiServices
import backoff


class ReportsActions(ApiServices):
    """"""
    def repa_get_incident_export_task_id(self):
        """"""
        resp = self.get_task_id_incident_export_report(allowed_codes=[202])
        assert resp, "The response should not be empty!"
        return resp.get('taskId')

    @backoff.on_exception(backoff.constant, AssertionError, interval=1, max_time=15)
    def repa_get_attach_id(self, task_id):
        """"""
        resp = self.get_report_id(task_id)
        assert resp, "The response should not be empty!"
        status = resp.get('status')
        if status:
            if status != 'completed':
                assert False, "Report has incorrect status {}".format(status)
        return resp.get('attachmentId')

    def repa_api_download_incident_export(self):
        """"""
        task_id = self.repa_get_incident_export_task_id()
        if not task_id:
            self.log.error("Report task id cannot be empty or report does not exist.")
            assert  task_id, "Empty report task id!"
        attach_id = self.repa_get_attach_id(task_id)
        if not attach_id:
            self.log.error("Report's attachment id cannot be empty or does not exist.")
            assert task_id, "Empty report attachment id!"
        report_data = self.download_attachment(attach_id)[0]
        return report_data

    def repa_get_ticket_export_task_id(self):
        """"""
        resp = self.get_task_id_ticket_export_report(allowed_codes=[202])
        assert resp, "The response should not be empty!"
        return resp.get('taskId')

    def repa_api_download_ticket_export(self):
        """"""
        task_id = self.repa_get_ticket_export_task_id()
        if not task_id:
            self.log.error("Report task id cannot be empty or report does not exist.")
            assert task_id, "Empty report task id!"
        attach_id = self.repa_get_attach_id(task_id)
        if not attach_id:
            self.log.error("Report's attachment id cannot be empty or does not exist.")
            assert task_id, "Empty report attachment id!"
        report_data = self.download_attachment(attach_id)[0]
        return report_data

    def repa_transform_text_report_to_list(self, report_data, need_reverse):
        """"""
        if isinstance(report_data, str):
            report_list = report_data.split('\n')
            report_list.pop(0)
        else:
            self.log.error('Report should be in pure text format. Skip transforming...')
            return [report_data]
        if need_reverse:
            report_list.reverse()
        return report_list

    def repa_check_entity_in_report(self, ids_list, report_data, need_reverse=False):
        """"""
        report_list = self.repa_transform_text_report_to_list(report_data, need_reverse)
        list_to_check = []
        for entity_id in ids_list:
            for report_entity in report_list:
                if entity_id in report_entity:
                    entity_exist = True
                    list_to_check.append(report_entity)
                    self.log.debug('Entity {} is presented in report')
                    break
                else:
                    entity_exist = False
            if not entity_exist:
                error = 'Entity {} is not presented in report!!!'.format(entity_id)
                self.log.error(error)
                assert False, error
        return list_to_check
