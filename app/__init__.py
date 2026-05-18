from flask import Flask
from .extensions import appbuilder, db


def create_app():
    app = Flask(__name__)

    app.config.from_object("config")

    db.init_app(app)

    with app.app_context():
        appbuilder.init_app(app, db.session)

        from . import views
        from . import models

        db.create_all()

    return app


app = create_app()