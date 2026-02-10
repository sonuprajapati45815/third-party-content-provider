import json
from ai_models.extensions import openai_client, gemini_model
from ai_models.schema.astrology_json_schema import astrology_json_schema
from ai_models.prompts.astrologer_prompt import build_astrology_prompt

def call_chatgpt_astrology(user: dict, language: str) -> dict:
    if openai_client is None:
        raise RuntimeError("OpenAI client not initialized")

    schema = astrology_json_schema()
    prompt = build_astrology_prompt(user, language)

    resp = openai_client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": "You output ONLY valid JSON that matches the schema."},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_schema", "json_schema": schema},
    )
    return json.loads(resp.output_text)

def call_gemini_astrology(user: dict, language: str) -> dict:
    if gemini_model is None:
        raise RuntimeError("Gemini model not initialized")

    prompt = build_astrology_prompt(user, language)
    prompt_response = prompt + f' {prompt} \n Here is response format in markdown json content must return. \n {astrology_json_schema()}'.strip()

    r = gemini_model.generate_content(
        prompt_response,
        generation_config={"temperature": 0.7,
                           "response_mime_type": "application/json"},
    )

    text = (r.text or "").strip()
    try:
        return json.loads(text)
    except Exception:
        return {"_error": "Gemini did not return valid JSON", "_gemini_raw": text}