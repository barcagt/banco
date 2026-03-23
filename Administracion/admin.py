from django.contrib import admin
from .models import Cliente, Cuenta, Transaccion

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'dpi', 'telefono', 'fecha_registro')
    search_fields = ('nombre', 'dpi')

@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    list_display = ('numero_cuenta', 'cliente', 'tipo_cuenta', 'saldo', 'fecha_creacion')
    search_fields = ('numero_cuenta', 'cliente__nombre')

@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ('cuenta', 'tipo', 'monto', 'descripcion', 'fecha')
    search_fields = ('cuenta__numero_cuenta', 'tipo')
    list_filter = ('tipo', 'fecha')
