from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.decorators import method_decorator

from block_ip_address.decorators import white_list


class WhiteListAPI(APIView):
    permission_classes = ()
    authentication_classes = ()

    @method_decorator(white_list)
    def get(self, request):
        return Response("Checking", status=200)
