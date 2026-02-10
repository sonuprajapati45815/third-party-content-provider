from datetime import datetime, timezone
from ai_models.clients.llm_clients import call_chatgpt_astrology, call_gemini_astrology

def merge_results(chatgpt_json: dict, gemini_json: dict) -> dict:
    out = dict(chatgpt_json)
    out["sources"] = {
        "chatgpt": {"ok": True},
        "gemini": {"ok": "_error" not in gemini_json, "data": gemini_json},
    }
    return out

def get_astrology_prediction(payload: dict, default_language: str) -> dict:
    language = payload.get("language") or default_language

    # Add a small server-side summary (useful for debugging/UI)
    payload = dict(payload)
    payload["_request_time"] = datetime.now(timezone.utc).isoformat()

    chatgpt_data = call_chatgpt_astrology(payload, language)
    gemini_data = call_gemini_astrology(payload, language)

    return merge_results(chatgpt_data, gemini_data)