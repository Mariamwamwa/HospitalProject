from django.urls import path
from . import views

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
    path( "patient/appointments/appointment_booking",views.book_appointment,name="appointment_booking"),
    path( "patient/medical_records",views.patient_medical_record,name="patient_medical_record"),
    path( "patient/medical_records/details",views.patient_medical_detail,name="patient_medical_detail"),
    path( "patient/health_summary",views.patient_health_summary,name="patient_health_summary"),
    path( "patient/account_settings",views.patient_account,name="patient_account"),

]

