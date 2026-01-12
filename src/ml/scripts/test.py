"""
test.py

Purpose:
    Generate demo predictions and metrics for a model.

Usage:
    py test.py
"""

import os

from ultralytics import YOLO

if __name__ == "__main__":
    OUTPUT_DIR = "../models/mm10/test_results"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    model = YOLO("../models/mm10/weights/best.pt")

    results = model.predict(
        source="../data/mm10/images/test",
        conf=0.25,
        iou=0.35,
        save=True,
        save_txt=True,
        save_conf=True,
        project=OUTPUT_DIR,
        name="preds",
        exist_ok=True
    )
    print(f"Predictions saved in: {OUTPUT_DIR}/preds")


    metrics = model.val(data="../data/mm10/dataset.yaml", split='test')
    metrics_out = {
        "mAP50": metrics.box.map50,
        "mAP50-95": metrics.box.map,
        "precision": metrics.box.mp,
        "recall": metrics.box.mr
    }
    with open(f"{OUTPUT_DIR}/metrics.txt", "w") as f:
        for k, v in metrics_out.items():
            f.write(f"{k}: {v}\n")
    print(f"Test metrics saved in: {OUTPUT_DIR}/metrics.txt")
