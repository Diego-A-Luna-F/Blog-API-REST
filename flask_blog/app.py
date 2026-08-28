from flask import Flask, jsonify
from routes.posts import posts_bp

app = Flask(__name__)

# Registrar Blueprint
# url_prefix aplica la ruta base "/api/posts" a TODAS las rutas dentro de posts_bp
app.register_blueprint(posts_bp, url_prefix="/api/posts")


@app.route("/")
def home():
    return jsonify({"message": "¡API del Blog funcionando con Blueprints!"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
