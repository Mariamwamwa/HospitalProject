from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from .models import Patient
from .forms import UserRegisterForm, PatientForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Patient, Appointment, MedicalRecord, Prescription
from datetime import datetime, timedelta
from .models import Appointment

# ==========================================
# HOME
# ==========================================

def home(request):
    return render(request, 'home/home.html')
def about(request):
    return render(request, 'home/about.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if hasattr(user, "patient_profile"):
                redirect_url = "patient_dashboard"
            elif hasattr(user, "doctor_profile"):
                redirect_url = "doctor_dashboard"
            elif hasattr(user, "receptionist_profile"):
                redirect_url = "receptionist_dashboard"
            else:
                redirect_url = "home"

            return render(request, "authentication/login.html", {
                "login_success": True,
                "redirect_url": redirect_url,
            })

        return render(request, "authentication/login.html", {
            "error": "Invalid username or password."
        })

    return render(request, "authentication/login.html")


def patient_register(request):
    return render(request, "authentication/register_patient.html")


def forgot_password(request):
    return render(request, "authentication/forgot_password.html")

def register(request):

    if request.method == "POST":

        # ==========================
        # Account
        # ==========================
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # ==========================
        # Patient Information
        # ==========================
        first_name = request.POST.get("first_name")
        middle_name = request.POST.get("middle_name")
        last_name = request.POST.get("last_name")

        date_of_birth = request.POST.get("date_of_birth")

        sex = request.POST.get("sex")

        blood_type = request.POST.get("blood_type")

        height = request.POST.get("height")

        weight = request.POST.get("weight")

        address = request.POST.get("address")

        contact_number = request.POST.get("contact_number")

        profile_picture = request.FILES.get("profile_picture")

        # ==========================
        # Validation
        # ==========================
        if password1 != password2:
            return render(
                request,
                "authentication/register_patient.html",
                {
                    "error": "Passwords do not match."
                }
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "authentication/register_patient.html",
                {
                    "error": "Username already exists."
                }
            )

        if User.objects.filter(email=email).exists():
            return render(
                request,
                "authentication/register_patient.html",
                {
                    "error": "Email already exists."
                }
            )

        # ==========================
        # Create User
        # ==========================
        user = User.objects.create_user(

            username=username,

            email=email,

            password=password1,

            first_name=first_name,

            last_name=last_name

        )

        # ==========================
        # Create Patient
        # ==========================
        Patient.objects.create(

            user=user,

            first_name=first_name,

            middle_name=middle_name,

            last_name=last_name,

            date_of_birth=date_of_birth,

            sex=sex,

            blood_type=blood_type,

            height=height if height else None,

            weight=weight if weight else None,

            address=address,

            contact_number=contact_number,

            profile_picture=profile_picture

        )

        messages.success(
            request,
            "Registration successful! You can now log in."
        )

        return redirect("login")

    return render(
        request,
        "authentication/register_patient.html"
    )


@login_required
def patient_dashboard(request):
    patient = request.user.patient_profile

    appointments = Appointment.objects.filter(
    patient=patient
).order_by("date", "time")
    medical_records = MedicalRecord.objects.filter(patient=patient)
    prescriptions = Prescription.objects.filter(
        appointment__patient=patient
    )

    context = {
        "patient": patient,
        "appointments": appointments,
        "medical_records": medical_records,
        "prescriptions": prescriptions,
    }

    return render(request, "patients/dashboard/patient_dashboard.html", context)
    
def logout(request):
    return render(request, "authentication/logout.html")
def patient_appointment_list(request):
    return render(request, 'patients/appointment/appointment_list.html')


def book_appointment(request):

    patient = request.user.patient_profile


    if request.method == "POST":

        # Temporary values
        appointment = Appointment()

        appointment.patient = patient

        appointment.doctor_id = 1   # temporary doctor
        appointment.date = "2026-07-15"

        appointment.start_time = "09:00"

        # calculate end time
        start = datetime.strptime(
            appointment.start_time,
            "%H:%M"
        )

        end = start + timedelta(hours=1)

        appointment.end_time = end.time()

        appointment.reason = "Regular check-up"


        appointment.save()


        return redirect(
            "patient_appointment_list"
        )


    return render(
        request,
        "patients/appointment/appointment_booking.html"
    )

def patient_medical_record(request):
    return render(request, "patients/medical_records/medical_record_list.html")
def patient_medical_detail(request):
    return render(request, "patients/medical_records/medical_record_detail.html")
def patient_health_summary(request):
    return render(request, "patients/medical_records/health_summary_ai.html")
def patient_account(request):
    return render(request, "patients/patient_details/patient_account.html")
