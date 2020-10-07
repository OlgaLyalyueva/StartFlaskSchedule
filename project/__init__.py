from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.debug = True

    app.config['SECRET_KEY'] = b'\xcb6\x836\xf6\xdd\xadl\x0fB\xb8\x14\xaa\xd3\r>'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://olga:7d7a4339@172.20.0.2:25432/flask'

    db.init_app(app)
    migrate.init_app(app, db)


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.filter_by(email=user).first()

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    # app.root_path()

    return app
