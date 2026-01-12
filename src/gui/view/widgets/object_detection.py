from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QPushButton,
    QColorDialog,
)
from PySide6.QtGui import QColor

class ObjectDetection(QWidget):
    def __init__(self, label, color, state, orchestrator):
        super().__init__()
        self.state = state
        self.orchestrator = orchestrator

        self.layout = QHBoxLayout(self)

        self.checkbox = QCheckBox()
        self.checkbox.toggled.connect(self._on_checkbox_toggled)
        self.label = QLabel(label)
        self.button = QPushButton()
        self.button.setFixedSize(24, 24)
        self.button.clicked.connect(self._on_button_clicked)
        self.button_color = None  # button_color.name() returns color in hex string

        self.layout.addWidget(self.checkbox, 1)
        self.layout.addWidget(self.label, 2)
        self.layout.addWidget(self.button, 1)

        # slots to state's signals
        self.state.new_video_capture.connect(self._enable)
        self.state.video_closed.connect(self._disable)

        # initialization
        self._set_button_color(color)
        self._disable()

    def _enable(self):
        self.checkbox.setEnabled(True)
        self.label.setEnabled(True)
        self.button.setEnabled(True)
    def _disable(self):
        self.checkbox.setEnabled(False)
        self.label.setEnabled(False)
        self.button.setEnabled(False)

    def _on_checkbox_toggled(self, checked):
        class_name = self.label.text().lower().replace(" ", "_")
        if checked:
            self.orchestrator.enable_class(class_name)
        else:
            self.orchestrator.disable_class(class_name)

    def _on_button_clicked(self):
        color = QColorDialog.getColor(
            self.button_color,
            self,
            "Choose a color"
        )
        # if user picks a color
        if color.isValid():
            self._set_button_color(color)
            class_name = self.label.text().lower().replace(" ", "_")
            self.orchestrator.change_class_color(class_name, color.name())
    def _set_button_color(self, color):
        qcolor = QColor(color)
        self.button.setStyleSheet(f"""
            QPushButton {{
                background-color: {qcolor.name()};
                border: 1px solid #ffffff;
            }}
        """)
        self.button_color = qcolor
