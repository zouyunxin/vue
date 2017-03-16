# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserProfile(AbstractUser):
    nick_name = models.CharField(verbose_name=u'昵称', max_length=50, default='')
    birthday = models.DateField(verbose_name=u'生日', null=True, blank=True)
    gender = models.CharField(verbose_name=u'性别', max_length=10,
                              choices=(('male', u'男'), ('female', '女')), default='female')
    address = models.CharField(verbose_name=u'地址', max_length=100, default='')
    mobile = models.CharField(verbose_name=u'联系电话', max_length=11, null=True, blank=True)
    image = models.ImageField(verbose_name=u'头像', max_length=100, upload_to='image/%Y/%m', default='image/default.png')
    add_time = models.DateTimeField(verbose_name=u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username

    def get_courses(self):
        return [user_course.course for user_course in self.usercourse_set.all()]

    def get_messages(self):
        return [user_message for user_message in self.usermessage_set.all()]

    def clear_unread_messages(self):
        for user_message in self.usermessage_set.filter(has_read=False):
            user_message.has_read = True
            user_message.save()
        return True

    def get_unread_messages(self):
        return [user_message for user_message in self.usermessage_set.filter(has_read=False)]

    def get_unread_nums(self):
        return self.usermessage_set.filter(has_read=False).count()

    def add_message(self, message=''):
        self.usermessage_set.create(message=message).save()
        return True


class EmailVerifyRecord(models.Model):
    code = models.CharField(verbose_name=u'验证码', max_length=20)
    email = models.EmailField(verbose_name=u'邮箱', max_length=50)
    send_type = models.CharField(verbose_name=u'验证码类型', max_length=15,
                                 choices=(('register', u'注册'), ('forget', u'找回密码'), ('update_email', u'修改邮箱')),
                                 default='register')
    # code 实例化的时间，注意default的取值datetime.now()或datetime.now
    send_time = models.DateTimeField(verbose_name=u'发送时间', default=datetime.now)

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField(verbose_name='标题', max_length=100)
    image = models.ImageField(verbose_name=u'轮播图', max_length=100, upload_to='banner/%Y/%m')
    url = models.URLField(verbose_name=u'访问地址', max_length=200)
    index = models.SmallIntegerField(verbose_name=u'顺序', default=100)
    add_time = models.DateTimeField(verbose_name=u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name
