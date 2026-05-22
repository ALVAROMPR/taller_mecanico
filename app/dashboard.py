from flask_appbuilder import BaseView, expose
from sqlalchemy import func

from .extensions import db
from .models import (
    Cliente,
    Vehiculo,
    Servicio,
    OrdenTrabajo,
    DetalleServicio,
)


class DashboardView(BaseView):
    route_base   = "/dashboard"
    default_view = "index"

    @expose("/")
    def index(self):

        # ──────────────────────────────────────
        # KPIs principales
        # ──────────────────────────────────────
        total_clientes  = db.session.query(Cliente).count()
        total_vehiculos = db.session.query(Vehiculo).count()
        total_ordenes   = db.session.query(OrdenTrabajo).count()

        # CORRECCIÓN: la variable ahora se llama ingresos_totales
        # para que coincida con el template
        ingresos_totales = float(
            db.session.query(func.sum(OrdenTrabajo.total)).scalar() or 0
        )

        # KPIs por estado
        ordenes_pendientes  = db.session.query(OrdenTrabajo).filter_by(
            estado="Pendiente").count()
        ordenes_en_proceso  = db.session.query(OrdenTrabajo).filter_by(
            estado="En Proceso").count()
        ordenes_finalizadas = db.session.query(OrdenTrabajo).filter_by(
            estado="Finalizado").count()
        ordenes_entregadas  = db.session.query(OrdenTrabajo).filter_by(
            estado="Entregado").count()

        servicios_activos = db.session.query(Servicio).filter_by(
            estado=True).count()

        # ──────────────────────────────────────
        # Gráfica 1 — Ingresos por orden (eje X = ID de orden)
        # CORRECCIÓN: variable renombrada a "valores" para
        # coincidir con dashboard.html
        # ──────────────────────────────────────
        ordenes_chart = (
            db.session.query(OrdenTrabajo.id, OrdenTrabajo.total)
            .filter(OrdenTrabajo.total > 0)
            .order_by(OrdenTrabajo.id.asc())
            .limit(20)
            .all()
        )
        labels_ingresos = [f"OT-{o.id}" for o in ordenes_chart]
        valores_ingresos = [float(o.total or 0) for o in ordenes_chart]

        # ──────────────────────────────────────
        # Gráfica 2 — Servicios más solicitados
        # ──────────────────────────────────────
        servicios_populares = (
            db.session.query(
                Servicio.nombre,
                func.sum(DetalleServicio.cantidad).label("total_uso")
            )
            .join(DetalleServicio, DetalleServicio.servicio_id == Servicio.id)
            .group_by(Servicio.id, Servicio.nombre)
            .order_by(func.sum(DetalleServicio.cantidad).desc())
            .limit(8)
            .all()
        )
        labels_servicios  = [s.nombre    for s in servicios_populares]
        valores_servicios = [int(s.total_uso) for s in servicios_populares]

        # ──────────────────────────────────────
        # Gráfica 3 — Órdenes por estado (dona)
        # ──────────────────────────────────────
        estados_labels = ["Pendiente", "En Proceso", "Finalizado", "Entregado"]
        estados_valores = [
            ordenes_pendientes,
            ordenes_en_proceso,
            ordenes_finalizadas,
            ordenes_entregadas,
        ]

        # ──────────────────────────────────────
        # Últimas 5 órdenes
        # ──────────────────────────────────────
        ordenes_recientes = (
            db.session.query(OrdenTrabajo)
            .order_by(OrdenTrabajo.id.desc())
            .limit(5)
            .all()
        )

        return self.render_template(
            "dashboard.html",
            # KPIs
            total_clientes=total_clientes,
            total_vehiculos=total_vehiculos,
            total_ordenes=total_ordenes,
            ingresos_totales=ingresos_totales,
            ordenes_pendientes=ordenes_pendientes,
            ordenes_en_proceso=ordenes_en_proceso,
            ordenes_finalizadas=ordenes_finalizadas,
            ordenes_entregadas=ordenes_entregadas,
            servicios_activos=servicios_activos,
            # Gráfica ingresos
            labels=labels_ingresos,
            valores=valores_ingresos,
            # Gráfica servicios
            labels_servicios=labels_servicios,
            valores_servicios=valores_servicios,
            # Gráfica estados
            estados_labels=estados_labels,
            estados_valores=estados_valores,
            # Tabla reciente
            ordenes=ordenes_recientes,
        )