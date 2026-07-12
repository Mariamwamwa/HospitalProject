from datetime import date
from django.db import models
from django.contrib.auth.models import User

# Helper for the upload path
def user_directory_path(instance, filename):
    return f'profile_pics/{instance.user.id}/{filename}'


# ==========================================
# 1. USER PROFILES (Roles)
# ==========================================
class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        ('Cardiology', 'Cardiology'),
        ('Dermatology', 'Dermatology'),
        ('Neurology', 'Neurology'),
        ('Pediatrics', 'Pediatrics'),
        ('Orthopedics', 'Orthopedics'),
        ('General Practice', 'General Practice'),
    ]

    SEX_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')

    first_name = models.CharField(max_length=50, default="Unknown")
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, default="Unknown")

    date_of_birth = models.DateField(blank=True, null=True)

    sex = models.CharField(
        max_length=10,
        choices=SEX_CHOICES,
        default='Male'
    )

    address = models.TextField(blank=True)

    specialization = models.CharField(
        max_length=50,
        choices=SPECIALIZATION_CHOICES,
        default='General Practice'
    )

    license_number = models.CharField(max_length=50, unique=True)
    contact_number = models.CharField(max_length=15)

    profile_picture = models.ImageField(
        upload_to=user_directory_path,
        default='default.jpg',
        blank=True,
        null=True
    )

    @property
    def user_id(self):
        return self.user.id

    @property
    def user_type(self):
        return "Doctor"

    @property
    def email(self):
        return self.user.email

    @property
    def age(self):
        if not self.date_of_birth:
            return "N/A"
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) <
            (self.date_of_birth.month, self.date_of_birth.day)
        )
    

class Patient(models.Model):

    SEX_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('Unknown', 'Unknown'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='patient_profile'
    )

    first_name = models.CharField(max_length=50, default="Unknown")
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, default="Unknown")

    date_of_birth = models.DateField()

    sex = models.CharField(
        max_length=10,
        choices=SEX_CHOICES,
        default='Male'
    )

    blood_type = models.CharField(
        max_length=10,
        choices=BLOOD_TYPE_CHOICES,
        default='Unknown'
    )

    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Height in centimeters"
    )

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Weight in kilograms"
    )

    address = models.TextField()

    contact_number = models.CharField(max_length=15)

    profile_picture = models.ImageField(
        upload_to=user_directory_path,
        default='default.jpg',
        blank=True,
        null=True
    )

    @property
    def age(self):
        if not self.date_of_birth:
            return "N/A"

        today = date.today()

        return today.year - self.date_of_birth.year - (
            (today.month, today.day) <
            (self.date_of_birth.month, self.date_of_birth.day)
        )

    def __str__(self):
        mid = f" {self.middle_name}" if self.middle_name else ""
        return f"{self.first_name}{mid} {self.last_name}"

    @property
    def user_id(self):
        return self.user.id

    @property
    def user_type(self):
        return "Patient"

    @property
    def email(self):
        return self.user.email


class Receptionist(models.Model):

    SEX_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='receptionist_profile')
    first_name = models.CharField(max_length=50, default="Unknown")
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, default="Unknown")
    date_of_birth = models.DateField(blank=True, null=True)
    sex = models.CharField(
        max_length=10,
        choices=SEX_CHOICES,
        default='Male'
    )

    address = models.TextField(blank=True)
    employee_id = models.CharField(max_length=20, unique=True)
    contact_number = models.CharField(max_length=15)

    profile_picture = models.ImageField(
        upload_to=user_directory_path,
        default='default.jpg',
        blank=True,
        null=True
    )

    @property
    def user_id(self):
        return self.user.id

    @property
    def user_type(self):
        return "Receptionist"

    @property
    def email(self):
        return self.user.email

    @property
    def age(self):
        if not self.date_of_birth:
            return "N/A"
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) <
            (self.date_of_birth.month, self.date_of_birth.day)
        )


# ==========================================
# 2. CORE HOSPITAL FEATURES (Unchanged)
# ==========================================
class DoctorSchedule(models.Model):

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE
    )

    day_of_week = models.CharField(max_length=10)

    start_time = models.TimeField()

    end_time = models.TimeField()

    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.doctor} - {self.day_of_week}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name='created_records')
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    visit_date = models.DateField(auto_now_add=True)

class Prescription(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='prescription')
    medication_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    instructions = models.TextField(blank=True, null=True)
    issued_date = models.DateField(auto_now_add=True)