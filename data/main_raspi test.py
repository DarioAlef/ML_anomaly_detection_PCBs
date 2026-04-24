import json
import os

import cv2
import matplotlib.pyplot as plt
import numpy as np
import torch
from anomalib.data import Folder
from anomalib.engine import Engine
from anomalib.metrics import AUPRO, AUROC, Evaluator, F1Score
from anomalib.metrics.evaluator import Evaluator
from anomalib.models import Cfa, Dfm, Dinomaly, Fre, Patchcore
from lightning.pytorch.callbacks import EarlyStopping
from PIL import Image
from skimage import measure
from torchvision.transforms import v2


def plot_predictions(predictions):
    if predictions is None:
        return

    def to_numpy(x):
        if hasattr(x, "cpu") and hasattr(x, "detach"):
            x = x.cpu().detach()
        if hasattr(x, "numpy"):
            return x.numpy()
        return np.array(x)

    def ensure_hw(arr):
        if arr.ndim == 3 and arr.shape[0] in (1, 3):
            return arr[0]
        if arr.ndim == 3 and arr.shape[2] in (1, 3):
            return arr[..., 0]
        return arr

    def draw_contours_cv(img, contours, color=(255, 0, 0), thickness=3):
        for contour in contours:
            pts = np.fliplr(contour).astype(np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(
                img,
                [pts],
                isClosed=True,
                color=color,
                thickness=thickness,
                lineType=cv2.LINE_AA,
            )

    for prediction in predictions:

        # --- imagem original ---
        image = np.asarray(Image.open(prediction.image_path[0]).convert("RGB"))
        h, w, _ = image.shape

        # --- labels ---
        gt_label = prediction.gt_label
        pred_label = prediction.pred_label
        pred_score = prediction.pred_score

        # --- mapas ---
        anomaly_map = ensure_hw(to_numpy(prediction.anomaly_map))
        gt_mask = ensure_hw(to_numpy(prediction.gt_mask))

        anomaly_map_rs = cv2.resize(
            anomaly_map.astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC
        )
        gt_mask_rs = cv2.resize(
            gt_mask.astype(np.float32), (w, h), interpolation=cv2.INTER_NEAREST
        )

        gt_bin = (gt_mask_rs >= 0.5).astype(np.uint8)

        # --- contornos GT ---
        contours_gt = measure.find_contours(gt_bin, 0.5)

        # --- imagem com overlays ---
        overlay = image.copy()

        # mapa de anomalia (heatmap)
        anomaly_norm = cv2.normalize(anomaly_map_rs, None, 0, 255, cv2.NORM_MINMAX)
        anomaly_color = cv2.applyColorMap(
            anomaly_norm.astype(np.uint8), cv2.COLORMAP_JET
        )

        alpha_map = 0.4
        overlay = cv2.addWeighted(overlay, 1 - alpha_map, anomaly_color, alpha_map, 0)

        # ground truth (verde)
        draw_contours_cv(
            overlay,
            contours_gt,
            color=(0, 255, 0),
            thickness=5,
        )

        # --- plot ---
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle(
            f"GT: {None if isinstance(gt_label, type(None)) else gt_label.item()} | "
            f"Pred: {pred_label.item()} | Score: {pred_score.item():.2f}",
            fontsize=14,
        )

        for ax in axes:
            ax.axis("off")

        axes[0].imshow(image)
        axes[0].set_title("Imagem Original")

        axes[1].imshow(overlay)
        axes[1].set_title("GT + Mapa de Anomalia")

        plt.tight_layout()
        plt.show()


augmentations = v2.Compose(
    [
        v2.ColorJitter(
            brightness=0.5,
            contrast=0.25,
            saturation=0.25,
            hue=0.0,
        ),
    ]
)

datamodule = Folder(
    name="raspi",
    normal_dir="raspi/ok",
    abnormal_dir="raspi/ng",
    mask_dir="raspi/mask",
    val_split_ratio=0.2,
    test_split_ratio=0.2,
    train_augmentations=augmentations,
    val_augmentations=augmentations,
    seed=42,
    train_batch_size=4,
    eval_batch_size=4,
)

datamodule.setup()

model = Dinomaly()
model.configure_pre_processor(image_size=(1973, 2953))

engine = Engine()

engine.fit(model=model, datamodule=datamodule)

test_results = engine.test(datamodule=datamodule, model=model)[0]

# predictions = engine.predict(dataset=datamodule.test_data)

# plot_predictions(predictions)
