# -*-coding:utf-8-*-
from __future__ import unicode_literals

import re
from collections import OrderedDict
from common.api import APIResponse
from rest_framework import pagination


class CustomPaginationSerializer(pagination.PageNumberPagination):

    page_query_param = 'page'
    page_size_query_param = 'page_size'

    def get_paginated_data(self, data):
        return OrderedDict([
            ('total_count', self.page.paginator.count),
            ('total_page', self.page.paginator.num_pages),
            ('current_page', self.page.number),
            ('results', data)
        ])

    def get_paginated_response(self, data):
        return APIResponse(self.get_paginated_data(data))


