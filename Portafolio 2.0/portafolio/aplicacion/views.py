from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.db import connection
from .models import *
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View, TemplateView, ListView, CreateView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic import (CreateView)
from .forms import AcompañanteForm, UserRegisterForm, LoginForm, UpdatePasswordForm, VerificationForm, ContactForm, ReservaForm, DepartamentoForms, AdminUserForm, ReservaAdminForm, ServicioExtraForm, TourForm, ConductorForm, VehiculoForm, VentaForm, ReservaFuncionarioForm, CiudadForm, ComunaForm, InventarioForm, MultaForm, ReservaVoucherForm, VentaClienteForm,VentaFuncionarioForm
from django.views.generic.edit import (FormView)
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .functions import code_generator, render_to_pdf, procesar_venta, detalle_ventas_no_cerradas
from django.core.mail import send_mail
from django.template import context
from .mixins import SuperUsuarioMixin, FuncionarioUsuarioMixin
from .managers import AgregarReservaManager
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersGetRequest, OrdersCaptureRequest
from django.db.models import Sum
from django.core.paginator import Paginator

import sys, json


class InicioView(TemplateView):
    template_name = "index.html"

'''

Login---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

'''
class UserRegisterView(FormView):
    template_name = 'register.html'
    form_class = UserRegisterForm
    success_url =  reverse_lazy('cliente_app:logeo')

    def form_valid(self, form):
        #generamos codigo
        codigo = code_generator()

        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['cli_Rut'],
            form.cleaned_data['password1'],
            cli_Nombre=form.cleaned_data['cli_Nombre'],
            cli_Apellidos=form.cleaned_data['cli_Apellidos'],
            cli_Edad=form.cleaned_data['cli_Edad'],
            cli_Nacionalidad=form.cleaned_data['cli_Nacionalidad'],
            email=form.cleaned_data['email'],
            cli_Telefono=form.cleaned_data['cli_Telefono'],
            codregistro=codigo
        )
        #enviar el codigo al email del user
        asunto = 'Confirmacion de Email'
        mensaje = 'Codigo de Verificacion: ' + codigo
        email_remitente = 'aguilerajordan2@gmail.com'
        send_mail(asunto, mensaje, email_remitente, [form.cleaned_data['email'],])
        #redirigir a pantalla de validacion
        return HttpResponseRedirect(
            reverse(
                'cliente_app:verification-user',
                kwargs={'pk': usuario.id}
            )
        )


class LoginUser(FormView):
    template_name = "registration/login.html"
    form_class = LoginForm
    success_url =  reverse_lazy('cliente_app:inicio')

    def form_valid(self, form):
        user = authenticate(
            username= form.cleaned_data['username'],
            password= form.cleaned_data['password']
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)

class LogoutView(View):
    
    def get(self, request, *args, **kargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'cliente_app:logeo'
            )
        )

class UpdatePasswordView(FormView):
    template_name = 'update.html'
    form_class = UpdatePasswordForm
    success_url =  reverse_lazy('cliente_app:logeo')

    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            username=usuario.username,
            password=form.cleaned_data['password1']
        )

        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()

        logout(self.request)

        return super(UpdatePasswordView, self).form_valid(form)

class CodeVerificationView(FormView):

    template_name = "verification.html"
    form_class = VerificationForm
    success_url =  reverse_lazy('cliente_app:logeo')

    def get_form_kwargs(self):
        kwargs = super(CodeVerificationView, self).get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs['pk']
        })
        return kwargs

    def form_valid(self, form):
        User.objects.filter(
            id=self.kwargs['pk']
        ).update(
            is_active=True
        )
        return super(CodeVerificationView, self).form_valid(form)

'''

Aqui terminar login---------------------------------------------------------
'''
'''
Cliente------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''
''' TEMPLATEVIEW-------------------------------------------- '''

class InicioclienteView(LoginRequiredMixin, View):
    template_name = "inicio.html"
    login_url = reverse_lazy('cliente_app:logeo')
    model = Reservando
    form_class = ReservaFuncionarioForm

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        contexto = {}
        contexto['reserva'] = self.get_queryset()
        contexto['departamentoscliente'] = Departamento.objects.all()
        contexto['vehiculo'] = Vehiculo.objects.all()
        contexto['tours'] = Tour.objects.all()
        contexto['reservatrue'] = Venta.objects.all()
        contexto['reservafalse'] = Reservando.objects.filter(Estado_Reservas=False)
        return contexto

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name, self.get_context_data())

''' ----------------------------LISTVIEW------------------------ '''

class ListCliente(LoginRequiredMixin, ListView):
    template_name = 'cliente.html'
    model = Reservando
    context_object_name = 'reservita'
    login_url = reverse_lazy('cliente_app:logeo')

    def get_queryset(self, *args, **kwargs):
        return Reservando.objects.filter(user=self.request.user)

class ListPerfil(LoginRequiredMixin, TemplateView):
    template_name = 'perfil.html'
    login_url = reverse_lazy('cliente_app:logeo')

class ListAcompañante(LoginRequiredMixin, ListView):
    template_name = 'lista_acompañante.html'
    model = Acompañante
    context_object_name = 'acompañante'
    login_url = reverse_lazy('cliente_app:logeo')

    def get_queryset(self, *args, **kwargs):
        return Acompañante.objects.filter(user=self.request.user)

class ListReservaListView(LoginRequiredMixin, ListView):
    template_name = 'informepdf.html'
    model = Reserva
    paginate_by = 1
    context_object_name = 'reservitapdf'
    login_url = reverse_lazy('cliente_app:logeo')

    def get_queryset(self, *args, **kwargs):
        return Reserva.objects.filter(user=self.request.user)

class ListReservaPdf(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        reservitapdf = Reservando.objects.get(id=self.kwargs['pk'])
        
        data = {
            'reservitapdf' : reservitapdf
        }
        pdf = render_to_pdf('listareserva.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

''' -----------------------------CreateVIEW-------------------- '''

class ContactCreateView(LoginRequiredMixin, CreateView):
    template_name = "contacto.html"
    form_class = ContactForm
    success_url = '.'
    login_url = reverse_lazy('cliente_app:logeo')

class CrearAcompañanteView(LoginRequiredMixin, CreateView):
    template_name = "registroacom.html"
    model = Acompañante
    form_class = AcompañanteForm
    success_url =  reverse_lazy('cliente_app:listadoacompañante')
    login_url = reverse_lazy('cliente_app:logeo')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(CrearAcompañanteView, self).form_valid(form)

class CrearReservaView(LoginRequiredMixin, FormView):
    template_name = "reserva.html"
    form_class = VentaClienteForm
    success_url =  reverse_lazy('cliente_app:cliente')
    login_url = reverse_lazy('cliente_app:logeo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["departamento"] = Departamento.objects.all()
        return context

    def form_valid(self, form):
        Codigo = form.cleaned_data['Codigo']
        count = form.cleaned_data['count']
        Fecha_Reserva_Inicios = form.cleaned_data['Fecha_Reserva_Inicios']
        Fecha_Reserva_Terminos = form.cleaned_data['Fecha_Reserva_Terminos']
        user = form.cleaned_data['user']
        obj, created = Reservando.objects.get_or_create(
            Codigo=Codigo,
            defaults={
                'departamento': Departamento.objects.get(Codigo=Codigo),
                'count': count,
                'Fecha_Reserva_Inicios': Fecha_Reserva_Inicios,
                'Fecha_Reserva_Terminos': Fecha_Reserva_Terminos,
                'user': user==self.request.user
            }
        )
        if not created:
            obj.count = obj.count + count
            obj.save()
        return super(CrearReservaView, self).form_valid(form)

''' -----------------------------UPDATEVIEW--------------------- '''

class AcompañanteUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "editacom.html"
    model = Acompañante
    form_class = AcompañanteForm
    success_url =  reverse_lazy('cliente_app:listadoacompañante')
    login_url = reverse_lazy('cliente_app:logeo')

''' -----------------------------DELETEVIEW--------------------- '''

class AcompañanteDelete(LoginRequiredMixin, DeleteView):
    template_name = "deleteacomp.html"
    model = Acompañante
    success_url =  reverse_lazy('cliente_app:listadoacompañante')
    login_url = reverse_lazy('cliente_app:logeo')

class ReservaDelete(LoginRequiredMixin, DeleteView):
    template_name = "cancelarreserva.html"
    model = Reservando
    success_url =  reverse_lazy('cliente_app:cliente')
    login_url = reverse_lazy('cliente_app:logeo')

'''

termina aqui Cliente----------------------------------------------------------------------------------------------------------------------------------------------------------------

'''
'''

Empieza Funcionario------------------------------------------------------------------------------------------------------------------------------------------------------------------

'''

class FuncionarioView(LoginRequiredMixin,TemplateView):
    template_name = 'funcionario.html'
    login_url = reverse_lazy('cliente_app:logeo')

class PerfilFuncionarioView(LoginRequiredMixin, FuncionarioUsuarioMixin,TemplateView):
    template_name = 'perfil_funcionario.html'
    login_url = reverse_lazy('cliente_app:logeo')

class CrearlistadoView(LoginRequiredMixin,TemplateView):
    template_name = 'crear_listado.html'
    login_url = reverse_lazy('cliente_app:logeo')

class ReservaFuncionarioUpdateView(LoginRequiredMixin, FuncionarioUsuarioMixin, UpdateView):
    template_name = "actualizarcheck.html"
    model = Reservando
    form_class = VentaFuncionarioForm
    success_url =  reverse_lazy('cliente_app:inicio')
    login_url = reverse_lazy('cliente_app:logeo')

class ListReservaFuncionarioPdf(LoginRequiredMixin, FuncionarioUsuarioMixin, View):

    def get(self, request, *args, **kwargs):
        reservalista = Reservando.objects.get(id=self.kwargs['pk'])
        data = {
            'reservalista' : reservalista
        }
        pdf = render_to_pdf('listareservafuncionario.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

'''
termina aqui Funcionario-----------------------------------------------------------------------------------------------------------------------------------------------------------

'''
'''

Empieza Administrador----------------------------------------------------------------------------------------------------------------------------------------------------------------

'''

''' mantenedor cliente ------------------------------------------------------'''

class MantenerClienteView(LoginRequiredMixin, SuperUsuarioMixin, View):
    model = User
    form_class = UserRegisterForm
    template_name = 'mantener_cliente.html'
    login_url = reverse_lazy('cliente_app:logeo')

    def get_queryset(self):
        return self.model.objects.filter(is_staff = False)

    def get_context_data(self, **kwargs):
        contexto = {}
        contexto['usuario'] = self.get_queryset()
        contexto['form'] = self.form_class
        contexto['usercount'] = User.objects.count()
        contexto['userultimo'] = User.objects.last()
        return contexto

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return redirect('cliente_app:mantener_cliente')

class ClienteUpdateView(LoginRequiredMixin, SuperUsuarioMixin, UpdateView):
    template_name = "actualizaruser.html"
    model = User
    form_class = AdminUserForm
    success_url =  reverse_lazy('cliente_app:mantener_cliente')
    login_url = reverse_lazy('cliente_app:logeo')

class UsuarioDeleteView(LoginRequiredMixin, SuperUsuarioMixin, DeleteView):
    template_name = "deleteuser.html"
    model = User
    success_url =  reverse_lazy('cliente_app:mantener_cliente')
    login_url = reverse_lazy('cliente_app:logeo')

''' mantenedor Departamento ------------------------------------------------------'''

class MantenerDepartamentoView(LoginRequiredMixin, SuperUsuarioMixin, View):
    model = Departamento
    form_class = DepartamentoForms
    template_name = 'mantener_departamento.html'
    login_url = reverse_lazy('cliente_app:logeo')

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        contexto = {}
        contexto['departamento'] = self.get_queryset()
        contexto['form'] = self.form_class
        contexto['departamentocount'] = Departamento.objects.count()
        contexto['departamentoultimo'] = Departamento.objects.last()
        return contexto

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('cliente_app:mantener_departamento')

class DepartamentoUpdateView(LoginRequiredMixin, SuperUsuarioMixin, UpdateView):
    template_name = "actualizardepartamento.html"
    model = Departamento
    form_class = DepartamentoForms
    success_url =  reverse_lazy('cliente_app:mantener_departamento')
    login_url = reverse_lazy('cliente_app:logeo')

class DepartamentoDeleteView(LoginRequiredMixin, SuperUsuarioMixin, DeleteView):
    template_name = "deletedepartamento.html"
    model = Departamento
    success_url =  reverse_lazy('cliente_app:mantener_departamento')
    login_url = reverse_lazy('cliente_app:logeo')

'''  Ciudad Crear------------------------------------------------------'''

class CiudadView(LoginRequiredMixin, SuperUsuarioMixin, View):
    model = Ciudad
    form_class = CiudadForm
    template_name = 'ciudad.html'
    login_url = reverse_lazy('cliente_app:logeo')

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        contexto = {}
        contexto['ciudad'] = self.get_queryset()
        contexto['form'] = self.form_class
        return contexto

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return redirect('cliente_app:ciudad')


'''  Comuna Crear------------------------------------------------------'''

class ComunaView(LoginRequiredMixin, SuperUsuarioMixin, View):
    model = Comuna
    form_class = ComunaForm
    template_name = 'comuna.html'
    login_url = reverse_lazy('cliente_app:logeo')

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        contexto = {}
        contexto['comuna'] = self.get_queryset()
        contexto['form'] = self.form_class
        return contexto

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return redirect('cliente_app:comuna')

'''  Inventario Crear------------------------------------------------------'''

class InventarioView(LoginRequiredMixin, SuperUsuarioMixin, View):
    model = Inventario
    form_class = InventarioForm
    template_name = 'inventario.html'
    login_url = reverse_lazy('cliente_app:logeo')

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        contexto = {}
        contexto['inventario'] = self.get_queryset()
        contexto['form'] = self.form_class
        return contexto

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('cliente_app:inventario')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(InventarioView, self).form_valid(form)

class InventarioDeleteView(LoginRequiredMixin, SuperUsuarioMixin, DeleteView):
    template_name = "deleteinventario.html"
    model = Inventario
    success_url =  reverse_lazy('cliente_app:inventario')
    login_url = reverse_lazy('cliente_app:logeo')

'''  Mantenedor Reserva ------------------------------------------------------'''

class MantenerReservaView(LoginRequiredMixin, SuperUsuarioMixin, View):
    model = Reserva
    form_class = ReservaAdminForm
    purchases_paginate_by = 2
    template_name = 'mantener_reserva.html'
    login_url = reverse_lazy('cliente_app:logeo')

    def get_context_data(self, **kwargs):
        contexto = {}
        contexto['reserva'] = self.model.objects.all()
        contexto['form'] = self.form_class
        contexto['reservacoun'] = Reserva.objects.count()
        contexto['reservaultima'] = Reserva.objects.last()

        return contexto

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return redirect('cliente_app:mantener_reserva')

class ActualizarReservaUpdateView(LoginRequiredMixin, SuperUsuarioMixin, UpdateView):
    template_name = "actualizarreserva.html"
    model = Reserva
    form_class = ReservaAdminForm
    success_url =  reverse_lazy('cliente_app:mantener_reserva')
    login_url = reverse_lazy('cliente_app:logeo')

class ReservaAdminDeleteView(LoginRequiredMixin, SuperUsuarioMixin, DeleteView):
    template_name = "deletereserva.html"
    model = Reserva
    success_url =  reverse_lazy('cliente_app:mantener_reserva')
    login_url = reverse_lazy('cliente_app:logeo')

class ReservaDetailView(LoginRequiredMixin, SuperUsuarioMixin, DetailView):

    template_name = "detailreserva.html"
    model = Reserva
    login_url = reverse_lazy('cliente_app:logeo')

''' Mantenedor Servicio ------------------------------------------------------'''

class MantenerServicioView(LoginRequiredMixin, SuperUsuarioMixin, View):
    model = ServicioExtra
    form_class = ServicioExtraForm
    template_name = 'mantener_servicio.html'
    login_url = reverse_lazy('cliente_app:logeo')

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        contexto = {}
        contexto['servicio'] = self.get_queryset()
        contexto['form'] = self.form_class
        contexto['serviciosextras'] = ServicioExtra.objects.count()
        contexto['servicioultimo'] = ServicioExtra.objects.last()
        return contexto

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return redirect('cliente_app:mantener_servicio')

class ServicioUpdateView(LoginRequiredMixin, SuperUsuarioMixin, UpdateView):
    template_name = "actualizarservicio.html"
    model = ServicioExtra
    form_class = ServicioExtraForm
    success_url =  reverse_lazy('cliente_app:mantener_servicio')
    login_url = reverse_lazy('cliente_app:logeo')

class ServicioAdminDeleteView(LoginRequiredMixin, SuperUsuarioMixin, DeleteView):
    template_name = "deleteservicio.html"
    model = ServicioExtra
    success_url =  reverse_lazy('cliente_app:mantener_servicio')
    login_url = reverse_lazy('cliente_app:logeo')

'''  Tour CRUD  ------------------------------------------------------'''

class TourView(LoginRequiredMixin, SuperUsuarioMixin, View):
    model = Tour
    form_class = TourForm
    template_name = 'mantener_tour.html'
    login_url = reverse_lazy('cliente_app:logeo')

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        contexto = {}
        contexto['tour'] = self.get_queryset()
        contexto['form'] = self.form_class
        return contexto

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('cliente_app:mantener_tour')

class TourUpdateView(LoginRequiredMixin, SuperUsuarioMixin, UpdateView):
    template_name = "actualizartour.html"
    model = Tour
    form_class = TourForm
    success_url =  reverse_lazy('cliente_app:mantener_tour')
    login_url = reverse_lazy('cliente_app:logeo')

class TourDeleteView(LoginRequiredMixin, SuperUsuarioMixin, DeleteView):
    template_name = "deletetour.html"
    model = Tour
    success_url =  reverse_lazy('cliente_app:mantener_tour')
    login_url = reverse_lazy('cliente_app:logeo')

'''  Conductor CRUD  ------------------------------------------------------'''

class ConductorView(LoginRequiredMixin, SuperUsuarioMixin, View):
    model = Conductor
    form_class = ConductorForm
    template_name = 'mantener_conductor.html'
    login_url = reverse_lazy('cliente_app:logeo')

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        contexto = {}
        contexto['conductor'] = self.get_queryset()
        contexto['form'] = self.form_class
        return contexto

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return redirect('cliente_app:mantener_conductor')

class ConductorUpdateView(LoginRequiredMixin, SuperUsuarioMixin, UpdateView):
    template_name = "actualizarconductor.html"
    model = Conductor
    form_class = ConductorForm
    success_url =  reverse_lazy('cliente_app:mantener_conductor')
    login_url = reverse_lazy('cliente_app:logeo')

class ConductorDeleteView(LoginRequiredMixin, SuperUsuarioMixin, DeleteView):
    template_name = "deleteconductor.html"
    model = Conductor
    success_url =  reverse_lazy('cliente_app:mantener_conductor')
    login_url = reverse_lazy('cliente_app:logeo')

'''  Vehiculo CRUD  ------------------------------------------------------'''

class VehiculoView(LoginRequiredMixin, SuperUsuarioMixin, View):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'mantener_vehiculo.html'
    login_url = reverse_lazy('cliente_app:logeo')

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        contexto = {}
        contexto['vehiculo'] = self.get_queryset()
        contexto['form'] = self.form_class
        return contexto

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('cliente_app:mantener_vehiculo')

class VehiculoUpdateView(LoginRequiredMixin, SuperUsuarioMixin, UpdateView):
    template_name = "actualizarvehiculo.html"
    model = Vehiculo
    form_class = VehiculoForm
    success_url =  reverse_lazy('cliente_app:mantener_vehiculo')
    login_url = reverse_lazy('cliente_app:logeo')

class VehiculoDeleteView(LoginRequiredMixin, SuperUsuarioMixin, DeleteView):
    template_name = "deletevehiculo.html"
    model = Vehiculo
    success_url =  reverse_lazy('cliente_app:mantener_vehiculo')
    login_url = reverse_lazy('cliente_app:logeo')

'''  multa CRUD  ------------------------------------------------------'''

class MultaView(LoginRequiredMixin, FuncionarioUsuarioMixin, View):
    model = Multa
    form_class = MultaForm
    template_name = 'multa.html'
    login_url = reverse_lazy('cliente_app:logeo')

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        contexto = {}
        contexto['multa'] = self.get_queryset()
        contexto['form'] = self.form_class
        contexto['multascount'] = Multa.objects.count()
        contexto['multalast'] = Multa.objects.last()
        return contexto

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('cliente_app:multa')

class MultaUpdateView(LoginRequiredMixin, FuncionarioUsuarioMixin, UpdateView):
    template_name = "actualizarmulta.html"
    model = Multa
    form_class = MultaForm
    success_url =  reverse_lazy('cliente_app:multa')
    login_url = reverse_lazy('cliente_app:logeo')

class MultaDeleteView(LoginRequiredMixin, FuncionarioUsuarioMixin, DeleteView):
    template_name = "deletemulta.html"
    model = Multa
    success_url =  reverse_lazy('cliente_app:multa')
    login_url = reverse_lazy('cliente_app:logeo')

'''Pago -----------------------------------------------------------------'''

class PagosView(LoginRequiredMixin, SuperUsuarioMixin, TemplateView):
    template_name = 'pagos_adm.html'
    login_url = reverse_lazy('cliente_app:logeo')

class ServiciosView(LoginRequiredMixin, SuperUsuarioMixin, TemplateView):
    template_name = 'mantener_servicios.html'
    login_url = reverse_lazy('cliente_app:logeo')

'''Estadisticas -----------------------------------------------------------------'''
class EstadisticaView(LoginRequiredMixin, SuperUsuarioMixin, TemplateView):
    template_name = 'generar_estadistica.html'
    login_url = reverse_lazy('cliente_app:logeo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clientes'] = User.objects.count()
        context['reservas'] = Reservando.objects.count()
        context['departamentos'] = Departamento.objects.count()
        context['servicios'] = Venta.objects.count()
        context['num_ventas_hoy'] = detalle_ventas_no_cerradas
        context['gananciamulta'] = Multa.objects.aggregate(Sum('monto_multa'))
        context['gananciareserva'] = Venta.objects.aggregate(Sum('amount'))
        return context


class InformeView(LoginRequiredMixin, SuperUsuarioMixin, TemplateView):
    template_name = 'generar_informe.html'
    login_url = reverse_lazy('cliente_app:logeo')

'''Perfil Administrador -------------------------------------------------'''

class PerfilAdminListView(LoginRequiredMixin, SuperUsuarioMixin,TemplateView):
    template_name = 'perfiladministrador.html'
    login_url = reverse_lazy('cliente_app:logeo')

class PerfilUpdateView(LoginRequiredMixin, SuperUsuarioMixin, UpdateView):
    template_name = "actualizar_perfil.html"
    model = User
    form_class = UserRegisterForm
    success_url =  reverse_lazy('cliente_app:inicio')
    login_url = reverse_lazy('cliente_app:logeo')

'''                           
termina aqui Administrador-----------------------------------------------------------------------------------------------------------------------------------------------------------

'''
def resultado(request):
    return render (request, 'resultado.html')

'''Venta ----------------------------------------------------------------------------------------------------------------------------------------------'''

class AgregarReservaView(LoginRequiredMixin, SuperUsuarioMixin,FormView):
    template_name = "reservando.html"
    form_class = VentaForm
    success_url =  reverse_lazy('cliente_app:reservando')
    login_url = reverse_lazy('cliente_app:logeo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Reserva"] = Reservando.objects.all()
        context["ReservaLast"] = Venta.objects.count()
        context["UltimaReserva"] = Venta.objects.last()
        context["ReservaSinPagar"] = Reservando.objects.count()
        context["total_cobrar"] = Reservando.objects.total_cobrar()
        context['form_voucher'] = ReservaVoucherForm
        return context
    
    def form_valid(self, form):
        Codigo = form.cleaned_data['Codigo']
        count = form.cleaned_data['count']
        Fecha_Reserva_Inicios = form.cleaned_data['Fecha_Reserva_Inicios']
        Fecha_Reserva_Terminos = form.cleaned_data['Fecha_Reserva_Terminos']
        user = form.cleaned_data['user']
        obj, created = Reservando.objects.get_or_create(
            Codigo=Codigo,
            defaults={
                'departamento': Departamento.objects.get(Codigo=Codigo),
                'count': count,
                'Fecha_Reserva_Inicios': Fecha_Reserva_Inicios,
                'Fecha_Reserva_Terminos': Fecha_Reserva_Terminos,
                'user': user,
            }
        )
        if not created:
            obj.count = obj.count + count
            obj.save()
        return super(AgregarReservaView, self).form_valid(form)

class ActualizarReservaView(LoginRequiredMixin, SuperUsuarioMixin, View):

    def post(self, request, *args, **kwargs):
        rese = Reservando.objects.get(id=self.kwargs['pk'])
        if rese.count > 1:
            rese.count = rese.count - 1
            rese.save()
        #
        return HttpResponseRedirect(
            reverse(
                'cliente_app:reservando'
            )
        )

class EliminarReservaView(LoginRequiredMixin, SuperUsuarioMixin, DeleteView):
    model = Reservando
    success_url =  reverse_lazy('cliente_app:reservando')

class ReservaDeleteAll(LoginRequiredMixin, View):
    
    def post(self, request, *args, **kwargs):
        #
        Reservando.objects.all().delete()
        #
        return HttpResponseRedirect(
            reverse(
                'cliente_app:reservando'
            )
        )

class ProcesoReservaView(LoginRequiredMixin, SuperUsuarioMixin, View):

    def post(self, request, *args, **kwargs):
        #
        procesar_venta(
            self=self,
            type_invoce=Venta.SIN_COMPROBANTE,
            type_payment=Venta.CASH,
            user=self.request.user,
        )
        #
        return HttpResponseRedirect(
            reverse(
                'cliente_app:reservando'
            )
        )

class ProcesoVentaVoucherView(LoginRequiredMixin, SuperUsuarioMixin, FormView):
    form_class = ReservaVoucherForm
    success_url = '.'
    
    def form_valid(self, form):
        type_payment = form.cleaned_data['type_payment']
        type_invoce = form.cleaned_data['type_invoce']
        
        venta = procesar_venta(
            self=self,
            type_invoce=type_invoce,
            type_payment=type_payment,
            user=self.request.user,
        )
        #
        if venta: 
            return HttpResponseRedirect(
                reverse(
                    'cliente_app:reserva-voucher_pdf',
                    kwargs={'pk': venta.pk },
                )
            )
        else:
            return HttpResponseRedirect(
                reverse(
                    'cliente_app:reservando'
                )
            )

class ReservaVoucherPdf(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        venta = Venta.objects.get(id=self.kwargs['pk'])
        data = {
            'venta': venta,
            'detalle_productos': ReservaDetalle.objects.filter(venta__id=self.kwargs['pk'])
        }
        pdf = render_to_pdf('voucher.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

class ListaVentaView(LoginRequiredMixin, ListView):
    template_name = 'ventasreserva.html'
    context_object_name = "ventas"

    def get_queryset(self):
        return Venta.objects.ventas_no_cerradas()

class EliminarVentaView(LoginRequiredMixin, DeleteView):
    template_name = 'cancelarventa.html'
    model = Venta
    success_url =  reverse_lazy('cliente_app:ventasreserva')
    login_url = reverse_lazy('cliente_app:logeo')
        