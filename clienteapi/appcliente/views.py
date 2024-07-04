from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm, UserUpdateForm

import requests

API_BASE_URL = "https://drapi-uqqx.onrender.com/api"

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        api_url = f"{API_BASE_URL}/authenticate/"
        user_details_url = f"{API_BASE_URL}/usuario/{username}/"

        response = requests.post(api_url, json={'username': username, 'password': password})

        if response.status_code == 200:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                user_details_response = requests.get(user_details_url)
                if user_details_response.status_code == 200:
                    user_data = user_details_response.json()
                    request.session['user_id'] = user_data.get('id')
                    request.session['first_name'] = user_data.get('first_name')
                    request.session['last_name'] = user_data.get('last_name')
                    request.session['nombre_cliente'] = user_data.get('nombre_cliente')
                    request.session['email'] = user_data.get('email')
                    request.session['fecha_nacimiento'] = user_data.get('fecha_nacimiento')
                    request.session['telefono_contacto'] = user_data.get('telefono_contacto')
                    return redirect('home')
            else:
                user_data = response.json()
                user = User.objects.create_user(username=username, password=password)
                user.first_name = user_data.get('first_name', '')
                user.last_name = user_data.get('last_name', '')
                user.email = user_data.get('email', '')
                user.save()

                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    user_details_response = requests.get(user_details_url)
                    if user_details_response.status_code == 200:
                        user_data = user_details_response.json()
                        request.session['user_id'] = user_data.get('id')
                        request.session['first_name'] = user_data.get('first_name')
                        request.session['last_name'] = user_data.get('last_name')
                        request.session['nombre_cliente'] = user_data.get('nombre_cliente')
                        request.session['email'] = user_data.get('email')
                        request.session['fecha_nacimiento'] = user_data.get('fecha_nacimiento')
                        request.session['telefono_contacto'] = user_data.get('telefono_contacto')
                        return redirect('home')
        else:
            messages.error(request, "Credenciales inválidas. Inténtalo de nuevo.")
    
    return render(request, 'appcliente/login.html')

@login_required
def home_view(request):
    return render(request, 'appcliente/home.html')

@login_required
def actualizar_usuario_view(request, usuario_id):
    # Verifica que el usuario autenticado es el mismo que el que se está actualizando
    if usuario_id != request.session.get('user_id'):
        messages.error(request, 'No tienes permiso para actualizar este usuario.')
        return redirect('home')
    
    api_url = f"{API_BASE_URL}/actualizar-usuario/{usuario_id}/"
    headers = {'X-CSRFToken': request.COOKIES.get('csrftoken')}

    if request.method == 'POST':
        form = UserUpdateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['fecha_nacimiento'] = data['fecha_nacimiento'].isoformat() if data['fecha_nacimiento'] else ''
            response = requests.put(api_url, headers=headers, json=data)
            if response.status_code == 200:
                messages.success(request, 'Datos actualizados correctamente')
                return redirect('actualizar_usuario', usuario_id=usuario_id)
            else:
                messages.error(request, 'Error al actualizar los datos')
    else:
        initial_data = {
            'first_name': request.session.get('first_name', ''),
            'last_name': request.session.get('last_name', ''),
            'email': request.session.get('email', ''),
            'fecha_nacimiento': request.session.get('fecha_nacimiento', ''),
            'telefono_contacto': request.session.get('telefono_contacto', ''),
            'nombre_cliente': request.session.get('nombre_cliente', '')
        }
        form = UserUpdateForm(initial=initial_data)

    return render(request, 'appcliente/actualizar_usuario.html', {'form': form, 'usuario_id': usuario_id})

def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            fecha_nacimiento = form.cleaned_data.get('fecha_nacimiento')
            telefono_contacto = form.cleaned_data.get('telefono_contacto')
            nombre_cliente = form.cleaned_data.get('nombre_cliente')

            # Hacer la solicitud POST a la API
            api_url = f"{API_BASE_URL}/crear-usuario/"
            user_data = {
                "username": username,
                "password": password,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "fecha_nacimiento": str(fecha_nacimiento),
                "telefono_contacto": telefono_contacto,
                "nombre_cliente": nombre_cliente
            }
            response = requests.post(api_url, json=user_data)

            if response.status_code == 201:
                # Usuario creado exitosamente
                messages.success(request, "Usuario registrado de forma correcta")
                return render(request, 'appcliente/register.html', {'form': form, 'registered': True})
            else:
                # Mostrar errores específicos devueltos por la API
                errors = response.json()
                for field, error_list in errors.items():
                    for error in error_list:
                        messages.error(request, f"{field}: {error}")
        else:
            # Si el formulario no es válido, mostrar errores del formulario
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f"{field}: {error}")
    else:
        form = SignUpForm()
    return render(request, 'appcliente/register.html', {'form': form})

@login_required
def eliminar_usuario_view(request, usuario_id):
    if usuario_id != request.session.get('user_id'):
        messages.error(request, 'No tienes permiso para eliminar este usuario.')
        return redirect('home')

    api_url = f"{API_BASE_URL}/eliminar-usuario/{usuario_id}/"
    headers = {
        'X-CSRFToken': request.COOKIES.get('csrftoken'),
        'Content-Type': 'application/json'
    }

    if request.method == 'POST' and request.POST.get('_method') == 'DELETE':
        response = requests.delete(api_url, headers=headers)
        if response.status_code == 204:
            #messages.success(request, 'Usuario eliminado correctamente.')
            logout(request)
            return render(request, 'appcliente/actualizar_usuario.html', {'success': True, 'usuario_id': usuario_id})
        else:
            messages.error(request, 'Error al eliminar el usuario.')
            return redirect('actualizar_usuario', usuario_id=usuario_id)

    return render(request, 'appcliente/actualizar_usuario.html', {'usuario_id': usuario_id})


def cerrar_sesion(request):
    logout(request)
    return redirect('login')

@login_required
def competencias_view(request):
    return render(request, 'appcliente/competencias.html')

@login_required
def contacto_view(request):
    return render(request, 'appcliente/contacto.html')

@login_required
def entrenamientos_view(request):
    return render(request, 'appcliente/entrenamientos.html')


