from framework.platform.SSH.ssh_core import PlatformSSHCore
import backoff
import pytest
import os


class PlatformSSHClient(PlatformSSHCore):
    """
    Класс работы с системой через ssh и ftp
    """

    def ssh_execute_cmd_command(self, command):
        """
        Метод выполнения команды по ssh

        :param command: команда
        :return: вывод команды
        """
        if isinstance(command, str):
            return self._save_cmd_execution(command)
        elif isinstance(command, list):
            full_data = ''
            for com in command:
                data = self._save_cmd_execution(com)
                full_data += data + '\n'
            return full_data

        else:
            self.logger.error("Unsupported format '{}'".format(command))
        return None

    def ssh_stop_win_service(self, service_name):
        """
        Метод остановки службы Windows по ssh

        :param service_name: название службы
        """
        cur_state = self.ssh_win_service_state(service_name)
        if cur_state != 'stopped':
            command = "sc stop {}".format(service_name)
            self._save_cmd_execution(command)
            cur_state = self.ssh_wait_for_service_state_changed(service_name, 'stopped')
        if cur_state != 'stopped':
            pytest.skip("Win service '{}' has incorrect state '{}'".format(service_name, cur_state))
        self.logger.info("Service '{}' in correct state '{}'".format(service_name, cur_state))

    def ssh_start_win_service(self, service_name):
        """
        Метод запуска службы Windows по ssh

        :param service_name: имя службы
        """
        cur_state = self.ssh_win_service_state(service_name)
        if cur_state != 'running':
            command = "sc start {}".format(service_name)
            self._save_cmd_execution(command)
            cur_state = self.ssh_wait_for_service_state_changed(service_name, 'running')
        if cur_state != 'running':
            pytest.skip("Win service '{}' has incorrect state '{}'".format(service_name, cur_state))
        self.logger.info("Service '{}' in correct state '{}'".format(service_name, cur_state))

    def ssh_restart_win_service(self, service_name):
        """
        Метод перезапуска службы Windows по ssh

        :param service_name: имя службы
        """
        self.ssh_stop_win_service(service_name)
        self.ssh_start_win_service(service_name)

    def ssh_win_service_state(self, service_name):
        """
        Метод получения состояния службы Windows по ssh

        :param service_name: имя службы
        :return: состояние службы
        """
        command = "sc query {}".format(service_name)
        cmd_resp = self._save_cmd_execution(command)
        state = self.ssh_get_cmdline_value(cmd_resp, 'STATE')
        return state.lower()

    @backoff.on_predicate(backoff.constant, lambda correct_state: not correct_state, max_time=60, interval=2)
    def ssh_wait_for_service_state_changed(self, service_name, expected_state):
        """
        Метод повторного получения ожидаемого состояния службы Windows по ssh

        :param service_name: имя службы
        :param expected_state: ожидаемое состояние
        :return: текущее состояние службы
        """
        correct_state = False
        state = self.ssh_win_service_state(service_name)
        if state == expected_state:
            correct_state = state
            return correct_state
        else:
            self.logger.info("Service '{}' in state '{}', expected '{}'".format(service_name, state, expected_state))
            return correct_state

    def ssh_get_cmdline_value(self, cmd_response, cmdline):
        """
        Метод получения значения параметра в командной строке Windows по ssh

        :param cmd_response: вывод командной строки
        :param cmdline: параметр
        :return: значение параметра
        """
        value = ''
        for line in cmd_response:
            if cmdline in line:
                value = line
                break
        if not value:
            self.logger.error("Unexpected cmd output! '{}' does not belong to cmd response: {}".format(cmdline,
                                                                                                       cmd_response))
            return value
        value = value.split(':')[1]
        value = value.split()[1]
        return value

    def ftp_create_backup_files_in_dir(self, dir_path):
        """
        Метод создания бекап-файлов в директории

        :param dir_path: полный путь до директории
        """
        if self.ftp.getcwd() != dir_path:
            self.ftp.chdir(dir_path)
        files_list = self.ftp.listdir()
        if files_list:
            for file in files_list:
                if '.backup' not in file:
                    self.ftp.rename(file, file + '.backup')
                    self.logger.debug("File '{}' was renamed to '{}'".format(file, file + '.backup'))
        else:
            self.logger.info("Directory '{}' is empty. Skip backuping...".format(dir_path))

    def ftp_restore_files_after_backup_in_dir(self, dir_path):
        """
        Метод востановления файлов из бекап-файлов внутри директории

        :param dir_path: полный путь до директории
        """
        self.ftp.chdir(dir_path)
        files_list = self.ftp.listdir()
        backup_files_list = []
        if files_list:
            for file in files_list:
                if '.backup' not in file:
                    self.ftp.remove(self.ftp.getcwd() + '/' + file)
                    self.logger.debug("File '{}' was deleted.".format(file))
                else:
                    backup_files_list.append(file)
                    self.logger.info("File '{}' has backup extension. Skip deleting...".format(file))
        else:
            self.logger.info("Directory '{}' is empty. Skip deleting...".format(dir_path))
        if backup_files_list:
            for file in backup_files_list:
                self.ftp.rename(file, file.replace('.backup', ''))
                self.logger.debug("File '{}' was renamed to '{}'".format(file, file.replace('.backup', '')))

    def ftp_rename_file_list_to_backup(self, file_list):
        """
        Метод переименовывает список файлов в файлы с расширением backup

        :param file_list: список полных путей до файлов
        """
        if not isinstance(file_list, list):
            file_list = [file_list]
        for file in file_list:
            try:
                self.ftp.rename(file, file + '.backup')
                self.logger.info(f"Файл {file} переименован в {file + '.backup'}")
            except OSError:
                self.logger.error(f'Файл {file} не найден')

    def ftp_restore_file_list_from_backup(self, file_list):
        """
        Метод восстановления файлов из бекап-файлов для списка файлов

        :param file_list: список полных путей до файлов
        """
        if not isinstance(file_list, list):
            file_list = [file_list]
        for file in file_list:
            self.ftp.remove(file)
            try:
                self.ftp.posix_rename(file + '.backup', file)
                self.logger.info(f'Файл {file} восстановлен из бекапа')
            except OSError:
                self.logger.error(f'Файл {file + ".backup"} не найден')

    def ftp_add_local_file_to_dir(self, from_path, to_path):
        """
        Метод добавления локального файла на удалённоый компьютер

        :param from_path: полный путь локального файла
        :param to_path: полный путь файла на удалённом компьютере
        """
        local_file_name = os.path.basename(from_path)
        full_path = to_path + '/' + local_file_name
        self.ftp.put(from_path, full_path)
        self.logger.info("New file {} was added to {}".format(local_file_name, to_path))

    def ftp_move_file_to_dir(self, local_file_path, remote_dir, service_to_restart=None):
        """
        Метод безопасного добавления локального файла на удалённоый компьютер

        :param local_file_path: полный путь локального файла
        :param remote_dir: полный путь файла на удалённом компьютере
        :param service_to_restart: службы Windows, которые нужно будет перезапустить
        """
        self.ftp.chdir(remote_dir)
        dir_files = self.ftp.listdir()
        if dir_files:
            self.ftp_create_backup_files_in_dir(remote_dir)
            self.ftp_add_local_file_to_dir(local_file_path, remote_dir)
        else:
            self.ftp_add_local_file_to_dir(local_file_path, remote_dir)

    def ftp_copy_file_list_to_dir_with_backup(self, local_files_path, remote_dir):
        """
        Метод добавления списка локальных файлов на удаленный компьютер

        :param local_files_path: список полных путей локальных файлов
        :param remote_dir: полный путь к папке на удалённом компьютере, в которую копиуем файлы
        """
        remote_file_list = list()
        if not isinstance(local_files_path, list):
            local_files_path = [local_files_path]
        for file in local_files_path:
            remote_file_list.append(os.path.join(remote_dir, os.path.basename(file)))
        self.ftp_rename_file_list_to_backup(remote_file_list)
        for file in local_files_path:
            self.ftp_add_local_file_to_dir(file, remote_dir)
        return remote_file_list
