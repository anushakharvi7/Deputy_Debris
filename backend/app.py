from flask import Flask
from flask_cors import CORS
from routes.api import api

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Register API
    app.register_blueprint(api, url_prefix="/api")

    # Home route
    @app.route("/")
    def home():
        return "Debris Deputy Backend Running 🚀"

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)