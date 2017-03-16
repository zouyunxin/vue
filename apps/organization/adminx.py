# -*- coding: utf-8 -*-
__author__ = 'zyx'
__date__ = '2017/1/2 12:43'

import xadmin

from .models import CityDict, Organization, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    list_filter = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']


class OrganizationAdmin(object):
    list_display = ['name', 'desc', 'category', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']
    list_filter = ['name', 'desc', 'category', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']
    search_fields = ['name', 'desc', 'category', 'click_nums', 'fav_nums', 'image', 'address', 'city']
    relfiled_style = 'fk-ajax'

class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums',
                    'add_time']
    list_filter = ['org__name', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums',
                   'fav_nums',
                   'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(Organization, OrganizationAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
