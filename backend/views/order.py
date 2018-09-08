#!/usr/bin/env python
__author__ = 'Chocolee'

from backend.views.login import *
from repository import models
from utils import pager
from utils.get_argv import *


# 工单首页
def index_order(request):
    request_info = GetArgvHelper(request)
    request_info.auth_user()
    if request_info.status:
        return render(
                request, 'backend/backend_dev_order.html',
                {
                    'username': request_info.username,
                    'permission_list': request_info.permission_list,
                    'personal_info': request_info.personal_info,
                    'menu_info': request_info.menu_info,
                    'dev_work_list': request_info.dev_work_list,
                    'project_list': request_info.project_list,
                    'env_list': request_info.env_list,
                })
    else:
        return redirect('/backend/403.html')


# 创建工单
def create_order(request):
    request_info = GetArgvHelper(request)
    request_info.auth_user()
    response = {'status': True, 'message': None}
    if request_info.status:
        if request.method == "POST":
            title = request.POST.get('title')
            detail = request.POST.get('detail')
            if not title or not detail:
                response['status'] = False
                response['message'] = "标题或内容不能为空"
                return HttpResponse(json.dumps(response, ensure_ascii=False))
            project_name = request.POST.get('project_name')
            env_label = request.POST.get('env_label')
            try:
                models.Workorders.objects.create(
                    title=title,
                    detail=detail,
                    project_name_id=project_name,
                    env_label_id=env_label,
                    creator_id=request_info.nid(),
                )
            except Exception as e:
                response['status'] = False
                response['message'] = e
            return HttpResponse(json.dumps(response, ensure_ascii=False))
    else:
        return redirect('/backend/403.html')


# 获取 变更内容, 获取删除信息内容
def get_detail(request):
    request_info = GetArgvHelper(request)
    request_info.auth_user()
    response = {'status': True, 'title': None, 'detail': None}
    if request_info.status:
        if request.method == "GET":
            nid = request.GET.get('nid')
            det_info = models.Workorders.objects.filter(id=nid, creator_id=request_info.nid()).first()
            response['title'] = det_info.title
            response['detail'] = det_info.detail
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        else:
            response['status'] = False
            return HttpResponse(json.dumps(response, ensure_ascii=False))


# 开发人员删除工单
def del_order(request):
    request_info = GetArgvHelper(request)
    request_info.auth_user()
    response = {'status': True, 'data': None}
    if request_info.status:
        if request.method == "GET":
            nid = request.GET.get('nid')
            try:
                models.Workorders.objects.filter(id=nid, creator_id=request_info.nid()).delete()
            except Exception as e:
                response['status'] = False
                response['data'] = e
            return HttpResponse(json.dumps(response, ensure_ascii=False))
    else:
        return redirect('/backend/403.html')


# 开发人员编辑工单
def edit_order(request):
    request_info = GetArgvHelper(request)
    request_info.auth_user()
    response = {'status': True, 'data': None}
    if request_info.status:
        if request.method == "POST":
            nid = request.POST.get('nid')
            title = request.POST.get('title')
            detail = request.POST.get('detail')
            project_name_id = request.POST.get('project_name')
            env_label_id = request.POST.get('env_label')
            try:
                models.Workorders.objects.filter(id=nid, creator_id=request_info.nid()).update(
                    title=title,
                    detail=detail,
                    project_name_id=project_name_id,
                    env_label_id=env_label_id,
                )
            except Exception as e:
                response['status'] = False
                response['data'] = e
            return HttpResponse(json.dumps(response, ensure_ascii=False))

    else:
        return redirect('/backend/403.html')
