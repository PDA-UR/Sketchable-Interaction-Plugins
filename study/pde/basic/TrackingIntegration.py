import os

from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.study.pde.basic.Tip import Tip
from plugins.E import E
import socket
import threading

class TrackingIntegration(SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ TrackingIntegration __"
    region_display_name = "TrackingIntegration"
    TRACKER_STATE_HOVER = 0
    TRACKER_STATE_DRAG = 1

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(TrackingIntegration, self).__init__(shape, uuid, "", TrackingIntegration.regiontype, TrackingIntegration.regionname, kwargs)
        self.is_running = True
        self.num_tips = 3
        self.tips = {}
        self.thread = threading.Thread(target=self.init_source, args=())
        self.thread.start()

    """
    new method for PySI which allows to trigger mouse events
    use pyautogui for click/dbl click absetzen
    """
    def init_source(self):
        server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        if os.path.exists("/home/juergen/Desktop/socket_test.s"):
            os.remove("/home/juergen/Desktop/socket_test.s")
        server_socket.bind("/home/juergen/Desktop/socket_test.s")
        server_socket.listen(2)
        conn, address = server_socket.accept()

        while self.is_running:
            data = conn.recv(1024).decode()
            if data[0] != "l":
                continue

            r, g, b, x, y, state = data.split(" ")[2:]

            _id = 0 if int(r) > 0 else 1 if int(g) > 0 else 2 if int(b) > 0 else -1

            if _id == -1:
                continue

            self.tips[int(_id)].__update__(float(x), float(y), self.to_SI_state(int(state)))

        server_socket.close()

    def to_SI_state(self, state):
        if state == TrackingIntegration.TRACKER_STATE_HOVER:
            return Tip.TIP_STATE_HOVER

        if state == TrackingIntegration.TRACKER_STATE_DRAG:
            return Tip.TIP_STATE_DRAG

    def __on_destroy__(self):
        self.is_running = False

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        for i in range(self.num_tips):
            x = i * Tip.region_width
            y = 0
            w = Tip.region_width / 8
            h = Tip.region_height / 8

            shape = PySI.PointVector([
                [x, y],
                [x, y + h],
                [x + w, y + h],
                [x + w, y]
            ])

            self.create_region_via_name(shape, Tip.regionname, False, {"tracker": self, "id": i})