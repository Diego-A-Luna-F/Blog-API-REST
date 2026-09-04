from flask import Blueprint, jsonify, request
from database import db
from models.post import Post

# Definimos el Blueprint
# "posts_bp" es el nombre interno del blueprint
posts_bp = Blueprint("posts_bp", __name__)

# Obtener todos los posts
@posts_bp.route("", methods=["GET"])
def get_posts():
    # Consulta SQL: SELECT * FROM posts;
    all_posts = Post.query.all()
    return jsonify([post.to_dict() for post in all_posts]), 200

#Obtener post por id
@posts_bp.route("/<int:post_id>", methods=["GET"])
def get_post(post_id):
    # Consulta SQL: SELECT * FROM posts WHERE id = post_id;
    post = Post.query.get(post_id)
    if post is None:
        return jsonify({"error": "Artículo no encontrado"}), 404
    return jsonify(post.to_dict()), 200

# Crear post
@posts_bp.route("", methods=["POST"])
def create_post():
    data = request.get_json()

    if not data or "title" not in data or "content" not in data:
        return jsonify({"error": "Faltan campos obligatorios ('title' y 'content')"}), 400

    new_post = Post(
        title=data["title"],
        content=data["content"],
        author=data.get("author", "Anónimo")
    )

    # Guardamos en la base de datos
    db.session.add(new_post)
    db.session.commit()

    return jsonify(new_post.to_dict()), 201

# Actualizar post
@posts_bp.route("/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    post = Post.query.get(post_id)
    if post is None:
        return jsonify({"error": "Artículo no encontrado"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Se requieren datos en formato JSON"}), 400

    post.title = data.get("title", post.title)
    post.content = data.get("content", post.content)
    post.author = data.get("author", post.author)

    db.session.commit()

    return jsonify(post.to_dict()), 200

# Eliminar post
@posts_bp.route("/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = Post.query.get(post_id)

    if post is None:
        return jsonify({"error": "Artículo no encontrado"}), 404

    db.session.delete(post)
    db.session.commit()

    return jsonify({"message": f"Artículo con ID {post_id} eliminado exitosamente"}), 200