def astrology_json_schema():
    # Stable schema for Flutter UI (ChatGPT will follow strictly)
    return {
        "name": "astro_response",
        "schema": {
            "type": "object",
            "properties": {
                "meta": {
                    "type": "object",
                    "properties": {
                        "language": {"type": "string"},
                        "disclaimer": {"type": "string"},
                        "inputs_summary": {"type": "object"},
                    },
                    "required": ["language", "disclaimer", "inputs_summary"],
                    "additionalProperties": True,
                },
                "predictions": {
                    "type": "object",
                    "properties": {
                        "today": {"type": "object"},
                        "week": {"type": "object"},
                        "month": {"type": "object"},
                        "year": {"type": "object"},
                    },
                    "required": ["today", "week", "month", "year"],
                    "additionalProperties": True,
                },
                "remedies": {
                    "type": "object",
                    "properties": {
                        "if_something_wrong": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "mitigation_steps": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "do_and_dont": {
                            "type": "object",
                            "properties": {
                                "do": {"type": "array", "items": {"type": "string"}},
                                "dont": {"type": "array", "items": {"type": "string"}},
                            },
                            "required": ["do", "dont"],
                            "additionalProperties": False,
                        },
                    },
                    "required": ["if_something_wrong", "mitigation_steps", "do_and_dont"],
                    "additionalProperties": True,
                },
                "lucky": {
                    "type": "object",
                    "properties": {
                        "color": {"type": "string"},
                        "number": {"type": "string"},
                        "day": {"type": "string"},
                    },
                    "required": ["color", "number", "day"],
                    "additionalProperties": False,
                },
            },
            "required": ["meta", "predictions", "remedies", "lucky"],
            "additionalProperties": False,
        },
    }