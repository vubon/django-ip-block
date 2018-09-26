from django.core.cache import cache
from django.http import HttpResponseForbidden

from block_ip.models import WhiteListIP


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


def white_list(func):
    """
    :param func:
    :return:
    """
    def wrapper(request, *args, **kwargs):
        ip = get_ip_address(request)

        white_ip_address = cache.get("white:list")
        # cache.delete("ip:list")
        if white_ip_address is None:
            white_ip_address = WhiteListIP.objects.all()
            cache.set("white:list", white_ip_address)

        white_ips = [i.get_ip_address() for i in white_ip_address]

        if ip in white_ips:
            return func(request, *args, **kwargs)

        return HttpResponseForbidden("<h1> Access denied </h1>")

    return wrapper

