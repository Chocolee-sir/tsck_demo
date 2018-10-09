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


class DeployBatchView(View):

    def get(self, request, *args, **kwargs):
        request_info = DeployGetArgv(request)
        request_info.auth_user()
        if request_info.status():
            render_argv = request_info.base_render_argv()
            render_argv['app_list'] = request_info.app_list()
            render_argv['app_version'] = request_info.app_version()
            return render(request, 'backend/backend_deploy.html', render_argv)
        else:
            return redirect('/backend/403.html')

    def post(self, request, *args, **kwargs):
        response = {'status': True, 'data': None}
        request_info = DeployGetArgv(request)
        request_info.auth_user()
        if request_info.status():
            app_id = request.POST.get('app_id')
            if int(app_id) == 0:
                response['data'] = 0
                return HttpResponse(json.dumps(response, ensure_ascii=False))
            ret = request_info.get_hosts_info(app_id)
            response['data'] = list(ret)
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        else:
            return redirect('/backend/403.html')


def deploy_run(request):
    request_info = DeployGetArgv(request)
    request_info.auth_user()
    response = {'status': True, 'message': None}
    if request_info.status():
        if request.method == "POST":
            app_list = request.POST.get('app_list')
            version = request.POST.get('version')
            host_list = request.POST.get('host_list')
            print(app_list, version, host_list)
            # 获取到要部署的信息，这里开始部署
            response['message'] = '后端获取到信息'
            return HttpResponse(json.dumps(response))
        else:
            return HttpResponse('非法请求')
    else:
        return redirect('/backend/403.html')