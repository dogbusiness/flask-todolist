from core.config import settings
from core.database import db
from domain.views import bp
from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config["SECRET_KEY"] = settings.app_secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = settings.database_uri

Bootstrap(app)

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(bp)
