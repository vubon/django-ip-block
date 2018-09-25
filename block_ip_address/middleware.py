from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

from block_ip.models import BlockListIP


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

    def process_request(self, request):
        """
        :param request:
        :return:
        """
        # get IP address
        ip = get_ip_address(request)

        print(request)

        block_ip_address = cache.get("ip:list")
        # cache.delete("ip:list")
        if block_ip_address is None:
            block_ip_address = BlockListIP.objects.all()
            cache.set("ip:list", block_ip_address)

        block_ips = [i.get_ip_address() for i in block_ip_address]

        if ip in block_ips:
            return HttpResponseForbidden("Access denied")





