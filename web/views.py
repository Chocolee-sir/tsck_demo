from django.shortcuts import render, redirect
from repository import models


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


