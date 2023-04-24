from libPySI import PySI
import time
import math
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable

from plugins.standard_environment_library.palette.RadialPalette import RadialPalette
from plugins.standard_environment_library.palette.Selector import Selector

from plugins.E import E


class Tip(Movable, SIEffect):
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
        self.max_distance_movement_for_click = 30 # px
        self.min_num_drag_events_for_dragging_activation = 25 # px
        self.input_history = []
        self.has_hovered = True
        self.has_dbl_clicked = False
        self.is_dragging_counter = 0
        self.assigned_effect = ""
        self.current_effect_texture = ""
        self.current_effect_name = ""
        self.parent_canvas = None
        self.palette = None
        self.can_spawn_rmenu = True
        self.tracker = None if "tracker" not in kwargs else kwargs["tracker"]
        self.is_dragging = True
        self.is_drawing_blocked = False
        self.move_target = None

        if self.tracker is not None:
            self.tracker.tips[self.id] = self

        if self.id == 0:
            self.color = PySI.Color(255, 0, 0, 255)
        elif self.id == 1:
            self.color = PySI.Color(0, 255, 0, 255)
        elif self.id == 2:
            self.color = PySI.Color(0, 0, 255, 255)

        pass

    def __update__(self, oid, x, y, state):
        self.last_x = self.x
        self.last_y = self.y
        self.move(x, y)

        if self.move_target is not None:
            self.emit_linking_action(self._uuid, PySI.LinkingCapability.POSITION, (self.x - self.last_x, self.y - self.last_y, self.x, self.y))

        self.evaluate_input_event(oid, x, y, state)

    def evaluate_input_event(self, oid, x, y, state):
        self.current_time = time.time()

        if state == Tip.TIP_STATE_DRAG:
            self.handle_dragging_data(oid, x, y)

        if state == Tip.TIP_STATE_HOVER:
            self.handle_hover_data(oid)

    def handle_dragging_data(self, oid, x, y):
        if self.has_hovered:
            self.determine_click_event(oid, x, y)
        else:
            self.determine_drag_event(oid, x, y)

    def determine_click_event(self, oid, x, y):
        self.has_hovered = False

        if self.current_time - self.last_click_time < self.double_click_time_ms:
            if self.is_click_candidate_movement(x, y):
                self.input_history.clear()
                self.has_dbl_clicked = True
                self.perform_dbl_click(oid, x, y)
            else:
                self.input_history.clear()
                self.perform_click(oid, x, y)
        else:
            self.input_history.append([x, y])

        self.last_click_time = self.current_time

    def determine_drag_event(self, oid, x, y):
        self.is_dragging_counter += 1

        if self.is_dragging_counter < self.min_num_drag_events_for_dragging_activation:
            return

        if self.has_dbl_clicked:
            return

        self.perform_dragging(oid, x, y)
        self.input_history.clear()

    def handle_hover_data(self, oid):
        self.has_hovered = True
        self.has_dbl_clicked = False
        self.is_dragging = False
        self.is_dragging_counter = 0

        if PySI.CollisionCapability.SKETCH in self.cap_emit.keys():
            self.disable_effect(PySI.CollisionCapability.SKETCH, True)
            if self.parent_canvas is not None:
                args = self.on_sketch_leave_emit(self.parent_canvas)
                self.parent_canvas.on_sketch_leave_recv(*args)
                self.parent_canvas = None

        if PySI.CollisionCapability.MOVE in self.cap_emit.keys():
            self.disable_effect(PySI.CollisionCapability.MOVE, True)
            if self.move_target is not None:
                args = self.on_move_leave_emit(self.move_target)
                self.move_target.on_move_leave_recv(*args)
                self.move_target = None

            # if self.move_target is not None:
            #     if len(self.ctrl_selected) == 0:
            #         for i in range(sum([1 for lr in self.move_target.link_relations if lr.sender == self._uuid])):
            #             self.move_target.remove_link(self._uuid, PySI.LinkingCapability.POSITION, self.move_target._uuid,
            #                                          PySI.LinkingCapability.POSITION)

        if len(self.input_history) == 0:
            return

        if self.current_time - self.last_click_time <= self.double_click_time_ms:
            return

        self.perform_click(oid, self.input_history[0][0], self.input_history[0][1])
        self.input_history.clear()

    def is_click_candidate_movement(self, x, y):
        return self.distance(x, y, self.x, self.y) < self.max_distance_movement_for_click

    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def perform_dragging(self, oid, x, y):
        if not self.is_dragging:
            self.is_dragging = True

            collisions = [uuid for uuid, name in self.present_collisions()]
            regions = [r for r in self.current_regions() if r._uuid in collisions and (isinstance(r, Movable) or r.regionname == PySI.EffectName.SI_STD_NAME_SELECTOR)]

            if len(regions) == 0 or (len(regions) == 1 and regions[0].regionname == "__ Painter __"):
                if self.assigned_effect != "":
                    if not self.is_drawing_blocked and PySI.CollisionCapability.SKETCH not in self.cap_emit.keys():
                        self.enable_effect(PySI.CollisionCapability.SKETCH, True, self.on_sketch_enter_emit, self.on_sketch_continuous_emit, self.on_sketch_leave_emit)
            else:
                if PySI.CollisionCapability.MOVE not in self.cap_emit.keys():
                    self.enable_effect(PySI.CollisionCapability.MOVE, True, self.on_move_enter_emit, self.on_move_continuous_emit, self.on_move_leave_emit)

    def perform_click(self, oid, x, y):
        self.__click_mouse__(self.absolute_x_pos(), self.absolute_y_pos())

    def show_radial_palette(self):
        if self.can_spawn_rmenu:
            kwargs = {"source": self, "source_id": self.id}
            self.create_region_via_name(PySI.PointVector([[self.x, self.y], [self.x, self.y + 50], [self.x + 50, self.y + 50], [self.x + 50, self.y]]), RadialPalette.regionname, kwargs=kwargs)

        self.can_spawn_rmenu = False

    def perform_dbl_click(self, oid, x, y):
        collisions = [uuid for uuid, name in self.present_collisions()]
        regions = [r for r in self.current_regions() if r._uuid in collisions and (isinstance(r, Movable) or r.regionname == PySI.EffectName.SI_STD_NAME_SELECTOR)]

        if (len(regions) == 0) or (len(regions) == 1 and regions[0].regionname == "__ Painter __"):
            sorts = [s.is_popup_shown for s in self.current_regions() if s.regionname == "__ FolderSort __"]
            if not any(sorts):
                if self.palette is None and self.can_spawn_rmenu:
                    self.show_radial_palette()
                else:
                    self.delete_palette()

        elif (len(regions) == 1 and regions[0].regionname == PySI.EffectName.SI_STD_NAME_SELECTOR):
            self.delete_palette()

        self.__dbl_click_mouse__(self.absolute_x_pos(), self.absolute_y_pos())

    def delete_palette(self):
        if self.palette is not None:
            for selector in self.palette.selectors:
                selector.delete()

            self.palette.remove()
            self.palette = None
            self.can_spawn_rmenu = True

    @SIEffect.on_continuous(PySI.CollisionCapability.ASSIGN, SIEffect.RECEPTION)
    def on_assign_continuous_recv(self, effect_to_assign, effect_display_name, effect_texture, kwargs):
        if self.assigned_effect != effect_to_assign:
            self.assigned_effect = effect_to_assign
            self.current_effect_texture = effect_texture
            self.current_effect_name = effect_display_name

            self.assign_effect(self.assigned_effect, effect_display_name, effect_texture, kwargs)

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        pass

    @SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
    def position(self):
        x, y = self.x - self.last_x, self.y - self.last_y
        # self.last_x = self.x
        # self.last_y = self.y

        return x, y, self.x, self.y

    def on_move_enter_emit(self, other):
        # if other.regionname == Painter.regionname and other == self.paint_tool:
        #     return "", ""

        if self.move_target is None:
            self.move_target = other

        if self.move_target is other:
            return self._uuid, PySI.LinkingCapability.POSITION

        return "", ""

    def on_move_continuous_emit(self, other):
        pass

    def on_move_leave_emit(self, other):
        if self.move_target is other:
            return self._uuid, PySI.LinkingCapability.POSITION

        return "", ""

    def on_sketch_enter_emit(self, other):
        self.parent_canvas = other
        # if self.paint_tool is not None and self.assigned_effect == Painter.regionname:
        #     self.set_cursor_stroke_width_by_cursorid(self._uuid, self.paint_tool.stroke_width)
        #     self.set_cursor_stroke_color_by_cursorid(self._uuid, self.paint_tool.color)
        return self.x, self.y, self._uuid

    def on_sketch_continuous_emit(self, other):
        if self.parent_canvas is None:
            self.parent_canvas = other

        return self.x, self.y, self._uuid

    def on_sketch_leave_emit(self, other):
        kwargs = {}
        # if self.paint_tool is not None and self.assigned_effect == Painter.regionname:
        #     kwargs["color"] = self.paint_tool.color
        #     kwargs["stroke_width"] = self.paint_tool.stroke_width
        #     kwargs["__name__"] = Painter.regionname
        return self.x, self.y, self._uuid, False, kwargs