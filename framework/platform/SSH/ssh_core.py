import paramiko
import logging
from tools.utils import extract_domain_from_url


class PlatformSSHCore:
    """
    Класс инициализации работы по SSH
    """
    def __init__(self, host, login='user', password='password', port=22):
        self.host = extract_domain_from_url(host)
        self.user = login
        self.password = password
        self.port = port
        self.logger = logging.getLogger(__name__)
        self.ssh_conn, self.ftp, self.connection_error = self._create_ssh_connection()

    def _create_ssh_connection(self):
        """
        Метод создания ssh и ftp соединения

        :return: клиент ssh, клиент ftp, ошибка создания соединения
        """
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Подключение
        try:
            ssh_client.connect(hostname=self.host, username=self.user, password=self.password, port=self.port)
            ftp_client = ssh_client.open_sftp()
        except paramiko.ssh_exception.AuthenticationException:
            error = "SSH connection failed for user '{}'!".format(self.user)
            self.logger.error(error)
            return None, None, error
        except paramiko.ssh_exception.NoValidConnectionsError:
            error = "SSH connection cannot be created on host {}:{}!".format(self.host, self.port)
            self.logger.error(error)
            return None, None, error
        except paramiko.ssh_exception.SSHException:
            error = "FTP connection cannot be created on host {}:{}!".format(self.host, self.port)
            self.logger.error(error)
            return None, None, error
        return ssh_client, ftp_client, None

    def close_ssh_connection(self):
        """
        Метод закрытия ssh и ftp соединения

        """
        self.ssh_conn.close()
        self.ftp.close()

    def _save_cmd_execution(self, command):
        """
        Метод безопасного выполнения ssh команд

        :param command: команда
        :return: необработанный вывод команды
        """
        command = str(command)
        self.logger.info("Execute cmd command: '{}', on {}:{}".format(command, self.host, self.port))
        try:
            stdin, stdout, stderr = self.ssh_conn.exec_command(command)
        except Exception:
            self.logger.error("Incorrect cmd command format: '{}'!".format(command))
        data = stdout.readlines() + stderr.readlines()
        if data:
            self.logger.debug("Result cmd: {}".format(data))
        else:
            self.logger.debug("The command has correct empty output.")
        return data
