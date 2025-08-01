from flask import Flask,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models.models import db, User, Admin


# Initialize LoginManager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    # Admin ID is prefixed with "admin_"
    if str(user_id).startswith("admin_"):
        return Admin.query.get(int(user_id.split("_")[1]))
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return redirect(url_for('auth.login'))

    # --- Configurations ---
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- Initialize Extensions ---
    db.init_app(app)
    login_manager.init_app(app)

    # --- Register Blueprints ---
    from controllers.auth_controller import auth_bp
    from controllers.admin_controller import admin_bp
    from controllers.user_controller import user_bp
    from controllers.api_controller import api_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

# --- Run the App ---
if __name__ == '__main__':
    app = create_app()
    app.app_context().push()
    app.run(debug=True)
