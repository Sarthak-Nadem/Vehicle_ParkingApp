from flask import Flask
from models.models import db
from controllers.admin_controller import admin_bp



def create_app():
    app = Flask(__name__)

    app.register_blueprint(admin_bp)

    from controllers.auth_controller import auth_bp, login_manager
    from flask_login import LoginManager

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    app.register_blueprint(auth_bp)

    # --- Configs ---
    app.config['SECRET_KEY'] = 'supersecretkey'  # Change for production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # --- Blueprints or Routes will go here later ---

    return app


if __name__ == '__main__':
    app = create_app()
    app.app_context().push()
    app.run(debug=True)
