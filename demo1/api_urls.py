from __future__ import unicode_literals

from django.conf.urls import include, url
from .router import router, router_no_slash

urlpatterns = [
    url(r'^book/', include('book.api_urls')),
]

urlpatterns += [
    url(r'', include(router.urls)),
    url(r'', include(router_no_slash.urls)),
]