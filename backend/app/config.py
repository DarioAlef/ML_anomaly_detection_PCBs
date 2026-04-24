from __future__ import annotations

import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

_BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_REPO_ROOT = os.path.dirname(_BACKEND_DIR)


class Settings(BaseSettings):
    # ── PatchCore model ───────────────────────────────────────────────────────
    patchcore_ckpt: str = os.path.join(_BACKEND_DIR, "app", "patchcore-raspi.ckpt")

    # ── Inference ─────────────────────────────────────────────────────────────
    anomaly_threshold: float = 0.05
    # Scores acima deste valor = imagem provavelmente não é PCB
    anomaly_max_threshold: float = 0.75

    # ── Upload limits ─────────────────────────────────────────────────────────
    max_upload_bytes: int = 50 * 1024 * 1024  # 50 MB

    # ── Image rendering ───────────────────────────────────────────────────────
    heatmap_alpha: float = 0.4
    jpeg_quality: int = 90

    # ── Data ──────────────────────────────────────────────────────────────────
    data_dir: str = os.path.join(_REPO_ROOT, "data")
    metrics_filename: str = "resultados_experimentos_transistor_val_pixel_AUPRO.json"

    # ── Dataset / Training ───────────────────────────────────────────────────
    dataset_name: str = "raspi"
    dataset_normal_dir: str = os.path.join(_REPO_ROOT, "data", "raspi", "ok")
    dataset_abnormal_dir: str = os.path.join(_REPO_ROOT, "data", "raspi", "ng")
    dataset_mask_dir: str = os.path.join(_REPO_ROOT, "data", "raspi", "mask")
    # Native resolution of the raspi PCB images (H × W)
    train_image_height: int = 1973
    train_image_width: int = 2953
    # Black borders present in every training image (pixels, measured empirically)
    # All 99 OK and 20 NG images share exactly these fixed borders.
    # PatchCore memorises features at each spatial location, so test images must
    # have the same border layout or the model will flag border areas as anomalies.
    border_top: int = 30
    border_bottom: int = 20
    border_left: int = 36
    border_right: int = 14
    val_split_ratio: float = 0.2
    test_split_ratio: float = 0.2
    train_batch_size: int = 4
    eval_batch_size: int = 4
    train_seed: int = 42
    # ColorJitter augmentation strengths
    aug_brightness: float = 0.5
    aug_contrast: float = 0.25
    aug_saturation: float = 0.25
    aug_hue: float = 0.0

    # ── CORS ──────────────────────────────────────────────────────────────────
    cors_origins: list[str] = [
        "http://localhost:4200",
        "http://localhost:3000",
        "http://127.0.0.1:4200",
    ]

    @property
    def train_image_size(self) -> tuple[int, int]:
        """(H, W) tuple expected by Anomalib's configure_pre_processor."""
        return (self.train_image_height, self.train_image_width)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
