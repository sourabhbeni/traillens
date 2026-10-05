"""Runtime configuration. Override with environment variables."""

import os

# Default: Moondream2 — tiny (~1.7B) open-weight vision model, runs on modest
# hardware. Swap up with TRAILLENS_MODEL=qwen2.5vl:7b on beefier machines.
MODEL = os.environ.get("TRAILLENS_MODEL", "moondream2")

# Where Ollama listens. Everything stays on this machine — no cloud calls.
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

# Reject absurdly large uploads before they hit the model.
MAX_IMAGE_BYTES = 10 * 1024 * 1024
