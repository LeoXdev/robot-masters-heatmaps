from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QComboBox,
)
from PySide6.QtGui import (
    QFont,
    QIcon,
)
from PySide6.QtCore import Qt

import gui.view.widgets.title as Title

class SelectedModel(QWidget):
    def __init__(self, state, orchestrator):
        super().__init__()
        self.state = state
        self.orchestrator = orchestrator

        self.layout = QVBoxLayout(self)

        self.dropdown = QComboBox()
        self.dropdown.setPlaceholderText("Select a model...")
        # yolo model is not loaded at this point, until heatmap generation
        self.dropdown.currentTextChanged.connect(lambda: self._on_dropdown_changed(self.dropdown.currentText()))

        self.layout.addWidget(self.dropdown)

        # slots to state's signals
        self.state.new_models_list.connect(self._update_options)
        self.state.new_video_capture.connect(self._enable)
        self.state.video_closed.connect(self._disable)

        # initialization
        self._load_options()
        self._disable()

    def _enable(self):
        self.dropdown.setEnabled(True)
    def _disable(self):
        # removes user selection, placeholder appears again
        # without this reset, it may be impossible to trigger again the event currentTextChange
        # should there be only a single model available
        self.dropdown.setCurrentIndex(-1)
        self.dropdown.setEnabled(False)

    def _load_options(self):
        self.orchestrator.set_available_models()
    def _update_options(self, models):
        self.dropdown.clear()
        if models:
            self.dropdown.addItems(models)
    def _on_dropdown_changed(self, new_model):
        self.orchestrator.select_model(new_model)
