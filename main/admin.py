from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django import forms

from .models import (
    Doctor,
    Patient,
    Receptionist,
    DoctorSchedule,
    Appointment,
    MedicalRecord,
   
)



# ==========================================
# DOCTOR FORM
# ==========================================

class DoctorCreationForm(forms.ModelForm):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    email = forms.EmailField()

    class Meta:
        model = Doctor

        fields = [
            "username",
            "password",
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "specialization",
            "sex",
            "license_number",
        ]


    def save(self, commit=True):

        doctor = super().save(commit=False)


        user = User.objects.create(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            password=make_password(
                self.cleaned_data["password"]
            )
        )


        doctor.user = user


        if commit:
            doctor.save()


        return doctor






# ==========================================
# PATIENT FORM
# ==========================================

class PatientCreationForm(forms.ModelForm):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    email = forms.EmailField()


    class Meta:

        model = Patient

        fields = [
            "username",
            "password",
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "sex",
        ]


    def save(self, commit=True):

        patient = super().save(commit=False)


        user = User.objects.create(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            password=make_password(
                self.cleaned_data["password"]
            )
        )


        patient.user = user


        if commit:
            patient.save()


        return patient






# ==========================================
# RECEPTIONIST FORM
# ==========================================

class ReceptionistCreationForm(forms.ModelForm):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    email = forms.EmailField()


    class Meta:

        model = Receptionist

        fields = [
            "username",
            "password",
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "sex",
            "employee_id",
        ]



    def save(self, commit=True):

        receptionist = super().save(commit=False)


        user = User.objects.create(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            password=make_password(
                self.cleaned_data["password"]
            )
        )


        receptionist.user = user


        if commit:
            receptionist.save()


        return receptionist







# ==========================================
# ADMIN
# ==========================================


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):

    form = DoctorCreationForm


    list_display = (
        "user",
        "first_name",
        "last_name",
        "specialization",
        "license_number",
        "sex",
    )






@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):

    form = PatientCreationForm


    list_display = (
        "user",
        "first_name",
        "last_name",
        "sex",
    )






@admin.register(Receptionist)
class ReceptionistAdmin(admin.ModelAdmin):

    form = ReceptionistCreationForm


    list_display = (
        "user",
        "first_name",
        "last_name",
        "employee_id",
        "sex",
    )





@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):

    list_display = (
        "doctor",
        "day_of_week",
        "morning_schedule",
        "afternoon_schedule",
    )


    def morning_schedule(self, obj):

        if obj.morning_available:
            return f"{obj.morning_start} - {obj.morning_end}"

        return "OFF"


    def afternoon_schedule(self, obj):

        if obj.afternoon_available:
            return f"{obj.afternoon_start} - {obj.afternoon_end}"

        return "OFF"




@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):

    list_display = (
        "patient",
        "doctor",
        "date",
        "time_period",
        "status",
    )





@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):

    list_display = (
        "patient",
        "doctor",
        "visit_date",
    )
