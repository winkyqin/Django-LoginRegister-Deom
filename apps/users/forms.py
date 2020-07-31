#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: 小羊驼
@contact: wouldmissyou@163.com
@time: 2020/7/29 下午2:12
@file: forms.py
@desc: 
"""
from django import forms
from django.contrib.auth import get_user_model
from django.core.cache import cache

User = get_user_model()


class FormMixin(object):
    '''
    get_errors: 获取错误信息并返回成json
    '''

    def get_errors(self):
        if hasattr(self, 'errors'):
            errors = self.errors.get_json_data()
            print(errors)
            new_errors = {}
            for key, message_dicts in errors.items():
                messages = []
                for message in message_dicts:
                    messages.append(message['message'])
                new_errors[key] = messages
            return new_errors
        else:
            return {}


class LoginForm(forms.Form, FormMixin):
    username = forms.CharField(max_length=20,error_messages={"max_length": "账号最多不能超过20个字符！", "required": "请输入用户名"})
    password = forms.CharField(max_length=20, min_length=6,
                               error_messages={"max_length": "密码最多不能超过20个字符！", "min_length": "密码最少不能少于6个字符！", "required": "请输入密码"})
    remember = forms.IntegerField(required=False)
    img_captcha = forms.CharField(min_length=4, max_length=4,
                                  error_messages={"required": "请输入图形验证码", "max_length": "图形码格式错误",
                                                  "min_length": "图形验证码格式错误"})

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()

        img_captcha = cleaned_data.get('img_captcha')
        cached_img_captcha = cache.get(img_captcha)
        if not cached_img_captcha or cached_img_captcha.lower() != img_captcha.lower():
            raise forms.ValidationError("图形验证码错误！")


class RegisterForm(forms.Form, FormMixin):
    username = forms.CharField(max_length=20, error_messages={"max_length": "账号最多不能超过20个字符！", "required": "请输入用户名"})
    telephone = forms.CharField(max_length=11, min_length=11,
                                error_messages={"max_length": "手机号格式错误", "min_length": "手机号格式错误", "required": "请输入手机号"})
    password1 = forms.CharField(max_length=20, min_length=6,
                                error_messages={"max_length": "密码最多不能超过20个字符！", "min_length": "密码最少不能少于6个字符！",
                                                "required": "请输入密码"})
    password2 = forms.CharField(max_length=20, min_length=6,
                                error_messages={"max_length": "密码最多不能超过20个字符！", "min_length": "密码最少不能少于6个字符！",
                                                "required": "请输入校验密码"})
    img_captcha = forms.CharField(min_length=4, max_length=4,
                                  error_messages={"required": "请输入图形验证码", "max_length": "图形码格式错误",
                                                  "min_length": "图形验证码格式错误"})
    sms_captcha = forms.CharField(min_length=4, max_length=4,
                                  error_messages={"required": "请输入短信验证码", "max_length": "短信验证码格式错误",
                                                  "min_length": "短信验证码格式错误"})

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('两次密码输入不一致！')

        img_captcha = cleaned_data.get('img_captcha')
        cached_img_captcha = cache.get(img_captcha)
        if not cached_img_captcha or cached_img_captcha.lower() != img_captcha.lower():
            raise forms.ValidationError("图形验证码错误！")

        telephone = cleaned_data.get('telephone')
        sms_captcha = cleaned_data.get('sms_captcha')
        cached_sms_captcha = cache.get(telephone)

        if not cached_sms_captcha or cached_sms_captcha.lower() != sms_captcha.lower():
            raise forms.ValidationError('短信验证码错误！')

        exists = User.objects.filter(telephone=telephone).exists()
        if exists:
            raise forms.ValidationError('该手机号码已经被注册！')

        username = cleaned_data.get('username')
        exists = User.objects.filter(username=username).exists()
        if exists:
            raise forms.ValidationError('此用户名已被注册，请更换用户名')

        return cleaned_data


class ForgetPasswordForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11, min_length=11,
                                error_messages={"max_length": "手机号格式错误", "min_length": "手机号格式错误", "required": "请输入手机号"})
    password1 = forms.CharField(max_length=20, min_length=6,
                                error_messages={"max_length": "密码最多不能超过20个字符！", "min_length": "密码最少不能少于6个字符！",
                                                "required": "请输入密码"})
    password2 = forms.CharField(max_length=20, min_length=6,
                                error_messages={"max_length": "密码最多不能超过20个字符！", "min_length": "密码最少不能少于6个字符！",
                                                "required": "请输入校验密码"})
    sms_captcha = forms.CharField(min_length=4, max_length=4,
                                  error_messages={"required": "请输入短信验证码", "max_length": "短信验证码格式错误",
                                                  "min_length": "短信验证码格式错误"})

    def clean(self):
        cleaned_data = super(ForgetPasswordForm, self).clean()

        telephone = cleaned_data.get('telephone')
        sms_captcha = cleaned_data.get('sms_captcha')
        cached_sms_captcha = cache.get(telephone)

        if not cached_sms_captcha or cached_sms_captcha.lower() != sms_captcha.lower():
            raise forms.ValidationError('短信验证码错误！')

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('两次密码输入不一致！')

        return cleaned_data

class ResetPasswordForm(forms.Form, FormMixin):
    old_password = forms.CharField(max_length=20, min_length=6,
                                error_messages={"max_length": "密码最多不能超过20个字符！", "min_length": "密码最少不能少于6个字符！",
                                                "required": "请输入旧密码"})
    new_password1 = forms.CharField(max_length=20, min_length=6,
                                   error_messages={"max_length": "密码最多不能超过20个字符！", "min_length": "密码最少不能少于6个字符！",
                                                   "required": "请输入新密码"})
    new_password2 = forms.CharField(max_length=20, min_length=6,
                                    error_messages={"max_length": "密码最多不能超过20个字符！", "min_length": "密码最少不能少于6个字符！",
                                                    "required": "请重复新密码"})

    def clean(self):
        cleaned_data = super(ResetPasswordForm, self).clean()

        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 != new_password2:
            raise forms.ValidationError('两次密码输入不一致！')

        return cleaned_data



class SmsCaptchaLoginForm(forms.Form,FormMixin):
    telephone = forms.CharField(max_length=11, min_length=11,
                                error_messages={"max_length": "手机号格式错误", "min_length": "手机号格式错误", "required": "请输入手机号"})
    sms_captcha = forms.CharField(min_length=4, max_length=4,
                                  error_messages={"required": "请输入短信验证码", "max_length": "短信验证码格式错误",
                                                  "min_length": "短信验证码格式错误"})
    remember = forms.IntegerField(required=False)

    def clean(self):
        cleaned_data = super(SmsCaptchaLoginForm, self).clean()

        telephone = cleaned_data.get('telephone')
        exists = User.objects.filter(telephone=telephone).exists
        if not exists:
            raise forms.ValidationError('该手机号未注册！')

        sms_captcha = cleaned_data.get('sms_captcha')
        cached_sms_captcha = cache.get(telephone)

        if not cached_sms_captcha or cached_sms_captcha.lower() != sms_captcha.lower():
            raise forms.ValidationError('短信验证码错误！')

        return cleaned_data

