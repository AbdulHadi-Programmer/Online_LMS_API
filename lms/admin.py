from django.contrib import admin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username','is_instructor', 'is_student', 'bio', 'is_staff']

admin.site.register(CustomUser, CustomUserAdmin)

# Admin : admin , 2006
# Project: admin, 1234
