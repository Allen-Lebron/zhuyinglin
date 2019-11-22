from __future__ import unicode_literals
from datetime import datetime
from rest_framework import viewsets
from rest_framework.decorators import action
from common.api import APIResponse

from .serializer import AttendanceSerializer
from .models import *

class AttendanceViewset(viewsets.GenericViewSet):
    serializer_class = AttendanceSerializer
    @action(methods=['POST'],detail=False)
    def attendance(self,request,*args,**kwargs):
        sz=AttendanceSerializer(data=request.data)
        if not sz.is_valid():
            return APIResponse(errors=sz.errors)
        attendance_group=sz.validated_data.get('attendance_group')
        attendance_date=sz.validated_data.get('attendance_date')
        in_date=sz.validated_data.get('in_date')
        back_date=sz.validated_data.get('back_date')
        print(attendance_date,in_date,back_date)
        try:
            attendance_date=datetime.strptime(attendance_group,'%Y-%m-%d')
            in_date=datetime.strptime(in_date,'%H-%M-%S')
            back_date = datetime.strptime(back_date,'%H-%M-%S')
        except:
            return APIResponse(errors={'date_invalid':['时间格式错误']})
        try:
            people=ProjectPeople.objects.get(attendance_group=attendance_group)
        except ProjectPeople.DoesNotExist:
            return APIResponse(errors={'name_invalid':'项目组成员不存在'})
        Attendance.objects.create(people=people,
                                  attendance_date=attendance_date,
                                  in_date=in_date,
                                  back_date=back_date)
        return APIResponse()
