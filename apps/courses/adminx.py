# -*- coding: utf-8 -*-
__author__ = 'zyx'
__date__ = '2017/1/2 12:10'

import xadmin

from .models import Course, Lesson, Video, CourseResource


class CourseAdmin(object):
    list_display = ['name', 'tag', 'degree', 'student_nums', 'fav_nums', 'image', 'click_nums',
                    'add_time']
    list_filter = ['name', 'tag', 'degree', 'student_nums', 'fav_nums', 'image', 'click_nums',
                   'add_time']
    search_fields = ['name', 'tag', 'degree', 'student_nums', 'fav_nums', 'image', 'click_nums']
    ordering = ['-click_nums']
    readonly_fields = ['click_nums']
    exclude = ['fav_nums']

class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    list_filter = ['course__name', 'name', 'add_time']
    search_fields = ['name']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'url', 'learn_times', 'add_time']
    list_filter = ['lesson__name', 'name', 'url', 'learn_times', 'add_time']
    search_fields = ['name', 'url', 'learn_times']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    list_filter = ['course__name', 'name', 'download', 'add_time']
    search_fields = ['name', 'download']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
