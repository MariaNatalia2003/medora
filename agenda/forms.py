# Códigos de formulários para cadastro de usuários

from django import forms
from django.contrib.auth.models import User
from .models import Doctor


class DoctorRegistrationForm(forms.ModelForm):
    """
    Formulário para registrar um médico com dados de usuário.
    """
    username = forms.CharField(label="Usuário", max_length=150)
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirme a senha", 
                                       widget=forms.PasswordInput)

    class Meta:
        """
        Indica o modelo ao qual os campos do formulário está vinculado
        """
        model = Doctor
        # Define os campos do modelo que devem ser incluídos no formulário
        fields = ['crm', 'specialty', 'phone_number', 'start_time', 'end_time']

    def clean(self):
        """
        Valida se as duas senhas passadas no registro de usuário são iguais.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("As senhas não conferem.")

        return cleaned_data

    def save(self, commit=True):
        """
        Salva as informações passadas no banco de dados.
        """
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )

        doctor = super().save(commit=False)
        doctor.user = user
        if commit:
            doctor.save()
        return doctor
