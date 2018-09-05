#!/usr/bin/env python
__author__ = 'Chocolee'

from django.shortcuts import render, redirect, HttpResponse
from repository import models
import hashlib
import json


# Create your views here.


def password_md5(password):
    pwd_md5 = hashlib.md5()
    pwd_md5.update(password.encode(encoding='utf-8'))
    return pwd_md5.hexdigest()


def login_auth(func):
    def inner(request, *args, **kwargs):
        user_info = request.session.get('user_info')
        if not user_info:
            return redirect('/web/login.html')
        nid = user_info['nid']
        username = user_info['username']
        obj = models.User.objects.filter(username=username, id=nid).first()
        if not obj:
            return redirect('/web/login.html')
        kwargs['nid'] = nid
        kwargs['username'] = username
        kwargs['permission_list'] = user_info['permission_list']
        kwargs['action_list'] = user_info['action_list']
        kwargs['login_status'] = True
        return func(request, *args, **kwargs)

    return inner


def allow_url_auth(request, action_list):
    status = True
    if request.path not in action_list:
        status = False
    return status


def status_403(request):
    return render(request, 'backend/403.html')


def login_out(request):
    request.session.clear()
    return redirect('/web/login.html')


@login_auth
def index(request, *args, **kwargs):
    login_status = kwargs.get('login_status')
    username = kwargs.get('username')
    permission_list = kwargs.get('permission_list')
    personal_info = models.User2Role.objects.filter(u_id=kwargs.get('nid')).first()
    if login_status:
        return render(
                request, 'backend/backend_index.html',
                {
                    'username': username,
                    'permission_list': permission_list,
                    'personal_info': personal_info,
                })


@login_auth
def personal_info(request, *args, **kwargs):
    response = {'status': True, 'message': None}
    if request.method == "POST":
        nid = kwargs.get('nid')
        pwd = request.POST.get('password')
        if pwd:
            if len(pwd) < 8:
                response = {'status': False, 'message': '密码长度必须为8位以上'}
            else:
                password = password_md5(pwd)
                models.User.objects.filter(id=nid).update(password=password)
                request.session.clear()
        else:
            response = {'status': False, 'message': '密码不能为空'}
        return HttpResponse(json.dumps(response, ensure_ascii=False))





