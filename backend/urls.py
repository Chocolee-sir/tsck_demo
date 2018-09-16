#!/usr/bin/env python
__author__ = 'Chocolee'


"""tsck_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from backend.views import login as loginview
from backend.views import user as userview
from backend.views import order as orderview
from backend.views import assets as assetsview

urlpatterns = [
    path('index.html', loginview.index),
    path('login-out.html', loginview.login_out),
    path('403.html', loginview.status_403),
    path('personal-info.html', loginview.personal_info),

    path('user.html', userview.index_user),
    path('add-user.html', userview.add_user),
    path('del-user.html', userview.del_user),
    path('edit-user.html', userview.edit_user),

    path('order.html', orderview.index_order),
    path('create-order.html', orderview.create_order),
    path('get-detail.html', orderview.get_detail),
    path('del-order.html', orderview.del_order),
    path('edit-order.html', orderview.edit_order),
    path('ops-handle-order.html', orderview.ops_handle_order),
    path('test-handle-order.html', orderview.test_handle_order),

    # path('assets-json.html', assetsview.AssetsJsonView.as_view()),
    path('assets.html', assetsview.AssetsView.as_view()),
    path('add-assets.html', assetsview.AssetsAddView.as_view()),
    path('edit-assets.html', assetsview.AssetsEditView.as_view()),
    path('gateone-auth.html', assetsview.AssetsGateOneAuthView.as_view()),

]
