from django.contrib import admin

from .models import Configuration, Audience, Billing

@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ['ad_pk', 'submitted']
    readonly_fields = ['updated', 'timestamp']

@admin.register(Audience)
class AudienceAdmin(admin.ModelAdmin):
    list_display = ['ad_pk', 'submitted']
    readonly_fields = ['updated', 'timestamp']

@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ['ad_pk', 'submitted']
    readonly_fields = ['updated', 'timestamp']