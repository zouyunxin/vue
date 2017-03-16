# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

from .models import CityDict, Organization, Teacher
from .forms import UserAskForm
from operation.models import UserFavorite


# Create your views here.

class OrgView(View):
    """
    课程机构列表功能
    """

    def get(self, request):
        page_view = 'org'
        # 城市
        cities = CityDict.objects.all()
        # 机构
        all_orgs = Organization.objects.all()
        hot_orgs = all_orgs.order_by('-click_nums')

        # 查询
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords))

        # 类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 城市筛选
        try:
            city_id = int(request.GET.get('city'))
        except (ValueError, TypeError):
            city_id = ''
        if city_id:
            all_orgs = all_orgs.filter(city_id=city_id)

        org_nums = all_orgs.count()

        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-student_nums')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')

        # 分页
        p = Paginator(all_orgs, 5, request=request)
        try:
            page = int(request.GET.get('page'))
        except (ValueError, TypeError):
            page = 1
        orgs = p.page(page)
        return render(request, 'org-list.html', locals())


class AddUserAskView(View):
    def post(self, request):
        form = UserAskForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '请求错误'})


class OrgHomeView(View):
    """
    机构首页
    """

    def get(self, request, org_id):
        try:
            org = Organization.objects.get(id=org_id)
        except Organization.DoesNotExist:
            return HttpResponse('页面不存在！')
        page = 'home'
        org.click_nums += 1
        org.save()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2):
                has_fav = True
        all_courses = org.course_set.all()[:3]
        all_teachers = org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', locals())


class OrgCourseView(View):
    """
    机构课程
    """

    def get(self, request, org_id):
        try:
            org = Organization.objects.get(id=org_id)
        except Organization.DoesNotExist:
            return HttpResponse('页面不存在！')
        page = 'course'
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2):
                has_fav = True
        all_courses = org.course_set.all()
        return render(request, 'org-detail-course.html', locals())


class OrgDescView(View):
    """
    机构介绍
    """

    def get(self, request, org_id):
        try:
            org = Organization.objects.get(id=org_id)
        except Organization.DoesNotExist:
            return HttpResponse('页面不存在！')
        page = 'desc'
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', locals())


class OrgTeacherView(View):
    """
    机构教师
    """

    def get(self, request, org_id):
        try:
            org = Organization.objects.get(id=org_id)
        except Organization.DoesNotExist:
            return HttpResponse('页面不存在！')
        page = 'teacher'
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2):
                has_fav = True
        all_teachers = org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', locals())


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


class TeacherListView(View):
    """
    课程讲师列表
    """

    def get(self, request):
        page_view = 'teacher'
        all_teachers = Teacher.objects.all()
        hot_teachers = all_teachers.order_by('-click_nums')[:3]

        # 查询
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=keywords) |
                                               Q(work_company__icontains=keywords) |
                                               Q(work_position__icontains=keywords))

        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by('-click_nums')

        # 分页
        p = Paginator(all_teachers, 3, request=request)
        try:
            page = int(request.GET.get('page'))
        except (ValueError, TypeError):
            page = 1
        teachers = p.page(page)
        return render(request, 'teachers-list.html', locals())


def has_fav(request, fav_id, fav_type):
    result = False
    if request.user.is_authenticated():
        if UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type):
            result = True
    return result


class TeacherDetailView(View):
    """
    课程讲师详情
    """

    def get(self, request, teacher_id):
        page_view = 'teacher'
        try:
            teacher = Teacher.objects.get(id=teacher_id)
        except Teacher.DoesNotExist:
            return HttpResponse('页面不存在！')
        teacher.click_nums += 1
        teacher.save()
        has_fav_teacher = has_fav(request, teacher.id, 3)
        has_fav_org = has_fav(request, teacher.org.id, 2)
        hot_teachers = Teacher.objects.order_by('-click_nums')[:3]
        return render(request, 'teacher-detail.html', locals())
