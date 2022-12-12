from django.contrib import admin

from apps.patient.models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):

    list_display = ("id", "user_id", "study", "status", "cancelled")
    list_filter = ("status", "cancelled")
