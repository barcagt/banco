from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from decimal import Decimal
from .forms import ClienteForm, CuentaForm, TransaccionForm
from Administracion.models import Cliente, Cuenta, Transaccion


@login_required(login_url='login')
def inicio(request):
    """Página de inicio"""
    return render(request, 'inicio.html')


@login_required(login_url='login')
def registrar_cliente(request):

    form = ClienteForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('registrar_clientes')

    return render(request, 'registro_clientes.html', {'form': form})


@login_required(login_url='login')
def registrar_cuenta(request):

    form = CuentaForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('registrar_cuentas')

    return render(request, 'registro_cuentas.html', {'form': form})


@login_required(login_url='login')
def registrar_transaccion(request):

    form = TransaccionForm(request.POST or None)

    if form.is_valid():
        transaccion = form.save(commit=False)
        cuenta = transaccion.cuenta

        # Validar que haya saldo suficiente en caso de retiro
        if transaccion.tipo == 'retiro' and cuenta.saldo < transaccion.monto:
            messages.error(request, f'Fondos insuficientes. Saldo disponible: {cuenta.saldo}')
            return redirect('registrar_transaccion')

        # Ajustar saldo de la cuenta y guardar la transacción
        with transaction.atomic():
            if transaccion.tipo == 'deposito':
                cuenta.saldo += transaccion.monto
            else:
                cuenta.saldo -= transaccion.monto
            cuenta.save()
            transaccion.save()

        messages.success(request, 'Transacción registrada correctamente.')
        return redirect('registrar_transaccion')

    return render(request, 'registro_transaccion.html', {'form': form})


@login_required(login_url='login')
def consultas(request):
    """Vista principal de consultas"""
    clientes = Cliente.objects.all()
    return render(request, 'consultas.html', {'clientes': clientes})


@login_required(login_url='login')
def cuentas_cliente(request, dpi):
    """Ver cuentas de un cliente específico"""
    cliente = get_object_or_404(Cliente, dpi=dpi)
    cuentas = Cuenta.objects.filter(cliente=cliente)
    return render(request, 'cuentas_cliente.html', {
        'cliente': cliente,
        'cuentas': cuentas
    })


@login_required(login_url='login')
def transacciones_cuenta(request, numero_cuenta):
    """Ver transacciones de una cuenta con filtro por fecha"""
    cuenta = get_object_or_404(Cuenta, numero_cuenta=numero_cuenta)
    transacciones = Transaccion.objects.filter(cuenta=cuenta).order_by('-fecha')
    
    # Filtro por fecha
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    
    if fecha_inicio:
        transacciones = transacciones.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        transacciones = transacciones.filter(fecha__lte=fecha_fin)
    
    return render(request, 'transacciones_cuenta.html', {
        'cuenta': cuenta,
        'transacciones': transacciones,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin
    })


@login_required(login_url='login')
def transferencia(request):
    """Realizar transferencia entre cuentas"""
    if request.method == 'POST':
        cuenta_origen = request.POST.get('cuenta_origen')
        cuenta_destino = request.POST.get('cuenta_destino')
        monto = Decimal(request.POST.get('monto'))
        descripcion = request.POST.get('descripcion', 'Transferencia')
        
        try:
            origen = Cuenta.objects.get(numero_cuenta=cuenta_origen)
            destino = Cuenta.objects.get(numero_cuenta=cuenta_destino)
            
            # Verificar saldo suficiente
            if origen.saldo < monto:
                messages.error(request, f'Fondos insuficientes. Saldo disponible: {origen.saldo}')
                return redirect('transferencia')
            
            # Realizar transacción atómica
            with transaction.atomic():
                # Retiro de cuenta origen
                origen.saldo -= monto
                origen.save()
                Transaccion.objects.create(
                    cuenta=origen,
                    tipo='retiro',
                    monto=monto,
                    descripcion=f'Transferencia a {destino.numero_cuenta}: {descripcion}'
                )
                
                # Depósito a cuenta destino
                destino.saldo += monto
                destino.save()
                Transaccion.objects.create(
                    cuenta=destino,
                    tipo='deposito',
                    monto=monto,
                    descripcion=f'Transferencia desde {origen.numero_cuenta}: {descripcion}'
                )
            
            messages.success(request, f'Transferencia exitosa de Q{monto} de {cuenta_origen} a {cuenta_destino}')
            return redirect('consultas')
        
        except Cuenta.DoesNotExist:
            messages.error(request, 'Una o ambas cuentas no existen')
            return redirect('transferencia')
        except Exception as e:
            messages.error(request, f'Error en la transferencia: {str(e)}')
            return redirect('transferencia')
    
    cuentas = Cuenta.objects.all()
    return render(request, 'transferencia.html', {'cuentas': cuentas})