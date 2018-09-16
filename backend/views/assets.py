#!/usr/bin/env python
__author__ = 'Chocolee'

from backend.views.login import *
from utils.get_argv import *
from django.http import JsonResponse
from django.views import View



class AssetsView(View):

    def get(self, request, *args, **kwargs):
        request_info = AssetsGetArgv(request)
        request_info.auth_user()
        if request_info.status():
            render_argv = request_info.base_render_argv()
            render_argv['page_obj'] = request_info.get_host_paper()['page_obj']
            render_argv['data_list'] = request_info.get_host_paper()['data_list']
            return render(
                request, 'backend/backend_assets.html', render_argv)
        else:
            return redirect('/backend/403.html')


class AssetsAddView(View):

    def get(self, request, *args, **kwargs):
        request_info = AssetsGetArgv(request)
        request_info.auth_user()
        if request_info.status():
            render_argv = request_info.base_render_argv()
            render_argv['forms_add_asset'] = request_info.forms_add_asset
            return render(request, 'backend/backend_add_assets.html', render_argv)
        else:
            return redirect('/backend/403.html')

    def post(self, request, *args, **kwargs):
        request_info = AssetsGetArgv(request)
        request_info.auth_user()
        if request_info.status():
            if request_info.forms_add_asset_to_db() is True:
                return redirect('/backend/assets.html')
            else:
                render_argv = request_info.base_render_argv()
                render_argv['forms_add_asset'] = request_info.forms_add_asset_to_db()
                return render(request, 'backend/backend_add_assets.html', render_argv)
        else:
            return redirect('/backend/403.html')


class AssetsEditView(View):

    def get(self, request, *args, **kwargs):
        request_info = AssetsGetArgv(request)
        request_info.auth_user()
        nid = request.GET.get('nid')
        action = request.GET.get('Action')
        if request_info.status():
            render_argv = request_info.base_render_argv()
            if action == "编辑":
                forms_edit_asset = request_info.forms_edit_asset(nid)
                render_argv['forms_edit_asset'] = forms_edit_asset
                render_argv['nid'] = nid
                return render(request, 'backend/backend_edit_assets.html', render_argv)
            elif action == "连接":
                """不写了，webssh有点不怎么好用，这边可以
                通过nid找到这条host记录，通过登录用户及连表找到相应权限的用户进行登录，就是一个damo测试"""
                render_argv['ip'] = '192.168.31.100'
                render_argv['port'] = 22
                render_argv['username'] = 'dev'
                return render(request, 'backend/backend_gateone.html', render_argv)
            else:
                return redirect('/backend/assets.html')
        else:
            return redirect('/backend/403.html')

    def post(self, request, *args, **kwargs):
        request_info = AssetsGetArgv(request)
        request_info.auth_user()
        nid = request.POST.get('nid')
        action = request.POST.get('Action')
        if request_info.status():
            if action == "提交":
                if request_info.forms_edit_asset_to_db(nid) is True:
                    return redirect('/backend/assets.html')
                else:
                    render_argv = request_info.base_render_argv()
                    render_argv['forms_edit_asset'] = request_info.forms_edit_asset_to_db(nid)
                    return render(request, 'backend/backend_edit_assets.html', render_argv)
            elif action == "删除这条记录":
                result = request_info.del_asset(nid)
                if result:
                    return redirect('/backend/assets.html')
                else:
                    return HttpResponse(result)
            else:
                pass
        else:
            return redirect('/backend/403.html')


class AssetsGateOneAuthView(View):

    def get(self,request, *args, **kwargs):
        request_info = AssetsGetArgv(request)
        request_info.auth_user()
        '''
        gateone继承到web界面上
        :return:返回gateone url及认证参数
        '''
        # 安装gateone的服务器以及端口.
        gateone_server = 'https://192.168.31.100:443'
        # 之前生成的api_key 和secret
        api_key = 'ZDlmOTkzMjlhNDc4NDY5Y2I1M2I0MzQwNGU4ZmM1OTNmM'
        secret = 'ZjlhOWZkY2JlZjlkNGUzOGIyNDc5ZmQ4ODNiYTI1MjM3M'
        authobj = {
            'api_key': api_key,
            'upn': 'gateone',
            'timestamp': str(int(time.time() * 1000)),
            'signature_method': 'HMAC-SHA1',
            'api_version': '1.0'
        }
        authobj['signature'] = request_info.create_signature(secret, authobj['api_key'], authobj['upn'], authobj['timestamp'])
        auth_info_and_server = {'url': gateone_server, 'auth': authobj}
        print(1)
        return JsonResponse(auth_info_and_server)



# class AssetsJsonView(View):
#
#     def get(self, request, *args, **kwargs):
#         request_info = GetArgvHelper(request)
#         request_info.auth_user()
#
#         if request_info.status():
#             data_list = data_list_all()
#
#             result = {
#                 'table_config': table_config,
#                 'data_list': list(data_list),
#                 'global_dict': {
#                     'assets_type_choices': models.Host.assets_type_choices,
#                 }
#             }
#             return HttpResponse(json.dumps(result))
#         else:
#             return redirect('/backend/403.html')





