from __future__ import unicode_literals
from django.db import models

from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
# Create your models here.
class User(models.Model):

    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    username = models.CharField('昵称',max_length=128, unique=True, help_text='昵称长度4-20个字符，支持中英文、数字、-、_',
        validators=[
            validators.RegexValidator('^[a-zA-Z0-9-_\u4e00-\u9fa5]+$',
                                      '昵称长度4-20个字符，支持中英文、数字、-、_', 'invalid')
        ])
    password = models.CharField('密码',max_length=256,blank=True, null=True)
    email = models.EmailField('邮箱',unique=True,default=None,null=True, blank=True)
    sex = models.CharField('性别',max_length=32, choices=gender, default="男")
    c_time = models.DateTimeField(auto_now_add=True)
    is_password_set=models.BooleanField('是否设置密码',default=True,help_text='true:设置密码，false：生成随机密码')
    date_join=models.DateTimeField('注册时间',default=timezone.now)
    is_staff=models.BooleanField('是否职员',default=False)
    objects=UserManager()
    USERNAME_FIELD='APPLE'
    REQUIERED_FIELD=['hello dog']
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"


class ProjectGroup(models.Model):
    project_name=models.CharField('项目组名称',max_length=50)
    def __str__(self):
        return '%s' %self.project_name
    class Meta:
        verbose_name='项目组'
        verbose_name_plural=verbose_name

class ProjectPeople(models.Model):
    project=models.ForeignKey(ProjectGroup,related_name='project_people',on_delete=models.CASCADE,verbose_name='项目组')
    name=models.CharField('姓名',max_length=30,unique=True)
    attendance_group=models.CharField('考勤系统用户名',max_length=128)
    def __str__(self):
        return '%s'%self.name
    class Meta:
        verbose_name='人员表'
        verbose_name_plural=verbose_name


class Attendance(models.Model):
    people = models.ForeignKey(ProjectPeople, related_name='attendance_people', on_delete=models.CASCADE,
                               verbose_name='姓名')
    attendance_date = models.DateField('考勤时间', default=timezone.now)
    reason = models.CharField('具体事由', max_length=500, null=True, blank=True)
    in_date = models.TimeField('签到时间')
    back_date = models.TimeField('签退时间')
    NOTE_TYPE = (
        ('M', '加班'),
        ('F', '考勤')
    )
    note = models.CharField('备注', choices=NOTE_TYPE, max_length=10,
                            default='F')

    def __str__(self):
        return '%s' % self.people

    class Meta:
        verbose_name = '考勤表'
        verbose_name_plural = verbose_name