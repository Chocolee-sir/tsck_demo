#!/usr/bin/env python
__author__ = 'Chocolee'

from backend.views.login import *
from utils.get_argv import *
from django.views import View
from  utils.multitask import MultiTaskManger


class DeployCmdView(View):

    def get(self, request, *args, **kwargs):
        request_info = DeployGetArgv(request)
        request_info.auth_user()
        if request_info.status():
            render_argv = request_info.base_render_argv()
            return render(request, 'backend/backend_cmd.html', render_argv)
        else:
            return redirect('/backend/403.html')

    def post(self, request, *args, **kwargs):
        request_info = DeployGetArgv(request)
        request_info.auth_user()
        if request_info.status():
            task_obj = MultiTaskManger(request)
            response = {
            'task_id':task_obj.task_obj.id,
            'selected_hosts': list(task_obj.task_obj.tasklogdetail_set.all().values(
                    'id',
                    'host_to_remote_user__host__ip_address',
                    'host_to_remote_user__host__hostname',
                    'host_to_remote_user__remote_user__username'
                    ))
            }
            return HttpResponse(json.dumps(response))
        else:
            return redirect('/backend/403.html')


def task_result(request):
    request_info = DeployGetArgv(request)
    request_info.auth_user()
    if request_info.status():
        task_id = request.GET.get('task_id')
        sub_tasklog_objs = models.TaskLogDetail.objects.filter(task_id=task_id)
        log_data = list(sub_tasklog_objs.values('id','status','result'))
        return HttpResponse(json.dumps(log_data))
    else:
        return redirect('/backend/403.html')

