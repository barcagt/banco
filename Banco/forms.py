from django import forms
from Administracion.models import Cliente, Cuenta, Transaccion


class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ['nombre', 'dpi', 'telefono']


class CuentaForm(forms.ModelForm):

    class Meta:
        model = Cuenta
        fields = ['cliente', 'numero_cuenta', 'tipo_cuenta', 'saldo']


class TransaccionForm(forms.ModelForm):

    class Meta:
        model = Transaccion
        fields = ['cuenta', 'tipo', 'monto', 'descripcion']