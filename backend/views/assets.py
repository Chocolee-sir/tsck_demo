#!/usr/bin/env python
__author__ = 'Chocolee'

from backend.views.login import *
from utils.get_argv import *
from django.views import View
from utils import pager


class AssetsView(View):

    def get(self, request, *args, **kwargs):
        request_info = GetArgvHelper(request)
        request_info.auth_user()
        if request_info.status():
            return render(
                request, 'backend/backend_assets.html',
                {
                    'username': request_info.username,
                    'permission_list': request_info.permission_list,
                    'personal_info': request_info.personal_info,
                    'menu_info': request_info.menu_info,
                })
        else:
            return redirect('/backend/403.html')


class AssetsJsonView(View):

    def get(self, request, *args, **kwargs):

        table_config = [

            {
                'q': 'id',
                'title': 'ID',
                'display': False,
                'text': {},
                'attrs': {}
            },

            {
                'q': 'ip_address',
                'title': 'IP地址',
                'display': True,
                'text': {'content': "{n}", 'kwargs': {'n': "@ip_address"}},
                'attrs': {}
            },

            {
                'q': 'assets_type',
                'title': '资产类型',
                'display': True,
                'text': {'content': "{n}", 'kwargs': {'n': "@@assets_type_choices"}},
                'attrs': {'edit-enable': 'true', 'edit-type': 'select'}
            },

            {
                'q': 'disk',
                'title': '硬盘',
                'display': True,
                'text': {'content': "{n}", 'kwargs': {'n': "@disk"}},
                'attrs': {}
            },

            {
                'q': 'idc__name',
                'title': 'IDC机房',
                'display': True,
                'text': {'content': "{n}", 'kwargs': {'n': "@idc__name"}},
                'attrs': {'edit-enable': 'true', 'edit-type': 'select'}
            },



            {
                'q': None,
                'title': '操作',
                'display': True,
                'text': {'content': "<a class='btn btn-dark btn-xs web-ssh' href='#'>{n}</a>", 'kwargs': {'n': '连接'}},
                'attrs': {},
            },



        ]

        q_list = []
        for i in table_config:
            if not i['q']:
                continue
            q_list.append(i['q'])

        data_list = models.Host.objects.all().values(*q_list)

        result = {
            'table_config': table_config,
            'data_list': list(data_list),
            'global_dict': {
                'assets_type_choices': models.Host.assets_type_choices,
            }
        }

        return HttpResponse(json.dumps(result))





