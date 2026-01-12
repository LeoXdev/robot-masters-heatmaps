from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
)

class ExportHeatmap(QWidget):
    def __init__(self, state, orchestrator):
        super().__init__()
        self.state = state
        self.orchestrator = orchestrator

        self.layout = QVBoxLayout(self)

        self.png_button = QPushButton("Cummulative PNG")
        self.png_button.setEnabled(False)
        self.png_button.clicked.connect(lambda: self.orchestrator.export_heatmap("png"))
        self.layout.addWidget(self.png_button)

        self.jpg_button = QPushButton("Cummulative JPG")
        self.jpg_button.setEnabled(False)
        self.jpg_button.clicked.connect(lambda: self.orchestrator.export_heatmap("jpg"))
        self.layout.addWidget(self.jpg_button)

        #self.mp4_button = QPushButton("Frame-by-Frame MP4")
        #self.mp4_button.setEnabled(False)
        #self.mp4_button.clicked.connect()
        #self.layout.addWidget(self.mp4_button)

        # slots to state's signals
        self.state.new_heatmap.connect(self._enable)
        self.state.video_closed.connect(self._disable)

        # initialization
        self._disable()

    def _enable(self):
        self.png_button.setEnabled(True)
        self.jpg_button.setEnabled(True)
    def _disable(self):
        self.png_button.setEnabled(False)
        self.jpg_button.setEnabled(False)

    def _on_png_clicked(self):
        pass
