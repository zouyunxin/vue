# -*- coding: utf-8 -*-

from datetime import datetime
import numpy

from django.db import models
from django.db.models import Q

from organization.models import Organization, Teacher


# Create your models here.

class Course(models.Model):
    org = models.ForeignKey(verbose_name='课程机构', to=Organization, null=True, blank=True)
    teacher = models.ForeignKey(verbose_name='讲师', to=Teacher, null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u'课程名')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    is_banner = models.BooleanField(verbose_name=u'是否轮播', default=False)
    detail = models.TextField(verbose_name=u'课程详情')
    degree = models.CharField(max_length=10, verbose_name='课程难度',
                              choices=[('cj', u'初级'), ('zj', '中级'), ('gj', '高级')], default='cj')
    learn_times = models.IntegerField(verbose_name=u'学习时长/分钟', default=0)
    student_nums = models.IntegerField(verbose_name=u'学习人数', default=0)
    fav_nums = models.IntegerField(verbose_name=u'收藏人数', default=0)
    image = models.ImageField(max_length=100, verbose_name=u'封面图', upload_to='courses/%Y/%m')
    click_nums = models.IntegerField(verbose_name=u'点击数', default=0)
    category = models.IntegerField(verbose_name=u'课程类别',
                                   choices=[(1, u'前端开发'), (2, '后端开发')], default=1)
    tag = models.CharField(verbose_name=u'课程标签', max_length=10, default='')
    you_need_know = models.CharField(verbose_name=u'课程须知', max_length=300, default='')
    teacher_tell = models.CharField(verbose_name=u'老师告诉你', max_length=300, default='')
    add_time = models.DateTimeField(verbose_name=u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_lesson_nums(self):
        return self.lesson_set.all().count()

    def lessons(self):
        return self.lesson_set.all()

    def get_learn_student_nums(self):
        return self.usercourse_set.count()

    def get_learn_students(self):
        students = []
        for user_course in self.usercourse_set.all():
            students.append(user_course.user)
        return students[:5]

    def resources(self):
        return self.courseresource_set.all()

    def comments(self):
        return self.coursecomments_set.all()

    def get_users(self):
        return [user_course.user for user_course in self.usercourse_set.all()]

    def get_related_courses(self):
        return Course.objects.filter(Q(tag=self.tag) & ~Q(id=self.id))[:2]

    def get_recommended_courses(self):
        # user_ids = [user.id for user in self.usercourse_set.all()]
        # all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = []
        for user in self.get_users():
            course_ids += [course.id for course in user.get_courses()]
        courses = Course.objects.filter(id__in=course_ids)
        return courses.order_by('-click_nums')


class Lesson(models.Model):
    course = models.ForeignKey(verbose_name=u'所属课程', to=Course)
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(verbose_name=u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def videos(self):
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(verbose_name=u'所属章节', to=Lesson)
    name = models.CharField(verbose_name=u'视频名', max_length=100)
    url = models.URLField(verbose_name=u'访问地址', default='')
    learn_times = models.IntegerField(verbose_name=u'学习时长/分钟', default=0)
    add_time = models.DateTimeField(verbose_name=u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(verbose_name=u'所属课程', to=Course)
    name = models.CharField(verbose_name=u'资源名', max_length=100)
    download = models.FileField(verbose_name=u'下载地址', max_length=200, upload_to='course/resource/%Y/%m')
    add_time = models.DateTimeField(verbose_name=u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
