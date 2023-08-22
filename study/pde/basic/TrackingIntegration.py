import os
import queue
import time

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
    UNIX_SOCK_NAME = "/home/vigitia/Desktop/IRPenTracking/uds_test"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(TrackingIntegration, self).__init__(shape, uuid, "", TrackingIntegration.regiontype, TrackingIntegration.regionname, kwargs)
        self.last_time = time.process_time()
        self.is_running = True
        self.num_tips = 3
        self.tips = {}
        self.queue = queue.Queue()

    #     self.msg_thread = threading.Thread(target=self.init_source, args=(), daemon=True)
    #     self.msg_thread.start()
    #
    #     self.parse_thread = threading.Thread(target=self.init_parse, args=(), daemon=True)
    #     self.parse_thread.start()
    #
    #     self.cw, self.ch = self.context_dimensions()
    #     self.has_hovered = {0: False, 1: False, 2: False}
    #
    # def init_source(self):
    #     server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    #     server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #
    #     if os.path.exists(TrackingIntegration.UNIX_SOCK_NAME):
    #         os.remove(TrackingIntegration.UNIX_SOCK_NAME)
    #     server_socket.bind(TrackingIntegration.UNIX_SOCK_NAME)
    #     server_socket.listen(2)
    #     conn, address = server_socket.accept()
    #
    #     while self.is_running:
    #         header = conn.recv(4, socket.MSG_WAITALL).decode(encoding="ascii")
    #         header = list(map(ord, header))
    #         buffer_length = (header[0] << 24) | (header[1] << 16) | (header[2] << 8) | header[3]
    #         data = conn.recv(buffer_length, socket.MSG_WAITALL).decode(encoding="ascii")
    #
    #         if data[0] != "l":
    #             continue
    #
    #         cur_time = time.process_time()
    #         #if cur_time - self.last_time < delta:
    #         #continue
    #
    #         oid, r, g, b, x, y, state = data.split(" ")[1:]
    #         _id = 0 if int(r) > 0 else 1 if int(g) > 0 else 2 if int(b) > 0 else -1
    #
    #         if _id == -1:
    #             continue
    #
    #         self.queue.put([oid, _id, x, y, self.to_SI_state(int(state))], block=False)
    #         self.last_time = cur_time
    #
    #     server_socket.close()
    #
    # def init_parse(self):
    #     last_time = time.process_time()
    #     while self.is_running:
    #
    #         if not self.queue.empty():
    #             current_time = time.process_time()
    #
    #             oid, _id, x, y, state = self.queue.get(block=False)
    #             self.tips[_id].__update__(oid, float(x), float(y), self.to_SI_state(int(state)))
    #             # print("TIME PenColorDetector", current_time - last_time)
    #             last_time = current_time
    #
    # def to_SI_state(self, state):
    #     if state == TrackingIntegration.TRACKER_STATE_HOVER:
    #         return Tip.TIP_STATE_HOVER
    #
    #     if state == TrackingIntegration.TRACKER_STATE_DRAG:
    #         return Tip.TIP_STATE_DRAG
    #
    # def __on_destroy__(self):
    #     self.is_running = False
    #
    # @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    # def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
    #     for i in range(self.num_tips):
    #         x = i * Tip.region_width
    #         y = 0
    #         w = Tip.region_width / 8
    #         h = Tip.region_height / 8
    #         shape = PySI.PointVector([
    #             [x, y],
    #             [x, y + h],
    #             [x + w, y + h],
    #             [x + w, y]
    #         ])
    #
    #         self.create_region_via_name(shape, Tip.regionname, False, {"tracker": self, "id": i})