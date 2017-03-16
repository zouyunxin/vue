# -*- coding: utf-8 -*-
__author__ = 'zyx'
__date__ = '2017/1/2 18:25'

import re

from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=5, required=True)
    password = forms.CharField(max_length=20, min_length=5, required=True)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=20, min_length=5, required=True)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


class ResetPwdForm(forms.ModelForm):
    password1 = forms.CharField(max_length=20, min_length=5, required=True)
    password2 = forms.CharField(max_length=20, min_length=5, required=True)

    class Meta:
        model = UserProfile
        fields = []

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError("密码输入不一致")
        return password2

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data['password1'])
        return user.save()


class UserImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birthday', 'address', 'mobile']

    def clean_mobile(self):
        """
        验证手机是否合法
        """
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}|^176\d{8}$"
        if re.compile(REGEX_MOBILE).match(mobile):
            return mobile
        else:
            raise forms.ValidationError("手机号码不合法")
