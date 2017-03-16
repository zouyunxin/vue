# -*- coding: utf-8 -*-
__author__ = 'zyx'
__date__ = '2017/1/14 21:09'

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import View


class LoginRequiredView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredView, self).dispatch(request, *args, **kwargs)
