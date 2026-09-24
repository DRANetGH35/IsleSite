from flask import Blueprint, jsonify
from flask_login import login_required, current_user

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/health")
def health():
    return jsonify({"ok": True})

@api_bp.route("/carnivores")
def carnivores():
    return jsonify({"name": "Allosaurus"})