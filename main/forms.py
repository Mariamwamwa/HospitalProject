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

)

class DoctorCreationForm(forms.ModelForm):

    username = forms.CharField(
        max_length=150,
        label="Username"
    )

    email = forms.EmailField(
        label="Email"
    )

    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password"
    )


    class Meta:
        model = Doctor

        fields = [
            "username",
            "email",
            "password",

            "first_name",
            "middle_name",
            "last_name",

            "date_of_birth",
            "sex",
            "address",

            "specialization",
            "license_number",
            "contact_number",

            "profile_picture",
        ]


    def save(self, commit=True):

        doctor = super().save(commit=False)


        # Create User account
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
        )


        user.save()


        doctor.user = user


        if commit:
            doctor.save()


        return doctor
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
