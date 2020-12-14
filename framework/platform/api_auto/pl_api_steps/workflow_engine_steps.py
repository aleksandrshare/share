from framework.platform.api_auto.pl_services.int_api_services import ApiServices
import os
from tools.utils import TEST_ROOT_DIR, read_yaml_from_file_with_ruyaml, write_yaml_to_file_with_ruyaml


class WorkflowEngineActions(ApiServices):
    """"""

    we_rule_path = os.path.join(TEST_ROOT_DIR, 'test_data')
    we_assign_operator_on_alert_rule = os.path.join(TEST_ROOT_DIR, 'test_data',
                                                    'scenarios.assign_operator_to_alert.yaml')
    we_remote_directory = '/C:/ProgramData/Positive Technologies/PT IPC/Configurations/PT.SP.WorkflowEngineService/work'
    we_service_name = 'PT.SP.WorkflowEngineService'

    def _we_change_operator_in_assign_operator_on_alert_rule(self, operator_id):
        """"""
        data = read_yaml_from_file_with_ruyaml(self.we_rule_path, self.we_assign_operator_on_alert_rule)
        data['rules'][0]['scenario']['parameters']['operatorToAssign'] = operator_id
        write_yaml_to_file_with_ruyaml(self.we_rule_path, self.we_assign_operator_on_alert_rule, data)

    def we_add_assign_operator_on_alert_scenario_on_host(self, operator_id=None):
        """"""
        if not operator_id:
            operator_id = self.sa_get_operator()['id']
        self._we_change_operator_in_assign_operator_on_alert_rule(operator_id)
        remote_file_list = self.ssh_client.ftp_copy_file_list_to_dir_with_backup([self.we_assign_operator_on_alert_rule],
                                                                                 self.we_remote_directory)
        self.ssh_client.ssh_restart_win_service(self.we_service_name)
        return remote_file_list

    def we_restore_files_and_restart_we_service(self, file_list):
        """"""
        self.ssh_client.ftp_restore_file_list_from_backup(file_list)
        self.ssh_client.ssh_restart_win_service(self.we_service_name)