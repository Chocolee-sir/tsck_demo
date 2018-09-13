#!/usr/bin/env python
__author__ = 'Chocolee'

from backend.views.login import *
from utils.get_argv import *
from utils import pager


# 工单首页
def index_order(request):
    request_info = GetArgvHelper(request)
    request_info.auth_user()
    current_page = request.GET.get('p')
    if request_info.get_role_id() == 4:
        if request.GET.get('q'):
            all_list = request_info.dev_work_list(1)
            list_counts = request_info.dev_work_list_count(1)
        else:
            all_list = request_info.dev_work_list()
            list_counts = request_info.dev_work_list_count()
        render_url = 'backend/backend_dev_order.html'
    elif request_info.get_role_id() == 3:
        if request.GET.get('q'):
            all_list = request_info.test_work_list(1)
            list_counts = request_info.test_work_list_count(1)
        else:
            all_list = request_info.test_work_list()
            list_counts = request_info.test_work_list_count()
        render_url = 'backend/backend_test_order.html'
    else:
        if request.GET.get('q'):
            all_list = request_info.ops_work_list(1)
            list_counts = request_info.ops_work_list_count(1)
        else:
            all_list = request_info.ops_work_list()
            list_counts = request_info.ops_work_list_count()
        render_url = 'backend/backend_ops_order.html'
    page_obj = pager.Pagination(list_counts, current_page, 5, 7, 'order.html')
    work_list = all_list[page_obj.start():page_obj.end()]
    if request_info.status():
        return render(
                request, render_url,
                {
                    'username': request_info.username,
                    'permission_list': request_info.permission_list,
                    'personal_info': request_info.personal_info,
                    'menu_info': request_info.menu_info,
                    'work_list': work_list,
                    'project_list': request_info.project_list,
                    'env_list': request_info.env_list,
                    'page_obj': page_obj,
                })
    else:
        return redirect('/backend/403.html')


# 创建工单
def create_order(request):
    request_info = GetArgvHelper(request)
    request_info.auth_user()
    response = {'status': True, 'message': None}
    if request_info.status():
        if request.method == "POST":
            title = request.POST.get('title')
            detail = request.POST.get('detail')
            if not title or not detail:
                response['status'] = False
                response['message'] = "标题或内容不能为空"
                return HttpResponse(json.dumps(response, ensure_ascii=False))
            if len(title) > 20:
                response['status'] = False
                response['message'] = "标题长度不能超过20个字符"
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


# 获取 变更内容, 获取删除信息内容等
def get_detail(request):
    request_info = GetArgvHelper(request)
    request_info.auth_user()
    response = {
        'status': True,
        'title': None,
        'detail': None,
        'ops_result': None,
        'test_result': None
    }
    if request_info.status():
        if request.method == "GET":
            nid = request.GET.get('nid')
            role = request.GET.get('role')
            if role == 'handler':
                det_info = models.Workorders.objects.filter(id=nid).first()
            else:
                det_info = models.Workorders.objects.filter(id=nid, creator_id=request_info.nid()).first()
            response['title'] = det_info.title
            response['detail'] = det_info.detail
            response['ops_result'] = det_info.ops_result
            response['test_result'] = det_info.test_result
            return HttpResponse(json.dumps(response, ensure_ascii=False))
        else:
            response['status'] = False
            return HttpResponse(json.dumps(response, ensure_ascii=False))


# 开发人员删除工单
def del_order(request):
    request_info = GetArgvHelper(request)
    request_info.auth_user()
    response = {'status': True, 'data': None}
    if request_info.status():
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
    if request_info.status():
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


# 运维处理工单
def ops_handle_order(request):
    request_info = GetArgvHelper(request)
    request_info.auth_user()
    response = {'status': True, 'message': None}
    if request_info.status():
        if request.method == "POST":
            nid = request.POST.get('nid')
            result = request.POST.get('result')
            if not result:
                response['status'] = False
                response['message'] = "内容不能为空"

            try:
                models.Workorders.objects.filter(id=nid).update(
                    handler_role=2,
                    handle_status=2,
                    handler_id=request_info.nid(),
                    role_status=2,
                    ops_result=result,
                    handle_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                )
            except Exception as e:
                response['status'] = False
                response['data'] = e

            return HttpResponse(json.dumps(response, ensure_ascii=False))


# 测试处理工单
def test_handle_order(request):
    request_info = GetArgvHelper(request)
    request_info.auth_user()
    response = {'status': True, 'message': None}
    if request_info.status():
        if request.method == "POST":
            nid = request.POST.get('nid')
            result = request.POST.get('result')
            last_result = request.POST.get('last_result')
            if not result:
                response['status'] = False
                response['message'] = "内容不能为空"
            print(nid,result,last_result)
            try:
                if int(last_result) == 1:
                    models.Workorders.objects.filter(id=nid).update(
                        handler_role=4,
                        handle_status=3,
                        handler_id=request_info.nid(),
                        role_status=3,
                        test_result=result,
                        handle_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                    )
                else:
                    models.Workorders.objects.filter(id=nid).update(
                        handler_role=3,
                        handle_status=4,
                        handler_id=request_info.nid(),
                        role_status=3,
                        test_result=result,
                        handle_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                    )

            except Exception as e:
                response['status'] = False
                response['data'] = e

            return HttpResponse(json.dumps(response, ensure_ascii=False))
