#!/usr/bin/env python
__author__ = 'Chocolee'

from repository import models
from utils import pager

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
        'attrs': {}
    },

    {
        'q': 'project_name__project_name',
        'title': '所属项目',
        'display': True,
        'text': {'content': "{n}", 'kwargs': {'n': "@project_name__project_name"}},
        'attrs': {}
    },

    {
        'q': 'env_type__env',
        'title': '所属环境',
        'display': True,
        'text': {'content': "{n}", 'kwargs': {'n': "@env_type__env"}},
        'attrs': {}
    },

    {
        'q': 'cpu',
        'title': 'CPU',
        'display': True,
        'text': {'content': "{n}", 'kwargs': {'n': "@cpu"}},
        'attrs': {}
    },

     {
        'q': 'memory',
        'title': '内存',
        'display': True,
        'text': {'content': "{n}", 'kwargs': {'n': "@memory"}},
        'attrs': {}
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
        'attrs': {}
    },

    {
        'q': None,
        'title': '操作',
        'display': True,
        'text': {
            'content': "<a class='btn btn-primary btn-xs asset-edit'>{m}</a>|<a class='btn btn-dark btn-xs web-ssh' href='#'>{n}</a>",
            'kwargs': {'m': '编辑', 'n': '连接'}
        },
        'attrs': {'nid': '@id'},
    },

]


def data_list_all():
    q_list = []
    for i in table_config:
        if not i['q']:
            continue
        q_list.append(i['q'])
    data_list = models.Host.objects.all().values(*q_list)
    return data_list


def data_list_conut():
    count = models.Host.objects.all().count()
    return count


def get_host_paper(request):
    current_page = request.GET.get('p')
    list_counts = models.Host.objects.all().count()
    page_obj = pager.Pagination(list_counts, current_page, 5, 7, 'assets.html')
    data_list = data_list_all()[page_obj.start():page_obj.end()]
    return {'page_obj': page_obj, 'data_list': data_list}




