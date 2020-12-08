import random
import string
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO
from django.http import HttpResponse#
from .models import ReservaDetalle, Reservando, Venta, Departamento
from django.utils import timezone
from django.db.models import Prefetch, F, FloatField, ExpressionWrapper


def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def render_to_pdf(template_src, context_dic={}):
    template = get_template(template_src)
    html = template.render(context_dic)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')

    return None

def procesar_venta(self, **params_venta):
    # recupera la lista de productos en carrtio
    productos_en_car = Reservando.objects.all()
    if productos_en_car.count() > 0:
        
        # crea el objeto venta
        venta = Venta.objects.create(
            date_sale=timezone.now(),
            count=0,
            amount=0,
            type_invoce=params_venta['type_invoce'],
            type_payment=params_venta['type_payment'],
            user=params_venta['user'],
        )
        #
        ventas_detalle = []
        productos_en_venta = []
        for producto_car in productos_en_car:
            venta_detalle = ReservaDetalle(
                departamento=producto_car.departamento,
                venta=venta,
                count=producto_car.count,
                price_purchase=producto_car.departamento.precio_compra,
                price_sale=producto_car.departamento.Valor_Diario,
                tax=0.18,
            )
            # actualizmos stock de producto en iteracion
            departamento = producto_car.departamento
            departamento.habitaciones = departamento.habitaciones - producto_car.count
            departamento.numero_venta = departamento.numero_venta + producto_car.count
            #
            ventas_detalle.append(venta_detalle)
            productos_en_venta.append(departamento)
            #
            venta.count = venta.count + producto_car.count
            venta.amount = venta.amount + producto_car.count*producto_car.departamento.Valor_Diario

        venta.save()
        ReservaDetalle.objects.bulk_create(ventas_detalle)
        # actualizamos el stok
        Departamento.objects.bulk_update(productos_en_venta, ['habitaciones', 'Valor_Diario'])
        # completada la venta, eliminamos productos delc arrito
        productos_en_car.delete()
        return venta
    else:
        return None

def detalle_ventas_no_cerradas():
    # recuepramos arry de id de ventas no cerradas
    ventas = Venta.objects.ventas_no_cerradas()
    consulta = ventas.prefetch_related(
        Prefetch(
            'detail_sale', 
            queryset=ReservaDetalle.objects.filter(venta__id__in=ventas).annotate(
                subtotal=ExpressionWrapper(
                    F('price_sale')*F('count'),
                    output_field=FloatField()
                )
            )
        )
    )

    return consulta
