from flask_appbuilder import BaseView, expose
from sqlalchemy import func

from .extensions import db
from .models import (
    Cliente,
    Vehiculo,
    OrdenTrabajo
)


class DashboardView(BaseView):
    route_base = "/dashboard"
    default_view = "index"

    @expose("/")
    def index(self):

        # KPIs
        total_clientes = db.session.query(Cliente).count()

        total_vehiculos = db.session.query(Vehiculo).count()

        total_ordenes = db.session.query(
            OrdenTrabajo
        ).count()

        ingresos = db.session.query(
            func.sum(OrdenTrabajo.total)
        ).scalar() or 0

        # Últimas órdenes
        ordenes = (
            db.session.query(OrdenTrabajo)
            .order_by(OrdenTrabajo.id.desc())
            .limit(5)
            .all()
        )

        # Datos reales para gráfica
        ordenes_chart = (
            db.session.query(
                OrdenTrabajo.id,
                OrdenTrabajo.total
            )
            .filter(OrdenTrabajo.total != None)
            .order_by(OrdenTrabajo.id.asc())
            .all()
        )

        labels = [
            f"OT-{o.id}"
            for o in ordenes_chart
        ]

        data = [
            float(o.total or 0)
            for o in ordenes_chart
        ]

        return self.render_template(
            "dashboard.html",
            total_clientes=total_clientes,
            total_vehiculos=total_vehiculos,
            total_ordenes=total_ordenes,
            ingresos=ingresos,
            ordenes=ordenes,
            labels=labels,
            data=data
        )