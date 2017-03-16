# -*- coding: utf-8 -*-
__author__ = 'zyx'
__date__ = '2017/1/2 12:58'

import xadmin

from .models import UserAsk, UserCourse, CourseComments, UserFavorite, UserMessage


class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name']


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']
    list_filter = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']


class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'comments', 'add_time']
    list_filter = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user', 'course', 'comments']


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    list_filter = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
