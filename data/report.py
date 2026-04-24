import json

import pandas as pd

dataset = pd.DataFrame()

for file in [
    "resultados_experimentos_raspi_val_pixel_AUPRO.json",
    "resultados_experimentos_raspi_val_pixel_F1Score.json",
]:
    with open(file) as f:
        data = json.load(f)
    data = pd.DataFrame(data)
    data["file"] = file
    dataset = pd.concat([dataset, data])

dataset.groupby(by=["model", "file"]).agg(["mean", "std"]).sort_values(
    ("test_image_F1Score", "mean"),
    ascending=False,
)

dataset.groupby(by=["model", "file"]).agg(["mean", "std"]).sort_values(
    ("test_pixel_F1Score", "mean"),
    ascending=False,
)
