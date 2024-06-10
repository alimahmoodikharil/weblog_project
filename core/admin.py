from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['id','first_name','last_name', 'email','is_staff',]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("first_name", "last_name", "username", "password1", "password2", "email", ),
            },
        ),
    )
    ordering = ['id']

    
