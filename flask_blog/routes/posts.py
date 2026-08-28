# routes/posts.py
from flask import Blueprint, jsonify, request

# 1. Definimos el Blueprint
# "posts_bp" es el nombre interno del blueprint
posts_bp = Blueprint("posts_bp", __name__)

# Base de datos temporal
posts = [
    {
        "id": 1,
        "title": "Mi primer post en Flask",
        "content": "¡Hola a todos! Este es el inicio de mi blog creado con Python y Flask.",
        "author": "Dev"
    },
    {
        "id": 2,
        "title": "Por qué usar GitHub Codespaces",
        "content": "Codespaces nos permite programar en la nube sin preocuparnos por instalar nada localmente.",
        "author": "Dev"
    }
]

# Variable incremental de id
current_id = 3


# Obtener todos los posts
@posts_bp.route("", methods=["GET"])
def get_posts():
    return jsonify(posts), 200

#Obtener post por id
@posts_bp.route("/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = next((p for p in posts if p["id"] == post_id), None)
    if post is None:
        return jsonify({"error": "Artículo no encontrado"}), 404
    return jsonify(post), 200

# Crear post
@posts_bp.route("", methods=["POST"])
def create_post():
    global current_id
    data = request.get_json()

    if not data or "title" not in data or "content" not in data:
        return jsonify({"error": "Faltan campos obligatorios ('title' y 'content')"}), 400

    new_post = {
        "id": current_id,
        "title": data["title"],
        "content": data["content"],
        "author": data.get("author", "Anónimo")
    }

    posts.append(new_post)
    current_id += 1
    return jsonify(new_post), 201

# Actualizar post
@posts_bp.route("/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    post = next((p for p in posts if p["id"] == post_id), None)
    if post is None:
        return jsonify({"error": "Artículo no encontrado"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Se requieren datos en formato JSON"}), 400

    post["title"] = data.get("title", post["title"])
    post["content"] = data.get("content", post["content"])
    post["author"] = data.get("author", post["author"])

    return jsonify(post), 200

# Eliminar post
@posts_bp.route("/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    global posts
    post = next((p for p in posts if p["id"] == post_id), None)

    if post is None:
        return jsonify({"error": "Artículo no encontrado"}), 404

    posts = [p for p in posts if p["id"] != post_id]
    return jsonify({"message": f"Artículo con ID {post_id} eliminado exitosamente"}), 200