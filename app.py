from flask import Flask
from models.models import db

def create_app():
    app = Flask(__name__)

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
