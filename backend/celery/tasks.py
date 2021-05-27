from time import sleep
import traceback

from celery import states

from .worker import celery

import paramiko
import socket

from io import StringIO
from ..models.models import Command
from ..database import SessionLocal

from .SSHManager import SSHManager

def save_to_db(cmd, rslt):
    session = SessionLocal()
    command = Command(command=cmd, result=rslt)
    session.add(command)
    session.commit()
    session.close()

@celery.task(name='hello.task', bind=True)
def hello_world(self, *name):
    print(f'{name[0]} \t port={name[1]}, \tusername={name[2]} , \t{name[3]} \t {name}>>>>>>>>>>\n')

    # p = paramiko.SSHClient()
    # p.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    private_key = StringIO('''-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----''')
    ssh_manager = None
    try:
        ssh_manager = SSHManager(hostname=name[0], port=name[1], username=name[2], private_key = private_key)
        output = ssh_manager.run_command(name[3])
        save_to_db(name[3], output)
        return {"result": "Response from VMI is\n {}".format(str(output))}
    except Exception as ex:
        save_to_db(name[3], type(ex).__name__)
        self.update_state(
                state=states.FAILURE,
                meta={
                    'exc_type': type(ex).__name__,
                    'exc_message': traceback.format_exc().split('\n')
                })
        raise ex
    finally:
        if ssh_manager:
            ssh_manager.close_ssh_connection()

    # pk = paramiko.RSAKey.from_private_key(private_key)

    # try:
    #     p.connect(hostname=name[0], port=name[1], username=name[2], pkey = pk)
    # except (IOError,
    #         socket.error,
    #         paramiko.ssh_exception.PasswordRequiredException,
    #         paramiko.ssh_exception.AuthenticationException,
    #         paramiko.ssh_exception.NoValidConnectionsError,
    #         paramiko.ssh_exception.BadHostKeyException,
    #         paramiko.ssh_exception.SSHException,
    #         socket.timeout
    #         ) as ex:
    #     save_to_db(name[3],type(ex).__name__)
    #     print(f'\nexception_______________{ex}')
    #     self.update_state(
    #         state=states.FAILURE,
    #         meta={
    #             'exc_type': type(ex).__name__,
    #             'exc_message': traceback.format_exc().split('\n')
    #         })
    #     raise ex
    # try:
    #     stdin, stdout, stderr = p.exec_command(name[3])
    #     sleep(5)
    #
    #     opt = stdout.readlines()
    #     opt = "".join(opt)
    #     # print("before")
    #     # print(stdout.channel.recv_exit_status())
    #     # print("(******************* error is **************")
    #
    #     if(stdout.channel.recv_exit_status() == 0):
    #         save_to_db(name[3], opt)
    #         return {"result": "Response from VMI is\n {}".format(str(opt))}
    #     else:
    #         raise Exception('Command not found')
    #
    # except Exception as ex:
    #     save_to_db(name[3], 'Invalid Command')
    #     self.update_state(
    #         state=states.FAILURE,
    #         meta={
    #             'exc_type': type(ex).__name__,
    #             'exc_message': "command not found"
    #         })
    #     raise ex

