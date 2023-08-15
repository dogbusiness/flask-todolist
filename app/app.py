from config import settings
from database import db
from flask import Flask
from flask_bootstrap import Bootstrap
from views import bp

app = Flask(__name__)
app.config["SECRET_KEY"] = settings.app_secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = settings.database_uri
Bootstrap(app)  # ???

db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(bp)
