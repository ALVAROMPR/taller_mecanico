import os
import pymysql
from flask_appbuilder.security.manager import (
    AUTH_REMOTE_USER,
    AUTH_DB,
    AUTH_LDAP,
    AUTH_OAUTH,
)

basedir = os.path.abspath(os.path.dirname(__file__))

# Your App secret key
SECRET_KEY = os.environ.get("SECRET_KEY", "taller_mecanico_secret_2026")

# The SQLAlchemy connection string.
#SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/taller_mecanico'
# SQLALCHEMY_DATABASE_URI = 'postgresql://root:password@localhost/myapp'

SQLALCHEMY_TRACK_MODIFICATIONS = False

# IA — OpenRouter / DeepSeek (Fase 2)
# ─────────────────────────────────────────────
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "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")
OPENROUTER_MODEL   = "deepseek/deepseek-chat-v3-0324"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Flask-WTF flag for CSRF
CSRF_ENABLED = True
WTF_CSRF_ENABLED = True

# ------------------------------
# GLOBALS FOR APP Builder
# ------------------------------
# Uncomment to setup Your App name
# APP_NAME = "My App Name"

# Uncomment to setup Setup an App icon
# APP_ICON = "static/img/logo.jpg"

# ----------------------------------------------------
# AUTHENTICATION CONFIG
# ----------------------------------------------------
# The authentication type
# AUTH_OID : Is for OpenID
# AUTH_DB : Is for database (username/password()
# AUTH_LDAP : Is for LDAP
# AUTH_REMOTE_USER : Is for using REMOTE_USER from web server
AUTH_TYPE = AUTH_DB
APP_NAME  = "Taller Mecánico"
APP_THEME = "flatly.css"

# Uncomment to setup Full admin role name
# AUTH_ROLE_ADMIN = 'Admin'

# Uncomment to setup Public role name, no authentication needed
# AUTH_ROLE_PUBLIC = 'Public'

# Will allow user self registration
# AUTH_USER_REGISTRATION = True

# The default user self registration role
# AUTH_USER_REGISTRATION_ROLE = "Public"

# When using LDAP Auth, setup the ldap server
# AUTH_LDAP_SERVER = "ldap://ldapserver.new"

# Uncomment to setup OpenID providers example for OpenID authentication
# OPENID_PROVIDERS = [
#    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
#    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
#    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
#    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]
# ---------------------------------------------------
# Babel config for translations
# ---------------------------------------------------
# Setup default language
BABEL_DEFAULT_LOCALE = "es"
# Your application default translation path
BABEL_DEFAULT_FOLDER = "translations"
# The allowed translation for you app
LANGUAGES = {
    "en": {"flag": "gb", "name": "English"},
#    "pt": {"flag": "pt", "name": "Portuguese"},
#    "pt_BR": {"flag": "br", "name": "Pt Brazil"},
    "es": {"flag": "es", "name": "Spanish"},
#    "de": {"flag": "de", "name": "German"},
#    "zh": {"flag": "cn", "name": "Chinese"},
#    "ru": {"flag": "ru", "name": "Russian"},
#    "pl": {"flag": "pl", "name": "Polish"},
}
# ---------------------------------------------------
# Image and file configuration
# ---------------------------------------------------
UPLOAD_FOLDER   = os.path.join(basedir, "app", "static", "uploads") + os.sep
IMG_UPLOAD_FOLDER = UPLOAD_FOLDER
IMG_UPLOAD_URL  = "/static/uploads/"

# The file upload folder, when using models with files
#    UPLOAD_FOLDER = basedir + "/app/static/uploads/"

# The image upload folder, when using models with images
#    IMG_UPLOAD_FOLDER = basedir + "/app/static/uploads/"

# The image upload url, when using models with images
#    IMG_UPLOAD_URL = "/static/uploads/"
# Setup image size default is (300, 200, True)
# IMG_SIZE = (300, 200, True)

# Theme configuration
# these are located on static/appbuilder/css/themes
# you can create your own and easily use them placing them on the same dir structure to override
# APP_THEME = "bootstrap-theme.css"  # default bootstrap
# APP_THEME = "cerulean.css"
# APP_THEME = "amelia.css"
# APP_THEME = "cosmo.css"
# APP_THEME = "cyborg.css"
# APP_THEME = "flatly.css"
# APP_THEME = "journal.css"
# APP_THEME = "readable.css"
# APP_THEME = "simplex.css"
# APP_THEME = "slate.css"
# APP_THEME = "spacelab.css"
# APP_THEME = "united.css"
# APP_THEME = "yeti.css"