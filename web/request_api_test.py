#!/usr/bin/env python
__author__ = 'Chocolee'

import requests
import hashlib
import time

#requests.get(url='http://127.0.0.1:8000/web/api.html', params={'k1': 'v1', 'k2': 'v2'})


# requests.post(
#     url='http://127.0.0.1:8000/web/api.html',
#     params={'k1': 'v1', 'k2': 'v2'},  #GET形式传值
#     data={'username': '111', 'pwd': '666'},  #POST形式传值
#     headers={'a': '123'}
# )

host_data = {
    'status': True,
    'data': {
        'hostname': 'VMWARE-TEST-1001',
        'disk': {'status': True, 'data': '20G'},
        'memory': {'status': True, 'data': '1G'},
        'cpu': {'status': True, 'data': '2核'},
    }
}

current_time = time.time()
app_id = 'e10adc3949ba59abbe56e057f20f883e'
app_id_time = "%s|%s" % (app_id, current_time)


def hash_key(key):
    v = hashlib.md5()
    v.update(bytes(key, encoding='utf-8'))
    ret = v.hexdigest()
    return ret

auth_key_time = "%s|%s" % (hash_key(app_id_time), current_time)

response = requests.post(
    url='http://127.0.0.1:8000/web/api.html',
    json=host_data,
    headers={'authkey': auth_key_time},
)
print(response.text)









"""
API安全验证设计方式：



"""