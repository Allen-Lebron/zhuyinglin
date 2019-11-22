from rest_framework import status
from rest_framework.response import Response

class APIResponse(Response):
    def __init__(self, data={'status': True}, errors=None, http_status=status.HTTP_200_OK):
        resp = {"errors": errors} if errors else data
        super(APIResponse, self).__init__(
            resp, http_status
        )