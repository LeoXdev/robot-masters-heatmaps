from PySide6.QtWidgets import QFileDialog
import cv2

def select_export_path(extension) -> str:
    """
    select_export_path opens a system file dialog that prompts for a path to save a png or jpg.
    """
    file_path = None
    
    if extension == "png":
        file_path, _ = QFileDialog.getSaveFileName(
            None,
            "Export Heatmap",
            "",
            "PNG (*.png)"
        )
    else:
        file_path, _ = QFileDialog.getSaveFileName(
            None,
            "Export Heatmap",
            "",
            "JPEG (*.jpg *.jpeg)"
        )
    if not file_path:  # user does not choose a path
        return None
    return file_path

def export_heatmap(heatmap, export_path):
    """
    export_heatmap saves a heatmap file on the chosen export path.
    """
    cv2.imwrite(export_path, heatmap)
