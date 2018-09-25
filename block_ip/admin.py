from django.contrib import admin
from .models import BlockListIP, WhiteListIP

# Register your models here.

admin.site.register(BlockListIP)
admin.site.register(WhiteListIP)
