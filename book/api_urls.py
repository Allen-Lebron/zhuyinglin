from __future__ import unicode_literals
from book import api
from demo1.router import router
router.register(r'book',api.AttendanceViewset,'book_attendance')
urlpatterns=[
]