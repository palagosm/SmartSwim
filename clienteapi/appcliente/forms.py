# clienteapi/appcliente/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=False, help_text='Opcional', widget=forms.TextInput(attrs={'class': 'form-control'}), label='Primer Apellido')
    last_name = forms.CharField(max_length=30, required=False, help_text='Opcional', widget=forms.TextInput(attrs={'class': 'form-control'}), label='Segundo Apellido')
    fecha_nacimiento = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), label='Fecha de Nacimiento')
    telefono_contacto = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Teléfono de Contacto')
    nombre_cliente = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Nombre')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'fecha_nacimiento', 'telefono_contacto', 'nombre_cliente')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden. Inténtalo de nuevo.")


# forms.py
from django import forms

class UserUpdateForm(forms.Form):
    nombre_cliente = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Nombre')
    first_name = forms.CharField(max_length=30, required=False, help_text='Opcional', widget=forms.TextInput(attrs={'class': 'form-control'}), label='Primer Apellido')
    last_name = forms.CharField(max_length=30, required=False, help_text='Opcional', widget=forms.TextInput(attrs={'class': 'form-control'}), label='Segundo Apellido')
    fecha_nacimiento = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), label='Fecha de Nacimiento')
    telefono_contacto = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Teléfono de Contacto')
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))


