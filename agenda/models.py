from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta


class Specialty(models.Model):
    '''
    Modelo para representar especialidades médicas.
    '''
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Especialidade"
        verbose_name_plural = "Especialidades"
        ordering = ["name"]

    # Define uma forma legível de apresentar um objeto com texto
    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=False, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    # crm = XXXXXX-CRM/SP
    crm = models.CharField(max_length=20, unique=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    start_time = models.TimeField(
        help_text="Horário de início do expediente"
    )
    end_time = models.TimeField(help_text="Horário de término do expediente")

    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"
        ordering = ["user__first_name"]

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.specialty})"

    def create_schedule(self, duration=30):
        """
        Gera uma lista de horários fixos (grade) para agendamento com um médico
        específico, baseado no horário de expediente do médico em questão.
        :param duracao_minutos: Duração de cada consulta em minutos.

        :return: Lista de horários da grade horária do médico.
        """
        schedule = []
        # Necessário criar datas fictícias para manipular horários
        current_dt = datetime.combine(datetime.today(), self.start_time)
        end_dt = datetime.combine(datetime.today(), self.end_time)
        appointment_duration = timedelta(minutes=duration)

        # Gera a lista com a grade horária do médico
        while current_dt < end_dt:
            # Adiciona apenas o horário (time) à lista
            schedule.append(current_dt.time())
            current_dt += appointment_duration

        return schedule


class Patient(models.Model):
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    # cfp = XXX.XXX.XXX-XX
    cpf = models.CharField(max_length=14, unique=True)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    history = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("AGENDADA", "Agendada"),
        ("CONFIRMADA", "Confirmada"),
        ("CANCELADA", "Cancelada"),
        ("REALIZADA", "Realizada"),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    appointment_duration = models.PositiveIntegerField(
        default=30, 
        help_text="Duração em minutos"
    )
    status = models.CharField(max_length=20, 
        choices=STATUS_CHOICES, 
        default="AGENDADA"
    )
    details = models.TextField(blank=True)

    class Meta:
        unique_together = ("doctor", "appointment_date", "appointment_time")
        ordering = ["appointment_date", "appointment_time"]
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"

    def __str__(self):
        appointment_start = datetime.combine(
            self.appointment_date, self.appointment_time
        )

        appointment_end = (
            appointment_start + timedelta(minutes=self.appointment_duration)
        ).time()

        return (
            f"{self.appointment_date} "
            f"{self.appointment_time.strftime('%H:%M')}–"
            f"{appointment_end.strftime('%H:%M')} | "
            f"{self.doctor} / {self.patient}"
        )

    def check_conflicts(self):
        """
        Valida:
        - Se o horário está dentro do expediente do médico
        - Se há conflito com outra consulta (considerando a duração)
        """
        new_start_time = datetime.combine(self.appointment_date, self.appointment_time)
        new_end_time = new_start_time + timedelta(minutes=self.appointment_duration)

        # Verifica conflito de horário considerando duração
        existing_appointments = Appointment.objects.filter(
            doctor=self.doctor,
            appointment_date=self.appointment_date
        ).exclude(pk=self.pk)

        for a in existing_appointments:
            a_starting = datetime.combine(self.appointment_date, a.appointment_time)
            a_ending = a_starting + timedelta(minutes=a.appointment_duration)
            if new_start_time < a_ending and new_end_time > a_starting:
                raise ValidationError(
                    "Este horário conflita com outra consulta do mesmo médico."
                )

        # Verifica se está dentro do expediente
        if not (self.doctor.start_time <= self.appointment_time < self.doctor.end_time):
            raise ValidationError("Horário fora do expediente do médico.")
