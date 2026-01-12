import sys

from PySide6.QtWidgets import QApplication

from gui.state import State
from gui.business.orchestrator import Orchestrator
from gui.view.main_window import MainWindow
import gui.utils.fonts as fonts

app = QApplication(sys.argv)
fonts.init()

state = State()
orchestrator = Orchestrator(state)
window = MainWindow(state, orchestrator)
window.showMaximized()
sys.exit(app.exec())
