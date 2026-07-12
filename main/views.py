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
from .models import Appointment, MedicalRecord, Prescription, Doctor
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import MedicalRecord
from django.db.models import Q
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


    # ALL APPOINTMENTS
    appointments = Appointment.objects.filter(
        patient=patient
    ).order_by(
        "date"
    )


    # COUNTS
    appointment_count = appointments.count()


    prescription_count = Prescription.objects.filter(
        appointment__patient=patient
    ).count()


    medical_records = MedicalRecord.objects.filter(
        patient=patient
    )


    medical_record_count = medical_records.count()


    doctor_count = Doctor.objects.count()



    # UPCOMING APPOINTMENT

    upcoming_appointment = appointments.filter(
        date__gte=timezone.localdate()
    ).order_by(
        "date"
    ).first()



    # HISTORY

    appointment_history = appointments.filter(
        status__in=[
            "Completed",
            "Cancelled"
        ]
    ).order_by(
        "-date"
    )



    context = {

        "patient": patient,

        # dashboard cards
        "appointment_count": appointment_count,
        "prescription_count": prescription_count,
        "medical_record_count": medical_record_count,
        "doctor_count": doctor_count,


        # dashboard sections
        "appointments": appointments,
        "appointment_history": appointment_history,
        "upcoming_appointment": upcoming_appointment,


        # other data
        "medical_records": medical_records,

    }


    return render(
        request,
        "patients/dashboard/patient_dashboard.html",
        context
    ) 
def logout(request):
    return render(request, "authentication/logout.html")
def forgot_password(request):
    return render(request, "authentication/forgot_password.html")


@login_required
def book_appointment(request):

    patient = request.user.patient_profile

    appointment = None

    doctors = Doctor.objects.all() 
    # Check if this is a reschedule request
    reschedule_id = request.GET.get("reschedule")


    if reschedule_id:

        appointment = get_object_or_404(
            Appointment,
            id=reschedule_id,
            patient=patient
        )


    if request.method == "POST":


        if appointment:
            # Update existing appointment

            appointment.doctor_id = request.POST.get("doctor")

            appointment.date = request.POST.get("date")

            appointment.time_period = request.POST.get(
                "time_period"
            )

            appointment.reason = request.POST.get(
                "reason"
            )

            appointment.status = "Pending"


        else:
            # Create new appointment

            appointment = Appointment()

            appointment.patient = patient

            appointment.doctor_id = request.POST.get(
                "doctor"
            )

            appointment.date = request.POST.get(
                "date"
            )

            appointment.time_period = request.POST.get(
                "time_period"
            )

            appointment.reason = request.POST.get(
                "reason"
            )

            appointment.status = "Pending"


        appointment.save()


        return redirect(
            "patient_appointment_list"
        )


    context = {

        "appointment": appointment,
        "doctors": doctors,
    }


    return render(
        request,
        "patients/appointment/appointment_booking.html",
        context
    )

@login_required
def patient_appointment_list(request):

    patient = request.user.patient_profile

    appointments = Appointment.objects.filter(
        patient=patient
    ).select_related("doctor")

    search = request.GET.get("search")
    status = request.GET.get("status")

    if search:
        appointments = appointments.filter(
            Q(doctor__user__first_name__icontains=search) |
            Q(doctor__user__last_name__icontains=search) |
            Q(reason__icontains=search)
        )

    if status:
        appointments = appointments.filter(status=status)

    appointments = appointments.order_by("date")

    context = {
        "appointments": appointments,
        "upcoming_count": Appointment.objects.filter(
            patient=patient,
            status__in=["Pending", "Confirmed"]
        ).count(),
        "completed_count": Appointment.objects.filter(
            patient=patient,
            status="Completed"
        ).count(),
        "cancelled_count": Appointment.objects.filter(
            patient=patient,
            status="Cancelled"
        ).count(),
    }

    return render(
        request,
        "patients/appointment/appointment_list.html",
        context
    )


def patient_health_summary(request):
    return render(request, "patients/medical_records/health_summary_ai.html")
def patient_account(request):
    return render(request, "patients/patient_details/patient_account.html")
def doctor_list(request):
    return render(request, "patients/doctors/doctors_list.html")

@login_required
def appointment_detail(request, id):

    patient = request.user.patient_profile

    appointment = get_object_or_404(
        Appointment,
        id=id,
        patient=patient
    )

    context = {
        "appointment": appointment
    }


    return render(
        request,
        "patients/appointment/appointment_details.html",
        context
    )
@login_required
def patient_medical_record(request):
    patient = request.user.patient_profile

    records = MedicalRecord.objects.filter(
        patient=patient
    ).select_related(
        "doctor",
        "doctor__user"
    ).order_by("-visit_date")

    search = request.GET.get("search")

    if search:
        records = records.filter(
            Q(diagnosis__icontains=search) |
            Q(prescription__icontains=search) |
            Q(notes__icontains=search) |
            Q(doctor__user__first_name__icontains=search) |
            Q(doctor__user__last_name__icontains=search) |
            Q(doctor__specialization__icontains=search)
        )

    context = {
        "records": records,
        "total_records": records.count(),
    }

    return render(
        request,
        "patients/medical_records/medical_record_list.html",
        context,
    )