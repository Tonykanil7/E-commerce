from django.contrib import admin

# Register your models here.

from app1.models import Menu,MenuItem

admin.site.register(Menu)
admin.site.register(MenuItem)