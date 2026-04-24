"""
Inspection router — engine mirrors the reference api.py (global model + engine,
reads image from prediction.image_path, standard JET blend).
"""
from __future__ import annotations

import base64
import logging
import os
import tempfile
import time
from io import BytesIO
from threading import Lock

import cv2
import numpy as np
from fastapi import APIRouter, File, HTTPException, UploadFile
from PIL import Image
from pydantic import BaseModel


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/inspection", tags=["inspection"])   

_model = None
_engine = None
_lock = Lock()

_ALLOWED_MIME_TYPES = frozenset({
    "image/jpeg", "image/png", "image/webp", "image/bmp", "image/tiff",
})


def _ensure_model():
    global _model, _engine
    if _model is None:
        with _lock:
            if _model is None:
                from anomalib.engine import Engine
                from app.core.model_loader import get_model
                _model = get_model()
                _engine = Engine()
    return _model, _engine


def _to_numpy(x):
    if hasattr(x, "cpu") and hasattr(x, "detach"):
        x = x.cpu().detach()
    if hasattr(x, "numpy"):
        return x.numpy()
    return np.array(x)


def _ensure_hw(arr: np.ndarray) -> np.ndarray:
    if arr.ndim == 3 and arr.shape[0] in (1, 3):
        return arr[0]
    if arr.ndim == 3 and arr.shape[2] in (1, 3):
        return arr[..., 0]
    return arr


class AnalyzeResponse(BaseModel):
    original_b64: str
    heatmap_b64: str
    anomaly_score: float
    verdict: str
    inference_ms: float


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_image(file: UploadFile = File(...)) -> AnalyzeResponse:
    from anomalib.data import PredictDataset
    from app.config import get_settings

    settings = get_settings()

    if file.content_type not in _ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported media type: {file.content_type}",
        )

    image_bytes = await file.read()
    if len(image_bytes) > settings.max_upload_bytes:
        raise HTTPException(status_code=413, detail="File too large.")

    mdl, eng = _ensure_model()

    # Write to temp file — PredictDataset requires a path on disk
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        Image.open(BytesIO(image_bytes)).convert("RGB").save(tmp, format="PNG")
        tmp_path = tmp.name

    t0 = time.perf_counter()
    try:
        dataset = PredictDataset(path=tmp_path, image_size=settings.train_image_size)
        predictions = eng.predict(model=mdl, dataset=dataset)

        if not predictions:
            raise HTTPException(status_code=500, detail="No predictions returned.")

        prediction = predictions[0]

        # Read the image that the model processed (from temp file, same as reference)
        image_np = np.asarray(Image.open(prediction.image_path[0]).convert("RGB"))

    except HTTPException:
        raise
    except Exception:
        logger.exception("Inference failed")
        raise HTTPException(status_code=500, detail="Inference failed. Check server logs.")
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass

    h, w, _ = image_np.shape

    anomaly_map = _ensure_hw(_to_numpy(prediction.anomaly_map))
    pred_score  = prediction.pred_score


    logger.info(
        "anomaly_map shape=%s min=%.4f max=%.4f mean=%.4f",
        anomaly_map.shape,
        float(anomaly_map.min()), float(anomaly_map.max()), float(anomaly_map.mean()),
    )

    anomaly_map_rs = cv2.resize(
        anomaly_map.astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC
    )

    # Render heatmap:
    # image_np is RGB (PIL), anomaly_color is BGR (OpenCV)
    # Convert anomaly_color to RGB before blending to avoid swapped channels
    anomaly_norm  = cv2.normalize(anomaly_map_rs, None, 0, 255, cv2.NORM_MINMAX)
    anomaly_color = cv2.applyColorMap(anomaly_norm.astype(np.uint8), cv2.COLORMAP_JET)
    anomaly_rgb   = cv2.cvtColor(anomaly_color, cv2.COLOR_BGR2RGB)
    overlay       = cv2.addWeighted(image_np, 0.6, anomaly_rgb, 0.4, 0)

    # Encode original as JPEG
    buf = BytesIO()
    Image.fromarray(image_np).save(buf, format="JPEG", quality=100)
    original_b64 = base64.b64encode(buf.getvalue()).decode()

    # Encode heatmap as PNG
    buf2 = BytesIO()
    Image.fromarray(overlay).save(buf2, format="PNG")
    heatmap_b64 = base64.b64encode(buf2.getvalue()).decode()

    raw_score     = float(pred_score.item())
    anomaly_score = raw_score
    inference_ms  = round((time.perf_counter() - t0) * 1000, 1)
    if anomaly_score > settings.anomaly_max_threshold:
        verdict = "IMAGEM_INVALIDA"
    elif anomaly_score > settings.anomaly_threshold:
        verdict = "REPROVADO"
    else:
        verdict = "APROVADO"

    logger.info(
        "Inference: %.0f ms | raw=%.4f | normalised=%.4f | %s",
        inference_ms, raw_score, anomaly_score, verdict,
    )

    return AnalyzeResponse(
        original_b64=original_b64,
        heatmap_b64=heatmap_b64,
        anomaly_score=anomaly_score,
        verdict=verdict,
        inference_ms=inference_ms,
    )
