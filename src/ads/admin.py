from django.contrib import admin

from .models import Ad

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'status']
    readonly_fields = ['updated', 'timestamp']