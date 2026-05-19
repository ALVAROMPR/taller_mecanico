from flask import Flask

from .extensions import appbuilder, db


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("config")

    db.init_app(app)

    with app.app_context():

        # Importar modelos explícitamente
        from .models import (
            Cliente,
            Vehiculo,
            Servicio,
            OrdenTrabajo,
            DetalleServicio
        )

        db.create_all()

        appbuilder.init_app(app, db.session)

        # Registrar vistas
        from . import views
        from . import dashboard
        from .dashboard import DashboardView

        #appbuilder.add_view_no_menu(DashboardView())
        appbuilder.add_view(
        DashboardView,
        "Dashboard",
        icon="fa-dashboard",
        category="Inicio"
        )

    return app


app = create_app()