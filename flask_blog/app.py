import os
from flask import Flask, jsonify
from routes.posts import posts_bp
from database import db
from models.post import Post

app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(base_dir, "blog.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Registrar Blueprint
# url_prefix aplica la ruta base "/api/posts" a TODAS las rutas dentro de posts_bp
app.register_blueprint(posts_bp, url_prefix="/api/posts")

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return jsonify({"message": "¡API con SQLite y SQLAlchemy funcionando!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
