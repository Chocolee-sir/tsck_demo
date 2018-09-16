#!/usr/bin/env python
__author__ = 'Chocolee'

from django.shortcuts import redirect
from repository import models
from django.db.models import Q
from utils import pager
from utils import forms_plugin
import time, hmac, hashlib

import time



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

    # 基础render数据
    def base_render_argv(self):
        ret = {
            'username': self.username(),
            'permission_list': self.permission_list(),
            'personal_info': self.personal_info(),
            'menu_info': self.menu_info()
        }
        return ret

    # 获取开发权限工单页面数据列表
    def dev_work_list(self, argv=None):
        nid = self.user_info['nid']
        if not argv:
            work_list = models.Workorders.objects.filter(creator_id=nid).order_by('handle_status').only(
                    'title',
                    'detail',
                    'handle_status',
                    'create_time',
                    'handler',
                    'env_label',
                    'project_name',
                    'handler_role',
            )
        else:
            work_list = models.Workorders.objects.filter(creator_id=nid, title__icontains=self.request.GET.get('q')).order_by('handle_status').only(
                    'title',
                    'detail',
                    'handle_status',
                    'create_time',
                    'handler',
                    'env_label',
                    'project_name',
                    'handler_role',
            )
        return work_list


    # 获取开发工单总数
    def dev_work_list_count(self, argv=None):
        if not argv:
            list_counts = models.Workorders.objects.filter(creator_id=self.nid()).count()
        else:
            list_counts = models.Workorders.objects.filter(creator_id=self.nid(), title__icontains=self.request.GET.get('q')).count()
        return list_counts


    # 获取角色id
    def get_role_id(self):
        nid = self.user_info['nid']
        role_id = models.User2Role.objects.filter(u_id=nid).values('r_id')
        for i in role_id:
            return i['r_id']


    # 运维获取需要处理的数据列表
    def ops_work_list(self, argv=None):
        if not argv:
            work_list = models.Workorders.objects.order_by('handle_status').only(
                    'title',
                    'detail',
                    'handle_status',
                    'create_time',
                    'creator',
                    'env_label',
                    'project_name',
            )
        else:
            work_list = models.Workorders.objects.filter(title__icontains=self.request.GET.get('q')).order_by('handle_status').only(
                    'title',
                    'detail',
                    'handle_status',
                    'create_time',
                    'creator',
                    'env_label',
                    'project_name',
            )
        return work_list


    # 获取运维工单总数
    def ops_work_list_count(self, argv=None):
        if not argv:
            list_counts = models.Workorders.objects.all().count()
        else:
            list_counts = models.Workorders.objects.filter(title__icontains=self.request.GET.get('q')).count()
        return list_counts


    # 测试获取需要处理的数据
    def test_work_list(self, argv=None):
        if not argv:
            work_list = models.Workorders.objects.filter(Q(handle_status=2) | Q(handle_status=3) | Q(handle_status=4)).order_by('handle_status').only(
                    'title',
                    'detail',
                    'handle_status',
                    'create_time',
                    'creator',
                    'env_label',
                    'project_name',
            )
        else:
            work_list = models.Workorders.objects.filter\
                (Q(handle_status=2) | Q(handle_status=3) | Q(handle_status=4), title__icontains=self.request.GET.get('q')).\
                order_by('handle_status').only(
                    'title',
                    'detail',
                    'handle_status',
                    'create_time',
                    'creator',
                    'env_label',
                    'project_name',
            )
        return work_list


    # 获取测试工单总数
    def test_work_list_count(self, argv=None):
        if not argv:
            list_counts = models.Workorders.objects.filter(Q(handle_status=2) | Q(handle_status=3) | Q(handle_status=4)).count()
        else:
            list_counts = models.Workorders.objects.filter\
                (Q(handle_status=2) | Q(handle_status=3) | Q(handle_status=4), title__icontains=self.request.GET.get('q')).count()
        return list_counts


# 资产页方法使用
class AssetsGetArgv(GetArgvHelper):

     # 资产管理分页使用
    def get_host_paper(self):
        if not self.request.GET.get('q'):
            data_list_all = models.Host.objects.all().order_by('-id')
            list_counts = models.Host.objects.all().count()
        else:
            data_list_all = models.Host.objects.filter(Q(ip_address__icontains=self.request.GET.get('q')) | Q(project_name__project_name__icontains=self.request.GET.get('q'))).order_by('-id')
            list_counts = models.Host.objects.filter(Q(ip_address__icontains=self.request.GET.get('q')) | Q(project_name__project_name__icontains=self.request.GET.get('q'))).count()
        current_page = self.request.GET.get('p')
        page_obj = pager.Pagination(list_counts, current_page, 5, 7, 'assets.html')
        data_list = data_list_all[page_obj.start():page_obj.end()]
        return {'page_obj': page_obj, 'data_list': data_list}

    # 添加主机资产
    def forms_add_asset(self):
        ret = forms_plugin.FormsAddAsset()
        return ret

    # 编辑主机资产
    def forms_edit_asset(self, nid):
        obj = models.Host.objects.filter(id=nid).values()
        ret = forms_plugin.FormsAddAsset(obj[0])
        return ret

    #获取主机资产储存到数据库
    def forms_add_asset_to_db(self):
        forms_add_asset = forms_plugin.FormsAddAsset(self.request.POST)
        if forms_add_asset.is_valid():
            asset_dict = forms_add_asset.cleaned_data
            models.Host.objects.create(**asset_dict)
            return True
        else:
            return forms_add_asset

    # 编辑主机资产
    def forms_edit_asset_to_db(self, nid):
        forms_edit_asset = forms_plugin.FormsAddAsset(self.request.POST)
        if forms_edit_asset.is_valid():
            asset_dict = forms_edit_asset.cleaned_data
            models.Host.objects.filter(id=nid).update(**asset_dict)
            return True
        else:
            return forms_edit_asset

    # 删除一条主机资产
    def del_asset(self, nid):
        try:
            models.Host.objects.filter(id=nid).delete()
            return True
        except Exception as e:
            return e

    # gateone webssh 加密使用
    def create_signature(self, secret, *parts):
        hash = hmac.new(bytes(secret, 'utf8'), digestmod=hashlib.sha1)
        for part in parts:
            hash.update(str(part).encode('utf8'))
        return hash.hexdigest()
