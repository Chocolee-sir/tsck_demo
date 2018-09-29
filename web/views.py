from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from repository import models
import json, hashlib, time

# Create your views here.

def login(request):
    if request.method == "GET":
        return render(request, 'web/login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(password)
        obj = models.User.objects.filter(username=username, password=password).first()
        if obj:
            role_list = models.Role.objects.filter(user2role__u__username=username)
            menu_leaf_list = models.Permission2Role.objects.filter \
                (r__in=role_list).values('p__url', 'p__caption', 'p__menu_id', 'p__icon').exclude(p__menu__isnull=True)
            action_info = models.Permission2Role.objects.filter(r__in=role_list).values('p__url')
            action_list = []
            permission_list = {}
            for i in menu_leaf_list:
                permission_list[i['p__menu_id']] = [i['p__caption'], i['p__url'], i['p__icon']]
            for item in action_info:
                action_list.append(item['p__url'])
            request.session['user_info'] = {
                'nid': obj.id,
                'username': obj.username,
                "permission_list": permission_list,
                'action_list': action_list
            }
            return redirect('/backend/index.html')
        else:
            return render(request, 'web/login.html', {'msg': "用户名或密码错误"})
    else:
        return render(request, 'web/login.html')


""" api demo 代码 """
def hash_key(key):
    v = hashlib.md5()
    v.update(bytes(key, encoding='utf-8'))
    ret = v.hexdigest()
    return ret

ck = "e10adc3949ba59abbe56e057f20f883e"

# 将这个列表放到redis里，设置过期时间
auth_list = []

@csrf_exempt  #POST不受CSRF保护
def api(request):
    auth_key_time = request.META['HTTP_AUTHKEY']
    client_auth_key, client_time = auth_key_time.split('|')
    server_time = time.time()
    # 通过时间节点，将时间久远的key先过滤掉
    if server_time - 10 > float(client_time):
        return HttpResponse('授权失败')

    # 通过空间节点，将已经访问过的key过滤掉
    if auth_key_time in auth_list:
        return HttpResponse('授权失败')

    # 然后将MD5 key进行反解对比验证
    key_time = "%s|%s" % (ck, client_time)
    server_auth_key = hash_key(key_time)

    # key对应不上，授权失败
    if client_auth_key != server_auth_key:
        return HttpResponse('授权失败')

    # 这边就用redis设置过期key就行
    auth_list.append(auth_key_time)
    if request.method == "POST":
        host_info = json.loads(str(request.body, encoding='utf-8'))
        if host_info['status'] is True:
            hostname = host_info['data']['hostname']
            host_status = models.Host.objects.filter(hostname=hostname).count()
            if host_status == 1:
                # 这边主机存在，就更新记录，不写了。
                return HttpResponse('success')
            else:
                # 这边可以创建主机，不写了。
                return HttpResponse('主机不存在')
        else:
            return HttpResponse('JSON数据异常')

