from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save, post_delete


class BlockListIP(models.Model):
    ip_address = models.CharField(max_length=45)

    def get_ip_address(self):
        return self.ip_address

    def __str__(self):
        return "Blocked IP {}".format(self.ip_address)


class WhiteListIP(models.Model):
    ip_address = models.CharField(max_length=45)

    def __str__(self):
        return "White IP address {}".format(self.ip_address)


def clear_cache(sender, instance, **kwargs):
    cache.set("ip:list", BlockListIP.objects.all())


post_save.connect(clear_cache, sender=BlockListIP)
post_delete.connect(clear_cache, sender=BlockListIP)
