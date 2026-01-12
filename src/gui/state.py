from PySide6.QtCore import (
    QObject,
    Signal,
)
from numpy import ndarray

class State(QObject):
    # signals
    new_models_list = Signal(list)
    """
    new_models_list is captured by selected_model to update the selectable options.
    """
    new_selected_model = Signal()
    """
    new_selected_model is captured by generate_heatmap to enable the heatmap generation button.
    """
    
    new_video_capture = Signal()
    """
    new_video_capture is captured by video_player to enable the playback controls.
    new_video_capture is captured by selected_model to enable the model selection dropdown.
    new_video_capture is captured by object_detection to enable the checkbox and color picker.
    """
    new_video_total_frames = Signal(int)
    """
    new_video_total_frames is captured by the video_player slider to define a maximum value for itself.
    """
    video_frame_index_changed = Signal(int)
    """
    video_frame_index_changed is captured by the video_player slider to change its value.
    """
    video_frame_changed = Signal(ndarray)
    """
    video_frame_changed is captured by video_preview to change the frame being shown.
    """
    new_video_is_playing = Signal(bool)
    """
    new_video_is_playing is captured by the video_player play button to have its icon change between play and pause.
    """
    video_closed = Signal()
    """
    video_closed is captured by video_player to disable the playback controls.
    video_closed is captured by the video_player slider to reset its value to zero.
    video_closed is captured by video_preview to reset the frame and heatmap shown to the default one and an empty one repectively.
    video_closed is captured by selected_model to disable the model selection dropdown.
    video_closed is captured by generate_heatmap to disable the heatmap generation button.
    video_closed is captured by overlay_mode to toggle to off the heatmap overlay button group and to disable it.
    video_closed is captured by export_heatmap to disable the exportation buttons.
    """

    new_heatmap = Signal(ndarray)
    """
    new_heatmap is captured by video_preview to change the foreground to the new heatmap.
    new_heatmap is captured by overlay_mode to enable the button group and to change the selected value to cummulative.
    new_heatmap is captured by export_heatmap to enable the exportation buttons.
    """
    new_heatmap_is_being_shown = Signal(bool)
    """
    new_heatmap_is_being_shown is captured by video_preview to determine whether to display the heatmap over the video or not.
    """

    def __init__(self):
        super().__init__()

        # settings fields
        self._models_list = None
        """
        _models_list holds the available yolo computer vision models for use.
        """
        self._selected_model = ""
        self._yolo_model = None
        """
        _yolo_model holds the return value of YOLO.model(self._selected_model).
        """
        self._object_detection = {
            "player": {
                "enabled": False,
                "color": "#060270",
            },
            "player_shot": {
                "enabled": False,
                "color": "#7dda58",
            },
            "enemy": {
                "enabled": False,
                "color": "#e4080a",
            },
            "enemy_shot": {
                "enabled": False,
                "color": "#fe9900",
            },
        }
        """
        _object_detection holds the object detection settings for the selected model.
        If a class is not enabled, model's detections will be ignored on heatmap generation.
        A class' color will determine the color for activity on the heatmap.
        """

        # memory fields
        self._video_path = ""
        self._video_capture = None
        """
        _video_capture holds the return value of cv2.VideoCapture(self._video_path).
        """
        self._video_total_frames = -1
        self._video_current_frame_index = -1
        """
        _video_current_frame_index holds the index of the current frame being displayed.
        """
        self._video_current_frame = None
        """
        _video_current_frame holds the current frame being displayed on video_preview, np.ndarray format.
        """
        self._video_is_playing = False

        self._heatmap_current_frame = None
        """
        _heatmap_current_frame holds the current heatmap being displayed on video_preview, np.ndarray format.
        """
        self._heatmap_is_being_shown = False

    # getters, setters
    def get_models_list(self):
        return self._models_list
    def set_models_list(self, value):
        # there's not an equality check as this setter is executed only once on app initialization
        self._models_list = value
        self.new_models_list.emit(value)
    
    def get_selected_model(self):
        return self._selected_model
    def set_selected_model(self, value):
        if self._selected_model == value:
            return
        self._selected_model = value
        self.new_selected_model.emit()

    def get_yolo_model(self):
        return self._yolo_model
    def set_yolo_model(self, value):
        self._yolo_model = value

    # self._object_detection api
    def get_enabled_classes(self):
        res = {}
        for class_name, class_data in self._object_detection.items():
            if class_data["enabled"]:
                res[class_name] = class_data
        return res
    def enable_class(self, yolo_class):
        for class_name, class_data in self._object_detection.items():
            if class_name == yolo_class:
                class_data["enabled"] = True
    def disable_class(self, yolo_class):
        for class_name, class_data in self._object_detection.items():
            if class_name == yolo_class:
                class_data["enabled"] = False
    def set_class_color(self, yolo_class, color):
        for class_name, class_data in self._object_detection.items():
            if class_name == yolo_class:
                class_data["color"] = color

    def get_video_path(self):
        return self._video_path
    def set_video_path(self, value):
        if self._video_path == value:
            return
        self._video_path = value

    def get_video_capture(self):
        return self._video_capture
    def set_video_capture(self, value):
        # in practice, this if statement never evaluates to true
        # the set_video_path always prevents the same video twice in a row
        if self._video_capture == value:
            return
        # memory release and state reset, not using setters as this may trigger unwanted signals
        if self._video_capture:
            self._video_capture.release()
            self._video_path = ""  # this line may be removed, video_path is not used after video_capture creation
            self._video_total_frames = -1
            self._video_current_frame_index = -1
            self._video_current_frame = None
            self._video_is_playing = False
        
        self._video_capture = value
        if self._video_capture is None:
            self.video_closed.emit()
        else:
            self.new_video_capture.emit()

    def get_video_total_frames(self):
        return self._video_total_frames
    def set_video_total_frames(self, value):
        if self._video_total_frames == value:
            return
        self._video_total_frames = value

        self.new_video_total_frames.emit(value)

    def get_video_current_frame_index(self):
        return self._video_current_frame_index
    def set_video_current_frame_index(self, value):
        if self._video_current_frame_index == value:
            return
        self._video_current_frame_index = value

        self.video_frame_index_changed.emit(value)

    def get_video_current_frame(self):
        return self._video_current_frame
    def set_video_current_frame(self, frame):
        # comparing the actual frame with the new one is impractical and expensive
        self._video_current_frame = frame
        
        self.video_frame_changed.emit(frame)

    def get_video_is_playing(self):
        return self._video_is_playing
    def set_video_is_playing(self, value):
        if self._video_is_playing == value:
            return
        self._video_is_playing = value        

        self.new_video_is_playing.emit(value)

    def get_heatmap_current_frame(self):
        return self._heatmap_current_frame
    def set_heatmap_current_frame(self, heatmap):
        # comparing the actual heatmap with the new one is impractical and expensive
        self._heatmap_current_frame = heatmap
        
        self.new_heatmap.emit(heatmap)

    def get_heatmap_is_being_shown(self):
        return self._heatmap_is_being_shown
    def set_heatmap_is_being_shown(self, value):
        if self._heatmap_is_being_shown == value:
            return
        self._heatmap_is_being_shown = value        

        self.new_heatmap_is_being_shown.emit(value)
