from flask import Flask
from config import Config
from database.db import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    init_db(app)

    from routes.main import main_bp
    from routes.cafes import cafes_bp
    from routes.ai import ai_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(cafes_bp)
    app.register_blueprint(ai_bp)

    return app

app = create_app()

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)