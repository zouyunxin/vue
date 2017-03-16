# -*- coding: utf-8 -*-
__author__ = 'zyx'
__date__ = '2017/1/8 19:28'

import re

from django import forms

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

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
