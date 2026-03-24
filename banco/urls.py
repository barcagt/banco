"""
URL configuration for Banco project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', consultas, name='index'),
    path('consultas/', consultas, name='consultas'),
    path('registrar_clientes/', registrar_cliente, name='registrar_clientes'),
    path('registro_cuentas/', registrar_cuenta, name='registrar_cuentas'),
    path('registrar_transaccion/', registrar_transaccion, name='registrar_transaccion'),
    path('cuentas/<str:dpi>/', cuentas_cliente, name='cuentas_cliente'),
    path('transacciones/<str:numero_cuenta>/', transacciones_cuenta, name='transacciones_cuenta'),
    path('transferencia/', transferencia, name='transferencia'),
]
