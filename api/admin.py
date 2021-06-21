from django.contrib import admin
from .models import user,section,box,files
# Register your models here.
admin.site.register(user)
admin.site.register(section)
admin.site.register(box)
admin.site.register(files)
