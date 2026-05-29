from flask import Flask
from config import Config
from database.db import init_db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database
    init_db(app)

    # Register blueprints
    from routes.main import main_bp
    from routes.cafes import cafes_bp
    from routes.ai import ai_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(cafes_bp)
    app.register_blueprint(ai_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
