from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
)
from PySide6.QtGui import (
    QPixmap,
)
from PySide6.QtCore import Qt

from gui.utils import image

class VideoPreview(QWidget):
    def __init__(self, background, foreground, width, height, state, orchestrator):
        super().__init__()
        self.state = state
        self.orchestrator = orchestrator
        
        self.background_default: str = background
        # foreground_current gets updated when video_preview receives a new heatmap via signal
        # it'll serve as a cache when toggling on/off heatmap visualization
        self.foreground_current = None
        self.width = width
        self.height = height

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.display = QWidget()
        self.display.setFixedSize(self.width, self.height)

        back_pixmap = QPixmap(background)
        fore_pixmap = QPixmap(foreground)

        # background for video
        self.back_label = QLabel(self.display)
        self.back_label.setFixedSize(self.width, self.height)
        self.back_label.setPixmap(back_pixmap.scaled(
            self.width, self.height,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        ))
        #self.back_label.setStyleSheet("background: black;")

        # foreground for heatmap
        self.fore_label = QLabel(self.display)
        self.fore_label.setFixedSize(self.width, self.height)
        self.fore_label.setPixmap(fore_pixmap.scaled(
            self.width, self.height,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        ))
        self.fore_label.setAttribute(Qt.WA_TranslucentBackground)
        #self.fore_label.setStyleSheet("background: transparent;")
        self.fore_label.raise_()  # guarantees being on top of the BG

        self.layout.addWidget(self.display)

        # slots to state's signals
        self.state.video_frame_changed.connect(self._change_background)
        self.state.video_closed.connect(self._reset_preview)
        self.state.new_heatmap.connect(self._change_foreground)
        self.state.new_heatmap_is_being_shown.connect(self._toggle_heatmap_overlay)

        # initialization

    def _change_background(self, frame):
        src = None
        if frame is None:
            src = self.background_default
        else:
            src = frame

        # is guaranteed that frame is None only when closing a video
        # all other calls will have a frame as parameter to display
        pixmap = image.src_to_pixmap(src).scaled(
            self.width, self.height,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.back_label.setPixmap(pixmap)

    def _change_foreground(self, heatmap):
        src = None
        if heatmap is None:
            src = ""
        else:
            src = heatmap

        # is guaranteed that heatmap is None only when closing a video
        # all other calls will have a heatmap as parameter to display
        pixmap = image.src_to_pixmap(src).scaled(
            self.width, self.height,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.foreground_current = pixmap  # save to cache
        self.fore_label.setPixmap(pixmap)

    def _reset_preview(self):
        self._change_background(None)
        self._change_foreground(None)
    def _toggle_heatmap_overlay(self, boolean):
        if boolean:
            self.fore_label.setPixmap(self.foreground_current)
        else:
            self.fore_label.setPixmap(QPixmap(""))
