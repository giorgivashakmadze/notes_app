from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

db = SQLAlchemy()
DATAB = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "QWERTY"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATAB}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .models import User, Note

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app


def create_database(app):
    with app.app_context():
        if not inspect(db.engine).has_table("note"):
            db.create_all()
            print('Database created')
