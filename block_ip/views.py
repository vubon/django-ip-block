from rest_framework.response import Response
from rest_framework.views import APIView


class WhiteListAPI(APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self, request):
        return Response("Checking", status=200)