from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QSlider,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

class VideoPlayer(QWidget):
    def __init__(self, state, orchestrator):
        super().__init__()
        self.state = state
        self.orchestrator = orchestrator

        self.layout = QHBoxLayout(self)        

        self.start_button = QPushButton()
        self.start_button.setIcon(QIcon("gui/resources/icons/start.png"))
        self.start_button.clicked.connect(self._on_start_clicked)
        self.layout.addWidget(self.start_button)

        self.prev_button = QPushButton()
        self.prev_button.setIcon(QIcon("gui/resources/icons/prev.png"))
        self.prev_button.clicked.connect(self._on_prev_clicked)
        self.layout.addWidget(self.prev_button)

        self.play_button = QPushButton()
        self.play_button.setIcon(QIcon("gui/resources/icons/play.png"))
        self.play_button.clicked.connect(self.orchestrator.toggle_playback)
        self.layout.addWidget(self.play_button)

        self.next_button = QPushButton()
        self.next_button.setIcon(QIcon("gui/resources/icons/next.png")),
        self.next_button.clicked.connect(self._on_next_clicked)
        self.layout.addWidget(self.next_button)

        self.end_button = QPushButton()
        self.end_button.setIcon(QIcon("gui/resources/icons/end.png")),
        self.end_button.clicked.connect(self._on_end_clicked)
        self.layout.addWidget(self.end_button)

        self.slider = QSlider(Qt.Horizontal)
        # lack of slider.setRange(x, y) here as this value is input-dependent
        # design choice: sliderMoved over sliderReleased would cause more function calls which is expensive
        # altough not impossible to work around
        self.slider.sliderReleased.connect(self._on_slider_released)
        self.layout.addWidget(self.slider)
        
        # slots to state's signals
        self.state.new_video_capture.connect(self._enable)
        self.state.video_closed.connect(self._disable)
        # a new video_capture will always display the first frame of the video,
        # this slot resets the slider to the value 0
        self.state.new_video_capture.connect(lambda: self._set_slider_value(0))
        self.state.video_closed.connect(lambda: self._set_slider_value(0))
        self.state.new_video_total_frames.connect(self._set_slider_range)
        self.state.new_video_is_playing.connect(self._change_playback_icon)
        self.state.video_frame_index_changed.connect(self._set_slider_value)

        # initialization
        self._disable()

    def _set_enabled(self, boolean):
        if boolean:
            self._enable()
        else:
            self._disable()
    def _enable(self):
        self.start_button.setEnabled(True)
        self.prev_button.setEnabled(True)
        self.play_button.setEnabled(True)
        self.next_button.setEnabled(True)
        self.end_button.setEnabled(True)
        self.slider.setEnabled(True)
    def _disable(self):
        self.start_button.setEnabled(False)
        self.prev_button.setEnabled(False)
        self.play_button.setEnabled(False)
        self.next_button.setEnabled(False)
        self.end_button.setEnabled(False)
        self.slider.setEnabled(False)

    def _set_slider_range(self, total_frames):
        self.slider.setRange(0, total_frames - 1)
    def _set_slider_value(self, value):
        self.slider.setValue(value)

    def _change_playback_icon(self, value):
        if value is True:
            self.play_button.setIcon(QIcon("gui/resources/icons/pause.png"))
        else:
            self.play_button.setIcon(QIcon("gui/resources/icons/play.png"))

    def _on_start_clicked(self):
        self._navigate_to_frame(0)
    def _on_prev_clicked(self):
        self._navigate_to_frame(self.slider.value() - 1)
    def _on_next_clicked(self):
        self._navigate_to_frame(self.slider.value() + 1)
    def _on_end_clicked(self):
        self._navigate_to_frame(self.slider.maximum())
    def _navigate_to_frame(self, new_index):
        self.orchestrator.seek_to_frame(new_index)
        self._set_slider_value(new_index)

    def _on_slider_released(self):
        frame_index = self.slider.value()
        self.orchestrator.seek_to_frame(frame_index)
