from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QButtonGroup,
    QRadioButton,
)

class OverlayMode(QWidget):
    def __init__(self, state, orchestrator):
        super().__init__()
        self.state = state
        self.orchestrator = orchestrator

        self.layout = QHBoxLayout(self)

        self.button_group = QButtonGroup()

        self.off_button = QRadioButton("Off")
        self.off_button.toggled.connect(self._on_off_toggled)
        self.cumulative_button = QRadioButton("Cumulative")
        self.cumulative_button.toggled.connect(self._on_cumulative_toggled)
        #self.fbf_button = QRadioButton("Frame-by-Frame")

        self.off_button.setEnabled(False)
        self.cumulative_button.setEnabled(False)
        #self.fbf_button.setEnabled(False)

        self.button_group.addButton(self.off_button)
        self.button_group.addButton(self.cumulative_button)
        #self.button_group.addButton(self.fbf_button)

        self.layout.addWidget(self.off_button)
        self.layout.addWidget(self.cumulative_button)
        #self.layout.addWidget(self.fbf_button)

        # slots to state's signals
        self.state.new_heatmap.connect(self._enable)
        self.state.new_heatmap.connect(lambda: self.cumulative_button.setChecked(True))
        self.state.video_closed.connect(lambda: self._on_off_toggled(True))
        self.state.video_closed.connect(self._disable)

        # initialization
        self.off_button.setChecked(True)
        self._disable()

    def _enable(self):
        self.off_button.setEnabled(True)
        self.cumulative_button.setEnabled(True)
    def _disable(self):
        if self.off_button.isChecked():
            self.off_button.setChecked(False)
        if self.cumulative_button.isChecked():
            self.cumulative_button.setChecked(False)

        self.off_button.setEnabled(False)
        self.cumulative_button.setEnabled(False)

    def _on_off_toggled(self, checked):
        if checked:
            self.orchestrator.toggle_heatmap_overlay(False)
    def _on_cumulative_toggled(self, checked):
        if checked:
            self.orchestrator.toggle_heatmap_overlay(True)
