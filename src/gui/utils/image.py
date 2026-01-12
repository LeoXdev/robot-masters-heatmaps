from numpy import ndarray
from PySide6.QtGui import (
    QPixmap,
    QImage,
)
import cv2

def src_to_pixmap(src) -> QPixmap:
    """
    src_to_pixmap converts either an image path string or a cv2 frame to a PySide6 pixmap.
    """
    # when processing np.ndarray, a cv2 frame is assumed
    if isinstance(src, ndarray):
        h, w = src.shape[:2]
        if src.shape[2] == 3:
            # video frames
            frame_rgb = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
            ch = 3
            return QPixmap.fromImage(
                QImage(frame_rgb.data, w, h, ch * w, QImage.Format_RGB888)
            )
        elif src.shape[2] == 4:
            # heatmap frames with transparency
            frame_rgba = cv2.cvtColor(src, cv2.COLOR_BGRA2RGBA)
            ch = 4
            return QPixmap.fromImage(
                QImage(frame_rgba.data, w, h, ch * w, QImage.Format_RGBA8888)
            )
    if isinstance(src, str):
        return QPixmap(src)
