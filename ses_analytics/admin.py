from django.contrib import admin

from ses_analytics.models import Email

class EmailAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'to_email', 'type', 'time', 'status', 'is_read')
    ordering = ('-time',)
    search_fields = ('recipient', 'type', 'status')
    raw_id_fields = ('recipient',)

admin.site.register(Email, EmailAdmin)
