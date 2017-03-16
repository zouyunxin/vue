# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse, JsonResponse

from .models import UserFavorite, CourseComments, UserCourse
from courses.models import Course


# Create your views here.

class AddFavView(View):
    """
    用户收藏
    """

    def post(self, request):
        try:
            fav_id = int(request.POST.get('fav_id', 0))
            fav_type = int(request.POST.get('fav_type', 0))
        except (ValueError, TypeError):
            return JsonResponse({'status': 'fail', 'msg': u'请求错误'})

        if not request.user.is_authenticated():
            return JsonResponse({'status': 'fail', 'msg': u'用户未登录'})

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
        if exist_records:
            exist_records.delete()
            return JsonResponse({'status': 'success', 'msg': u'收藏'})
        else:
            user_fav = UserFavorite()
            user_fav.user = request.user
            user_fav.fav_id = fav_id
            user_fav.fav_type = fav_type
            user_fav.save()
            return JsonResponse({'status': 'success', 'msg': u'已收藏'})


class AddCommentView(View):
    """
    用户评论
    """

    def post(self, request):
        try:
            course_id = int(request.POST.get('course_id', 0))
            course = Course.objects.get(id=course_id)
            comments = request.POST.get('comments', '')
        except (ValueError, TypeError, Course.DoesNotExist):
            return JsonResponse({'status': 'fail', 'msg': u'请求错误'})

        if not request.user.is_authenticated():
            return JsonResponse({'status': 'fail', 'msg': u'用户未登录'})

        course_comment = CourseComments()
        course_comment.user = request.user
        course_comment.course = course
        course_comment.comments = comments
        course_comment.save()
        return JsonResponse({'status': 'success', 'msg': u'已添加评论'})


class AddUserCourse(View):
    """
    添加用户课程
    """

    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except (ValueError, TypeError, Course.DoesNotExist):
            return JsonResponse({'status': 'fail', 'msg': u'请求错误'})
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        return JsonResponse({'status': 'success', 'msg': u'添加成功'})
