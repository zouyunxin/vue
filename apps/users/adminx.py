# -*- coding: utf-8 -*-
__author__ = 'zyx'
__date__ = '2017/1/2 9:43'

import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin
from django.contrib.auth.models import User
from xadmin.layout import Fieldset, Main, Side, Row, FormHelper

from .models import UserProfile, EmailVerifyRecord, Banner


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = '慕学后台管理系统'
    site_footer = '慕学在线网'
    menu_style = 'accordion'


class UserProfileAdmin(UserAdmin):
    def get_form_layout(self):
        if self.org_obj:
            self.form_layout = (
                Main(
                    Fieldset('',
                             'username', 'password',
                             css_class='unsort no_title'
                             ),
                    Fieldset(_('Personal info'),
                             Row('first_name', 'last_name'),
                             'email'
                             ),
                    Fieldset(_('Permissions'),
                             'groups', 'user_permissions'
                             ),
                    Fieldset(_('Important dates'),
                             'last_login', 'date_joined'
                             ),
                ),
                Side(
                    Fieldset(_('Status'),
                             'is_active', 'is_staff', 'is_superuser',
                             ),
                )
            )
        return super(UserAdmin, self).get_form_layout()


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    model_icon = 'fa fa-envelope'
    ordering = ['-send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    model_icon = 'fa fa-bandcamp'


# 卸载认证和授权中的用户管理
# xadmin.site.unregister(User)
# xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(xadmin.views.BaseAdminView, BaseSetting)
xadmin.site.register(xadmin.views.CommAdminView, GlobalSetting)
