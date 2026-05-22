from flask_appbuilder import AppBuilder
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
 
# Instancias globales — se inicializan en create_app()
db          = SQLAlchemy()
migrate     = Migrate()
appbuilder  = AppBuilder()