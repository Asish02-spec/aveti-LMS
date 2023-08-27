from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Cususer, Admin,  Students, Teachers
 
# Register your models here.
class UserModel(UserAdmin):
    pass
 
 
admin.site.register(Cususer, UserModel)
admin.site.register(Admin)
admin.site.register(Teachers)
admin.site.register(Students)
