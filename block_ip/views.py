from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.decorators import method_decorator

from block_ip.models import BlockListIP
from block_ip_address.decorators import white_list


class WhiteListAPI(APIView):
    permission_classes = ()
    authentication_classes = ()

    white_list_ip = True

    # @method_decorator(white_list)
    def get(self, request):
        return Response("Checking", status=200)


class BlockIPList(APIView):

    def get(self, request):
        response = BlockListIP.objects.all().values('id', 'ip_address')
        return Response(response, status=200)

    def post(self, request):
        obj = BlockListIP.objects.filter(pk=request.data['id'])[0]
        obj.delete()
        return Response('Done', status=200)


class TestView(View):
    white_list_ip = True

    def get(self, request):
        html = "<html><body>It is now</body></html>"
        return HttpResponse(html)
