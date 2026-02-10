from flask import Blueprint, request, jsonify, current_app
from ai_models.utils.validate_payload import validate_payload
from ai_models.services.astrology_service import get_astrology_prediction
import os

astrology_bp = Blueprint("astrology", __name__, url_prefix='/third-party-service/astrology')


@astrology_bp.post("/predict")
def predict():
    payload = request.get_json(silent=True) or {}

    ok, msg = validate_payload(payload)
    if not ok:
        return jsonify({"error": msg}), 400

    result = get_astrology_prediction(
        payload=payload,
        default_language=os.environ.get("DEFAULT_LANGUAGE", "en"),
    )
    return jsonify(result)
