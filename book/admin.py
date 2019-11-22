
from __future__ import unicode_literals

from django.contrib import admin
from django.http import HttpResponse
from datetime import datetime, timedelta

from import_export.admin import ImportExportModelAdmin
from openpyxl import Workbook
from dateutil import parser


# Register your models here.
from .models import *
class ReadOnlyModelAdmin(admin.ModelAdmin):
    """ModelAdmin class that prevents modifications through the admin.

    The changelist and the detail view work, but a 403 is returned
    if one actually tries to edit an object.
    """

    actions = None

    def get_readonly_fields(self, request, obj=None):
        return self.fields or [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    # Allow viewing objects but not actually changing them
    def has_change_permission(self, request, obj=None):
        if request.method not in ('GET', 'HEAD'):
            return False
        return super(ReadOnlyModelAdmin, self).has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False


class UserAdmin(admin.ModelAdmin):
    list_display = ('username','email','password','is_password_set','is_staff','date_join')
    ordering =['-id']
    list_per_page =20
    save_on_top = True


class ProjectGroupAdmin(admin.ModelAdmin):
    list_display =('project_name','id')
    search_fields = ('project_name',)


class  ProjectPeopleAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'attendance_group')

    search_fields = ('name', 'attendance_group')
    ordering = ['-id']
    save_on_top = True
    list_per_page = 50

class AttendanceAdmin(admin.ModelAdmin):
    actions = ['export_as_excel']  # 增加动作, 对应相应的方法名
    # list_display = ('people', 'attendance_date', 'reason', 'in_date', 'back_date', 'note')
    list_display = ('people', 'project_group', 'attendance_date', 'reason', 'in_date', 'back_date',
                    'note', 'duration')
    radio_fields = {'note': admin.VERTICAL}
    list_filter = ('attendance_date', 'note')
    search_fields = ('people__name', )
    ordering = ['-id']
    save_on_top = True
    list_per_page = 50

    def get_queryset(self, request):
        qs = super(AttendanceAdmin, self).get_queryset(request)
        return qs

    def project_group(self, obj):
        return obj.people.project.project_name

    def duration(self, obj):
        return round((parser.parse(str(obj.back_date)) - parser.parse(str(obj.in_date))).seconds / 3600.0, 1)

    def export_as_excel(self, request, queryset):  # 具体的导出csv方法的实现
        meta = self.model._meta
        field_names = []

        for field in meta.fields:
            if field.name == 'people':
                field_name = '姓名'
            elif field.name == 'attendance_date':
                field_name = '打卡日期'
            elif field.name == 'in_date':
                field_name = '签到时间'
            elif field.name == 'back_date':
                field_name = '签退时间'
            elif field.name == 'reason':
                field_name = '具体事项'
            elif field.name == 'note':
                field_name = '备注'
            else:
                continue
            field_names.append(field_name)
        field_names.append('加班时长（小时）')
        field_names.append('项目组')
        response = HttpResponse(content_type='application/msexcel')
        response['Content-Disposition'] = f'attachment; filename={meta}.xlsx'
        wb = Workbook()
        ws = wb.active
        ws.append(field_names)
        for obj in queryset:
            data = []
            for field in field_names:
                if field == '姓名':
                    res = obj.people.name
                elif field == '项目组':
                    res = obj.people.project.project_name
                elif field == '打卡日期':
                    res = obj.attendance_date
                elif field == '签到时间':
                    res = obj.in_date
                elif field == '签退时间':
                    res = obj.back_date
                elif field == '具体事项':
                    res = obj.reason
                elif field == '备注':
                    if obj.note == 'M':
                        res = '加班'
                    else:
                        res = '考勤'
                else:
                    res = round((parser.parse(str(obj.back_date)) - parser.parse(str(obj.in_date))).seconds / 3600.0, 1)
                data.append(res)
            ws.append(data)

        wb.save(response)
        return response

    export_as_excel.short_description = '导出Excel'  # 该动作在admin中的显示文字

    duration.short_description = '加班时长(h)'
    project_group.short_description = '项目组'







admin.site.register(User,UserAdmin)
admin.site.register(ProjectGroup,ProjectGroupAdmin)
admin.site.register(ProjectPeople,ProjectPeopleAdmin)
admin.site.register(Attendance, AttendanceAdmin)