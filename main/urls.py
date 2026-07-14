from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ==========================================
    # HOME
    # ==========================================
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path("login/", views.login_view, name="login"),
    path("patient_register/", views.patient_register, name="register_patient"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    path("patient/dashboard/", views.patient_dashboard, name="patient_dashboard"),
         
    # path("doctor/dashboard/", views.doctor_dashboard, name="doctor_dashboard",
    # path("receptionist/dashboard/", views.receptionist_dashboard, name="receptionist_dashboard",
     path("patient/appointment_list/", views.patient_appointment_list, name="patient_appointment_list"),
    path( "patient/appointment/appointment_booking",views.book_appointment,name="appointment_booking"),
    path( "patient/medical_records",views.patient_medical_record,name="patient_medical_record"),
    path( "patient/health_summary",views.patient_health_summary,name="patient_health_summary"),
    path( "patient/account_settings",views.patient_account,name="patient_account"),
    path( "patient/doctors",views.doctor_list,name="doctor_list"),
    path(  'appointment/<int:id>/', views.appointment_detail, name='appointment_detail'),
    path("AI Summary/", views.health_summary, name="health_summary"),
    path("change-password/",views.change_password,name="change_password"),
    path("doctors/dashboard/", views.doctor_dashboard, name="doctor_dashboard"),
    path("doctor/appointments/", views.doctor_appointments, name="doctor_appointments"),
    path("doctor/appointments/<int:appointment_id>/",views.doctor_appointment_detail, name="doctor_appointment_detail",),
    path("doctor/appointments/<int:appointment_id>/confirm/", views.confirm_appointment, name="confirm_appointment",),
    path("doctor/appointments/<int:appointment_id>/cancel/",views.cancel_appointment,name="cancel_appointment",),
    path("doctor/appointments/<int:appointment_id>/complete/",views.complete_appointment,name="complete_appointment",),
    path("doctor/appointments/<int:appointment_id>/reschedule/",views.reschedule_appointment,name="reschedule_appointment",),
    path( "doctor/schedule/",views.doctor_schedule,name="doctor_schedule" ),
    path( "doctor/medical-record/",views.doctor_medical_record,name="doctor_medical_record"),
    path( "doctor/create-medical/<int:appointment_id>/",views.doctor_create_medical,name="doctor_create_medical",),
    path("doctor/patients/",views.doctor_patient_list,name="doctor_patient_list"),
    path("receptionist/dashboard/",views.receptionist_dashboard,name="receptionist_dashboard"),
path(
    "receptionist/appointments/",
    views.receptionist_appointments,
    name="receptionist_appointments",
),path(
    "appointments/<int:appointment_id>/deny/",
    views.deny_appointment,
    name="deny_appointment",
),path(
    "receptionist/patients/",
    views.receptionist_patients,
    name="receptionist_patients"
),
path(
    "receptionist/doctors/",
    views.receptionist_doctors,
    name="receptionist_doctors"
),
path(
    "patient/appointment/<int:appointment_id>/cancel/",
    views.cancel_appointment,
    name="cancel_appointment",
),
path(
    "health-summary/",
    views.health_summary,
    name="health_summary"
),
path(
    "account/edit/",
    views.patient_account_edit,
    name="patient_account_edit"
),
path(
    "receptionist/appointments/approve/<int:id>/",
    views.approve_appointment,
    name="approve_appointment"
),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )