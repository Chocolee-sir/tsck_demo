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
            'placeholder': '姓名'}
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


