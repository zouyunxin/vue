# -*- coding: utf-8 -*-
__author__ = 'zyx'
__date__ = '2017/1/8 19:42'

from django.conf.urls import url

from .views import CourseListView, CourseDetailView, CourseVideoView, CourseCommentView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='list'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='detail'),
    url(r'^info/(?P<course_id>\d+)/$', CourseVideoView.as_view(), name='info'),
    url(r'^video/(?P<course_id>\d+)/$', CourseVideoView.as_view(), name='video'),
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='comment'),

]
