#!/usr/bin/env python
__author__ = 'Chocolee'


from django import forms
from django.forms import fields, widgets
from repository import models
from django.core.exceptions import ValidationError
from backend.views.login import *


class FormsAddUser(forms.Form):

    username = fields.CharField(
        widget=widgets.TextInput(attrs={
            'class': 'form-control',
            'name': 'username',
            'placeholder': '用户名'}
        ),
        max_length=18,
        min_length=3,
        required=True,
        error_messages={
            'required': '用户名不能为空',
            'max_length': '用户名太长了，不能超过18个字符',
            'min_length': '用户名太短了，最少5个字符',
            'invalid': '输入的参数不合法'
        }
    )

    password = fields.CharField(
        widget=widgets.PasswordInput(attrs={
            'class': 'form-control',
            'name': 'password',
            'placeholder': '密码'}
        ),
        max_length=20,
        min_length=8,
        required=True,
        error_messages={
            'required': '密码不能为空',
            'max_length': '用户名太长了，不能超过20位字符',
            'min_length': '用户名太短了，至少8位字符',
            'invalid': '输入的参数不合法'
        }
    )

    role_id = fields.IntegerField(
                widget=widgets.Select(attrs={
                    'class': 'form-control',
                    'name': 'role_id'
                })
            )

    # 动态获取数据库数据
    def __init__(self, *args, **kwargs):
        super(FormsAddUser, self).__init__(*args, **kwargs)
        self.fields['role_id'].widget.choices = models.Role.objects.values_list('id', 'caption')

    sex = fields.ChoiceField(
        choices=((1, '男'), (0, '女'),),
        initial=1,
        widget=widgets.RadioSelect(attrs={
            'name': 'sex',
            'class': 'radio-inline'
        })
    )

    realname = fields.CharField(
        widget=widgets.TextInput(attrs={
            'class': 'form-control',
            'name': 'realname',
            'placeholder': '真实姓名'}
        ),
        max_length=20,
        min_length=2,
        required=True,
        error_messages={
            'required': '不能为空',
            'max_length': '用户名太长了，不能超过20个字符',
            'min_length': '用户名太短了，至少2个字符',
            'invalid': '输入的参数不合法'
        }
    )


    phone = fields.CharField(
        widget=widgets.TextInput(attrs={
            'class': 'form-control',
            'name': 'phone',
            'placeholder': '手机号'}
        ),
        max_length=11,
        min_length=11,
        required=True,
        error_messages={
            'required': '不能为空',
            'max_length': '手机号格式不对',
            'min_length': '手机号格式不对',
            'invalid': '输入的参数不合法'
        }
    )


    email = fields.CharField(
        widget=widgets.EmailInput(attrs={
            'class': 'form-control',
            'name': 'email',
            'placeholder': '邮箱'}
        ),
        max_length=30,
        min_length=3,
        required=True,
        error_messages={
            'required': '不能为空',
            'max_length': '邮箱名太长了，不能超过30个字符',
            'min_length': '邮箱名太短了，至少3个字符',
            'invalid': '输入的参数不合法'
        }
    )

    def clean_username(self):
        v = self.cleaned_data['username']
        if models.User.objects.filter(username=v).count():
            raise ValidationError('用户名已存在')
        return v

    # clean方法，对整体错误进行验证
    def clean(self):
        value_dict = self.cleaned_data
        v1 = value_dict.get('username')
        if v1 == "lee":
            raise ValidationError('整体错误信息')
        return self.cleaned_data


class FormsAddAsset(forms.Form):

    hostname = fields.CharField(
        widget=widgets.TextInput(attrs={
            'class': 'form-control',
            'name': 'hostname',
            'placeholder': '主机名'}
        ),
        max_length=25,
        min_length=3,
        required=True,
        error_messages={
            'required': '主机名不能为空',
            'max_length': '主机名太长了，不能超过25个字符',
            'min_length': '主机名太短了，最少5个字符',
            'invalid': '输入的参数不合法'
        }
    )

    ip_address = fields.CharField(
        widget=widgets.TextInput(attrs={
            'class': 'form-control',
            'name': 'ip_address',
            'placeholder': 'IP地址'}
        ),
        max_length=16,
        min_length=7,
        required=True,
        error_messages={
            'required': 'IP地址不能为空',
            'max_length': 'IP地址太长了，不能超过16位',
            'min_length': 'IP地址太短了，最少7位以上',
            'invalid': '输入的参数不合法'
        }
    )

    port = fields.IntegerField(
        widget=widgets.TextInput(attrs={
            'class': 'form-control',
            'name': 'port',
            'placeholder': '端口',
            'value': '22'
            }
        ),
        max_value=65535,
        min_value=10,
        required=True,
        error_messages={
            'required': '端口不能为空',
            'max_value': '端口太大了，不能超过65535',
            'min_value': '端口太小了，最少为10以上',
            'invalid': '输入的参数不合法'
        }
    )

    idc_id = fields.IntegerField(
                widget=widgets.Select(attrs={
                    'class': 'form-control',
                    'name': 'idc_id'
                })
            )

    assets_type = fields.ChoiceField(
        choices=((1, '虚拟机'), (2, '交换机'), (3, '服务器'), (4, '防火墙'),),
        initial=1,
        widget=widgets.RadioSelect(attrs={
            'name': 'assets_type',
            'class': 'radio-inline'
        })
    )

    project_name_id = fields.IntegerField(
                widget=widgets.Select(attrs={
                    'class': 'form-control',
                    'name': 'project_name_id'
                })
            )

    env_type_id = fields.IntegerField(
                widget=widgets.Select(attrs={
                    'class': 'form-control',
                    'name': 'env_type_id'
                })
            )

    cpu = fields.CharField(
        widget=widgets.TextInput(attrs={
            'class': 'form-control',
            'name': 'cpu',
            'placeholder': 'cpu'}
        ),
        max_length=5,
        min_length=2,
        required=True,
        error_messages={
            'required': 'cpu不能为空',
            'max_length': 'cpu太长了，不能超过5个字符',
            'min_length': 'cpu太短了，最少2个字符',
            'invalid': '输入的参数不合法'
        }
    )

    memory = fields.CharField(
        widget=widgets.TextInput(attrs={
            'class': 'form-control',
            'name': 'memory',
            'placeholder': '内存'}
        ),
        max_length=6,
        min_length=2,
        required=True,
        error_messages={
            'required': '内存不能为空',
            'max_length': '内存太长了，不能超过6个字符',
            'min_length': '内存太短了，最少2个字符',
            'invalid': '输入的参数不合法'
        }
    )

    disk = fields.CharField(
        widget=widgets.TextInput(attrs={
            'class': 'form-control',
            'name': 'disk',
            'placeholder': '硬盘'}
        ),
        max_length=6,
        min_length=2,
        required=True,
        error_messages={
            'required': '硬盘不能为空',
            'max_length': '硬盘太长了，不能超过6个字符',
            'min_length': '硬盘太短了，最少2个字符',
            'invalid': '硬盘的参数不合法'
        }
    )

    # def clean_hostname(self):
    #     v = self.cleaned_data['hostname']
    #     if models.Host.objects.filter(hostname=v).count():
    #         raise ValidationError('主机名已存在')
    #     return v

    def __init__(self, *args, **kwargs):
        super(FormsAddAsset, self).__init__(*args, **kwargs)
        self.fields['idc_id'].widget.choices = models.IDC.objects.values_list('id', 'name')
        self.fields['project_name_id'].widget.choices = models.Projects.objects.values_list('id', 'project_name')
        self.fields['env_type_id'].widget.choices = models.Envlists.objects.values_list('id', 'env')

