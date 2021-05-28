import paramiko
import socket
from io import StringIO
from time import sleep

from paramiko.ssh_exception import AuthenticationException, BadAuthenticationType, BadHostKeyException, \
    NoValidConnectionsError, SSHException
from .exceptions import SSHAuthException, SSHCommandException,  SSHConnectException, SSHNoCredentialsException

class SSHManager:
    def __init__(self, hostname, username='root', password=None, port='22', private_key=None,pass_phrase=None):
        self.TIMEOUT = 8.0
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.private_key = None
        self.pass_phrase = None
        if private_key:
            self.private_key = paramiko.RSAKey.from_private_key(private_key)
            self.pass_phrase = pass_phrase

        self.__ssh_client = paramiko.SSHClient()
        self.__ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__connect()

    def __connect(self):
        client_args = dict(hostname=self.hostname, username=self.username)
        client_args["port"] = int(self.port)
        client_args['look_for_keys'] = False
        client_args['timeout'] = self.TIMEOUT
        if self.private_key:
            client_args['pkey'] = self.private_key
            if self.pass_phrase:
                client_args['passphrase'] = self.pass_phrase
        else:
            client_args['password'] = self.password

        try:
            print("Starting SSH session to: '{}'".format(self.hostname))
            self.__ssh_client.connect(**client_args)
        except (AuthenticationException, BadAuthenticationType, BadHostKeyException) as ex:
            print("An exception of type {0} was raised. Arguments:\n{1!r}".format(type(ex).__name__, ex.args))
            raise SSHAuthException(self.hostname, self.username)
        except (SSHException, NoValidConnectionsError, socket.timeout, socket.error) as ex:
            print("An exception of type {0} was raised. Arguments:\n{1!r}".format(type(ex).__name__, ex.args))
            raise SSHConnectException(self.hostname)

    def run_command(self, command):
        self.__connect()
        try:
            in_stream, out_stream, error_stream = self.__ssh_client.exec_command(command)
            sleep(5)
            exit_code = out_stream.channel.recv_exit_status()
            out_stream.channel.close()

            if exit_code == 0:
                opt = out_stream.readlines()
                opt = "".join(opt)
                print(f'________ result of command ________ \t {opt}')
                return str(opt)
            else:
                 raise SSHCommandException(self.hostname, command, error_stream)

        except SSHException as ex:
            raise SSHCommandException(self.hostname, command, ex)
        # else:
        #     output = ""
        #     for stream in [error_stream]:
        #         for line in stream:
        #             output += line
        #     else:
        #         raise SSHCommandException(self.hostname, command, "Exit Code: {}\nOUTPUT: {}".format(
        #             str(exit_code), output))


    def close_ssh_connection(self):
        """
        This function closes the transport for client. This SHOULD ALWAYS be called after using ssh manager object.
        """
        if self.__ssh_client:
            self.__ssh_client.close()

    def __del__(self):
        """
        This destructor is just for safety in case someone forgets to close the client. However, it should be done
        explicitly
        """
        self.close_ssh_connection()

