from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django import forms

from .models import (
    Doctor,
    Patient,
    Receptionist,
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
            "profile_picture",
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
            "profile_picture",
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
            "profile_picture",
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
# ADMIN REGISTRATION
# ==========================================


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):

    form = DoctorCreationForm

    list_display = (
        "user",
        "first_name",
        "last_name",
        "profile_picture",
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
        "profile_picture",
        "sex",
    )



@admin.register(Receptionist)
class ReceptionistAdmin(admin.ModelAdmin):

    form = ReceptionistCreationForm

    list_display = (
        "user",
        "first_name",
        "last_name",
        "profile_picture",
        "employee_id",
        "sex",
    )