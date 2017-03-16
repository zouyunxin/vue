# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.db.models import Q

from .models import Course, Lesson, Video, CourseResource
from operation.models import UserFavorite, UserCourse
from utils.mixin_utils import LoginRequiredView


# Create your views here.

class CourseListView(View):
    """
    课程列表
    """

    def get(self, request):
        page_view = 'course'
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = all_courses.order_by('-click_nums')[:3]

        # 查询
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_courses = all_courses.filter(Q(name__icontains=keywords) |
                                             Q(desc__icontains=keywords) |
                                             Q(detail__icontains=keywords))

        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-student_nums')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')

        # 分页
        p = Paginator(all_courses, 3, request=request)
        try:
            page = int(request.GET.get('page'))
        except (ValueError, TypeError):
            page = 1
        courses = p.page(page)
        return render(request, 'course-list.html', locals())


class CourseDetailView(View):
    """
    课程详情
    """

    def get(self, request, course_id):
        page_view = 'course'
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return HttpResponse('页面不存在！')
        course.click_nums += 1
        course.save()
        org = course.org
        tag = course.tag
        if tag:
            related_courses = Course.objects.filter(Q(tag=tag) & ~Q(id=course_id))[:2]
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2):
                has_fav_org = True
        return render(request, 'course-detail.html', locals())


class CourseVideoView(LoginRequiredView):
    """
    课程章节信息
    """

    def get(self, request, course_id):
        page_view = 'course'
        info_view = 'video'
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return HttpResponse('页面不存在！')
        # HttpResponseRedirect('/operation/add_user_course/{0}/'.format(course.id))
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            course.student_nums += 1
            course.save()
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        return render(request, 'course-info-video.html', locals())


class CourseCommentView(LoginRequiredView):
    """
    课程评论
    """

    def get(self, request, course_id):
        page_view = 'course'
        info_view = 'comment'
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return HttpResponse('页面不存在！')
        return render(request, 'course-info-comment.html', locals())
