"""
train.py

Purpose:
    Train a YOLO model on custom data.

Usage:
    py train.py
"""

from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO("yolov5m.pt")

    model.train(
        data="../data/mm10/dataset.yaml",
        epochs=100,
        imgsz=800,
        batch=-1,
        project="../models",
        name="mm10",
        exist_ok=True,
        device=0
    )
    print("Model saved to ../models/mm10/weights/best.pt")
