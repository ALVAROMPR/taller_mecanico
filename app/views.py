from datetime import datetime, time

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from wtforms import DateField
from wtforms.validators import Optional

from .extensions import appbuilder
from .models import (
    Cliente,
    Vehiculo,
    Servicio,
    OrdenTrabajo,
    DetalleServicio,
)


# ══════════════════════════════════════════════
# CLIENTE
# ══════════════════════════════════════════════
class ClienteView(ModelView):
    datamodel = SQLAInterface(Cliente)

    label_title = "Clientes"

    list_title   = "Listado de Clientes"
    add_title    = "Registrar Cliente"
    edit_title   = "Editar Cliente"
    show_title   = "Detalle del Cliente"

    list_columns = ["nombre", "apellido", "telefono", "direccion"]
    add_columns  = ["nombre", "apellido", "telefono", "direccion"]
    edit_columns = add_columns
    show_columns = ["nombre", "apellido", "telefono", "direccion",
                    "creado_en", "actualizado_en"]

    search_columns = ["nombre", "apellido", "telefono"]
    base_order     = ("apellido", "asc")

    # Etiquetas en español
    label_columns = {
        "nombre":         "Nombre",
        "apellido":       "Apellido",
        "telefono":       "Teléfono",
        "direccion":      "Dirección",
        "creado_en":      "Registrado el",
        "actualizado_en": "Última actualización",
    }


# ══════════════════════════════════════════════
# VEHICULO
# ══════════════════════════════════════════════
class VehiculoView(ModelView):
    datamodel = SQLAInterface(Vehiculo)

    label_title = "Vehículos"

    list_title  = "Listado de Vehículos"
    add_title   = "Registrar Vehículo"
    edit_title  = "Editar Vehículo"
    show_title  = "Detalle del Vehículo"

    list_columns = ["placa", "marca", "modelo", "anio", "color", "cliente"]
    add_columns  = ["cliente", "placa", "marca", "modelo", "anio", "color"]
    edit_columns = add_columns
    show_columns = ["placa", "marca", "modelo", "anio", "color",
                    "cliente", "creado_en"]

    search_columns = ["placa", "marca", "modelo"]
    base_order     = ("marca", "asc")

    label_columns = {
        "placa":          "Placa",
        "marca":          "Marca",
        "modelo":         "Modelo",
        "anio":           "Año",
        "color":          "Color",
        "cliente":        "Propietario",
        "creado_en":      "Registrado el",
    }


# ══════════════════════════════════════════════
# SERVICIO
# ══════════════════════════════════════════════
class ServicioView(ModelView):
    datamodel = SQLAInterface(Servicio)

    label_title = "Servicios"

    list_title  = "Catálogo de Servicios"
    add_title   = "Nuevo Servicio"
    edit_title  = "Editar Servicio"
    show_title  = "Detalle del Servicio"

    list_columns = ["nombre", "precio", "estado"]
    add_columns  = ["nombre", "descripcion", "precio", "estado"]
    edit_columns = add_columns
    show_columns = add_columns

    search_columns = ["nombre"]
    base_order     = ("nombre", "asc")

    label_columns = {
        "nombre":      "Nombre del Servicio",
        "descripcion": "Descripción",
        "precio":      "Precio (Bs)",
        "estado":      "Activo",
    }


# ══════════════════════════════════════════════
# ORDEN DE TRABAJO
# ══════════════════════════════════════════════
class OrdenTrabajoView(ModelView):
    datamodel = SQLAInterface(OrdenTrabajo)

    label_title = "Órdenes de Trabajo"

    list_title  = "Listado de Órdenes"
    add_title   = "Nueva Orden de Trabajo"
    edit_title  = "Editar Orden"
    show_title  = "Detalle de la Orden"

    list_columns = ["id", "vehiculo", "fecha_ingreso",
                    "fecha_salida", "estado", "total"]

    # CORRECCIÓN: "total" removido de add/edit — se calcula automáticamente
    add_columns  = ["vehiculo", "estado", "fecha_salida", "observacion"]
    edit_columns = add_columns

    show_columns = ["vehiculo", "fecha_ingreso", "fecha_salida",
                    "estado", "total", "observacion", "detalles"]

    search_columns = ["estado"]
    base_order     = ("id", "desc")

    label_columns = {
        "id":             "N° Orden",
        "vehiculo":       "Vehículo",
        "fecha_ingreso":  "Ingreso",
        "fecha_salida":   "Salida",
        "estado":         "Estado",
        "total":          "Total (Bs)",
        "observacion":    "Observaciones",
        "detalles":       "Servicios",
    }

    base_filters = []

    # ── CORRECCIÓN fecha_salida ────────────────────────────────────
    # El modelo usa DateTime pero el widget nativo solo envía "YYYY-MM-DD".
    # Definimos un DateField de WTForms + widget de date de FAB,
    # y sobreescribimos pre_update / pre_add para convertir date → datetime
    # antes de que SQLAlchemy intente persistir el valor.

    _fecha_salida_field = DateField(
        "Fecha de Salida",
        validators=[Optional()],
    )

    add_form_extra_fields  = {"fecha_salida": _fecha_salida_field}
    edit_form_extra_fields = {"fecha_salida": _fecha_salida_field}

    def _convertir_fecha_salida(self, item):
        """Convierte date → datetime(date, 00:00:00) si el campo tiene valor."""
        val = item.fecha_salida
        if val is not None and not isinstance(val, datetime):
            item.fecha_salida = datetime.combine(val, time.min)

    def pre_add(self, item):
        self._convertir_fecha_salida(item)

    def pre_update(self, item):
        self._convertir_fecha_salida(item)
        # Auto fecha_salida: si el estado llega a Entregado y no hay fecha, poner hoy
        if item.estado == "Entregado" and item.fecha_salida is None:
            item.fecha_salida = datetime.now()


# ══════════════════════════════════════════════
# DETALLE SERVICIO
# ══════════════════════════════════════════════
class DetalleServicioView(ModelView):
    datamodel = SQLAInterface(DetalleServicio)

    label_title = "Detalle de Servicios"

    list_title  = "Detalles de Servicios"
    add_title   = "Agregar Servicio a Orden"
    edit_title  = "Editar Detalle"
    show_title  = "Detalle"

    list_columns = ["orden", "servicio", "cantidad",
                    "precio_unitario", "subtotal"]

    # CORRECCIÓN: "subtotal" removido — se calcula automáticamente
    # precio_unitario se mantiene para permitir precios personalizados por orden
    add_columns  = ["orden", "servicio", "cantidad", "precio_unitario"]
    edit_columns = add_columns

    show_columns = ["orden", "servicio", "cantidad",
                    "precio_unitario", "subtotal"]

    search_columns = ["orden", "servicio"]
    base_order     = ("id", "desc")

    label_columns = {
        "orden":            "Orden de Trabajo",
        "servicio":         "Servicio",
        "cantidad":         "Cantidad",
        "precio_unitario":  "Precio Unitario (Bs)",
        "subtotal":         "Subtotal (Bs)",
    }

    def _recalcular_orden(self, item):
        """
        Recarga los detalles de la orden desde la DB y actualiza total.
        Se llama desde post_add / post_update / post_delete, cuando
        FAB ya hizo commit y la sesión está limpia.
        """
        from .extensions import db
        orden = db.session.get(OrdenTrabajo, item.orden_id)
        if orden:
            orden.recalcular_total()
            db.session.commit()

    def post_add(self, item):
        self._recalcular_orden(item)

    def post_update(self, item):
        self._recalcular_orden(item)

    def post_delete(self, item):
        self._recalcular_orden(item)


# ══════════════════════════════════════════════
# REGISTRO DE VISTAS EN EL MENÚ
# ══════════════════════════════════════════════
appbuilder.add_view(
    ClienteView,
    "Clientes",
    icon="fa-user",
    category="Gestión Taller",
    category_icon="fa-cogs",
)

appbuilder.add_view(
    VehiculoView,
    "Vehículos",
    icon="fa-car",
    category="Gestión Taller",
)

appbuilder.add_view(
    ServicioView,
    "Servicios",
    icon="fa-wrench",
    category="Gestión Taller",
)

appbuilder.add_view(
    OrdenTrabajoView,
    "Órdenes de Trabajo",
    icon="fa-clipboard",
    category="Gestión Taller",
)

appbuilder.add_view(
    DetalleServicioView,
    "Detalle de Servicios",
    icon="fa-cogs",
    category="Gestión Taller",
)