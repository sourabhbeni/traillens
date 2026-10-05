# DRAFT — DEV submission post (polish Sunday before submitting)

> Tags: #devchallenge #hf26challenge
> Template sections below follow the official submission template.

---

# I built a plant identifier that works where your phone doesn't: on the trail, with no signal

## What I built

**TrailLens** — point your phone at a plant on a hike, and a vision model running
*entirely on your own machine* tells you what it is: common name, scientific name,
confidence score, identifying features, habitat note. No cloud API, no account,
no internet connection required.

Repo: https://github.com/sourabhbeni/traillens

## Demo

`ollama pull moondream2 && pip install -r requirements.txt && uvicorn app:app`
→ open the phone UI → snap a plant → get a result card in seconds. [screenshots
from Saturday field test go here]

## How it gets people outside

The theme is Touch Grass, and the design brief wrote itself: the best trail tool
is the one that works *on the trail*. TrailLens makes the screen the shortest
part of the experience — one photo, one glance at the result, eyes back on the
world. Bonus: I took it outside and used it [field-test notes go here].

## Why open innovation matters for what I built

This project only exists because the AI is open. Three reasons:

1. **It runs where closed AI can't.** A cloud vision API is useless at a trailhead
   with zero bars. A 1.7B-parameter open-weight model (Moondream2) running locally
   via Ollama works in airplane mode. Openness isn't a philosophy here — it's the
   feature.
2. **Your photos stay yours.** Plant photos carry location data; trails you love
   are nobody's training data. Local inference means nothing ever leaves the device.
3. **It's inspectable and swappable.** The prompt, the JSON schema, the model —
   all visible, all replaceable. When a bigger open model fits my hardware, it's
   one environment variable (`TRAILLENS_MODEL=qwen2.5vl:7b`). Try that with a
   proprietary endpoint.

The open pieces aren't decoration — they're what makes the project work.

## How I built it

[2–3 paragraphs: FastAPI backend, strict-JSON system prompt (temperature 0.2,
schema validation, uncertainty instead of invention), mobile-first UI with camera
capture, eval on 5–10 trail photos. Mention the agent session / process briefly.]

## Prize Categories

- Best Use of Gemma — [only if swapped to Gemma; otherwise omit]

## What's next

[one honest paragraph: accuracy tuning, offline packaging, maybe a native wrapper]
