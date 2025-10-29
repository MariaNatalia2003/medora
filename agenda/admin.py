from django.contrib import admin
from .models import Doctor, Patient, Appointment, Specialty

# Registra os modelos para aparecerem no Django Admin

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'created_at', 
                    'crm', 
                    'specialty', 
                    'phone_number',
                    'start_time', 
                    'end_time']

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name',
                    'created_at',
                    'birth_date', 
                    'cpf', 
                    'email',
                    'phone_number']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['doctor', 
                    'patient', 
                    'appointment_date', 
                    'appointment_time',
                    'appointment_duration', 
                    'status',
                    'details']

@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ['name']
