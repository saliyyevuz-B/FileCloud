from django.contrib import admin
from .models import File,SharedLink
# Register your models here.

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('title','owner','size','is_public','views','created_at','is_expired_status')
    list_filter = ('is_public','created_at','owner')
    search_fields = ('title','owner__username')
    readonly_fields = ('views','created_at',)



    def is_expired_status(self, obj):
        return obj.is_expired
    is_expired_status.boolean = True
    is_expired_status.short_description = "Muddati o'tgan"



@admin.register(SharedLink)
class SharedLinkAdmin(admin.ModelAdmin):
    list_display = ('file', 'token', 'is_active', 'expire_date', 'created_at')
    list_filter = ('is_active', 'created_at')
    readonly_fields = ('token', 'created_at')