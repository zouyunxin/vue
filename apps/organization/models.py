# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime

from django.db import models


# Create your models here.
class CityDict(models.Model):
    name = models.CharField(verbose_name=u'城市名', max_length=50)
    desc = models.TextField(verbose_name=u'城市描述', default='')
    add_time = models.DateTimeField(verbose_name=u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(verbose_name=u'机构名', max_length=50)
    desc = models.TextField(verbose_name=u'机构描述')
    tag = models.CharField(verbose_name=u'机构标签', default=u'世界名校', max_length=10)
    category = models.CharField(verbose_name='机构类别', max_length=5,
                                choices=[('pxjg', '培训机构'), ('gx', '高校'), ('gr', '个人')], default='pxjg')
    click_nums = models.IntegerField(verbose_name=u'点击数', default=0)
    fav_nums = models.IntegerField(verbose_name=u'收藏数', default=0)
    student_nums = models.IntegerField(verbose_name=u'学习人数', default=0)
    course_nums = models.IntegerField(verbose_name=u'课程数', default=0)
    image = models.ImageField(verbose_name=u'封面图', max_length=100, upload_to='org/%Y/%m')
    address = models.CharField(verbose_name=u'机构地址', max_length=150)
    city = models.ForeignKey(verbose_name=u'所在城市', to=CityDict)
    add_time = models.DateTimeField(verbose_name=u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'机构'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def teacher_nums(self):
        return self.teacher_set.count()


class Teacher(models.Model):
    org = models.ForeignKey(verbose_name='所属机构', to=Organization)
    name = models.CharField(verbose_name=u'讲师名', max_length=50)
    work_years = models.SmallIntegerField(verbose_name=u'工作年限', default=0)
    age = models.SmallIntegerField(verbose_name=u'年龄', default=18)
    work_company = models.CharField(verbose_name=u'就职公司', max_length=50)
    work_position = models.CharField(verbose_name=u'公司职位', max_length=50)
    points = models.CharField(verbose_name=u'教学特点', max_length=50)
    click_nums = models.IntegerField(verbose_name=u'点击数', default=0)
    fav_nums = models.IntegerField(verbose_name=u'收藏数', default=0)
    image = models.ImageField(verbose_name=u'头像', max_length=100, upload_to='teacher/%Y/%m', default='')
    add_time = models.DateTimeField(verbose_name=u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'讲师'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_course_nums(self):
        return self.course_set.count()

    def get_courses(self):
        return [course for course in self.course_set.all()]