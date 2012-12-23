from django.contrib import admin

from ses_analytics.models import Email

# TODO: Admin extension for email stats analytics
class EmailAdmin(admin.ModelAdmin):
    list_display = ('to_email', 'campaign', 'time', 'status', 'is_read')
    ordering = ('-time',)
    search_fields = ('campaign', 'status')
    #raw_id_fields = ('recipient',)

admin.site.register(Email, EmailAdmin)
