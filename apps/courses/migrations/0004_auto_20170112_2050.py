# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-01-12 20:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_course_org'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='students',
            new_name='student_nums',
        ),
    ]
