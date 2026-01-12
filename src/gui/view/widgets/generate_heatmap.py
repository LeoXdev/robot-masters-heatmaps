from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon

class GenerateHeatmap(QPushButton):
    def __init__(self, label, state, orchestrator):
        super().__init__(label)
        self.state = state
        self.orchestrator = orchestrator

        self.setIcon(QIcon("gui/resources/icons/icon.png"))
        self.setDefault(True)  # adds a wee of style to the button
        self.clicked.connect(self.orchestrator.generate_heatmap)

        # slots to state's signals
        self.state.new_selected_model.connect(self._enable)
        self.state.video_closed.connect(self._disable)

        # initialization
        self._disable()

    def _enable(self):
        self.setEnabled(True)
    def _disable(self):
        self.setEnabled(False)
