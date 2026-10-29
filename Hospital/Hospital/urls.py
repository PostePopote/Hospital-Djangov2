from django.urls import path, include
from app_hospital import views

urlpatterns = [
    path('', views.home, name='home'),
    path('saludo/', views.saludo, name='saludo'),
    path('pacientes/', views.pacientes, name='pacientes'),
    path('medicos/', views.medicos, name='medicos'),
    path('tratamientos/', views.tratamientos, name='tratamientos'),
    path('pacientes/agregar/', views.agregar_paciente, name='agregar_paciente'),
    path('medicos/agregar/', views.agregar_medico, name='agregar_medico'),
    path('tratamientos/agregar/', views.agregar_tratamiento, name='agregar_tratamiento'),
    path('pacientes/editar/<int:id_paciente>/', views.editar_paciente, name='editar_paciente'),
    path('medicos/editar/<int:id_medico>/', views.editar_medico, name='editar_medico'),
    path('tratamientos/editar/<int:id_tratamiento>/', views.editar_tratamiento, name='editar_tratamiento'),
    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout, name='logout'),
]
