from flask import Flask, send_from_directory
from flask_cors import CORS
from backend.routes.api import api
import os

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(api, url_prefix="/api")

    @app.route("/")
    def home():
        return "Debris Deputy Backend Running 🚀"

    # 🔴 FIXED PATH
    @app.route('/assets/snapshots/<filename>')
    def serve_image(filename):
        return send_from_directory(
            os.path.abspath("assets/snapshots"),
            filename
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)