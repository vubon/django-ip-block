from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

from block_ip.models import BlockListIP, WhiteListIP


def get_ip_address(request):
    """
    By this function we will get requester IP address
    :param request:
    :return:
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


class IPAddressBlock(MiddlewareMixin):
    """
        By this Middleware can block user IP address and also you can make a white list
    """

    def process_request(self, request):
        """
        :param request:
        :return:
        """
        # get IP address
        ip = get_ip_address(request)

        block_ip_address = cache.get("ip:list")
        # cache.delete("ip:list")
        if block_ip_address is None:
            block_ip_address = BlockListIP.objects.all()
            cache.set("ip:list", block_ip_address)

        block_ips = [i.get_ip_address() for i in block_ip_address]

        if ip in block_ips:
            return HttpResponseForbidden("Access denied")

    def process_response(self, request, response):
        """
        :param request:
        :param response:
        :return:
        """
        # =============== Getting user API address ================= #
        ip = get_ip_address(request)

        # ============ Making dict =================== #
        res = response.__dict__
        print(res)
        django_default = res.get('context_data')
        print(django_default)

        # ========== getting white list IP address ===================#

        white_ip_address = cache.get("white:list")
        # cache.delete("ip:list")
        if white_ip_address is None:
            white_ip_address = WhiteListIP.objects.all()
            cache.set("white:list", white_ip_address)

        white_ips = [i.get_ip_address() for i in white_ip_address]

        # ============= getting white list IP address ===================#

        # ========== Django Default View ===================#

        if django_default:
            # get View Object from views.py
            view_obj = django_default.get('view')

            if view_obj.white_list_ip:
                if ip in white_ips:
                    return response
                return HttpResponseForbidden("<h1> Access denied </h1>")

        # ============ Django Default View ===================#

        # ============ Django Rest Framework  ===================#
        rest_api = res.get('renderer_context')

        if rest_api:
            # get View Object from views.py
            view_obj = rest_api.get('view')

            permission = view_obj.permission_classes
            auth = view_obj.authentication_classes
            white_list = view_obj.white_list_ip

            if not (permission or auth) and white_list:
                if ip in white_ips:
                    return response
                return HttpResponseForbidden("<h1> Access denied </h1>")

        # ============ Django Rest Framework  ===================#

        return response





