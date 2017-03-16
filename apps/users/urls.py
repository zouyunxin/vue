# -*- coding: utf-8 -*-
__author__ = 'zyx'
__date__ = '2017/1/8 19:42'

from django.conf.urls import url

from .views import UserInfoView, UserImageView, UserPwdView, SendEmailCodeView, UserEmailView, MyCourseView, \
    MyFavOrgView, MyFavCourseView, MyFavTeacherView, MyMessageView

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name='info'),
    url(r'^image/$', UserImageView.as_view(), name='image'),
    url(r'^update/pwd/$', UserPwdView.as_view(), name='update_pwd'),
    url(r'^update/email/$', UserEmailView.as_view(), name='update_email'),
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),
    url(r'^course/$', MyCourseView.as_view(), name='course'),
    url(r'^fav/org/$', MyFavOrgView.as_view(), name='fav_org'),
    url(r'^fav/course/$', MyFavCourseView.as_view(), name='fav_course'),
    url(r'^fav/teacher/$', MyFavTeacherView.as_view(), name='fav_teacher'),
    url(r'^message/$', MyMessageView.as_view(), name='message'),

]
