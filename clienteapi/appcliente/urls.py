# clienteapi/appcliente/urls.py
from django.urls import path
from .views import cerrar_sesion, actualizar_usuario_view, eliminar_usuario_view, competencias_view, entrenamientos_view, contacto_view
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home_view, name='home'),
    path('competencias/', competencias_view, name='competencias'),
    path('entrenamientos/', entrenamientos_view, name='entrenamientos'),
    path('contacto/', contacto_view, name='contacto'),
    path('actualizar_usuario/<int:usuario_id>/', actualizar_usuario_view, name='actualizar_usuario'),
    path('eliminar_usuario/<int:usuario_id>/', eliminar_usuario_view, name='eliminar-usuario'),  # Correcto
    path('logout/', cerrar_sesion, name='logout'),
]