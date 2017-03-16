# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse

from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetForm, ResetPwdForm, UserImageForm, UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredView
from operation.models import UserFavorite
from organization.models import Organization, Teacher
from courses.models import Course


# Create your views here.

class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username) | Q(nick_name=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None
        return None


class LogoutView(View):
    """
    用户登出
    """

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'error': u'用户未激活！'})
            else:
                return render(request, 'login.html', {'error': u'用户名或密码错误！'})
        else:
            return render_to_response('login.html', locals(), RequestContext(request))


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', locals())

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                error = u'该邮箱已经被注册！'
                return render(request, 'register.html', locals())
            password = request.POST.get('password', '')
            user = UserProfile()
            user.username = email
            user.email = email
            user.password = make_password(password)
            user.is_active = False
            user.save()

            # 欢迎注册慕学在线网
            request.user.add_message('欢迎注册慕学在线网！')

            if send_register_email(email, 'register'):
                return HttpResponseRedirect('/login')
            else:
                error = '请输入一个有效的邮箱！'
                return render(request, 'register.html', locals())
        else:
            return render(request, 'register.html', locals())


class ActiveUserView(View):
    def get(self, request, code):
        try:
            record = EmailVerifyRecord.objects.get(code=code)
            user = UserProfile.objects.get(email=record.email)
            user.is_active = True
            user.save()
            return HttpResponseRedirect('/login')
        except EmailVerifyRecord.DoesNotExist:
            return HttpResponse('%s 对象不存在，链接失效！' % 'EmailVerifyRecord')
        except UserProfile.DoesNotExist:
            return HttpResponse('%s 对象不存在，链接失效！' % 'UserProfile')


class ForgetPwdView(View):
    def get(self, request):
        form = ForgetForm()
        return render(request, 'forgetpwd.html', locals())

    def post(self, request):
        form = ForgetForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return HttpResponse('邮件已经发送，请查收！')
        else:
            return render(request, 'forgetpwd.html', locals())


class ResetPwdView(View):
    def get(self, request, code):
        try:
            record = EmailVerifyRecord.objects.get(code=code)
            email = record.email
            form = ResetPwdForm()
            return render(request, 'reset_pwd.html', locals())
        except EmailVerifyRecord.DoesNotExist:
            return HttpResponse('%s 对象不存在，链接失效！' % 'EmailVerifyRecord')

    def post(self, request):
        form = ResetPwdForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email', '')
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            if password1 != password2:
                error = '密码输入不一致！'
                return render(request, 'reset_pwd.html', locals())
            try:
                user = UserProfile.objects.get(email=email)
            except UserProfile.DoesNotExist:
                return HttpResponse('%s 对象不存在，链接失效！' % 'UserProfile')
            user.password = make_password(request.POST.get('password1'))
            user.save()
            return HttpResponseRedirect('/login')
        else:
            email = request.POST.get('email', '')
            return render(request, 'reset_pwd.html', locals())


class UserPwdView(LoginRequiredView):
    """
    个人中心密码修改
    """

    def post(self, request):
        form = ResetPwdForm(request.POST, instance=request.user)
        if form.is_valid():
            # 密码修改成功后，Django后台会自动登出
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            print form.errors.as_json()
            return JsonResponse(form.errors)


class UserInfoView(LoginRequiredView):
    """
    用户信息
    """

    def get(self, request):
        user = request.user
        return render(request, 'usercenter-info.html', locals())

    def post(self, request):
        form = UserInfoForm(request.POST, instance=request.user)
        if form.is_valid():
            if form.save():
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'failure'})
        else:
            return JsonResponse(form.errors)


class UserImageView(LoginRequiredView):
    """
    用户修改头像
    """

    def post(self, request):
        # 为什么最上面这种方式不生效？
        # image_form = UserImageForm(request.FILES, instance=request.user)
        # image_form = UserImageForm({}, request.FILES, instance=request.user)
        image_form = UserImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '请求错误'})


class SendEmailCodeView(LoginRequiredView):
    """
    发送邮箱验证码
    """

    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return JsonResponse({'email': '邮箱已经存在'})
        send_register_email(email, 'update_email')
        return JsonResponse({'status': 'success'})


class UserEmailView(LoginRequiredView):
    """
    修改个人邮箱
    """

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        if EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email'):
            user = request.user
            user.email = email
            user.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'email': '验证出错'})


class MyCourseView(LoginRequiredView):
    """
    我的课程
    """

    def get(self, request):
        courses = request.user.get_courses()
        return render(request, 'usercenter-mycourse.html', locals())


class MyFavOrgView(LoginRequiredView):
    """
    我收藏的课程机构
    """

    def get(self, request):
        orgs = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = Organization.objects.get(id=org_id)
            orgs.append(org)
        return render(request, 'usercenter-fav-org.html', locals())


class MyFavCourseView(LoginRequiredView):
    """
    我收藏的课程机构
    """

    def get(self, request):
        courses = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            courses.append(course)
        return render(request, 'usercenter-fav-course.html', locals())


class MyFavTeacherView(LoginRequiredView):
    """
    我收藏的课程机构
    """

    def get(self, request):
        teachers = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teachers.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', locals())


class MyMessageView(LoginRequiredView):
    """
    我的消息
    """

    def get(self, request):
        all_messages = request.user.get_messages()

        # 分页
        p = Paginator(all_messages, 3, request=request)
        try:
            page = int(request.GET.get('page'))
        except (ValueError, TypeError):
            page = 1
        try:
            messages = p.page(page)
        except (EmptyPage, PageNotAnInteger):
            return HttpResponse('页面不存在！')
        request.user.clear_unread_messages()
        return render(request, 'usercenter-message.html', locals())


class IndexView(View):
    """
    首页
    """

    def get(self, request):
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        orgs = Organization.objects.all()[:15]
        return render(request, 'index.html', locals())


class LoginUnsafeView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # Django的ORM已对SQL注入等攻击进行过防护
        # username    ' or 1=1#
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        import MySQLdb
        conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='111111', db='mxonline', charset='utf8')
        cursor = conn.cursor()
        sql_select = "select * from users_userprofile where email='{0}' and password='{1}'".format(username, password)
        result = cursor.execute(sql_select)
        for user in cursor.fetchall():
            pass
        return HttpResponseRedirect(reverse('index'))


def page_not_found(request):
    response = render_to_response('404.html', context_instance=RequestContext(request))
    response.status_code = 404
    return response


def internal_server_error(request):
    response = render_to_response('500.html', context_instance=RequestContext(request))
    response.status_code = 500
    return response
