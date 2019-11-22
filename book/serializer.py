from __future__ import  unicode_literals
from rest_framework import serializers
class AttendanceSerializer(serializers.Serializer):
    attendance_group=serializers.CharField(label='考勤系统用户名',help_text='考勤系统用户名')
    attendance_date=serializers.CharField(label='考勤时间',help_text='考勤时间')
    in_date=serializers.CharField(label='签到时间',help_text='签到时间')
    back_date=serializers.CharField(label='签退时间',help_text='签退时间')