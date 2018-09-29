#!/usr/bin/env python
__author__ = 'Chocolee'
import django
import sys, os, json
import time, socket
from concurrent.futures import ThreadPoolExecutor
import paramiko


def ssh_cmd(sub_task_obj):
    print("start therad ", sub_task_obj)
    host_to_user_obj = sub_task_obj.host_to_remote_user

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=host_to_user_obj.host.ip_address,
                    port=host_to_user_obj.host.port,
                    username=host_to_user_obj.remote_user.username,
                    password=host_to_user_obj.remote_user.password,
                    timeout=5)
        stdin, stdout, stderr = ssh.exec_command(sub_task_obj.task.content)
        stdout_res = stdout.read().decode()
        stderr_res = stderr.read().decode()
        sub_task_obj.result = stdout_res + stderr_res
        print("------------result-------------")
        print(sub_task_obj.result)

        if stderr_res:
            sub_task_obj.status = 2
        else:
            sub_task_obj.status = 1
    except Exception as e:
        sub_task_obj.result = e
        sub_task_obj.status = 2

    sub_task_obj.save()

    ssh.close()


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(base_dir)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tsck_demo.settings")
    django.setup()

    from repository import models

    if len(sys.argv) == 1:
        exit("task id not provided!")
    task_id = sys.argv[1]
    task_obj = models.Task.objects.get(id=task_id)
    print("task runner..", task_obj)

    pool = ThreadPoolExecutor(10)
    if task_obj.task_type == 'cmd':
        for sub_task_obj in task_obj.tasklogdetail_set.all():
            pool.submit(ssh_cmd, sub_task_obj)
    pool.shutdown(wait=True)
