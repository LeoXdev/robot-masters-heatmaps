from PySide6.QtCore import QTimer

from gui.state import State
import gui.business.video.loader as video_loader
import gui.business.video.reader as video_reader
import gui.business.model.loader as model_loader
import gui.business.model.predictor as model_predictor
import gui.business.heatmap.generator as heatmap_generator
import gui.business.heatmap.exporter as heatmap_exporter

class Orchestrator():
    """
    Orchestrator executes business logic in response to events such as user input, playback timer or initialization.

    - Bridges View events to business functions (one event -> one orchestrator method -> N business functions).
    - Accesses and modifies State.
    - Handles error logging.
    """
    def __init__(self, state: State):
        super().__init__()
        self.state = state

        # timer for updating video frames, runs when pressing the play button, stops when pressing the stop button
        self.playback_timer = QTimer()
        self.playback_timer.timeout.connect(self._play_next_frame)
        self.playback_timer.setInterval(33)  # 33ms -> ~30fps
    
    def load_video(self):
        """
        load_video handles five tasks:
        - Frees memory of the previous video and heatmap (if there's one).
        - Prompts user for a video file.
        - Creates a cv2.VideoCapture object based on the selected video file.
        - Enables the VideoPlayer widget.
        - Update the VideoPreview widget so it displays the first frame of the video.

        Triggered by MainWindow -> menuBar -> Open Video
        """

        #set video path
        video_path = video_loader.select_video_file()
        if not video_path:
            print("error: user did not select a video")
            return
        if video_path == self.state.get_video_path():
            print("error: user selected same video twice in a row")
            return
        self.state.set_video_path(video_path)

        # the state gets reset until user selects a valid video, otherwise the current video would get unloaded if the
        # user accidentally presses the "Open Video" button even without selecting any new video
        self.close_video()
        
        #load video from path (cv2.videoCapture object creation)
        video_capture = video_loader.load_video_file(video_path)
        if not video_capture:
            print("error: invalid or corrupted file")
            return
        # video capture setter makes a signal that enables video_player widget
        self.state.set_video_capture(video_capture)
        total_frames = video_reader.get_total_frames(video_capture)
        if total_frames == 0:
            print("error: video does not have at least one frame")
            return
        self.state.set_video_total_frames(total_frames)
        self.state.set_video_current_frame_index(0)        

        first_frame = video_reader.read_frame(video_capture, self.state.get_video_current_frame_index())
        # video current frame index setter makes a signal that changes the frame being displayed
        self.state.set_video_current_frame(first_frame)

    def close_video(self):
        """
        close_video resets video related state, state modification signals view to reset the frame and heatmap shown.

        Triggered by MainWindow -> menuBar -> Close Video
        Triggered by self.load_video
        """
        # in case video is closed while its playing
        self.state.set_video_is_playing(False)
        self.playback_timer.stop()
        
        self.state.set_video_path("")
        self.state.set_video_capture(None)

    def seek_to_frame(self, index):
        """
        Triggered by VideoPlayer -> Start Button
        Triggered by VideoPlayer -> Prev Button
        Triggered by VideoPlayer -> Next Button
        Triggered by VideoPlayer -> End Button
        Triggered by VideoPlayer -> Slider -> released
        """
        if index < 0 or index > self.state.get_video_total_frames() - 1:
            return

        self.state.set_video_current_frame_index(index)
        new_frame = video_reader.read_frame(self.state.get_video_capture(), self.state.get_video_current_frame_index())
        self.state.set_video_current_frame(new_frame)

    def toggle_playback(self):
        """
        Triggered by VideoPlayer -> Play Button
        """
        # if video's already running, pause
        if self.state.get_video_is_playing():
            #print("paused")
            self.state.set_video_is_playing(False)
            self.playback_timer.stop()
        else:
            #print("now playing")
            self.state.set_video_is_playing(True)
            self.playback_timer.start()

    def _play_next_frame(self):
        """
        Triggered by self.playback_timer
        """
        current_frame_index = self.state.get_video_current_frame_index()
        last_frame = self.state.get_video_total_frames() - 1
    
        if current_frame_index + 1 <= last_frame:
            self.seek_to_frame(current_frame_index + 1)
        else:
            self.state.set_video_is_playing(False)
            self.playback_timer.stop()
    
    def set_available_models(self):
        """
        set_available_models scans the models directory and updates state to reflect the available yolo models.

        Triggered by Selected Model -> initialization
        """
        models = model_loader.get_available_models()
        # setter sends a signal to Selected Model widget
        self.state.set_models_list(models)

    def select_model(self, model_name):
        """
        select_model stores the name of the selected yolo model without loading it, the model will be loaded
        until heatmap generation to avoid unnecessary reloading on each Selected Model dropdown change.

        Triggered by Selected Model -> dropdown changed
        """
        self.state.set_selected_model(model_name)

    def enable_class(self, yolo_class):
        """
        Triggered by Object Detection -> checkbox checked
        """
        self.state.enable_class(yolo_class)

    def disable_class(self, yolo_class):
        """
        Triggered by Object Detection -> checkbox unchecked
        """
        self.state.disable_class(yolo_class)

    def change_class_color(self, yolo_class, color):
        """
        Triggered by Object Detection -> Color Button -> change color
        """
        self.state.set_class_color(yolo_class, color)

    def generate_heatmap(self):
        """
        generate_heatmap generates a cummulative heatmap for the current video and saves it on memory,
        it will be automatically shown on top of the video once done, although it can still be hidden.

        Triggered by Generate Heatmap Button
        """
        video_capture = self.state.get_video_capture()
        # open selected game's yolo model
        yolo_model = model_loader.load_yolo_model(self.state.get_selected_model())
        if yolo_model is None:
            print("error: yolo model not found")
            return
        self.state.set_yolo_model(yolo_model)

        # make an empty canvas for each enabled class
        # detections increase pixel values, higher values indicate presence (and color) and lower numbers indicate absence (and alpha)
        enabled_classes = self.state.get_enabled_classes()
        canvases = {}
        for class_name, class_data in enabled_classes.items():
            canvases[class_name] = heatmap_generator.new_canvas(*video_reader.get_video_shape(video_capture))

        # cummulate all video detections on our canvases
        for i in range(self.state.get_video_total_frames()):
            frame = video_reader.read_frame(video_capture, i)
            detections = model_predictor.predict(yolo_model, frame)
            for class_name, bounding_box in detections:
                # I defined yolo classes as player shot instead of player_shot..., the replace function patches such
                class_name = class_name.replace(" ", "_")
                x1, y1, x2, y2 = bounding_box
                
                if class_name in enabled_classes:
                    heatmap_generator.add_presence(canvases[class_name], x1, y1, x2, y2)
        
        # heatmap_layers will hold single-color layers for each class
        heatmap_layers = {}
        for class_name, canvas in canvases.items():
            # normalize values from [0, max] to [0, 1]
            # design choice: normalization without np.max() as detections could be extremely concentrated in certain spots
            # and thus, diminishing the strength of colors in low detection areas
            # the minimum threshold helps low values get set into a minimum value, more predominant on longer videos
            heatmap_generator.normalize_canvas(canvas)

            # hex to rgb
            hex_color = enabled_classes[class_name]["color"].lstrip('#')
            bgr_color = (
                int(hex_color[4:6], 16),
                int(hex_color[2:4], 16),
                int(hex_color[0:2], 16),   
            )
            layer = heatmap_generator.create_rgba_layer(canvas, bgr_color)
            heatmap_generator.add_gaussian_blur(layer)
            heatmap_layers[class_name] = layer

        heatmap = heatmap_generator.create_heatmap(heatmap_layers)

        # View expects a 800x600 heatmap, resize is necessary
        heatmap_resized = heatmap_generator.resize_heatmap(heatmap)
        # save to state
        self.state.set_heatmap_current_frame(heatmap_resized)

        # Optionally, save to file
        #cv2.imwrite("debug_final.png", heatmap_resized)
        #cv2.imwrite("debug_final.jpg", heatmap_resized)
        
    def toggle_heatmap_overlay(self, boolean):
        """
        Triggered by Overlay Mode -> button group checked
        """
        self.state.set_heatmap_is_being_shown(boolean)

    def export_heatmap(self, extension):
        """
        Triggered by Export Heatmap -> PNG Button
        Triggered by Export Heatmap -> JPG Button
        """
        export_path = heatmap_exporter.select_export_path(extension)
        if not export_path:
            print("error: user did not select an export path")
            return
        heatmap_exporter.export_heatmap(self.state.get_heatmap_current_frame(), export_path)
