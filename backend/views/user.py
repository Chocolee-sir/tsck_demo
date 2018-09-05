#!/usr/bin/env python
__author__ = 'Chocolee'

from backend.views.login import *
from repository import models
from utils import pager
from utils import forms_plugin



# 用户页面首页，默认显示所有用户，倒序排列
@login_auth
def index_user(request, *args, **kwargs):
    action_list = kwargs.get('action_list')
    status = allow_url_auth(request, action_list)
    username = kwargs.get('username')
    permission_list = kwargs.get('permission_list')
    menu_info = models.Permission.objects.filter(url=request.path).values_list('caption', 'icon', 'url')[0]
    personal_info = models.User2Role.objects.filter(u_id=kwargs.get('nid')).first()
    role_list = models.Role.objects.all()
    if request.GET.get('q'):
        ret = models.User2Role.objects.filter(u__username__icontains=request.GET.get('q')).order_by('-u_id')
        list_counts = models.User2Role.objects.filter(u__username__icontains=request.GET.get('q')).count()
    else:
        ret = models.User2Role.objects.all().order_by('-u_id')
        list_counts = models.User2Role.objects.all().count()
    current_page = request.GET.get('p')
    page_obj = pager.Pagination(list_counts, current_page, 5, 7, 'user.html')
    users_info = ret[page_obj.start():page_obj.end()]

    if status:
        return render(
                request, 'backend/backend_user.html',
                {
                    'username': username,
                    'permission_list': permission_list,
                    'menu_info': menu_info,
                    'users_info': users_info,
                    'page_obj': page_obj,
                    'role_list': role_list,
                    'personal_info': personal_info,
                })
    else:
        return redirect('/backend/403.html')


# 使用form组件添加用户方法
@login_auth
def add_user(request, *args, **kwargs):
    action_list = kwargs.get('action_list')
    status = allow_url_auth(request, action_list)
    username = kwargs.get('username')
    permission_list = kwargs.get('permission_list')
    menu_info = models.Permission.objects.filter(url=request.path).values_list('caption', 'icon', 'url')[0]
    personal_info = models.User2Role.objects.filter(u_id=kwargs.get('nid')).first()
    if status:
        if request.method == "GET":
            forms_add_user = forms_plugin.FormsAddUser()
            return render(
                    request, 'backend/backend_add_user.html',
                    {
                        'username': username,
                        'permission_list': permission_list,
                        'menu_info': menu_info,
                        'forms_add_user': forms_add_user,
                        'personal_info': personal_info,
                    })

        elif request.method == "POST":
            forms_add_user = forms_plugin.FormsAddUser(request.POST)
            if forms_add_user.is_valid():
                user_dict = forms_add_user.cleaned_data
                user_dict['password'] = password_md5(user_dict['password'])
                role_id = user_dict['role_id']
                del user_dict['role_id']
                models.User.objects.create(**user_dict)
                user_id = models.User.objects.filter(username=user_dict['username']).values('id')[0]['id']
                models.User2Role.objects.create(u_id=user_id, r_id=role_id)
                return redirect('/backend/user.html')
            else:
                return render(
                    request, 'backend/backend_add_user.html',
                    {
                        'username': username,
                        'permission_list': permission_list,
                        'menu_info': menu_info,
                        'forms_add_user': forms_add_user,
                        'personal_info': personal_info,
                    })
    else:
        return redirect('/backend/403.html')


# 删除用户
@login_auth
def del_user(request, *args, **kwargs):
    action_list = kwargs.get('action_list')
    status = allow_url_auth(request, action_list)
    response = {'status': True, 'message': None}
    if status:
        if request.method == "GET":
            nid = request.GET.get('nid')
            del_user_count = models.User.objects.filter(id=nid).delete()
            if del_user_count[0] == 0:
                response['status'] = False
                response['message'] = "用户不存在，删除异常！！！"
                return HttpResponse(json.dumps(response))
            else:
                return HttpResponse(json.dumps(response))
        else:
            return HttpResponse('请求方式有问题')
    else:
        return redirect('/backend/403.html')


# 编辑用户
@login_auth
def edit_user(request, *args, **kwargs):
    action_list = kwargs.get('action_list')
    status = allow_url_auth(request, action_list)
    response = {'status': True, 'message': None}
    if status:
        if request.method == "POST":
            try:
                nid = request.POST.get('nid')
                username = request.POST.get('username')
                role_id = request.POST.get('role_id')
                sex = request.POST.get('sex')
                realname = request.POST.get('realname')
                phone = request.POST.get('phone')
                email = request.POST.get('email')
                """
                pwd = request.POST.get('password')
                if pwd:
                    password = password_md5(pwd)
                """
                models.User.objects.filter(id=nid).update(
                    username=username,
                    sex=sex,
                    realname=realname,
                    phone=phone,
                    email=email
                )
                models.User2Role.objects.filter(u_id=nid).update(r_id=role_id)
            except Exception as e:
                response['status'] = False
                response['message'] = e
            return HttpResponse(json.dumps(response, ensure_ascii=False))
    else:
        return redirect('/backend/403.html')

