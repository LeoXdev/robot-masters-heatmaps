from ultralytics import YOLO
from pathlib import Path
import torch

def get_available_models(dir=Path("gui/resources/models/")):
    """
    get_available_models returns a string list containing yolo computer vision models found at
    /src/gui/resources/models/*.pt without the file extension.
    """
    if not dir.exists():
        return None

    files = list(dir.glob("*.pt")) + list(dir.glob("*.PT"))
    model_names = [f.stem for f in files]  # trims extension

    if model_names:
        # dirty but quick way to delete dupes
        # covers testcase where some models end in .pt and some end in .PT
        return sorted(list(set(model_names)))
    else:
        return None

def load_yolo_model(model_name):
    """
    load_yolo_model takes a model name (mm1, mm2, mm10, mmu...) and returns a YOLO model object ready for inference.
    """
    model_path = "gui/resources/models/" + model_name + ".pt"
    try:
        model = YOLO(model_path)
        if torch.cuda.is_available():
            model.to('cuda')
        return model
    except Exception as e:
        return None
