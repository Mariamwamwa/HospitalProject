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
from .models import Patient, Appointment, MedicalRecord 
from datetime import datetime, timedelta
from .models import Appointment
from .models import Appointment, MedicalRecord, Doctor
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import MedicalRecord
from django.db.models import Q
from google import genai
from django.conf import settings
from django.http import HttpResponse
from google import genai
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Appointment
import calendar
from .models import DoctorSchedule, DoctorDateSchedule
from ai_assistant.services import generate_health_summary
from datetime import date
from datetime import date
from .models import Patient, Appointment, Doctor, DoctorSchedule
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MedicalRecord
from .models import (
    Doctor,
    Appointment,
    MedicalRecord,
    Patient,
)
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch

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

            appointment.status = "Waiting"


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
            status__in=["Pending", "Confirmed", "Waiting"]
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

@login_required
def patient_account(request):

    patient = request.user.patient_profile


    if request.method == "POST":

        # ==========================
        # PROFILE PHOTO
        # ==========================

        if "profile_picture" in request.FILES:

            patient.profile_picture = request.FILES["profile_picture"]



        # ==========================
        # PERSONAL INFORMATION
        # ==========================

        patient.first_name = request.POST.get(
            "first_name"
        )

        patient.middle_name = request.POST.get(
            "middle_name"
        )

        patient.last_name = request.POST.get(
            "last_name"
        )

        patient.date_of_birth = request.POST.get(
            "date_of_birth"
        )

        patient.sex = request.POST.get(
            "sex"
        )

        patient.contact_number = request.POST.get(
            "contact_number"
        )

        patient.address = request.POST.get(
            "address"
        )



        # ==========================
        # HEALTH INFORMATION
        # ==========================

        patient.blood_type = request.POST.get(
            "blood_type"
        )

        patient.height = request.POST.get(
            "height"
        ) or None

        patient.weight = request.POST.get(
            "weight"
        ) or None



        patient.save()


        return redirect(
            "patient_account"
        )



    return render(
        request,
        "patients/patient_details/patient_account.html",
        {
            "patient": patient
        }
    )


@login_required
def change_password(request):

    if request.method == "POST":

        form = PasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            user = form.save()

            # Keep user logged in after password change
            update_session_auth_hash(
                request,
                user
            )

            return redirect(
                "patient_account"
            )

    else:

        form = PasswordChangeForm(
            request.user
        )


    return render(
        request,
        "patients/authentication/change_password.html",
        {
            "form": form
        }
    )


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



@login_required
def doctor_dashboard(request):

    # Get logged-in doctor's profile
    try:
        doctor = request.user.doctor_profile

    except Doctor.DoesNotExist:
        return redirect("login")


    today = date.today()


    # ==============================
    # TODAY'S APPOINTMENTS
    # ==============================

    today_appointments = Appointment.objects.filter(
        doctor=doctor,
        date=today
    ).exclude(
         status__in=["Cancelled", "Waiting"]
    )



    # ==============================
    # ALL APPOINTMENTS
    # ==============================

    appointments = Appointment.objects.filter(
        doctor=doctor
    ).order_by(
        "-date"
    )



    # ==============================
    # TOTAL PATIENTS
    # ==============================

    total_patient_count = Appointment.objects.filter(
        doctor=doctor
    ).values(
        "patient"
    ).distinct().count()



    # ==============================
    # PENDING APPOINTMENTS
    # ==============================

    pending_appointment_count = Appointment.objects.filter(
        doctor=doctor,
        status="Pending"
    ).count()



    # ==============================
    # MEDICAL RECORDS CREATED
    # ==============================

    medical_record_count = MedicalRecord.objects.filter(
        doctor=doctor
    ).count()



    # ==============================
    # UPCOMING APPOINTMENT
    # ==============================

    upcoming_appointment = Appointment.objects.filter(
        doctor=doctor,
        date__gte=today
    ).exclude(
         status__in=["Cancelled", "Waiting"]
    ).order_by(
        "date"
    ).first()



    context = {

        "doctor": doctor,

        "today_appointment_count":
            today_appointments.count(),

        "total_patient_count":
            total_patient_count,

        "pending_appointment_count":
            pending_appointment_count,

        "medical_record_count":
            medical_record_count,

        "upcoming_appointment":
            upcoming_appointment,

        "appointments":
            appointments[:5],

    }


    return render(
        request,
        "doctors/dashboard/doctor_dashboard.html",
        context
    )

@login_required
def doctor_appointments(request):

    doctor = request.user.doctor_profile


    # Only this doctor's appointments
    appointments = Appointment.objects.filter(
        doctor=doctor
    ).order_by("-date")



    # ==========================
    # SEARCH PATIENT
    # ==========================

    search = request.GET.get("search")


    if search:

        appointments = appointments.filter(
            Q(patient__first_name__icontains=search) |
            Q(patient__middle_name__icontains=search) |
            Q(patient__last_name__icontains=search) |
            Q(patient__contact_number__icontains=search)
        )



    # ==========================
    # STATUS FILTER
    # ==========================

    status = request.GET.get("status")


    if status:

        appointments = appointments.filter(
            status=status
        )



    context = {

        "appointments": appointments,

        "search": search,

        "selected_status": status,

    }


    return render(
        request,
        "doctors/appointment/doctor_appointment_list.html",
        context
    )
@login_required
def doctor_appointment_detail(request, appointment_id):

    # Get the logged-in doctor
    try:
        doctor = request.user.doctor_profile

    except Doctor.DoesNotExist:
        return redirect("login")


    # Get only this doctor's appointment
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor=doctor
    )


    # Check if a medical record already exists
    has_medical_record = MedicalRecord.objects.filter(
        appointment=appointment
    ).exists()


    context = {

        "doctor": doctor,

        "appointment": appointment,

        "has_medical_record": has_medical_record,

    }


    return render(
        request,
        "doctors/appointment/doctor_appointment_details.html",
        context
    )

@login_required
def confirm_appointment(request, appointment_id):

    doctor = request.user.doctor_profile

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor=doctor
    )

    if appointment.status != "Pending":

        messages.warning(
            request,
            "This appointment cannot be confirmed."
        )

        return redirect(
            "doctor_appointment_detail",
            appointment_id=appointment.id
        )

    appointment.status = "Confirmed"
    appointment.save()

    messages.success(
        request,
        "Appointment confirmed successfully."
    )

    return redirect(
        "doctor_appointment_detail",
        appointment_id=appointment.id
    )
@login_required
def cancel_appointment(request, appointment_id):

    doctor = request.user.doctor_profile

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor=doctor
    )

    if appointment.status == "Completed":

        messages.error(
            request,
            "Completed appointments cannot be cancelled."
        )

        return redirect(
            "doctor_appointment_detail",
            appointment_id=appointment.id
        )

    appointment.status = "Cancelled"
    appointment.save()

    messages.success(
        request,
        "Appointment cancelled successfully."
    )

    return redirect(
        "doctor_appointment_detail",
        appointment_id=appointment.id
    )
@login_required
def complete_appointment(request, appointment_id):

    doctor = request.user.doctor_profile

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor=doctor
    )

    if not MedicalRecord.objects.filter(
        appointment=appointment
    ).exists():

        messages.error(
            request,
            "You must create a medical record before completing this appointment."
        )

        return redirect(
            "doctor_appointment_detail",
            appointment_id=appointment.id
        )

    appointment.status = "Completed"
    appointment.save()

    messages.success(
        request,
        "Appointment marked as completed."
    )

    return redirect(
        "doctor_appointment_detail",
        appointment_id=appointment.id
    )   
@login_required
def reschedule_appointment(request, appointment_id):

    doctor = request.user.doctor_profile

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor=doctor
    )

    # Don't allow rescheduling completed/cancelled appointments
    if appointment.status in ["Completed", "Cancelled"]:

        messages.error(
            request,
            "This appointment can no longer be rescheduled."
        )

        return redirect(
            "doctor_appointment_detail",
            appointment_id=appointment.id
        )

    if request.method == "POST":

        new_date = request.POST.get("date")
        new_time = request.POST.get("time")

        if not new_date or not new_time:

            messages.error(
                request,
                "Please select a new date and time."
            )

            return redirect(
                "reschedule_appointment",
                appointment_id=appointment.id
            )

        # Check if the selected slot is already taken
        existing = Appointment.objects.filter(
            doctor=doctor,
            date=new_date,
            time=new_time
        ).exclude(
            id=appointment.id
        ).exclude(
            status="Cancelled"
        )

        if existing.exists():

            messages.error(
                request,
                "The selected time slot is already occupied."
            )

            return redirect(
                "reschedule_appointment",
                appointment_id=appointment.id
            )

        appointment.date = new_date
        appointment.time = new_time
        appointment.save()

        messages.success(
            request,
            "Appointment rescheduled successfully."
        )

        return redirect(
            "doctor_appointment_detail",
            appointment_id=appointment.id
        )

    context = {

        "appointment": appointment,

        "doctor": doctor,

    }

    return render(
        request,
        "doctors/appointment/doctor_reschedule_appointment.html",
        context
    )


@login_required
def doctor_schedule(request):
    doctor = request.user.doctor_profile

    # ==================================================
    # SAVE SCHEDULES
    # ==================================================

    if request.method == "POST":
        action = request.POST.get("action")

        # ==============================================
        # REGULAR WORK SCHEDULE
        # ==============================================

        if action == "regular":


            days = request.POST.getlist(
                "working_days"
            )


            morning_start = request.POST.get(
                "regular_morning_start"
            )

            morning_end = request.POST.get(
                "regular_morning_end"
            )


            afternoon_start = request.POST.get(
                "regular_afternoon_start"
            )

            afternoon_end = request.POST.get(
                "regular_afternoon_end"
            )



            # remove old regular schedule

            DoctorSchedule.objects.filter(
                doctor=doctor
            ).delete()



            for day in days:


                DoctorSchedule.objects.create(

                    doctor=doctor,

                    day_of_week=day,


                    morning_available=True
                    if morning_start and morning_end
                    else False,


                    morning_start=morning_start
                    if morning_start
                    else None,


                    morning_end=morning_end
                    if morning_end
                    else None,



                    afternoon_available=True
                    if afternoon_start and afternoon_end
                    else False,


                    afternoon_start=afternoon_start
                    if afternoon_start
                    else None,


                    afternoon_end=afternoon_end
                    if afternoon_end
                    else None,


                )



            return redirect(
                "doctor_schedule"
            )

        # ==============================================
        # DATE OVERRIDE SCHEDULE
        # ==============================================

        elif action == "date":

            selected_date = request.POST.get("selected_date")

            status = request.POST.get("status")

            reason = request.POST.get("reason", "").strip()


            # -----------------------------
            # Convert empty strings to None
            # -----------------------------

            def clean_time(value):
                if not value:
                    return None
                value = value.strip()
                return value if value else None


            morning_start = clean_time(
                request.POST.get("morning_start")
            )

            morning_end = clean_time(
                request.POST.get("morning_end")
            )

            afternoon_start = clean_time(
                request.POST.get("afternoon_start")
            )

            afternoon_end = clean_time(
                request.POST.get("afternoon_end")
            )

            # -----------------------------
            # Clear unused times
            # -----------------------------

            if status == "OFF":

                morning_start = None
                morning_end = None

                afternoon_start = None
                afternoon_end = None

            elif status == "MORNING":

                afternoon_start = None
                afternoon_end = None

            elif status == "AFTERNOON":

                morning_start = None
                morning_end = None

            # -----------------------------
            # Get existing schedule or create
            # -----------------------------

            schedule, created = DoctorDateSchedule.objects.get_or_create(

                doctor=doctor,

                date=selected_date,

                defaults={
                    "status": status
                }

            )
            # -----------------------------
            # Update fields
            # -----------------------------

            schedule.status = status

            schedule.morning_start = morning_start
            schedule.morning_end = morning_end

            schedule.afternoon_start = afternoon_start
            schedule.afternoon_end = afternoon_end

            schedule.reason = reason

            schedule.save()

            return redirect("doctor_schedule")



    weekly_schedule = DoctorSchedule.objects.filter(
        doctor=doctor
    )

    # LOAD SAVED REGULAR SCHEDULE

    working_days = list(
        weekly_schedule.values_list(
            "day_of_week",
            flat=True
        )
    )

    regular_morning_start = ""
    regular_morning_end = ""

    regular_afternoon_start = ""
    regular_afternoon_end = ""

    first_schedule = weekly_schedule.first()

    if first_schedule:

        if first_schedule.morning_start:
            regular_morning_start = first_schedule.morning_start.strftime("%H:%M")

        if first_schedule.morning_end:
            regular_morning_end = first_schedule.morning_end.strftime("%H:%M")

        if first_schedule.afternoon_start:
            regular_afternoon_start = first_schedule.afternoon_start.strftime("%H:%M")

        if first_schedule.afternoon_end:
            regular_afternoon_end = first_schedule.afternoon_end.strftime("%H:%M")

    # ==================================================
    # ADDITIONAL SCHEDULE TABLE
    # ==================================================

    extra_schedule = DoctorDateSchedule.objects.filter(
    doctor=doctor
    ).exclude(
        status="AVAILABLE"
    ).order_by("date")
    today = date.today()

    year = today.year
    month = today.month

    first_day = date(year, month, 1)

    total_days = calendar.monthrange(year, month)[1]

    calendar_days = []

    # Empty cells before first day
    for i in range(first_day.weekday() + 1):
        calendar_days.append({
            "number": "",
            "date": None,
            "status": ""
        })

    # Calendar days
    for day_number in range(1, total_days + 1):

        current_date = date(year, month, day_number)

        override = DoctorDateSchedule.objects.filter(
            doctor=doctor,
            date=current_date
        ).first()

        if override:

            status = override.status

        else:

            weekday = current_date.strftime("%A")

            regular = DoctorSchedule.objects.filter(
                doctor=doctor,
                day_of_week=weekday
            ).first()

            if regular:

                if regular.morning_available and regular.afternoon_available:
                    status = "AVAILABLE"

                elif regular.morning_available:
                    status = "MORNING"

                elif regular.afternoon_available:
                    status = "AFTERNOON"

                else:
                    status = "OFF"

            else:
                status = "OFF"

        calendar_days.append({
            "date": current_date,
            "number": day_number,
            "status": status
        })

    # Fill remaining cells
    while len(calendar_days) < 42:
        calendar_days.append({
            "number": "",
            "date": None,
            "status": ""
        })
    confirmed_appointments = Appointment.objects.filter(
    doctor=request.user.doctor_profile,
    status="Confirmed"
    ).order_by("date", "time_period")
    confirmed_dates = Appointment.objects.filter(
    doctor=request.user.doctor_profile,
    status="Confirmed"
    ).values_list("date", flat=True)
    confirmed_schedules = Appointment.objects.filter(
    doctor=request.user.doctor_profile,
    status="Confirmed"
)

    context = {
        "weekly_schedule": weekly_schedule,
        "extra_schedule": extra_schedule,
        "calendar_days": calendar_days,
        "current_month": today.strftime("%B %Y"),
        "working_days": working_days,
        "regular_morning_start": regular_morning_start,
        "regular_morning_end": regular_morning_end,
        "regular_afternoon_start": regular_afternoon_start,
        "regular_afternoon_end": regular_afternoon_end,
        "current_month": today.strftime("%B"),
        "current_year": today.year,
        "confirmed_appointments": confirmed_appointments,
        "confirmed_dates": confirmed_dates,
           "confirmed_schedules": confirmed_schedules,

    }

    return render(
        request,
        "doctors/schedule/doctor_schedule.html",
        context
    )

@login_required
def health_summary(request):

    patient = request.user.patient_profile


    appointments = patient.appointments.all().order_by("-date")


    records = patient.medical_records.all().order_by("-visit_date")


    appointment_data = ""

    for appointment in appointments[:5]:

        appointment_data += f"""
        Date: {appointment.date}
        Doctor: Dr. {appointment.doctor.last_name}
        Reason: {appointment.reason}
        Status: {appointment.status}

        """


    medical_data = ""

    for record in records[:5]:

        medical_data += f"""
        Visit Date: {record.visit_date}
        Diagnosis: {record.diagnosis}
        Prescription: {record.prescription}
        Notes: {record.notes}

        """



    patient_data = f"""

Patient Information:

Name:
{patient.first_name} {patient.last_name}

Age:
{patient.age}

Sex:
{patient.sex}

Blood Type:
{patient.blood_type}

Height:
{patient.height} cm

Weight:
{patient.weight} kg


Appointment History:

{appointment_data}


Medical Records:

{medical_data}

"""


    if not appointments.exists() and not records.exists():

        summary = "You have no records yet."

    else:

        summary = generate_health_summary(patient_data)



    return render(
        request,
        "patients/medical_records/health_summary_ai.html",
        {
            "patient": patient,
            "summary": summary,
        }
    )
@login_required
def doctor_medical_records(request):

    doctor = request.user.doctor

    records = (
        MedicalRecord.objects
        .filter(doctor=doctor)
        .select_related(
            "patient__user",
            "appointment",
            "appointment__prescription"
        )
        .order_by("-visit_date")
    )

    return render(request,
                  "doctors/medical_record/doctor_medical_record.html",
                  {"records": records})


@login_required
def doctor_medical_record(request):

    doctor = request.user.doctor_profile
    records = (
        MedicalRecord.objects
        .filter(doctor=doctor)
        .select_related(
            "patient__user"
        )
        .order_by("-visit_date")
    )

    search = request.GET.get("search")

    if search:
        records = records.filter(
            Q(patient__user__first_name__icontains=search) |
            Q(patient__user__last_name__icontains=search) |
            Q(diagnosis__icontains=search) |
            Q(prescription__icontains=search) |
            Q(notes__icontains=search)
        )

    context = {
    "records": records,
    "total_records": records.count(),
    "total_patients": records.values("patient").distinct().count(),
}

    return render(
        request,
        "doctors/medical_record/doctor_medical_record.html",
        context,
    )


@login_required
def doctor_create_medical(request, appointment_id):

    doctor = request.user.doctor_profile

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor=doctor
    )

    if hasattr(appointment, "medical_record"):

        messages.warning(
            request,
            "A medical record already exists for this appointment."
        )

        return redirect("doctor_medical_record")

    if request.method == "POST":

        diagnosis = request.POST.get("diagnosis")
        prescription = request.POST.get("prescription")
        notes = request.POST.get("notes")

        MedicalRecord.objects.create(

            appointment=appointment,

            patient=appointment.patient,

            doctor=doctor,

            diagnosis=diagnosis,

            prescription=prescription,

            notes=notes

        )

        appointment.status = "Completed"
        appointment.save()

        messages.success(
            request,
            "Medical record created successfully."
        )

        return redirect("doctor_medical_record")

    return render(
        request,
        "doctors/medical_record/doctor_create_medical.html",
        {
            "appointment": appointment,
        }
    )

@login_required
def doctor_patient_list(request):

    doctor = request.user.doctor_profile

    patients = (
        Patient.objects
        .filter(
            appointments__doctor=doctor,
            appointments__status__in=["Confirmed", "Completed"]
        )
        .distinct()
        .prefetch_related("medical_records")
        .order_by("user__last_name", "user__first_name")
    )

    search = request.GET.get("search")

    if search:
        patients = patients.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search)
        ).distinct()

    patient_data = []

    for patient in patients:

        latest_record = (
            MedicalRecord.objects
            .filter(
                patient=patient,
                doctor=doctor
            )
            .order_by("-visit_date")
            .first()
        )

        latest_appointment = (
            Appointment.objects
            .filter(
                patient=patient,
                doctor=doctor,
                status__in=["Confirmed", "Completed"]
            )
            .order_by("-date", "-time_period")
            .first()
        )

        patient_data.append({
            "patient": patient,
            "diagnosis": latest_record.diagnosis if latest_record else "-",
            "appointment_date": latest_appointment.date if latest_appointment else "-",
        })

    context = {
        "patients": patient_data,
        "total_patients": len(patient_data),
    }

    return render(
        request,
        "doctors/medical_record/doctor_patient_list.html",
        context,
    )

@login_required
def receptionist_dashboard(request):

    total_patients = Patient.objects.count()

    today_appointments = Appointment.objects.filter(
        date=date.today()
    ).count()

    pending_requests = Appointment.objects.filter(
        status="Pending"
    ).count()

    pending_doctor_approval = Appointment.objects.filter(
        status="Waiting"
    ).count()

    upcoming_appointments = Appointment.objects.filter(
        date__gte=date.today()
    ).count()

    completed_today = Appointment.objects.filter(
        date=date.today(),
        status="Completed"
    ).count()

    total_doctors = Doctor.objects.count()


    # Get all doctors with their weekly schedules
    doctor_schedules = DoctorSchedule.objects.select_related(
        "doctor",
        "doctor__user"
    ).all()

    today = date.today()

    available_doctors_today = DoctorDateSchedule.objects.exclude(
    status="OFF").filter(
    date=today).count()
    context = {

        "total_patients": total_patients,

        "today_appointments": today_appointments,

        "pending_requests": pending_requests,

        "pending_doctor_approval": pending_doctor_approval,

        "upcoming_appointments": upcoming_appointments,

        "completed_today": completed_today,

        "total_doctors": total_doctors,

        "doctor_schedules": doctor_schedules,
        "available_doctors_today": available_doctors_today,

    }


    return render(
        request,
        "receptionist/dashboard/receptionist_dashboard.html",
        context
    )

@login_required
def receptionist_appointments(request):

    today = date.today()

    today_appointments = Appointment.objects.filter(
        date=today
    ).select_related(
        "doctor__user",
        "patient__user"
    ).order_by("date", "time_period")

    upcoming_appointments = Appointment.objects.filter(
        status="Confirmed",
        date__gt=today
    ).select_related(
        "doctor__user",
        "patient__user"
    ).order_by("-date", "-time_period")

    pending_requests = Appointment.objects.filter(
        status="Waiting"
    ).select_related(
        "doctor__user",
        "patient__user"
    ).order_by("-date", "-time_period")

    pending_doctor_approval = Appointment.objects.filter(
        status="Pending"
    ).select_related(
        "doctor__user",
        "patient__user"
    ).order_by("-date", "-time_period")

    completed_appointments = Appointment.objects.filter(
        status="Completed"
    ).select_related(
        "doctor__user",
        "patient__user"
    ).order_by("-date", "-time_period")
    cancelled_appointments = Appointment.objects.filter(
    status="Cancelled"
).select_related(
    "doctor__user",
    "patient__user"
).order_by("-date", "-time_period")

    # ----------------------------------------
    # Determine if Approve button should show
    # ----------------------------------------

    for appointment in pending_requests:

        appointment.can_approve = False

        # Check date-specific schedule first
        date_schedule = DoctorDateSchedule.objects.filter(
            doctor=appointment.doctor,
            date=appointment.date
        ).first()

        if date_schedule:

            if date_schedule.status == "AVAILABLE":
                appointment.can_approve = True

            elif (
                date_schedule.status == "MORNING"
                and appointment.time_period == "AM"
            ):
                appointment.can_approve = True

            elif (
                date_schedule.status == "AFTERNOON"
                and appointment.time_period == "PM"
            ):
                appointment.can_approve = True

        else:

            weekday = appointment.date.strftime("%A")

            weekly = DoctorSchedule.objects.filter(
                doctor=appointment.doctor,
                day_of_week=weekday
            ).first()

            if weekly:

                if (
                    appointment.time_period == "AM"
                    and weekly.morning_available
                ):
                    appointment.can_approve = True

                elif (
                    appointment.time_period == "PM"
                    and weekly.afternoon_available
                ):
                    appointment.can_approve = True


    context = {

        "today_appointments": today_appointments,
        "upcoming_appointments": upcoming_appointments,
        "pending_requests": pending_requests,
        "pending_doctor_approval": pending_doctor_approval,
        "completed_appointments": completed_appointments,
         "cancelled_appointments": cancelled_appointments,
    }

    return render(
        request,
        "receptionist/appointment/receptionist_appointment.html",
        context,
    )
@login_required
def deny_appointment(request, appointment_id):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id
    )

    appointment.status = "Cancelled"
    appointment.save()

    return redirect("receptionist_appointments")
@login_required
def receptionist_patients(request):

    patients = Patient.objects.prefetch_related(
        Prefetch(
            "appointment_set",
            queryset=Appointment.objects.filter(
                status="Confirmed"
            ).order_by("-date"),
            to_attr="confirmed_appointments"
        )
    )

    for patient in patients:
        if patient.confirmed_appointments:
            patient.last_appointment = patient.confirmed_appointments[0]
        else:
            patient.last_appointment = None


    context = {
        "patients": patients
    }


    return render(
        request,
        "receptionist_patient.html",
        context
    )
@login_required
def receptionist_doctors(request):

    doctors = Doctor.objects.select_related(
        "user"
    ).all()


    context = {
        "doctors": doctors
    }


    return render(
        request,
        "receptionist/appointment/receptionist_doctor.html",
        context
    )