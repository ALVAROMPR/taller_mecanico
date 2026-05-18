from .extensions import appbuilder, db
from flask_appbuilder import ModelView, BaseView, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface

from .models import (
    Cliente,
    Vehiculo,
    Servicio,
    OrdenTrabajo,
    DetalleServicio
)


# ==========================
# CLIENTES
# ==========================
class ClienteModelView(ModelView):
    datamodel = SQLAInterface(Cliente)

    label_columns = {
        "nombre": "Nombre",
        "apellido": "Apellido",
        "telefono": "Teléfono",
        "direccion": "Dirección",
        "creado_en": "Creado en"
    }

    list_columns = [
        "nombre",
        "apellido",
        "telefono"
    ]

    add_columns = [
        "nombre",
        "apellido",
        "telefono",
        "direccion"
    ]

    edit_columns = add_columns

    show_columns = [
        "nombre",
        "apellido",
        "telefono",
        "direccion",
        "creado_en",
        "actualizado_en"
    ]


# ==========================
# VEHICULOS
# ==========================
class VehiculoModelView(ModelView):
    datamodel = SQLAInterface(Vehiculo)

    label_columns = {
        "placa": "Placa",
        "marca": "Marca",
        "modelo": "Modelo",
        "color": "Color",
        "cliente": "Cliente"
    }

    list_columns = [
        "placa",
        "marca",
        "modelo",
        "cliente"
    ]

    add_columns = [
        "placa",
        "marca",
        "modelo",
        "color",
        "cliente"
    ]

    edit_columns = add_columns

    show_columns = [
        "placa",
        "marca",
        "modelo",
        "color",
        "cliente",
        "creado_en"
    ]


# ==========================
# SERVICIOS
# ==========================
class ServicioModelView(ModelView):
    datamodel = SQLAInterface(Servicio)

    label_columns = {
        "nombre": "Servicio",
        "descripcion": "Descripción",
        "precio": "Precio",
        "estado": "Estado"
    }

    list_columns = [
        "nombre",
        "precio",
        "estado"
    ]

    add_columns = [
        "nombre",
        "descripcion",
        "precio",
        "estado"
    ]

    edit_columns = add_columns

    show_columns = [
        "nombre",
        "descripcion",
        "precio",
        "estado",
        "creado_en"
    ]


# ==========================
# ORDENES DE TRABAJO
# ==========================
class OrdenTrabajoModelView(ModelView):
    datamodel = SQLAInterface(OrdenTrabajo)

    label_columns = {
        "vehiculo": "Vehículo",
        "fecha_ingreso": "Fecha ingreso",
        "estado": "Estado",
        "total": "Total",
        "observacion": "Observación"
    }

    list_columns = [
        "vehiculo",
        "fecha_ingreso",
        "estado",
        "total"
    ]

    add_columns = [
        "vehiculo",
        "estado",
        "total",
        "observacion"
    ]

    edit_columns = add_columns

    show_columns = [
        "vehiculo",
        "fecha_ingreso",
        "estado",
        "total",
        "observacion"
    ]


# ==========================
# DETALLE SERVICIOS
# ==========================
class DetalleServicioModelView(ModelView):
    datamodel = SQLAInterface(DetalleServicio)

    label_columns = {
        "orden": "Orden",
        "servicio": "Servicio",
        "cantidad": "Cantidad",
        "subtotal": "Subtotal"
    }

    list_columns = [
        "orden",
        "servicio",
        "cantidad",
        "subtotal"
    ]

    add_columns = [
        "orden",
        "servicio",
        "cantidad",
        "subtotal"
    ]

    edit_columns = add_columns


# ==========================
# MENUS
# ==========================

appbuilder.add_view(
    ClienteModelView,
    "Clientes",
    icon="fa-user",
    category="Gestión"
)

appbuilder.add_view(
    VehiculoModelView,
    "Vehículos",
    icon="fa-car",
    category="Gestión"
)

appbuilder.add_view(
    ServicioModelView,
    "Servicios",
    icon="fa-wrench",
    category="Gestión"
)

appbuilder.add_view(
    OrdenTrabajoModelView,
    "Órdenes",
    icon="fa-file-text",
    category="Operaciones"
)

appbuilder.add_view(
    DetalleServicioModelView,
    "Detalle Servicios",
    icon="fa-list",
    category="Operaciones"
)