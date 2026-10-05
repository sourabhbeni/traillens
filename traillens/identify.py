"""Local inference: photo -> strict JSON plant identification. No cloud calls."""

import json

from .config import MODEL, OLLAMA_HOST
from .prompts import SYSTEM_PROMPT, USER_PROMPT

SCHEMA = {
    "common_name": str,
    "scientific_name": str,
    "confidence": (int, float),
    "identifying_features": list,
    "habitat_note": str,
    "safety_note": str,
}


def extract_json(text: str) -> dict:
    """Pull the first {...} object out of model output (tolerates chatter)."""
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("model output contained no JSON object")
    return json.loads(text[start : end + 1])


def validate(data: dict) -> dict:
    """Enforce the schema; never let invented fields or bad types through."""
    if not isinstance(data, dict):
        raise ValueError("model output was not a JSON object")
    for key, types in SCHEMA.items():
        if key not in data or not isinstance(data[key], types):
            raise ValueError(f"missing or invalid key: {key}")
    data["confidence"] = max(0.0, min(1.0, float(data["confidence"])))
    data["identifying_features"] = [str(f) for f in data["identifying_features"]][:6]
    return data


def identify(image_bytes: bytes, model: str = MODEL) -> dict:
    """Identify the plant in a photo using the local Ollama model."""
    import ollama  # lazy: keeps import side-effect free if proxy env is odd

    client = ollama.Client(host=OLLAMA_HOST)
    resp = client.chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT, "images": [image_bytes]},
        ],
        options={"temperature": 0.2},
    )
    return validate(extract_json(resp["message"]["content"]))
