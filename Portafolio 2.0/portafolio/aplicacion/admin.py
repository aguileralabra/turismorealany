from django.contrib import admin
from aplicacion.models import *

class UserAdmin(admin.ModelAdmin):
    search_fields = ('cli_Rut','cli_Nombre','username')
    list_display = ('cli_Rut','cli_Nombre','username', 'is_staff','is_active','is_superuser', 'funcionario')

class ReservaAdmin(admin.ModelAdmin):
    search_fields = ('id','Fecha_Reserva_Inicio','Estado_Reserva')
    list_display = ('id','Fecha_Reserva_Inicio','Fecha_Reserva_Termino', 'Estado_Reserva','user','departamento')

class DepartamentoAdmin( admin.ModelAdmin):
    search_fields = ('Nombre_Departamento','Valor_Diario','Disponible')
    list_display = ('Nombre_Departamento','Numero_propiedad','Descripcion_departamento', 'Valor_Diario','Disponible','Direccion_departamento')

class ContactoAdmin( admin.ModelAdmin):
    search_fields = ('asunto','descripcioncontacto','correoaenviar')
    list_display = ('asunto','descripcioncontacto','correoaenviar')

class VehiculoAdmin( admin.ModelAdmin):
    search_fields = ('patente','disponibilidad_vehi','modelo')
    list_display = ('patente','disponibilidad_vehi','modelo')

admin.site.register(User, UserAdmin)
admin.site.register(Acompañante)
admin.site.register(Inventario)
admin.site.register(Ciudad)
admin.site.register(Comuna)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Conductor)
admin.site.register(Vehiculo)
admin.site.register(ServicioExtra)
admin.site.register(Tour)
admin.site.register(Reserva, ReservaAdmin)
admin.site.register(Contact, ContactoAdmin)
admin.site.register(Reservando)
admin.site.register(ReservaDetalle)
admin.site.register(Venta)