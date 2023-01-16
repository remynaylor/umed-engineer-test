from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from apps.patient.models import Patient, PatientDocument


@admin.register(Patient)
class PatientAdmin(SimpleHistoryAdmin):

    list_display = ("id", "user_id", "study", "status", "cancelled")
    list_filter = ("status", "cancelled")
    actions = ['send_enrolment_emails']

    @admin.action(description='Send enrolment emails')
    def send_enrolment_emails(self, request, queryset):
        queryset.send_enrolment_emails()

@admin.register(PatientDocument)
class PatientDocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "patient")

