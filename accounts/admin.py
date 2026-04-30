from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.



@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
            ('User Role Info',{'fields':('role',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('User Role Info', {'fields':('role',)}),
    )



# ✔ Custom User modelni admin panelga qo‘shyapti
# ✔ Default Django user adminni kengaytiryapti
# ✔ role fieldni:

# ro‘yxatda ko‘rsatadi
# edit sahifaga qo‘shadi---------Fieldsets sahifani edit qiladi o'zgartiradi
# create sahifaga ham qo‘shadi---------add_fieldsets 1