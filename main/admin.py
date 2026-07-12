from django.contrib import admin

from .models import (
    Doctor,
    Patient,
    Receptionist,
    Appointment,
    MedicalRecord,
    Prescription,
)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "first_name",
        "last_name",
        "specialization",
        "contact_number",
    )
    search_fields = (
        "first_name",
        "last_name",
        "license_number",
    )
    list_filter = ("specialization",)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "first_name",
        "last_name",
        "sex",
        "contact_number",
    )
    search_fields = (
        "first_name",
        "last_name",
    )
    list_filter = ("sex",)


@admin.register(Receptionist)
class ReceptionistAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "first_name",
        "last_name",
        "employee_id",
        "contact_number",
    )
    search_fields = (
        "first_name",
        "last_name",
        "employee_id",
    )




@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "doctor",
        "visit_date",
    )
    search_fields = (
        "patient__first_name",
        "patient__last_name",
        "doctor__first_name",
        "doctor__last_name",
    )


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = (
        "appointment",
        "medication_name",
        "issued_date",
    )
    search_fields = (
        "medication_name",
    )