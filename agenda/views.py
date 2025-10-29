from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import DoctorRegistrationForm
from .models import Doctor


def doctor_register(request):
    """
    Permite que um médico se registre no sistema.
    """
    if request.method == "POST":
        form = DoctorRegistrationForm(request.POST)
        # O método 'is_valid()' chama automaticamente o método de validação
        # de senha do form de registro do médico
        if form.is_valid():
            form.save()
            messages.success(request, 
                             "Cadastro realizado com sucesso! Faça login.")
            return redirect('login')
    else:
        form = DoctorRegistrationForm()
    return render(request, "registration/register.html", {"form": form})


def doctor_login(request):
    """
    Permite que um médico faça login.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Verifica se o usuário é médico
            if hasattr(user, 'doctor'):
                login(request, user)
                return redirect('doctor_dashboard')
            else:
                messages.error(request, 
                               "Apenas médicos podem acessar este sistema.")
        else:
            messages.error(request, "Usuário ou senha incorretos.")

    return render(request, "registration/login.html")


@login_required
def doctor_dashboard(request):
    """
    Página inicial do médico logado.
    """
    doctor = request.user.doctor
    appointments = doctor.appointment_set.all().order_by('appointment_date', 'appointment_time')
    return render(request, "doctor_dashboard.html", {"doctor": doctor, "appointments": appointments})


@login_required
def doctor_logout(request):
    logout(request)
    messages.info(request, "Você saiu da conta.")
    return redirect("login")
