from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

# IMPORTANTE
from .extensions import appbuilder
#from .dashboard import ReporteIngresosChart

from .models import (
    Cliente,
    Vehiculo,
    Servicio,
    OrdenTrabajo,
    DetalleServicio
)


# ==========================
# CLIENTE
# ==========================
class ClienteView(ModelView):
    datamodel = SQLAInterface(Cliente)

    list_columns = [
        "nombre",
        "apellido",
        "telefono",
        "direccion"
    ]

    add_columns = list_columns
    edit_columns = list_columns
    show_columns = list_columns


# ==========================
# VEHICULO
# ==========================
class VehiculoView(ModelView):
    datamodel = SQLAInterface(Vehiculo)

    list_columns = [
        "placa",
        "marca",
        "modelo",
        "color",
        "cliente"
    ]

    add_columns = [
        "cliente",
        "placa",
        "marca",
        "modelo",
        "color"
    ]

    edit_columns = add_columns
    show_columns = list_columns


# ==========================
# SERVICIO
# ==========================
class ServicioView(ModelView):
    datamodel = SQLAInterface(Servicio)

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
    show_columns = add_columns


# ==========================
# ORDEN DE TRABAJO
# ==========================
class OrdenTrabajoView(ModelView):
    datamodel = SQLAInterface(OrdenTrabajo)

    label_title = "Ordenes de Trabajo"

    list_columns = [
        "id",
        "vehiculo",
        "fecha_ingreso",
        "estado",
        "total"
    ]

    add_columns = [
        "vehiculo",
        "estado",
        "observacion",
        "total"
    ]

    edit_columns = add_columns

    show_columns = [
        "vehiculo",
        "fecha_ingreso",
        "estado",
        "total",
        "observacion"
    ]

    search_columns = ["estado"]

    base_order = ("id", "desc")


# ==========================
# DETALLE SERVICIO
# ==========================
class DetalleServicioView(ModelView):
    datamodel = SQLAInterface(DetalleServicio)

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
    show_columns = list_columns


# ==========================
# REGISTRO DE VISTAS
# ==========================
appbuilder.add_view(
    ClienteView,
    "Clientes",
    icon="fa-user",
    category="Gestion Taller"
)

appbuilder.add_view(
    VehiculoView,
    "Vehiculos",
    icon="fa-car",
    category="Gestion Taller"
)

appbuilder.add_view(
    ServicioView,
    "Servicios",
    icon="fa-wrench",
    category="Gestion Taller"
)

appbuilder.add_view(
    OrdenTrabajoView,
    "Ordenes",
    icon="fa-clipboard",
    category="Gestion Taller"
)

appbuilder.add_view(
    DetalleServicioView,
    "Detalle Servicios",
    icon="fa-cogs",
    category="Gestion Taller"
)
