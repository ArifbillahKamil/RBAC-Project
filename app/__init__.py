import os
from flask import Flask
from .models import db
from flask_login import LoginManager
from flask_migrate import Migrate

def create_app():
    # Dapatkan path absolut ke folder "templates" dan "static"
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    template_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')

    # Buat app dengan lokasi template dan static yang benar
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate = Migrate(app, db)  

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
