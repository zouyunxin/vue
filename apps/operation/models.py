# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from users.models import UserProfile
from courses.models import Course


# Create your models here.

class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'姓名')
    mobile = models.CharField(max_length=11, verbose_name=u'手机')
    course_name = models.CharField(max_length=50, verbose_name=u'课程名')
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'用户咨询'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class UserCourse(models.Model):
    user = models.ForeignKey(verbose_name='用户', to=UserProfile)
    course = models.ForeignKey(verbose_name='课程', to=Course)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'用户课程'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "{0}-{1}".format(self.user, self.course)


class CourseComments(models.Model):
    '课程评论'
    user = models.ForeignKey(verbose_name='用户', to=UserProfile)
    course = models.ForeignKey(verbose_name='课程', to=Course)
    comments = models.CharField(max_length=200, verbose_name=u'评论')
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'课程评论'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "{0}-{1}".format(self.user, self.course)


class UserFavorite(models.Model):
    user = models.ForeignKey(verbose_name='用户', to=UserProfile)
    fav_id = models.IntegerField(verbose_name=u'数据id', default=0)
    fav_type = models.IntegerField(verbose_name=u'收藏类型',
                                   choices=[(1, u'课程'), (2, u'机构'), (3, u'讲师')], default=1)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'用户收藏'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.user


class UserMessage(models.Model):
    user = models.ForeignKey(verbose_name=u'接收用户', to=UserProfile)
    message = models.CharField(verbose_name=u'消息内容', max_length=500)
    has_read = models.BooleanField(verbose_name=u'是否已读', default=False)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'用户消息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.user.username
