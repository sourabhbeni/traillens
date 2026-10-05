"""TrailLens server: serves the mobile UI and the local /api/identify endpoint."""

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from traillens import __version__
from traillens.config import MAX_IMAGE_BYTES, MODEL, OLLAMA_HOST
from traillens.identify import identify

app = FastAPI(title="TrailLens", version=__version__)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    return FileResponse("static/index.html")


@app.get("/api/health")
def health():
    """Check that Ollama is reachable and the model is pulled."""
    import ollama  # lazy: keeps import side-effect free if proxy env is odd

    try:
        models = ollama.Client(host=OLLAMA_HOST).list()
        have = [m.get("name", "") for m in models.get("models", [])]
        ready = any(MODEL in name for name in have)
        return {"ok": True, "model": MODEL, "model_ready": ready, "hint": None if ready else f"Run: ollama pull {MODEL}"}
    except Exception as exc:
        return JSONResponse(
            {"ok": False, "error": str(exc)[:200], "hint": "Run `ollama serve`, then `ollama pull moondream2`"},
            status_code=503,
        )


@app.post("/api/identify")
async def api_identify(photo: UploadFile = File(...)):
    data = await photo.read()
    if len(data) > MAX_IMAGE_BYTES:
        raise HTTPException(413, "Image too large (10 MB max)")
    if not photo.content_type or not photo.content_type.startswith("image/"):
        raise HTTPException(400, "Upload must be an image")
    try:
        return identify(data)
    except Exception as exc:
        raise HTTPException(502, f"Identification failed: {str(exc)[:200]}")
