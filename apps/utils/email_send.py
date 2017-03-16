# -*- coding: utf-8 -*-
__author__ = 'zyx'
__date__ = '2017/1/4 6:46'

from random import Random

from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from MxOnline.settings import EMAIL_FROM


def random_str(randomlength=8):
    str = ''
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    for i in range(randomlength):
        str += chars[Random().randint(0, len(chars) - 1)]
    return str


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    if send_type == 'update_email':
        email_record.code = random_str(4)
    else:
        email_record.code = random_str(16)
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == 'register':
        subject = '慕学在线网注册激活链接'
        message = '请点击下面的链接激活你的账号：http://127.0.0.1:2828/active/{0}'.format(email_record.code)
        if send_mail(subject, message, EMAIL_FROM, [email]):
            return True
        else:
            return False
    elif send_type == 'forget':
        subject = '慕学在线网重置密码'
        message = '请点击下面的链接重置您的密码：http://127.0.0.1:2828/reset/{0}'.format(email_record.code)
        if send_mail(subject, message, EMAIL_FROM, [email]):
            return True
        else:
            return False
    elif send_type == 'update_email':
        subject = '慕学在线网邮箱修改验证码'
        message = '您的邮箱验证码为：{0}'.format(email_record.code)
        if send_mail(subject, message, EMAIL_FROM, [email]):
            return True
        else:
            return False

    return False
