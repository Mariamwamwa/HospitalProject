from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django import forms
from django.urls import path
from django.utils.html import format_html
from .models import Patient
from .models import (
    Doctor,
    Patient,
    Receptionist,
)

admin.site.site_header = "CareNest Administration"
admin.site.site_title = "CareNest Admin"
admin.site.index_title = "Welcome to CareNest"

# ==========================================
# DOCTOR FORM
# ==========================================
class DoctorCreationForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(
            attrs={
                "type": "date"
            }
        )
    )

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

    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password",
        required=True
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


    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")


        if password != confirm_password:

            raise forms.ValidationError(
                "Passwords do not match."
            )


        return cleaned_data



    def save(self, commit=True):

        doctor = super().save(commit=False)


        user = User.objects.create_user(

            username=self.cleaned_data["username"],

            email=self.cleaned_data["email"],

            password=self.cleaned_data["password"],

            first_name=self.cleaned_data["first_name"],

            last_name=self.cleaned_data["last_name"],

        )


        doctor.user = user


        if commit:
            doctor.save()


        return doctor
    
class DoctorChangeForm(forms.ModelForm):

    username = forms.CharField(
        max_length=150,
        label="Username"
    )

    email = forms.EmailField(
        label="Email"
    )

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput,
        label="New Password"
    )

    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput,
        label="Confirm Password"
    )


    class Meta:

        model = Doctor

        fields = [
            "username",
            "email",
            "password",
            "confirm_password",

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



    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


        # Retrieve data from auth_user
        if self.instance and self.instance.user:

            self.fields["username"].initial = (
                self.instance.user.username
            )

            self.fields["email"].initial = (
                self.instance.user.email
            )



    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")


        if password or confirm_password:

            if password != confirm_password:

                raise forms.ValidationError(
                    "Passwords do not match."
                )


        return cleaned_data



    def save(self, commit=True):

        doctor = super().save(commit=False)


        # Update auth_user
        user = doctor.user

        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]


        # Update password only if entered
        password = self.cleaned_data.get("password")

        if password:

            user.set_password(password)


        user.save()



        if commit:

            doctor.save()


        return doctor

class PatientCreationForm(forms.ModelForm):


    date_of_birth = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(
            attrs={
                "type":"date"
            }
        )
    )


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


    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password"
    )



    class Meta:

        model = Patient

        fields = [

            "username",
            "email",
            "password",

            "first_name",
            "middle_name",
            "last_name",

            "date_of_birth",
            "sex",
            "blood_type",

            "height",
            "weight",

            "address",
            "contact_number",

            "profile_picture",

        ]



    def clean(self):

        cleaned_data = super().clean()


        password = cleaned_data.get("password")

        confirm_password = cleaned_data.get(
            "confirm_password"
        )


        if password != confirm_password:

            raise forms.ValidationError(
                "Passwords do not match."
            )


        return cleaned_data



    def save(self, commit=True):

        patient = super().save(commit=False)



        user = User.objects.create_user(

            username=self.cleaned_data["username"],

            email=self.cleaned_data["email"],

            password=self.cleaned_data["password"],

            first_name=self.cleaned_data["first_name"],

            last_name=self.cleaned_data["last_name"],

        )



        patient.user = user



        if commit:

            patient.save()



        return patient

class PatientChangeForm(forms.ModelForm):


    username = forms.CharField(
        max_length=150,
        label="Username"
    )


    email = forms.EmailField(
        label="Email"
    )


    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput,
        label="New Password"
    )


    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput,
        label="Confirm Password"
    )



    date_of_birth = forms.DateField(

        label="Date of Birth",

        widget=forms.DateInput(

            attrs={
                "type":"date"
            }

        )

    )



    class Meta:


        model = Patient


        fields = [

            "username",
            "email",
            "password",
            "confirm_password",


            "first_name",
            "middle_name",
            "last_name",


            "date_of_birth",

            "sex",

            "blood_type",


            "height",
            "weight",


            "address",

            "contact_number",


            "profile_picture",

        ]




    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)



        if self.instance and self.instance.user:


            self.fields["username"].initial = (

                self.instance.user.username

            )


            self.fields["email"].initial = (

                self.instance.user.email

            )





    def clean(self):

        cleaned_data = super().clean()


        password = cleaned_data.get("password")

        confirm_password = cleaned_data.get(
            "confirm_password"
        )


        if password or confirm_password:


            if password != confirm_password:

                raise forms.ValidationError(
                    "Passwords do not match."
                )


        return cleaned_data





    def save(self, commit=True):


        patient = super().save(commit=False)



        user = patient.user



        user.username = self.cleaned_data["username"]

        user.email = self.cleaned_data["email"]

        user.first_name = self.cleaned_data["first_name"]

        user.last_name = self.cleaned_data["last_name"]




        password = self.cleaned_data.get(
            "password"
        )


        if password:

            user.set_password(password)



        user.save()



        if commit:

            patient.save()



        return patient

# ==========================================
# RECEPTIONIST FORM
# ==========================================

class ReceptionistCreationForm(forms.ModelForm):


    date_of_birth = forms.DateField(

        required=False,

        label="Date of Birth",

        widget=forms.DateInput(

            attrs={
                "type": "date"
            }

        )

    )



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



    confirm_password = forms.CharField(

        widget=forms.PasswordInput,

        label="Confirm Password"

    )





    class Meta:


        model = Receptionist


        fields = [


            "username",

            "email",

            "password",



            "first_name",

            "middle_name",

            "last_name",



            "date_of_birth",

            "sex",



            "employee_id",



            "address",



            "contact_number",



            "profile_picture",


        ]







    def clean(self):


        cleaned_data = super().clean()



        password = cleaned_data.get(
            "password"
        )


        confirm_password = cleaned_data.get(
            "confirm_password"
        )



        if password != confirm_password:


            raise forms.ValidationError(

                "Passwords do not match."

            )



        return cleaned_data







    def save(self, commit=True):


        receptionist = super().save(
            commit=False
        )




        user = User.objects.create_user(


            username=self.cleaned_data["username"],


            email=self.cleaned_data["email"],


            password=self.cleaned_data["password"],


            first_name=self.cleaned_data["first_name"],


            last_name=self.cleaned_data["last_name"],


        )




        receptionist.user = user





        if commit:


            receptionist.save()





        return receptionist
class ReceptionistChangeForm(forms.ModelForm):


    username = forms.CharField(
        max_length=150,
        label="Username"
    )


    email = forms.EmailField(
        label="Email"
    )


    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput,
        label="New Password"
    )


    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput,
        label="Confirm Password"
    )



    date_of_birth = forms.DateField(

        required=False,

        label="Date of Birth",

        widget=forms.DateInput(

            attrs={
                "type":"date"
            }

        )

    )



    class Meta:


        model = Receptionist


        fields = [

            "username",

            "email",

            "password",

            "confirm_password",


            "first_name",

            "middle_name",

            "last_name",


            "date_of_birth",


            "sex",


            "employee_id",


            "address",


            "contact_number",


            "profile_picture",

        ]






    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)



        if self.instance and self.instance.user:


            self.fields["username"].initial = (

                self.instance.user.username

            )


            self.fields["email"].initial = (

                self.instance.user.email

            )







    def clean(self):

        cleaned_data = super().clean()



        password = cleaned_data.get(
            "password"
        )


        confirm_password = cleaned_data.get(
            "confirm_password"
        )



        if password or confirm_password:


            if password != confirm_password:


                raise forms.ValidationError(

                    "Passwords do not match."

                )



        return cleaned_data






    def save(self, commit=True):


        receptionist = super().save(
            commit=False
        )



        user = receptionist.user



        user.username = self.cleaned_data["username"]


        user.email = self.cleaned_data["email"]


        user.first_name = self.cleaned_data["first_name"]


        user.last_name = self.cleaned_data["last_name"]





        password = self.cleaned_data.get(
            "password"
        )



        if password:


            user.set_password(password)





        user.save()





        if commit:


            receptionist.save()





        return receptionist
# ==========================================
# ADMIN REGISTRATION
# ==========================================


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):

    add_form = DoctorCreationForm
    form = DoctorChangeForm


    list_display = (
        "doctor_name",
        "specialization",
        "license_number",
        "buttons",
    )


    actions = None



    def get_fieldsets(self, request, obj=None):

        if obj is None:

            return (

                (
                    "Account Information",
                    {
                        "fields": (
                            "username",
                            "email",
                            "password",
                            "confirm_password",
                        )
                    }
                ),


                (
                    "Doctor Information",
                    {
                        "fields": (
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
                        )
                    }
                ),

            )


        return (

            (
                "Account Information",
                {
                    "fields": (
                        "username",
                        "email",
                          "password",
                            "confirm_password",
                    )
                }
            ),


            (
                "Doctor Information",
                {
                    "fields": (
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
                    )
                }
            ),

        )



    def get_form(self, request, obj=None, **kwargs):

        if obj is None:
            return self.add_form

        return self.form



    def doctor_name(self, obj):

        return f"Dr. {obj.user.first_name} {obj.user.last_name}"

    doctor_name.short_description = "Doctor Name"
   

    def buttons(self, obj):

        return "Edit | Delete"

    buttons.short_description = "Actions"
    
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):


    add_form = PatientCreationForm

    form = PatientChangeForm



    list_display = (

        "user",

        "first_name",

        "last_name",

        "profile_picture",

        "sex",

        "buttons",

    )



    actions = None





    def get_fieldsets(self, request, obj=None):


        return (


            (

                "Account Information",

                {

                    "fields": (

                        "username",

                        "email",

                        "password",

                        "confirm_password",

                    )

                }

            ),




            (

                "Patient Information",

                {

                    "fields": (

                        "first_name",

                        "middle_name",

                        "last_name",

                        "date_of_birth",

                        "sex",

                        "blood_type",

                        "height",

                        "weight",

                        "address",

                        "contact_number",

                        "profile_picture",

                    )

                }

            ),


        )







    def get_form(self, request, obj=None, **kwargs):


        if obj is None:

            return self.add_form


        return self.form






    def buttons(self, obj):

        return "Edit | Delete"


    buttons.short_description = "Actions"

@admin.register(Receptionist)
class ReceptionistAdmin(admin.ModelAdmin):


    add_form = ReceptionistCreationForm

    form = ReceptionistChangeForm




    list_display = (

        "user",

        "first_name",

        "last_name",

        "profile_picture",

        "employee_id",

        "sex",

        "buttons",

    )



    actions = None





    def get_fieldsets(self, request, obj=None):


        return (


            (

                "Account Information",

                {

                    "fields": (

                        "username",

                        "email",

                        "password",

                        "confirm_password",

                    )

                }

            ),





            (

                "Receptionist Information",

                {

                    "fields": (

                        "first_name",

                        "middle_name",

                        "last_name",

                        "date_of_birth",

                        "sex",

                        "employee_id",

                        "address",

                        "contact_number",

                        "profile_picture",

                    )

                }

            ),


        )








    def get_form(self, request, obj=None, **kwargs):


        if obj is None:

            return self.add_form


        return self.form







    def buttons(self, obj):

        return "Edit | Delete"


    buttons.short_description = "Actions"