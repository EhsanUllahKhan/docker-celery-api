from time import sleep
import traceback

from celery import current_task
from celery import states
from celery.exceptions import Ignore

from worker import celery

import paramiko
import os
import socket

from io import StringIO


@celery.task(name='hello.task', bind=True)
def hello_world(self, *name):
    print(f'{name[0]}  port={name[1]}, username={name[2]} >>>>>>>>>>\n')

    p = paramiko.SSHClient()
    p.set_missing_host_key_policy(paramiko.AutoAddPolicy())  

    private_key = StringIO('''-----BEGIN OPENSSH PRIVATE KEY-----
paste your private ssh key here
-----END OPENSSH PRIVATE KEY-----''')
    pk = paramiko.RSAKey.from_private_key(private_key)

    try:
        p.connect(hostname=name[0], port=name[1], username=name[2], pkey = pk)
    
    except IOError as ex:
        print(f'\nexception_______________{ex}')
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            })
        raise ex

    except socket.error as ex:
        print(f'\nexception_______________{ex}')
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            })
        raise ex

    except paramiko.ssh_exception.PasswordRequiredException as ex:
        print(f'\nexception________-1_______{ex}')
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            })
        raise ex
    
    except paramiko.ssh_exception.AuthenticationException as ex: 
        print(f'\nexception________0_______{ex}')
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            })
        raise ex

    except paramiko.ssh_exception.NoValidConnectionsError as ex: 
        print(f'\nexception________1_______{ex}')
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            })
        raise ex

    except paramiko.ssh_exception.BadHostKeyException as ex:
        print(f'\nexception________3_______{ex}')
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            })
        raise ex

    except paramiko.ssh_exception.SSHException as ex:
        print(f'\nexception________4_______{ex}')
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            })
        raise ex

    except socket.timeout as ex:
        print(f'\ntimeout exception________5_______{ex}')
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            })
        raise ex

    try:
        stdin, stdout, stderr = p.exec_command(name[3])
        sleep(5)
        
        opt = stdout.readlines()
        opt = "".join(opt)
        # print("before")
        # print(stdout.channel.recv_exit_status())
        # print("(******************* error is **************")
        if(stdout.channel.recv_exit_status() == 0): 
            return {"result": "Response from VMI is\n {}".format(str(opt))}
        else: 
            raise Exception('Command not found')

    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': "command not found"
            })
        raise ex

