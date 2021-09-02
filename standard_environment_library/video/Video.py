from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.E import E

import cv2
import threading

class Video(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = E.id.video_regionname
    region_display_name = E.id.video_region_display_name

    def __init__(self, shape :PySI.PointVector=PySI.PointVector(), uuid: str="", kwargs: dict={}) -> None:
        super(Video, self).__init__(shape, uuid, E.id.video_texture, Video.regiontype, Video.regionname, kwargs)
        self.qml_path = self.set_QML_path(E.id.video_qml_path)
        self.origin_ip = "127.0.0.1"
        self.port = str(3335)
        self.started = False
        self.initialize_video_stream(E.id.video_selector in kwargs)

    def initialize_video_stream(self, is_selector: bool) -> None:
        if not is_selector:
            self.pipeline = E.id.video_pipeline.format(self.port)
            self.thread = threading.Thread(target=self.display)
            self.thread.start()

    def display(self) -> None:
        self.capture_receive = cv2.VideoCapture(self.pipeline, cv2.CAP_GSTREAMER)

        if not self.capture_receive.isOpened():
            print('Error: VideoCapture not opened')
            return

        self.started = True

        while self.started:
            self.show()

    def adjust_geometry(self, h: int, w: int) -> None:
        x = self.relative_x_pos()
        y = self.relative_y_pos()

        self.height, self.width = h, w
        self.shape = PySI.PointVector([[x, y], [x, y + self.height], [x + self.width, y + self.height], [x + self.width, y]])
        self.set_QML_data("img_width", self.width, PySI.DataType.INT)
        self.set_QML_data("img_height", self.height, PySI.DataType.INT)
        self.set_QML_data("widget_width", self.width, PySI.DataType.FLOAT)
        self.set_QML_data("widget_height", self.height, PySI.DataType.FLOAT)

    def show(self) -> None:
        ret, frame = self.capture_receive.read()

        if ret == 1:
            if(self.width != frame.shape[1] and self.height != frame.shape[0]):
                self.adjust_geometry(*frame.shape[:2])

            self.set_QML_data("image", frame.copy().tobytes(), PySI.DataType.VIDEO, {"width": self.width, "height": self.height})

    def __exit__(self, exec_type, exc_value, traceback):
        self.on_deletion_enter_recv()

    @SIEffect.on_enter(PySI.CollisionCapability.DELETION, SIEffect.RECEPTION)
    def on_deletion_enter_recv(self) -> None:
        self.started = False
        self.thread.join()
        self.capture_receive.release()
