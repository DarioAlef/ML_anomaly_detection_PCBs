"""
PatchCore singleton loader.

Handles two CPU-only quirks:
  1. PyTorch 2.6 changed weights_only default to True — breaks Anomalib checkpoints.
  2. Checkpoints trained with CUDA cause torchmetrics to request a CUDA device;
     we redirect those calls to CPU transparently.
"""
from __future__ import annotations

import logging
from threading import Lock

logger = logging.getLogger(__name__)

_model = None
_model_lock = Lock()


def _load_model(ckpt_path: str):
    import torch
    from anomalib.models import Patchcore

    logger.info("Loading PatchCore checkpoint: %s", ckpt_path)

    # PyTorch 2.6+ quirk: force weights_only=False for Anomalib checkpoints
    _orig_load = torch.load

    def _patched_load(*args, **kwargs):
        kwargs["weights_only"] = False
        return _orig_load(*args, **kwargs)

    torch.load = _patched_load
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        if device == "cpu":
            logger.warning("CUDA requested but not available. Falling back to CPU.")
        else:
            logger.info("CUDA detected. Moving model to GPU.")

        model = Patchcore.load_from_checkpoint(ckpt_path, map_location=device)
        model = model.to(device)
    finally:
        torch.load = _orig_load

    model.eval()
    logger.info("PatchCore loaded successfully on %s.", device)
    return model


def get_model(ckpt_path: str | None = None):
    """Return the global PatchCore singleton (lazy-loaded, thread-safe)."""
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:
                from app.config import get_settings
                path = ckpt_path or get_settings().patchcore_ckpt
                _model = _load_model(path)
    return _model


def set_model(model) -> None:
    """Replace the singleton with an already-trained in-memory model.

    Called by the training service after engine.fit() so that subsequent
    inference requests use the freshly trained model without reloading from disk.
    """
    global _model
    with _model_lock:
        _model = model
        logger.info("Model singleton updated with freshly trained model.")
