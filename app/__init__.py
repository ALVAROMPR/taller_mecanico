from flask import Flask
from .extensions import appbuilder, db, migrate
from flask_appbuilder import AppBuilder


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("config")

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)          # Flask-Migrate

    with app.app_context():

        # Importar modelos — necesario para que SQLAlchemy los registre
        from .models import (           # noqa: F401
            Cliente,
            Vehiculo,
            Servicio,
            OrdenTrabajo,
            DetalleServicio,
        )

        db.create_all()

        #appbuilder.init_app(app, db.session, base_template='appbuilder/mybase.html')
        appbuilder.init_app(app, db.session)

        # Registrar vistas (incluye add_view al menú)
        from . import views             # noqa: F401

        # Registrar dashboard
        from .dashboard import DashboardView
        appbuilder.add_view(
            DashboardView,
            "Dashboard",
            icon="fa-tachometer",
            category="Inicio",
            category_icon="fa-home",
        )

    return app


app = create_app()