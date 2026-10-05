# 🌿 TrailLens

**Offline trail plant identifier — Hacktoberfest 2026 Week 1: *Touch Grass* entry.**

Point your phone at a plant on the trail. A local open-weight vision model
([Moondream2](https://github.com/vikhyat/moondream) via [Ollama](https://ollama.com))
identifies it and returns strict JSON: common name, scientific name, confidence,
identifying features, habitat note. **No cloud, no account, no signal needed** —
your photos never leave your device.

## Why open matters here

The whole point is the trailhead with zero bars. A cloud API can't help you there;
a 1.7B-parameter open-weight model running on your own hardware can. Open weights
also mean you can swap the model, inspect the prompt, and run the entire pipeline
for free, forever.

## Quick start

```bash
# 1. Install Ollama: https://ollama.com/download
ollama pull moondream2

# 2. Install and run TrailLens
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

Open `http://<your-machine>:8000` on your phone (same Wi-Fi), snap a plant, hit
**Identify this plant**. Check `/api/health` if anything looks off.

Want better accuracy on beefier hardware? `TRAILLENS_MODEL=qwen2.5vl:7b uvicorn app:app`

## How it works

```
phone camera → FastAPI (/api/identify) → Ollama (moondream2, temperature 0.2)
  → strict-JSON system prompt → schema validation → result card
```

The prompt forces a single JSON object (no markdown, no chatter), requires an
explicit `confidence` score, and forbids edibility/medicinal advice. Anything that
isn't valid JSON or fails schema validation is rejected, not guessed.

## Evaluate

Drop 5–10 trail photos in `eval/samples/` and run `python eval/eval.py`.
`--stub` exercises the JSON pipeline without a model.

## Safety

For education and curiosity only. **Never eat or use wild plants** based on an
app's guess — the model says when it's uncertain, but verify with an expert.

## License

MIT — the open weights (Moondream2) and open inference stack (Ollama) are what
make this possible; this code is MIT to keep that spirit.
