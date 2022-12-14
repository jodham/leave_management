from django.contrib import admin
from .models import*
# Register your models here.
admin.site.register(Organisation)
admin.site.register(Organisation_branch)
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Leave_type)
admin.site.register(Leave_application)
