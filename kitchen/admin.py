from django.contrib import admin
from .models import Kitchen, MenuItem, Order

admin.site.register(Kitchen)
admin.site.register(MenuItem)
admin.site.register(Order)