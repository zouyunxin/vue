# -*- coding: utf-8 -*-
"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve
import xadmin

from users.views import LoginView, LogoutView, RegisterView, ActiveUserView, ForgetPwdView, ResetPwdView, IndexView, \
    LoginUnsafeView
from organization.views import OrgView
from .settings import MEDIA_ROOT, STATIC_ROOT

urlpatterns = [
    # 后台管理路径
    url(r'^xadmin/', xadmin.site.urls),

    # 静态文件路径
    # url(r'^static/(?P<path>.*/$)', serve, {'document_root': STATIC_ROOT}),
    url(r'^media/(?P<path>.*/$)', serve, {'document_root': MEDIA_ROOT}),

    # url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^$', IndexView.as_view(), name='index'),
    # url(r'^login/$', LoginUnsafeView.as_view(), name='login'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<code>.*)/$', ActiveUserView.as_view()),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget'),
    url(r'^reset/$', ResetPwdView.as_view(), name='reset'),
    url(r'^reset/(?P<code>.*)/$', ResetPwdView.as_view()),

    url(r'^org/', include('organization.urls', namespace='org')),
    url(r'^course/', include('courses.urls', namespace='course')),
    url(r'^operation/', include('operation.urls', namespace='operation')),
    url(r'^user/', include('users.urls', namespace='user')),

]

# 全局错误页面配置
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.internal_server_error'
