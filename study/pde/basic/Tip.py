from libPySI import PySI
import time
import math
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E


class Tip(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ Tip __"
    region_display_name = "Tip"
    region_width = E.id.cursor_width
    region_height = E.id.cursor_height
    TIP_STATE_HOVER = 0
    TIP_STATE_DRAG = 1

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(Tip, self).__init__(shape, uuid, "", Tip.regiontype, Tip.regionname, kwargs)

        self.id = kwargs["id"]
        self.context_width, self.context_height = self.context_dimensions()
        self.with_border = False
        self.double_click_time_ms = 0.5
        self.current_time = time.time()
        self.last_click_time = time.time()
        self.max_distance_movement_for_click = 15 # px
        self.min_num_drag_events_for_dragging_activation = 5 # px
        self.input_history = []
        self.has_hovered = True
        self.has_dbl_clicked = False
        self.is_dragging_counter = 0

        if self.id == 0:
            self.color = PySI.Color(255, 0, 0, 255)
        elif self.id == 1:
            self.color = PySI.Color(0, 255, 0, 255)
        elif self.id == 2:
            self.color = PySI.Color(0, 0, 255, 255)

        self.tracker = kwargs["tracker"]

        self.tracker.tips[self.id] = self

    def __update__(self, x, y, state):
        self.evaluate_input_event(x, y, state)

    def evaluate_input_event(self, x, y, state):
        self.current_time = time.time()

        if state == Tip.TIP_STATE_DRAG:
            self.handle_dragging_data(x, y)

        if state == Tip.TIP_STATE_HOVER:
            self.handle_hover_data()

    def handle_dragging_data(self, x, y):
        if self.has_hovered:
            self.determine_click_event(x, y)
        else:
            self.determine_drag_event(x, y)

    def determine_click_event(self, x, y):
        self.has_hovered = False

        if self.current_time - self.last_click_time < self.double_click_time_ms:
            if self.is_click_candidate_movement(x, y):
                self.input_history.clear()
                self.has_dbl_clicked = True
                self.perform_dbl_click(x, y)
            else:
                self.input_history.clear()
                self.perform_click(x, y)
        else:
            self.input_history.append([x, y])

        self.last_click_time = self.current_time

    def determine_drag_event(self, x, y):
        self.is_dragging_counter += 1

        if self.is_dragging_counter < self.min_num_drag_events_for_dragging_activation:
            return

        if self.has_dbl_clicked:
            return

        self.perform_dragging(x, y)
        self.input_history.clear()

    def handle_hover_data(self):
        self.has_hovered = True
        self.has_dbl_clicked = False
        self.is_dragging_counter = 0

        if len(self.input_history) == 0:
            return

        if self.current_time - self.last_click_time <= self.double_click_time_ms:
            return

        self.perform_click(self.input_history[0][0], self.input_history[0][1])
        self.input_history.clear()

    def is_click_candidate_movement(self, x, y):
        nx, ny = self.x + x, self.y + y
        ox, oy = self.x, self.y

        return self.distance(nx, ny, ox, oy) < self.max_distance_movement_for_click

    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def perform_dragging(self, x, y):
        self.move(x, y)
        # print(f"Dragging at ({x}, {y})")

    def perform_click(self, x, y):
        self.move(x, y)
        self.__click_mouse__(self.absolute_x_pos(), self.absolute_y_pos())

    def perform_dbl_click(self, x, y):
        self.move(x, y)
        self.__dbl_click_mouse__(self.absolute_x_pos(), self.absolute_y_pos())

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        pass
