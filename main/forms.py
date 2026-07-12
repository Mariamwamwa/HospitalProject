from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Appointment


from .models import (
    Doctor,
    Patient,
    Receptionist,
    Appointment,
    MedicalRecord,
    Prescription,
)


# ===========================
# USER REGISTRATION
# ===========================

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]


# ===========================
# DOCTOR
# ===========================

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        exclude = ["user"]


# ===========================
# PATIENT
# ===========================

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ["user"]


# ===========================
# RECEPTIONIST
# ===========================

class ReceptionistForm(forms.ModelForm):
    class Meta:
        model = Receptionist
        exclude = ["user"]


# ===========================
# APPOINTMENT
# ===========================


# ===========================
# MEDICAL RECORD
# ===========================

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = "__all__"

        widgets = {
            "diagnosis": forms.Textarea(attrs={"rows": 4}),
            "treatment_plan": forms.Textarea(attrs={"rows": 4}),
        }


# ===========================
# PRESCRIPTION
# ===========================

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = "__all__"

        widgets = {
            "instructions": forms.Textarea(attrs={"rows": 4}),
        }