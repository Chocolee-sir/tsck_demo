#!/usr/bin/env python
__author__ = 'Chocolee'

from repository import models
import subprocess
from django import conf


class MultiTaskManger(object):
    def __init__(self, request):
        self.request = request
        self.run_task()

    def task_parser(self):
        """解析任务"""
        task_type = self.request.POST.get('task_type')

        if hasattr(self, task_type):
            task_func = getattr(self, task_type)
            task_func()
        else:
            print("cannot find task ", task_type)

    def run_task(self):
        """调用任务"""

        self.task_parser()

    def cmd(self):
        """批量命令
        1. 生成任务在数据库中的记录,拿到任务id
        2.触发任务, 不阻塞
        3.返回任务id给前端
        """

        task_obj = models.Task.objects.create(
                task_type='cmd',
                content=self.request.POST.get('cmd'),
                user_id=self.request.POST.get('uid')
        )

        selected_host_ids = set(self.request.POST.getlist('selected_hosts'))
        task_log_objs = []
        for id in selected_host_ids:
            task_log_objs.append(
                    models.TaskLogDetail(task=task_obj, host_to_remote_user_id=id, result='init...')
            )
        models.TaskLogDetail.objects.bulk_create(task_log_objs)
        task_script = "python %s/utils/task_runner.py %s" % (conf.settings.BASE_DIR, task_obj.id)
        cmd_process = subprocess.Popen(task_script, shell=True)
        print("running batch commands....")
        self.task_obj = task_obj
