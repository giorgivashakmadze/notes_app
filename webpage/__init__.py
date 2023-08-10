from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from flask_login import LoginManager

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

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app


def create_database(app):
    with app.app_context():
        inspector = inspect(db.engine)
        if not inspector.has_table("note"):
            db.create_all()
            print('Database created')

