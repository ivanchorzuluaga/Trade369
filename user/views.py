from django.shortcuts import render, redirect , get_object_or_404
from .forms import loginForm , clienteForm 
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from user.models import User , cliente, contrato, retiro, valores
from user.forms import CreateUserForm , ContratoForm, RetiroForm, ValoresForm
from django.contrib import messages
from django.db.models import Sum
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
# Create your views here.

def login369(request):
    form = loginForm(request.POST or None)
    error = ""
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.Administrador:
                login(request, user)
                return redirect('dashboard369')
            elif user is not None and user.inversor:
                login(request, user)
                return redirect('dashboardUsuario369')
            else:
                error = 'Usuario o contraseña invalidos'
        else:
            error = 'Por favor ingresa datos de Usuario'
    return render (request , 'login369.html' ,{'form':form ,'error':error})

@login_required
def cerrarSesion(request):
    logout(request)
    return redirect('login369')

@login_required
def dashboard369(request):
    usuario = cliente.objects.filter(usuario=request.user)
    contratos = contrato.objects.all()
    top_contratos = contrato.objects.order_by('-inversion')[:3]
    total_contratos = contrato.objects.count()
    total_clientes = cliente.objects.count()
    ultimo_interes = valores.objects.order_by('fechaDia').last()
    suma = contrato.objects.all().aggregate(Sum('inversion'))
    suma =suma.get('inversion__sum')
    total_valores = valores.objects.order_by('fechaDia').distinct('fechaDia').count()
    total_valoresi = total_valores - 7
    total_valoresf = total_valores + 1
    if total_valores >= 8:
        chart_valores = valores.objects.order_by('fechaDia').distinct('fechaDia')[total_valoresi:total_valoresf]
    else:
        chart_valores = valores.objects.order_by('fechaDia').distinct('fechaDia')
    engine = create_engine("postgresql://postgres:4dgf0rc31v4n*.@localhost/Trade2")
    valores_query = 'SELECT * FROM user_valores'
    df = pd.read_sql_query(sql=text(valores_query), con=engine.connect())
    df["SubTotal"] =df["SubTotal"].astype(float)
    df["SubTotal"] =df["SubTotal"].astype(int)
    df2 = df.groupby(['fechaDia'])[['SubTotal']].sum()
    df2 = df2.reset_index()
    fecha_chart = list(df2['fechaDia'])[-5:]
    valor_chart = list(df2['SubTotal'])[-5:]
    if request.user.Administrador:
        return render(request, 'dashboard.html',{
            'usuario': usuario,
            'contratos': contratos,
            'top_contratos': top_contratos,
            'total_contratos': total_contratos,
            'total_clientes': total_clientes,
            'ultimo_interes': ultimo_interes,
            'suma': suma,
            'chart_valores': chart_valores,
            'fecha_chart': fecha_chart,
            'valor_chart': valor_chart

        })
    else:
        return redirect('dashboardUsuario369')

@login_required
def dashboardUsuario369(request):
     if request.user.Administrador:
        return render(request, 'dashboard.html')
     else:
        usuario = request.user.id
        valoresUser = valores.objects.filter(usuarioV=usuario)
        total_valores = valores.objects.order_by('fechaDia').distinct('fechaDia').count()
        ultimo_interes = valores.objects.filter(usuarioV=usuario).order_by('fechaDia').last()
        inversion = contrato.objects.filter(usuarioC=usuario).aggregate(Sum('inversion'))
        inversion =inversion.get('inversion__sum')
        suma = valores.objects.filter(usuarioV=usuario).aggregate(Sum('SubTotal'))
        suma =suma.get('SubTotal__sum')
        total_valoresi = total_valores - 7
        total_valoresf = total_valores + 1
        if total_valores >= 8:
            chart_valores = valores.objects.filter(usuarioV=usuario).order_by('fechaDia').distinct('fechaDia')[total_valoresi:total_valoresf]
        else:
            chart_valores = valores.objects.filter(usuarioV=usuario).order_by('fechaDia').distinct('fechaDia')

        return render(request, 'dashboardUsuario.html',{
            'valoresUser': valoresUser,
            'chart_valores': chart_valores,
            'inversion': inversion,
            'ultimo_interes': ultimo_interes,
            'suma':suma,
        })

@login_required
def usuario369(request):
    if request.user.Administrador:
        if request.method == 'GET':
            usuarios = User.objects.all()
            return render(request, 'users.html', {
                'formNuevoUsuario': CreateUserForm,
                'usuarios':usuarios
            })
        else:
            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.create_user(
                        username=request.POST['username'], password=request.POST['password1'])
                    user.save()
                    return redirect('usuario369')
                except:
                    return render(request, 'users.html', {
                        'formNuevoUsuario': CreateUserForm,
                        'error': "El Ususario ya existe"
                    })
            return render(request, 'users.html', {
                'formNuevoUsuario': CreateUserForm,
                'error': "Contraseñas no coinciden"
            })
    else:
        return redirect('login369')

@login_required
def editarUsuario369(request , id):
    if request.user.Administrador:
        usuario = get_object_or_404(User, id=id)
        data = {
            'form': CreateUserForm(instance=usuario)
        }
        if request.method == "POST":
            formulario = CreateUserForm(
                data=request.POST, instance=usuario, files=request.FILES)
            if request.POST['password1'] == request.POST['password2']:
                user = request.POST['username']
                password = request.POST['password1']
                u = User.objects.get(username=user)
                u.set_password(password)
                messages.success(request, "Contraseña actualizada correctamente")
                u.save()
                return redirect('usuario369')
            else:
                messages.error(request, "Error en los datos.")
                return render(request, 'editar_users.html',{
                    'form':formulario,
                })
        return render(request, 'editar_users.html',data)
    else:
        return redirect('dashboardUsuario369')

@login_required
def eliminarUsuario369(request, id):
    if request.user.Administrador:
        usuario = get_object_or_404(User, id=id)
        messages.success(request, "Eliminado correctamente")
        usuario.delete()
        return redirect('usuario369')
    else:
        return redirect('dashboardUsuario369')


@login_required
def detalleUsuario369(request):
    if request.user.Administrador:
        if request.method == 'GET':
            detalles = cliente.objects.all()        
            return render(request, 'users_detail.html', {
                'detalles':detalles,
                'form':clienteForm}
            )
        else:
            try:
                form = clienteForm(request.POST)
                form.save()
                return redirect('detalleUsuario369')
            except:
                return render(request, 'users_detail.html', {
                'detalles':detalles,
                'form':clienteForm,
                'error':"los datos ingresados estan invalidos"}
            )
    else:
        return redirect('dashboardUsuario369')

@login_required
def editarDetalleUsuario369(request , id):
    if request.user.Administrador:
        usuario = get_object_or_404(cliente, id=id)
        data = {
            'form': clienteForm(instance=usuario)
        }
        if request.method == "POST":
            formulario = clienteForm(
                data=request.POST, instance=usuario, files=request.FILES)
            if formulario.is_valid():
                messages.success(request, "Detalles de usuario actualizados correctamente")
                formulario.save()
                return redirect("detalleUsuario369")
            else:
                messages.error(request, "Error en los datos.")
                data["clienteForm"] = formulario

        return render(request, 'editar_users_detail.html',data)
    else:
        return redirect('dashboardUsuario369')


@login_required
def eliminarDetalleUsuario369(request, id):
    if request.user.Administrador:
        cliente1 = get_object_or_404(cliente, id=id)
        cliente1.delete()
        messages.success(request, "Eliminado correctamente")
        return redirect("detalleUsuario369")
    else:
        return redirect('dashboardUsuario369')


@login_required
def contrato369(request):
    if request.user.Administrador:
        if request.method == 'GET':
            contratos = contrato.objects.all()        
            return render(request, 'contratos.html', {
                'contratos':contratos,
                'form':ContratoForm}
            )
        else:
            try:
                usuario = request.POST.get('NomCliente')
                usuarioU = cliente.objects.filter(id=usuario).aggregate(Sum('usuario'))
                usuarioGet = usuarioU.get('usuario__sum')
                usuarioGet = int(usuarioGet)
                form = ContratoForm(request.POST)
                form.save()
                return redirect('contrato369')
            except:
                contratos = contrato.objects.all()
                return render(request, 'contratos.html', {
                'contratos':contratos,
                'form':ContratoForm,
                'error':"los datos ingresados estan invalidos"}
                )
    else:
        return redirect('dashboardUsuario369')

@login_required
def editarContrato369(request , id):
    if request.user.Administrador:
        contratos = get_object_or_404(contrato, id=id)
        data = {
            'form': ContratoForm(instance=contratos)
        }
        if request.method == "POST":
            formulario = ContratoForm(
                data=request.POST, instance=contratos, files=request.FILES)
            if formulario.is_valid():
                messages.success(request, "Contrato actualizado correctamente")
                formulario.save()
                return redirect("contrato369")
            else:
                messages.error(request, "Error en los datos.")
                data["ContratoForm"] = formulario
        return render(request, 'editar_contrato.html',data)
    else:
        return redirect('dashboardUsuario369')

@login_required
def eliminarContrato369(request, id):
    if request.user.Administrador:
        contrato1 = get_object_or_404(contrato, id=id)
        contrato1.delete()
        messages.success(request, "Eliminado correctamente")
        return redirect("contrato369")
    else:
        return redirect('dashboardUsuario369')


@login_required
def retiro369(request):
    if request.user.Administrador:
        if request.method == 'GET':
            retiros = retiro.objects.all()        
            return render(request, 'retiros.html', {
                'retiros':retiros,
                'form':RetiroForm}
            )
        else:
            try:
                form = RetiroForm(request.POST)
                form.save()
                return redirect('retiro369')
            except:
                return render(request, 'retiros.html', {
                'retiros':retiros,
                'form':RetiroForm,
                'error':"los datos ingresados estan invalidos"}
                )
    else:
        return redirect('dashboardUsuario369')

@login_required
def editarRetiro369(request, id):
    if request.user.Administrador:
        retiros = get_object_or_404(retiro, id=id)
        data = {
            'form': RetiroForm(instance=retiros)
        }
        if request.method == "POST":
            formulario = RetiroForm(
                data=request.POST, instance=retiros, files=request.FILES)
            if formulario.is_valid():
                messages.success(request, "Retiro actualizado correctamente")
                formulario.save()
                return redirect("retiro369")
            else:
                messages.error(request, "Error en los datos.")
                data["RetiroForm"] = formulario
        return render(request, 'editar_retiros.html',data)
    else:
        return redirect('dashboardUsuario369')

@login_required
def eliminarRetiro369(request, id):
    if request.user.Administrador:
        retiro1 = get_object_or_404(retiro, id=id)
        retiro1.delete()
        messages.success(request, "Eliminado correctamente")
        return redirect("retiro369")
    else:
        return redirect('dashboardUsuario369')


@login_required
def valor369(request):
    if request.user.Administrador:
        if request.method == 'GET':
            valor = valores.objects.all()        
            return render(request, 'valores.html', {
                'valor':valor,
                'form':ValoresForm}
            )
        else:
            try:
                interes = request.POST.get('interesDia')
                fecha = request.POST.get('fecha')
                engine = create_engine("postgresql://postgres:4dgf0rc31v4n*.@localhost/Trade2")
                usuarios = 'SELECT * FROM user_user'
                cliente = 'SELECT * FROM user_cliente'
                contrato = 'SELECT * FROM user_contrato'
                query_id_maximo =  'SELECT MAX("id") FROM user_valores'

                df_usuarios = pd.read_sql_query(sql=text(usuarios), con=engine.connect())
                df_cliente = pd.read_sql_query(sql=text(cliente), con=engine.connect())
                df_contrato = pd.read_sql_query(sql=text(contrato), con=engine.connect())

                query_id_maximo = pd.read_sql_query(sql=text(query_id_maximo), con=engine.connect())

                maximo = query_id_maximo.iloc[0]['max']

                df_usuarios = pd.DataFrame(df_usuarios, columns=['id', 'username', 'inversor'])
                df_usuarios = df_usuarios.rename(columns={'id':'id_usuario'})
                df_cliente = pd.DataFrame(df_cliente, columns=['id','usuario_id', 'nombre', 'estado'])
                df_cliente = df_cliente.rename(columns={'id':'id_cliente'})
                df_contrato = pd.DataFrame(df_contrato, columns=['id','NomCliente_id', 'inversion'])
                df_contrato = df_contrato.rename(columns={'id':'id_contrato'})


                merge_usu_client = pd.merge(df_usuarios, df_cliente, how='outer', 
                                sort=True, left_on='id_usuario', right_on='usuario_id')


                merge_usu_client_cont = pd.merge(merge_usu_client, df_contrato, how='outer', indicator='resultado',
                                    sort=True, left_on='id_cliente', right_on='NomCliente_id') 

                df_mask=merge_usu_client_cont['estado']==True

                filtered_df = merge_usu_client_cont[df_mask]

                list_ganancia = []
                for i in range(len(filtered_df)):
                    valor = filtered_df.iloc[i, 9]
                    ganancia = valor * float(interes) / 100
                    list_ganancia.append(ganancia)

                filtered_df.loc[:, "Ganancia"] = list_ganancia

                filtered_df["interesDia"] = float(interes)
                filtered_df["fechaDia"] = fecha

                df_guardar = pd.DataFrame(filtered_df, columns=['interesDia','fechaDia', 'Ganancia', 'id_usuario','id_contrato'])

                if maximo == None:
                    df_guardar["id"] = np.arange(len(df_guardar))
                else:
                    df_guardar["id"] = np.arange(maximo+1, len(df_guardar)+maximo+1)

                df_guardar = df_guardar.set_index('id')

                df_guardar = df_guardar.rename(columns={'Ganancia':'SubTotal','id_contrato':'contrato_id','id_usuario':'usuarioV_id'})

                df_guardar = df_guardar[df_guardar['SubTotal'].notna()]

                df_guardar.to_sql('user_valores', con=engine, if_exists="append")

                return redirect('valor369')
            except:
                return render(request, 'valores.html', {
                'valor':valor,
                'form':ValoresForm,
                'error':"los datos ingresados estan invalidos"}
                )
    else:
        return redirect('dashboardUsuario369')

@login_required
def editarValor369(request, id):
    if request.user.Administrador:
        valor = get_object_or_404(valores, id=id)
        data = {
            'form': ValoresForm(instance=valor)
        }
        if request.method == "POST":
            formulario = ValoresForm(
                data=request.POST, instance=valor, files=request.FILES)
            if formulario.is_valid():
                messages.success(request, "Valor actualizado correctamente")
                formulario.save()
                return redirect("valor369")
            else:
                messages.error(request, "Error en los datos.")
                data["ValoresForm"] = formulario
        return render(request, 'editar_valores.html',data)
    else:
        return redirect('dashboardUsuario369')

@login_required
def eliminarValor369(request, id):
    if request.user.Administrador:
        valor = get_object_or_404(valores, id=id)
        valor.delete()
        messages.success(request, "Eliminado correctamente")
        return redirect("valor369")
    else:
        return redirect('dashboardUsuario369')


