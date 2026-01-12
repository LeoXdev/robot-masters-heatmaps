from PySide6.QtWidgets import QFileDialog
import cv2

def select_video_file() -> str:
    """
    select_video_file opens a system file dialog that prompts for an mp4 video.
    """
    file_path, _ = QFileDialog.getOpenFileName(
        None,
        "Open Video",
        "",
        "Video Files (*.mp4);;All Files (*)",
    )
    if not file_path:  # user does not choose a video
        return None
    return file_path

def load_video_file(video_path):
    """
    load_video_file takes a video_path and returns a cv2.VideoCapture object.
    """
    video_capture = cv2.VideoCapture(video_path)
    if not video_capture.isOpened():
        return None
    return video_capture
