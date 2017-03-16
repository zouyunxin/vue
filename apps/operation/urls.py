# -*- coding: utf-8 -*-
__author__ = 'zyx'
__date__ = '2017/1/8 19:42'

from django.conf.urls import url

from .views import AddFavView, AddCommentView, AddUserCourse

urlpatterns = [
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),
    url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),
    url(r'^add_user_course/(?P<course_id>\d+)/$', AddUserCourse.as_view(), name='add_user_course'),

]
