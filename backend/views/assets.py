#!/usr/bin/env python
__author__ = 'Chocolee'

from backend.views.login import *
from utils.get_argv import *
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
            if action == "编辑":
                forms_edit_asset = request_info.forms_edit_asset(nid)
                render_argv = request_info.base_render_argv()
                render_argv['forms_edit_asset'] = forms_edit_asset
                render_argv['nid'] = nid
                return render(request, 'backend/backend_edit_assets.html', render_argv)
            elif action == "连接":
                return redirect('/backend/assets.html')
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





