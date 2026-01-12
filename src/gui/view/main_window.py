from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
)
from PySide6.QtGui import QIcon

import gui.view.widgets.title as Title
import gui.view.widgets.selected_model as SelectedModel
import gui.view.widgets.object_detection as ObjectDetection
import gui.view.widgets.video_preview as VideoPreview
import gui.view.widgets.video_player as VideoPlayer
import gui.view.widgets.generate_heatmap as GenerateHeatmap
import gui.view.widgets.overlay_mode as OverlayMode
import gui.view.widgets.export_heatmap as ExportHeatmap

class MainWindow(QMainWindow):
    def __init__(self, state, orchestrator):
        super().__init__()
        self.state = state
        self.orchestrator = orchestrator
        # --- ---
        # layout
        self.central = QWidget()
        self.c_layout = QHBoxLayout(self.central)
        # ---
        self.lcol = QWidget()
        self.lcol_layout = QVBoxLayout(self.lcol)
        # ---
        self.lline = QFrame()
        self.lline.setFrameShape(QFrame.VLine)
        self.lline.setFrameShadow(QFrame.Sunken)
        # ---
        self.mcol = QWidget()
        self.mcol_layout = QVBoxLayout(self.mcol)
        # ---
        self.rcol = QWidget()
        self.rcol_layout = QVBoxLayout(self.rcol)

        self.c_layout.addWidget(self.lcol, 1)
        self.c_layout.addWidget(self.lline)
        self.c_layout.addWidget(self.mcol, 2)
        self.c_layout.addWidget(self.rcol, 1)

        # --- --- ---

        # left column
        self.lcol_title = Title.Title("Settings", 1)
        self.lcol_layout.addWidget(self.lcol_title)

        self.lcol_sub = Title.Title("Selected Model", 2)
        self.lcol_layout.addWidget(self.lcol_sub)

        self.lcol_model = SelectedModel.SelectedModel(self.state, self.orchestrator)
        self.lcol_layout.addWidget(self.lcol_model)

        self.lcol_sub2 = Title.Title("Object Detection", 2)
        self.lcol_layout.addWidget(self.lcol_sub2)

        self.lcol_obj_pl = ObjectDetection.ObjectDetection(
            "Player",
            "#060270",
            self.state,
            self.orchestrator,
        )
        self.lcol_layout.addWidget(self.lcol_obj_pl)

        self.lcol_obj_plp = ObjectDetection.ObjectDetection(
            "Player Shot",
            "#7dda58",
            self.state,
            self.orchestrator,
        )
        self.lcol_layout.addWidget(self.lcol_obj_plp)

        self.lcol_obj_e = ObjectDetection.ObjectDetection(
            "Enemy",
            "#e4080a",
            self.state,
            self.orchestrator,
        )
        self.lcol_layout.addWidget(self.lcol_obj_e)

        self.lcol_obj_ep = ObjectDetection.ObjectDetection(
            "Enemy Shot",
            "#fe9900",
            self.state,
            self.orchestrator,
        )
        self.lcol_layout.addWidget(self.lcol_obj_ep)

        self.lcol_layout.addStretch()

        # middle column
        self.mcol_title = Title.Title("Video Preview", 1)
        self.mcol_layout.addWidget(self.mcol_title)

        self.mcol_video_preview = VideoPreview.VideoPreview(
            "gui/resources/default-video-frame.png",
            "",
            800, 600,
            self.state,
            self.orchestrator,
        )
        self.mcol_layout.addWidget(self.mcol_video_preview)

        self.mcol_video_player = VideoPlayer.VideoPlayer(self.state, self.orchestrator)
        self.mcol_layout.addWidget(self.mcol_video_player)

        # right column
        self.rcol_layout.addStretch()

        self.rcol_generate_button = GenerateHeatmap.GenerateHeatmap(
            "Generate Heatmap",
            self.state,
            self.orchestrator,
        )
        self.rcol_layout.addWidget(self.rcol_generate_button)

        self.rcol_layout.addStretch()

        self.rcol_sub = Title.Title("Overlay Mode", 2)
        self.rcol_layout.addWidget(self.rcol_sub)

        self.rcol_overlay_bg = OverlayMode.OverlayMode(self.state, self.orchestrator)
        self.rcol_layout.addWidget(self.rcol_overlay_bg)

        self.rcol_sub2 = Title.Title("Export Heatmap", 2)
        self.rcol_layout.addWidget(self.rcol_sub2)

        self.rcol_export = ExportHeatmap.ExportHeatmap(self.state, self.orchestrator)
        self.rcol_layout.addWidget(self.rcol_export)

        self.rcol_layout.addStretch()
        self.rcol_layout.addStretch()
        self.rcol_layout.addStretch()
        self.rcol_layout.addStretch()
        self.rcol_layout.addStretch()
        self.rcol_layout.addStretch()

        # --- ---
        # config
        self.setWindowTitle("Robot Master Heatmaps")
        self.setWindowIcon(QIcon("gui/resources/icons/heatmap.png"))
        self.statusBar().showMessage("")  # ==============

        self.menuBar().addAction("Open Video", self.orchestrator.load_video)
        self.menuBar().addAction("Close Video", self.orchestrator.close_video)

        self.setCentralWidget(self.central)
