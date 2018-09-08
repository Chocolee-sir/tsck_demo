#!/usr/bin/env python
__author__ = 'Chocolee'

from django.shortcuts import redirect
from repository import models
import hashlib


class GetArgvHelper(object):

    # 实例化，获取request，通过request 获取到session用户信息
    def __init__(self, request):
        self.request = request
        self.user_info = self.request.session.get('user_info')

    # 验证 session用户信息
    def auth_user(self):
        if not self.user_info:
            return redirect('/web/login.html')
        nid = self.user_info['nid']
        username = self.user_info['username']
        obj = models.User.objects.filter(username=username, id=nid).first()
        if not obj:
            return redirect('/web/login.html')

    # 获取 用户id
    def nid(self):
        return self.user_info['nid']

    # 获取 用户名
    def username(self):
        return self.user_info['username']

    # 获取 页面角色权限状态，是否有权限
    def status(self):
        ret = True
        if self.request.path not in self.user_info['action_list']:
            ret = False
        return ret

    # 获取 权限列表
    def permission_list(self):
        return self.user_info['permission_list']

    # 获取 菜单信息
    def menu_info(self):
        ret = models.Permission.objects.filter(url=self.request.path).values_list('caption', 'icon', 'url')[0]
        return ret

    # 获取 个人信息
    def personal_info(self):
        ret = models.User2Role.objects.filter(u_id=self.user_info['nid']).first()
        return ret

    # 获取 角色列表
    def role_list(self):
        ret = models.Role.objects.all()
        return ret

    # 获取 项目列表
    def project_list(self):
        ret = models.Projects.objects.all()
        return ret

    # 获取 环境列表
    def env_list(self):
        ret = models.Envlists.objects.all()
        return ret

    # 密码 MD5加密
    def password_md5(self,  password):
        pwd_md5 = hashlib.md5()
        pwd_md5.update(password.encode(encoding='utf-8'))
        return pwd_md5.hexdigest()

    # 获取开发权限工单页面数据
    def dev_work_list(self):
        nid = self.user_info['nid']
        work_list = models.Workorders.objects.filter(creator_id=nid).order_by('handle_status').only(
                'title',
                'detail',
                'handle_status',
                'create_time',
                'handler',
                'env_label',
                'project_name',
        )
        return work_list







