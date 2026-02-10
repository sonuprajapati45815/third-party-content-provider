import json

REQUIRED_FIELDS = ["dob", "tob", "birth_place"]

def validate_payload(payload: dict) -> tuple[bool, str]:
    missing = [f for f in REQUIRED_FIELDS if not payload.get(f)]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
    return True, ""

def try_parse_json(text: str) -> dict | None:
    text = (text or "").strip()
    try:
        return json.loads(text)
    except Exception:
        return None